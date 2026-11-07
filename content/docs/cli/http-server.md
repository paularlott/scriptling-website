---
title: HTTP Server Mode
description: Running Scriptling as an HTTP server with custom routes.
tags: [cli, http]
weight: 5
---

Scriptling can run as an HTTP server, allowing you to build REST APIs and web services.

## Starting the Server

Use the `--server` flag to start an HTTP server:

```bash
# Start HTTP server on port 8000
scriptling --server :8000 setup.py
```

The setup script is executed when the server starts and typically registers route handlers.

> **Keeping the setup script alive:** By default the setup script exits after registering handlers and the server runs until shutdown. To keep the script running alongside the server: e.g. to maintain gossip state, run a polling loop, or share objects with handlers via `runtime.sync`: call [`runtime.start_server()`](../../../reference/libraries/runtime/) instead of exiting. See the [runtime reference](../../../reference/libraries/runtime/) for details.

## Server Options

| Flag                | Environment Variable      | Description                      | Default    |
| ------------------- | ------------------------- | -------------------------------- | ---------- |
| `--server`          | `SCRIPTLING_SERVER`       | HTTP server address (host:port)  | (disabled) |
| `--json-rpc`        | `SCRIPTLING_JSONRPC`      | Mount JSON-RPC at `/json-rpc`    | false      |
| `--web-root`        | `SCRIPTLING_WEB_ROOT`     | Directory or zip to serve static files from | none       |
| `--bearer-token`    | `SCRIPTLING_BEARER_TOKEN` | Bearer token for authentication  | none       |
| `--oidc-issuer`     | `SCRIPTLING_OIDC_ISSUER`  | Accept OAuth JWT access tokens from this identity provider (issuer URL); with `--bearer-token`, either is accepted | none |
| `--oidc-jwks-url`   | `SCRIPTLING_OIDC_JWKS_URL` | Identity provider JWKS URL      | discovered from the issuer |
| `--oidc-audience`   | `SCRIPTLING_OIDC_AUDIENCE` | This server's resource identifier: the public URL of its `/mcp` endpoint, which tokens' `aud` must name (required with `--oidc-issuer`) | none |
| `--oidc-required-scopes` | `SCRIPTLING_OIDC_REQUIRED_SCOPES` | Scopes every identity-provider token must grant (comma or space separated) | none |
| `--oidc-require-at-jwt` | `SCRIPTLING_OIDC_REQUIRE_AT_JWT` | Require RFC 9068 access tokens (JWT `typ` `at+jwt`), refusing ID tokens | false |
| `--oidc-ca-file` | `SCRIPTLING_OIDC_CA_FILE` | PEM file of CA certificates trusted (with the system roots) for the identity provider's discovery and JWKS fetches | none |
| `--oidc-tls-insecure` | `SCRIPTLING_OIDC_TLS_INSECURE` | Skip TLS certificate verification for the identity provider's discovery and JWKS fetches (development only) | false |
| `--allowed-paths`   | `SCRIPTLING_ALLOWED_PATHS`| Restrict participating library filesystem I/O; `-` denies it | (none)     |
| `--disable-lib`     | `SCRIPTLING_DISABLE_LIB`  | Disable a built-in library by name (repeatable) | (none) |
| `--tls-cert`        | `SCRIPTLING_TLS_CERT`     | TLS certificate file             | none       |
| `--tls-key`         | `SCRIPTLING_TLS_KEY`      | TLS key file                     | none       |
| `--tls-generate`    | -                         | Generate self-signed certificate | false      |

## Static Assets

Use `--web-root` to serve static files (HTML, CSS, JS, images) from a directory or a zip archive. When a request doesn't match any registered route, the server looks for a matching file in the web root. If no file is found either, the `not_found` handler is called (if registered).

```bash
# Serve from a directory
scriptling --server :8000 --web-root ./public setup.py

# Serve from a zip archive
scriptling --server :8000 --web-root ./public.zip setup.py
```

Requests for `/` automatically serve `index.html` from the web root if present, and a request for a directory serves that directory's `index.html`. Directories without one are not listed.

