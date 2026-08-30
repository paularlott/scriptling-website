---
description: Serve the plugin protocol from plain PHP over HTTP JSON-RPC.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/plugins/php-plugins/
sources:
    - resource: https://scriptling.dev/docs/plugins/php-plugins/
status: stable
tags:
    - plugins
    - php
    - json-rpc
    - http
title: PHP Plugins
type: Guide
---
# PHP Plugins

PHP serves the HTTP plugin transport: instead of stdio, the same protocol
speaks JSON-RPC over HTTP POST, so any language that can read and write JSON
can host a plugin and no SDK is needed. The whole contract is two methods,
`scriptling.handshake` and `function.call`.

The complete, commented example lives at
`examples/plugins/php-server` in the repository
([PHP 8](https://www.php.net/), no dependencies); this page shows its core.

```php
<?php
function respond(array $payload): never
{
    header('Content-Type: application/json');
    echo json_encode($payload, JSON_UNESCAPED_SLASHES);
    exit;
}

// Optional bearer enforcement: with a token in this process's environment,
// every request must carry it. The host side is --plugin-header
// "Authorization=Bearer <token>"; see Authentication below.
$token = getenv('PHPDEMO_TOKEN');
if ($token !== false && ($_SERVER['HTTP_AUTHORIZATION'] ?? '') !== "Bearer {$token}") {
    http_response_code(401);
    respond(['jsonrpc' => '2.0', 'id' => null,
        'error' => ['code' => -32001, 'message' => 'missing or invalid bearer token']]);
}

$request = json_decode(file_get_contents('php://input') ?: '', true);
$method = $request['method'] ?? '';

switch ($method) {
    case 'scriptling.handshake':
        respond(['jsonrpc' => '2.0', 'id' => $request['id'], 'result' => [
            'protocol' => '1.0',
            'transport' => 'json',
            'library' => [
                'name' => 'hello',
                'version' => '1.0.0',
                'description' => 'PHP hello plugin',
            ],
            'capabilities' => [],
            'schema' => [
                'functions' => [['name' => 'greet']],
                'classes' => [], 'constants' => [],
            ],
        ]]);

    case 'function.call':
        $who = $request['params']['args'][0]['value'] ?? 'world';
        respond(['jsonrpc' => '2.0', 'id' => $request['id'], 'result' => [
            'type' => 'string',
            'value' => "Hello, {$who}",
        ]]);

    default:
        respond(['jsonrpc' => '2.0', 'id' => $request['id'] ?? null,
            'error' => ['code' => -32601, 'message' => "unknown method {$method}"]]);
}
```

Values travel as tagged objects, which is how scripts see native types across
the wire: a string is `{"type": "string", "value": "..."}`, a dict carries
`entries`, a list carries `items`. See the
[protocol reference](https://scriptling.dev/okf/scriptling-docs/plugins/protocol.md) for every type and method.

## Running and Loading

PHP's built-in server is enough:

```bash
php -S 127.0.0.1:8080 index.php
```

Load it by URL and call it like any plugin:

```bash
scriptling --plugin http://127.0.0.1:8080 \
           -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

The handshake declares the short name `hello`; Scriptling imports it as
`plugin.hello`, exactly like an executable plugin. In production, terminate
TLS in front of the server and load the `https://` URL; when the certificate
is self-signed (development, internal networks), name the URL with
`--plugin-insecure` to skip verification for it alone.

## Authentication

The host authenticates with headers, and both forms are one line on the
script side: a bearer token with `--plugin-header`, or username and password
in the URL as Basic auth.

```bash
# the token stays out of the process listing
export SCRIPTLING_PLUGIN_HEADER="Authorization=Bearer $PLUGIN_TOKEN"
scriptling --plugin https://plugins.internal:8443 script.py

# username and password ride the URL as Basic auth
scriptling --plugin https://user:pass@plugins.internal:8443 script.py
```

On the server side the header arrives as `$_SERVER['HTTP_AUTHORIZATION']`
(plain `Bearer <token>` or `Basic <base64>`). The snippet above enforces one
when `PHPDEMO_TOKEN` is set, exactly like the repository example: start it
with `PHPDEMO_TOKEN=seekrit php -S 127.0.0.1:8080 index.php` and a load
without the header fails with `401: missing or invalid bearer token`, while
the `--plugin-header "Authorization=Bearer seekrit"` form above loads it.

## HTTP Transport Notes

- **The server owns its environment.** The host connects to an HTTP plugin,
  it does not spawn it, so `--plugin-env` (which passes variables to
  executable plugins) does not apply: configure the PHP process's environment
  where you start it.
- **Request/response only.** The HTTP transport carries handshakes, function
  calls, object lifecycle and batches, but the server cannot call back into
  the host. This is not negotiated at load: a plugin that registers
  callback-bearing functions loads without warning, and the failure happens
  at call time. Load-time refusal would be the wrong default anyway, since
  the host often cannot reach back to the network a plugin server sits on.
  Host callbacks and `plugin.Logger(ctx)` require the stdio transport.
- **Errors are JSON-RPC errors.** An `error` object in a response surfaces in
  the script as an ordinary error, so unknown functions or a failing handler
  report themselves plainly.

The same protocol served from Go is in `examples/plugins/http-go`, and the
bash example implements the stdio transport if you want to see both sides.
