---
title: scriptling.runtime.jsonrpc
linkTitle: runtime.jsonrpc
weight: 2
---

Concurrent JSON-RPC 2.0 server method and notification registration.

`scriptling.runtime.jsonrpc` registers handlers for a JSON-RPC 2.0 server that
can run over stdin/stdout or HTTP. Handlers are referenced by string
(`"library.function"`), the same model used by `runtime.http`, so each request
runs on a fresh, isolated evaluator in its own goroutine and a slow handler
never blocks the next request.

Start the stdio server with the `--json-rpc` flag:

```bash
scriptling --json-rpc setup.py
```

Logging is automatically redirected to stderr so it never corrupts the JSON-RPC
stream on stdout.

Start the HTTP server with `--server` and `--json-rpc`:

```bash
scriptling --server :8000 --json-rpc setup.py
```

HTTP JSON-RPC is served at `POST /json-rpc` and can run alongside normal
`runtime.http` routes and MCP tools.

## Available Functions

| Function | Description |
|----------|-------------|
| `method(name, handler)` | Register a JSON-RPC method handler |
| `notification(name, handler)` | Register a notification handler (no response) |
| `error(code, message, data=None)` | Build a structured JSON-RPC error response |

## Method Registration

### scriptling.runtime.jsonrpc.method(name, handler)

Register a JSON-RPC method handler.

**Parameters:**

- `name` (str): JSON-RPC method name
- `handler` (str): Handler function as `"library.function"`

The handler receives the decoded JSON-RPC `params` as its single argument and
returns a JSON-compatible result. Raise an exception, or return
`runtime.jsonrpc.error(...)`, to produce an error response.

### scriptling.runtime.jsonrpc.notification(name, handler)

Register a JSON-RPC notification handler.

**Parameters:**

- `name` (str): JSON-RPC notification name
- `handler` (str): Handler function as `"library.function"`

Notifications are JSON-RPC requests without an `id` field. The handler receives
the decoded params but no response is written. Return values are ignored.

### scriptling.runtime.jsonrpc.error(code, message, data=None)

Build a structured JSON-RPC error response.

**Parameters:**

- `code` (int): JSON-RPC error code (e.g. `-32602` for invalid params)
- `message` (str): Human-readable error message
- `data` (any, optional): Optional structured data attached to the error

Return this from a method handler to emit a JSON-RPC error response with a
custom code.

## Concurrency Model

Each request is dispatched on its own goroutine with a fresh Scriptling
evaluator, mirroring `runtime.http`, MCP, and WebSocket serving. Handlers cannot
share in-memory state across requests; coordinate through `runtime.kv` or
`runtime.sync` instead.

## Stdio Wire Format

- Requests are newline-delimited JSON objects (NDJSON), one per line.
- Batches (JSON arrays) are supported: each element is dispatched concurrently
  and a single JSON array of responses is returned.
- Notifications (requests with no `id`) produce no response.
- Integer precision is preserved (numbers are not coerced to floats).

## HTTP Wire Format

- Send a single JSON-RPC object or batch array with `POST /json-rpc`.
- Requests return `200 application/json`.
- Notifications and all-notification batches return `204 No Content`.
- Notifications inside a mixed batch are handled but omitted from the response
  array.
- Integer precision is preserved.

## Error Codes

| Code | Meaning | Source |
|------|---------|--------|
| `-32700` | Parse error | Malformed JSON on stdin or in the HTTP request body |
| `-32600` | Invalid request | Not a valid JSON-RPC 2.0 request |
| `-32601` | Method not found | No handler registered for `method` |
| `-32602` | Invalid params | Params failed to decode (or via `error()`) |
| `-32603` | Internal error | Request cancelled |
| `-32000` | Server error | Handler raised an exception or returned an error |

## Examples

### Setup script

```python
# setup.py
import scriptling.runtime as runtime

runtime.jsonrpc.method("echo", "handlers.echo")
runtime.jsonrpc.method("divide", "handlers.divide")
runtime.jsonrpc.notification("progress", "handlers.on_progress")
```

### Handlers

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
    # Side effects only; no response is written.
    pass
```

### Sample session

```bash
$ echo '{"jsonrpc":"2.0","method":"echo","params":{"hello":"world"},"id":1}' \
  | scriptling --json-rpc setup.py
{"jsonrpc":"2.0","result":{"hello":"world"},"id":1}

$ echo '[{"jsonrpc":"2.0","method":"divide","params":{"a":1,"b":0},"id":1},
         {"jsonrpc":"2.0","method":"echo","params":42,"id":2}]' \
  | scriptling --json-rpc setup.py
[{"jsonrpc":"2.0","error":{"code":-32602,"message":"division by zero","data":{"field":"b"}},"id":1},
 {"jsonrpc":"2.0","result":42,"id":2}]
```

### HTTP session

```bash
$ curl -X POST http://127.0.0.1:8000/json-rpc \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"echo","params":{"hello":"world"},"id":1}'
{"jsonrpc":"2.0","result":{"hello":"world"},"id":1}

$ curl -i -X POST http://127.0.0.1:8000/json-rpc \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"progress","params":{"done":1}}'
HTTP/1.1 204 No Content
```

## Notes

- Routes/methods are registered during setup script execution, then frozen.
- The `JSONRPCError` class is exposed as `runtime.jsonrpc.JSONRPCError` for
  type checks.
- Use `--json-rpc` together with `--kv-storage` or `--libpath` exactly as you
  would for the HTTP `--server` mode.