A web root only ever serves files by their relative path inside it: requests containing `..` or an absolute path are never resolved. The same rule applies to a zip archive's member names. A member whose name is not a plain relative path (such as `/etc/passwd`, `../x` or `a/../b`) is never served, and the server logs a warning naming each one when it opens the archive.

In your setup script, register a custom 404 handler for unmatched requests:

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/api/hello", "handlers.hello")
runtime.http.not_found("handlers.not_found")
```

```python
# handlers.py
import scriptling.runtime as runtime

def not_found(request):
    return runtime.http.html(404, f"<h1>404 - {request.path} not found</h1>")
```

Priority order for incoming requests:
1. Registered script routes (literal or `{param}` wildcard match)
2. Registered static routes (`runtime.http.static()`)
3. Web root directory (`--web-root`)
4. `not_found` handler (if registered)
5. Plain `404 Not Found`

## JSON-RPC Endpoint

Add `--json-rpc` to mount `scriptling.runtime.jsonrpc` handlers at
`POST /json-rpc` on the same HTTP server:

```bash
scriptling --server :8000 --json-rpc setup.py
```

This can run alongside normal HTTP routes, static files, MCP tools, and the MCP
script execution tool. See [JSON-RPC Server Mode](../jsonrpc-server/) for
single request, batch, and notification examples.

## Health Checks

Every server (`--server` with HTTP routes, `--json-rpc`, or `--mcp-tools`)
answers `GET /health` with `200 OK` by default — a plain liveness probe with
no dependencies.

To report your own readiness instead, register a handler for the path: a
route claiming `GET /health` replaces the built-in responder, in HTTP-server
mode and MCP/JSON-RPC server mode alike:

```python
# setup.py
import scriptling.runtime.http as http

@http.get("/health")
def health(request):
    # a health check that reflects real readiness
    try:
        conn = sql.connect("mariadb://user:pass@db:3306/app")
        conn.query("select 1")
        conn.close()
    except Exception:
        return http.json(503, {"status": "unhealthy", "db": "down"})
    return http.json(200, {"status": "ok"})
```

Two things to know before claiming the path:

- A claimed `/health` is a script route like any other, so script middleware
  runs for it. If your middleware rejects unauthenticated requests, health
  probes (which usually send no credentials) will be rejected too — allow
  `/health` through in the middleware, or keep the built-in and expose
  dependency status on a separate authenticated route. The built-in `/health`
  itself never runs middleware.
- `--bearer-token` (and `--oidc-issuer`) wraps `/health` whichever responder is active (see
  [Authentication](#authentication)); probes must carry a token.

## TLS/HTTPS

Provide both `--tls-cert` and `--tls-key`, or use `--tls-generate`. If only one of the certificate/key flags is set, Scriptling does not enable TLS and starts the server over plaintext HTTP.

### Self-Signed Certificate

Quick setup for development:

```bash
scriptling --server :8443 --tls-generate setup.py
```

This generates a self-signed certificate automatically.

### Custom Certificate

Provide your own certificate and key:

```bash
scriptling --server :8443 --tls-cert /path/to/cert.pem --tls-key /path/to/key.pem setup.py
```

## Authentication

Use bearer token authentication to protect your API:

```bash
# Set token via flag
scriptling --server :8000 --bearer-token my-secret-token setup.py

# Or via environment variable
SCRIPTLING_BEARER_TOKEN=my-secret-token scriptling --server :8000 setup.py
```

Clients must include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer my-secret-token" http://localhost:8000/api/hello
```

A request without a valid token gets `401 Unauthorized` with a `WWW-Authenticate: Bearer` challenge (RFC 6750), and an identity-provider token missing a required scope gets `403` with `error="insufficient_scope"`.

### Identity Provider (OAuth / OIDC)

To accept access tokens from an OAuth identity provider (Keycloak, Auth0, Okta, Entra ID and the like) instead of, or alongside, a static token, name its issuer and this server's own `/mcp` URL:

```bash
scriptling --server :8000 \
  --oidc-issuer https://idp.example.com/realms/acme \
  --oidc-audience https://mcp.example.com/mcp \
  --oidc-required-scopes mcp:use setup.py
```

The server then follows the MCP authorization spec:

