---
title: JSON-RPC Server Mode
description: Running Scriptling as a concurrent JSON-RPC 2.0 server over stdio or HTTP.
weight: 3
---

Scriptling can run as a JSON-RPC 2.0 server over stdin/stdout or over HTTP,
letting host processes (editors, daemons, tool runners) invoke Scriptling
handlers as JSON-RPC methods.

## Starting the Server

Use the `--json-rpc` flag by itself to start a stdio JSON-RPC server:

```bash
scriptling --json-rpc setup.py
```

The setup script runs once at startup and registers method and notification
handlers via `scriptling.runtime.jsonrpc`. The server then reads newline-
delimited JSON-RPC 2.0 requests from stdin and writes one response per line to
stdout.

> **Keeping the setup script alive:** As with the HTTP server, the setup script can call [`runtime.start_server()`](../../../reference/libraries/scriptling/runtime/) to stay alive alongside the stdio server instead of exiting after registration: useful for sharing state or running background work while serving requests.

> **Logging goes to stderr.** In `--json-rpc` mode, all log output is
> automatically redirected to **stderr** so it never corrupts the JSON-RPC
> stream on stdout. You can safely combine `--log-level debug` with piping
> requests on stdin.

Use `--json-rpc` with `--server` to mount the same handlers over HTTP:

```bash
scriptling --server :8000 --json-rpc setup.py
```

HTTP JSON-RPC is served at `POST /json-rpc`. It can run alongside regular
`runtime.http` routes and MCP tools:

```bash
scriptling --server :8000 --json-rpc --mcp-tools ./tools setup.py
```

## Server Options

| Flag              | Environment Variable       | Description                          | Default    |
| ----------------- | -------------------------- | ------------------------------------ | ---------- |
| `--json-rpc`       | `SCRIPTLING_JSONRPC`       | Enable JSON-RPC server mode: stdio by default, HTTP `/json-rpc` with `--server` | false      |
| `--server`         | `SCRIPTLING_SERVER`        | HTTP server address for HTTP JSON-RPC | (disabled) |
| `--allowed-paths` | `SCRIPTLING_ALLOWED_PATHS` | Allowed filesystem paths             | (none)     |
| `--kv-storage`    | `SCRIPTLING_KV_STORAGE`    | Directory for persistent KV store    | in-memory  |
| `--libpath`       | `SCRIPTLING_LIBPATH`       | Extra library search directories     | none       |
| `--package`       | -                          | Load libraries from a package (zip)  | none       |
| `--plugin-dir`    | `SCRIPTLING_PLUGIN_DIR`    | Load plugin libraries                | none       |

`--json-rpc` selects one transport. Without `--server` it uses stdio; with
`--server` it mounts HTTP JSON-RPC at `/json-rpc`.

## Registering Handlers

Handlers are referenced by string (`"library.function"`), the same model used by
`runtime.http`. Each request runs on a fresh, isolated evaluator, so handlers
are fully concurrent and a slow handler never blocks the next request.

```python
# setup.py
import scriptling.runtime as runtime

runtime.jsonrpc.method("echo", "handlers.echo")
runtime.jsonrpc.method("divide", "handlers.divide")
runtime.jsonrpc.notification("progress", "handlers.on_progress")
```

```python
# handlers.py
import scriptling.runtime as runtime

def echo(params):
    return params

def divide(params):
    if params["b"] == 0:
        return runtime.jsonrpc.error(-32602, "division by zero", {"field": "b"})
    return params["a"] / params["b"]

def on_progress(params):
    # Notifications receive params but produce no response.
    pass
```

See the [scriptling.runtime.jsonrpc reference](../../../reference/libraries/scriptling/runtime/jsonrpc/)
for the full API.

## Talking to the Stdio Server

```bash
# Single request
echo '{"jsonrpc":"2.0","method":"echo","params":{"hello":"world"},"id":1}' \
  | scriptling --json-rpc setup.py
# {"jsonrpc":"2.0","result":{"hello":"world"},"id":1}

# Batch (returned as a single JSON array)
echo '[{"jsonrpc":"2.0","method":"divide","params":{"a":1,"b":0},"id":1},
       {"jsonrpc":"2.0","method":"echo","params":42,"id":2}]' \
  | scriptling --json-rpc setup.py
# [{"jsonrpc":"2.0","error":{"code":-32602,"message":"division by zero","data":{"field":"b"}},"id":1},
#  {"jsonrpc":"2.0","result":42,"id":2}]

# Notification (no id): no response is written
echo '{"jsonrpc":"2.0","method":"progress","params":{"done":1}}' \
  | scriptling --json-rpc setup.py
```

## Talking to the HTTP Server

```bash
# Single request
curl -X POST http://127.0.0.1:8000/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"echo","params":{"hello":"world"},"id":1}'
# {"jsonrpc":"2.0","result":{"hello":"world"},"id":1}

# Batch. Notifications inside the batch are handled but omitted from the response.
curl -X POST http://127.0.0.1:8000/json-rpc \
  -H "Content-Type: application/json" \
  -d '[{"jsonrpc":"2.0","method":"divide","params":{"a":1,"b":0},"id":1},
       {"jsonrpc":"2.0","method":"progress","params":{"done":1}},
       {"jsonrpc":"2.0","method":"echo","params":42,"id":2}]'

# Notification-only requests return 204 No Content.
curl -i -X POST http://127.0.0.1:8000/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"progress","params":{"done":1}}'
```

## Concurrency

Each request is dispatched on its own goroutine with a fresh Scriptling
evaluator, mirroring `runtime.http`, MCP, and WebSocket serving. Two slow
handlers running back-to-back finish in roughly one handler's time, not the sum.

Handlers cannot share in-memory state across requests. To coordinate between
requests, use `runtime.kv` (with `--kv-storage` for persistence) or the
`runtime.sync` primitives (WaitGroup, Queue, Atomic, Shared).

## Error Handling

| Code | Meaning | When |
|------|---------|------|
| `-32700` | Parse error | Malformed JSON on stdin or in the HTTP request body |
| `-32600` | Invalid request | Not a valid JSON-RPC 2.0 request |
| `-32601` | Method not found | No handler registered for `method` |
| `-32602` | Invalid params | Params failed to decode, or via `runtime.jsonrpc.error()` |
| `-32603` | Internal error | Request cancelled (e.g. signal) |
| `-32000` | Server error | Handler raised an exception |

Return `runtime.jsonrpc.error(code, message, data=None)` from a handler to emit
a response with a custom error code and optional structured `data`.

## See Also

- [scriptling.runtime.jsonrpc reference](../../../reference/libraries/scriptling/runtime/jsonrpc/)
- [HTTP Server Mode](../http-server/) for the equivalent HTTP concurrency model