- It verifies each JWT access token's issuer, signature (keys from the provider's JWKS, discovered from the issuer unless `--oidc-jwks-url` is set), expiry, audience (`aud` must name `--oidc-audience`) and any `--oidc-required-scopes`. Add `--oidc-require-at-jwt` to refuse ID tokens and accept only RFC 9068 access tokens.
- Discovery and JWKS fetches verify the provider's TLS certificate against the system roots. For a provider with a private or self-signed CA, pass `--oidc-ca-file ca.pem` to trust that PEM file's certificates as well; `--oidc-tls-insecure` skips verification altogether (development only; a warning is logged at startup).
- It publishes OAuth protected resource metadata (RFC 9728) at `/.well-known/oauth-protected-resource/mcp` (and `/.well-known/oauth-protected-resource`), naming the issuer, without requiring a token; the `401` challenge points clients at it, so MCP clients can discover where to sign in.
- With `--bearer-token` also set, either credential is accepted.

Every flag has a `SCRIPTLING_OIDC_*` environment variable and a `server.oidc_*` config key (see [Command-Line Options](../command-line-options/)).

Handlers see who is calling as `request.auth`: a dict with `subject`, `audience`, `scopes`, `expiry` and `claims` (the token's JWT claims), or `None` when no credential is configured. A request authenticated with the static `--bearer-token` has the subject `"bearer"` and no claims. MCP tools and JSON-RPC methods read it through `get_request()`.

```python
import scriptling.runtime as runtime

def whoami(request):
    who = request.auth
    return runtime.http.json(200, {"subject": who["subject"], "scopes": who["scopes"]})
```

### Per-User Keys

For more than one key, skip the static token and register a script middleware
that checks the `Authorization` header itself — a dict lookup, the KV store,
or an API call all work. The middleware covers script routes, WebSocket
handlers, and the `/mcp` and `/json-rpc` endpoints. It does **not** cover the
built-in `/health` endpoint, registered static routes, or `--web-root` fallback
files:

```python
# auth.py
KEYS = {
    "Bearer alice-key": "alice",
    "Bearer bob-key": "bob",
}

def check(request):
    auth = request.header("authorization", "")
    if auth in KEYS:
        return None
    return {"status": 401, "body": "unauthorized"}
```

```python
# setup.py
import auth
import scriptling.runtime as runtime

runtime.http.middleware("auth.check")
```

A server bound to loopback (`--server 127.0.0.1:8000`, `[::1]` or `localhost`) checks the request's `Host` header on every endpoint and refuses any name but a loopback one (`localhost`, `*.localhost` or a loopback IP) with `421 Misdirected Request`. That stops DNS rebinding, where a page on an attacker's domain re-points its name at your machine and so becomes same-origin with your local server; nothing else guards a loopback server, and you reach it by those names anyway. A server bound to all interfaces (`--server :8000`, `0.0.0.0:8000`) or another address answers every `Host` until you set `--allowed-hosts`, like every other restriction that is off until configured; it logs a note at startup saying so. Once set (`--allowed-hosts app.example.com`, or `.example.com` for a domain and its subdomains; a port on an entry is ignored), it answers loopback names, IP addresses, the machine's own host name as the OS reports it with its first label (`web01.corp.example` and `web01`), and the listed names, and refuses the rest with `421`. List every name the server is reached by: a DNS name that points at it, or the public name a reverse proxy forwards in `Host` (Caddy does by default; nginx does with `proxy_set_header Host $host`). The `421` body names the refused `Host`, and the first refusal of each name is logged as a warning, so a missing entry is visible from either end.

WebSocket upgrades are same-origin by default, so a hostile page cannot open a WebSocket to your server from a browser on another site (non-browser clients send no origin and pass). Pass `--websocket-origin` to allowlist specific origins, or `--websocket-origin '*'` behind a trusted proxy to allow any.

`/mcp` and `/json-rpc` are same-origin by default too: a browser request from another origin is refused with `403` before anything runs. Allowlist browser apps on other origins with `--mcp-cors-origin` and `--json-rpc-cors-origin`. Setting any of `--websocket-origin`, `--mcp-cors-origin` or `--json-rpc-cors-origin` replaces the same-origin default for that endpoint rather than adding to it: if the server's own pages also use the endpoint, list the server's own origin too. Script routes registered with `runtime.http` have no origin check; guard state-changing routes with a middleware or `--bearer-token`.

Request bodies are capped at 32 MiB by default (`--max-request-body` to change, negative to disable) and the server enforces header, read, write and idle timeouts; an oversized body receives a deterministic `413 Request Entity Too Large` rather than reaching a handler truncated. MCP's SSE streams are exempt from the write timeout.

A configured `--bearer-token` or `--oidc-issuer` wraps every endpoint, middleware or not: the middleware guards script routes, WebSocket handlers, `/mcp`, and `/json-rpc`, while the token also covers what the middleware never sees — `/health`, registered static routes, and `--web-root` fallback files. With both configured the token applies first and the middleware layers on top, so the middleware sees only token-bearing requests.

## Filesystem Restrictions

`--allowed-paths` restricts filesystem operations made through participating Scriptling libraries; it does not constrain subprocesses, plugins, static assets, or other host-side I/O. Library loading is constrained only for symlinks: a library reached through a symlink in a library directory must resolve inside a library directory or an allowed path.

```bash
# Restrict participating libraries to specific directories
scriptling --server :8000 --allowed-paths "/var/www,./uploads" setup.py

# Deny all participating library filesystem I/O
scriptling --server :8000 --allowed-paths - setup.py
```

For server modes, use `--disable-lib subprocess` when subprocess access must be removed. This also stops scripts loading executable plugins via `scriptling.plugin.load()`; operator-supplied `--plugin` / `--plugin-dir` plugins and HTTP(S) plugins are unaffected.

## Defining Routes

Register route handlers in your setup script:

```python
# setup.py
import scriptling.runtime as runtime

# Register routes (handler functions referenced as "module.function")
runtime.http.get("/api/hello", "handlers.hello")
runtime.http.post("/api/echo", "handlers.echo")
runtime.http.get("/api/users/{id}", "handlers.get_user")
```

Handler modules can live in subdirectories: `routes/me.py` is imported as
`import routes.me` and its functions are referenced as `"routes.me.get_user"`.
The module part of a handler reference may be any dotted module path.

```python
# handlers.py
import scriptling.runtime as runtime

def hello(request):
    return runtime.http.json(200, {"message": "Hello, World!"})

def echo(request):
    return runtime.http.json(200, request.json())

def get_user(request):
    user_id = request.path_param("id")
    return runtime.http.json(200, {"user_id": user_id})
```

### HTTP Methods

```python
runtime.http.get("/path", "handlers.get")
runtime.http.post("/path", "handlers.post")
runtime.http.put("/path", "handlers.put")
runtime.http.patch("/path", "handlers.patch")
runtime.http.delete("/path", "handlers.delete")
```

### Path Parameters

Route patterns capture path segments with `{name}` for a single segment and `{name...}` for the rest of the path. Values are read in the handler with `request.path_param(name)` and arrive percent-decoded:

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/api/users/{id}", "handlers.get_user")
runtime.http.get("/files/{path...}", "handlers.get_file")
```

```python
# handlers.py
import scriptling.runtime as runtime

def get_user(request):
    user_id = request.path_param("id")          # "/api/users/42"  -> "42"
    return runtime.http.json(200, {"user_id": user_id})

def get_file(request):
    path = request.path_param("path")           # "/files/a/b.txt" -> "a/b.txt"
    return runtime.http.json(200, {"path": path})
```

Matching follows Go's `ServeMux` rules: a literal route wins over a wildcard at the same position, so `/api/users/me` hits its own handler while `/api/users/42` matches `/api/users/{id}`. HEAD requests are dispatched to GET handlers, and values keep encoded slashes within one segment (`/api/users/a%2Fb` captures `a/b`).

### Decorator Syntax

Instead of registering routes separately in a setup script, attach them
directly to handler functions with decorators. Import the HTTP sub-library
and use `@http.get`, `@http.post`, `@http.put`, `@http.patch`, `@http.delete`,
`@http.route`, `@http.websocket`, `@http.middleware`, or `@http.not_found`:

```python
# handlers.py
import scriptling.runtime.http as http

@http.get("/health")
def health_check(request):
    return http.json(200, {"status": "ok"})

@http.post("/api/users")
def create_user(request):
    data = request.json()
    return http.json(201, {"name": data["name"]})

@http.route("/api/items", methods=["GET", "POST"])
def items(request):
    return http.json(200, [])

@http.websocket("/ws")
def ws_handler(client):
    client.send("Welcome!")

@http.middleware
def auth(request):
    if request.header("Authorization") == "":
        return http.json(401, {"error": "unauthorized"})
    return None  # continue to handler

@http.not_found
def handle_404(request):
    return http.html(404, "<h1>Not Found</h1>")
```

The setup script still triggers registration — it imports the handler library,
which fires the decorators:

```python
# setup.py
import handlers  # decorators fire, routes are registered
```

When the file is imported, the decorators register each route with the correct
`"module.function"` reference. The module name is derived from `__name__`
(or `__file__` when `__name__` is `"__main__"`), so decorators also work
directly in the setup/main script itself.

At request time, the server re-imports the library on a fresh evaluator and
calls the handler function. Re-import is idempotent — duplicate route
registrations are detected and skipped silently.

Route decorators must sit on module-level functions. A decorated method
inside a class registers a reference the server cannot dispatch (the function
is not at the top level of the module) — the route fails with a logged
"function not found" error on first request. Decorate a module-level function
that delegates to the class instead.

The imperative API (`runtime.http.get("/path", "lib.func")`) continues to
work unchanged. Both forms can coexist in the same project.

### Request Object

The request object passed to handlers provides:

```python
def handler(request):
    # HTTP method
    method = request.method

    # Path parameters (from URL patterns like /users/{id})
    user_id = request.path_param("id")

    # Query parameters
    page = request.query_param("page", "1")

    # Headers
    content_type = request.header("Content-Type")

    # Request body (a string field)
    body = request.body

    # JSON body (parsed)
    data = request.json()

    # Remote address
    remote_addr = request.remote_addr
```

### Response Helpers

```python
import scriptling.runtime as runtime

def handler(request):
    # JSON response
    return runtime.http.json(200, {"status": "ok"})

    # Text response
    return runtime.http.text(200, "Hello, World!")

    # HTML response
    return runtime.http.html(200, "<h1>Hello</h1>")

    # Custom status
    return runtime.http.json(404, {"error": "Not found"})

    # Redirect
    return runtime.http.redirect("/new-location")
```

## Complete Example

### REST API Server

```bash
scriptling --server :8000 --bearer-token secret123 app.py
```

```python
# app.py
import scriptling.runtime as runtime

# Register routes
runtime.http.get("/", "handlers.index")
runtime.http.get("/api/users", "handlers.list_users")
runtime.http.post("/api/users", "handlers.create_user")
runtime.http.get("/api/users/{id}", "handlers.get_user")
```

```python
# handlers.py
import scriptling.runtime as runtime

users = {
    "1": {"id": "1", "name": "Alice"},
    "2": {"id": "2", "name": "Bob"},
}

def index(request):
    return runtime.http.json(200, {"service": "User API", "version": "1.0"})

def list_users(request):
    return runtime.http.json(200, list(users.values()))

def get_user(request):
    user_id = request.path_param("id")
    if user_id in users:
        return runtime.http.json(200, users[user_id])
    return runtime.http.json(404, {"error": "User not found"})

def create_user(request):
    data = request.json()
    user_id = str(len(users) + 1)
    users[user_id] = {"id": user_id, "name": data.get("name")}
    return runtime.http.json(201, users[user_id])
```

### Testing the API

```bash
# List users
curl -H "Authorization: Bearer secret123" \
  http://localhost:8000/api/users

# Get specific user
curl -H "Authorization: Bearer secret123" \
  http://localhost:8000/api/users/1

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Authorization: Bearer secret123" \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'
```

## See Also

- [Basic Usage](../basic-usage/) - Running scripts, interactive mode, and lint mode
- [Command Line Options](../command-line-options/) - Every flag and configuration file setting
- [MCP Server Mode](../mcp-server/) - Model Context Protocol integration
- [Runtime HTTP Library](../../../reference/libraries/runtime/http/) - HTTP server API reference
