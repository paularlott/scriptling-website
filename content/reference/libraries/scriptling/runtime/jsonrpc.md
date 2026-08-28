---
title: scriptling.runtime.jsonrpc
linkTitle: runtime.jsonrpc
description: Register JSON-RPC 2.0 server methods and notifications served over stdio or HTTP.
tags: [libraries, runtime, json-rpc]
weight: 2
---

## Overview

The `scriptling.runtime.jsonrpc` library registers handlers for a JSON-RPC 2.0 **server** that runs over stdin/stdout or HTTP: it does not make outbound JSON-RPC calls. Handlers are referenced by string (`"library.function"`), the same model used by `runtime.http`, so each request runs on a fresh, isolated evaluator in its own goroutine and a slow handler never blocks the next request.

Start the stdio server with the `--json-rpc` flag:

```bash
scriptling --json-rpc setup.py
```

Logging is automatically redirected to stderr so it never corrupts the JSON-RPC stream on stdout.

Start the HTTP server with `--server` and `--json-rpc`:

```bash
scriptling --server :8000 --json-rpc setup.py
```

HTTP JSON-RPC is served at `POST /json-rpc` and can run alongside normal `runtime.http` routes and MCP tools.

## Available Functions

| Function | Description |
|----------|-------------|
| `method(name, handler)` | Register a JSON-RPC method handler |
| `notification(name, handler)` | Register a notification handler (no response) |
| `error(code, message, data=None)` | Build a structured JSON-RPC error response |
| `get_request()` | Get the HTTP request this call arrived on, or `None` over stdio |
| `request_context()` | Get the context dict set by the middleware (empty dict if none) |
| `transport()` | How the server is being served: `"http"`, `"stdio"` or `None` |

## Functions

### `method(name, handler)`

Registers a JSON-RPC method handler. The handler receives the decoded JSON-RPC `params` as its single argument and returns a JSON-compatible result. Raise an exception, or return `jsonrpc.error(...)`, to produce an error response.

**Parameters:**
- `name` (`str`): JSON-RPC method name.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
# setup.py
import scriptling.runtime as runtime

runtime.jsonrpc.method("echo", "handlers.echo")
runtime.jsonrpc.method("divide", "handlers.divide")
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
```

### `notification(name, handler)`

Registers a JSON-RPC notification handler. Notifications are JSON-RPC requests without an `id` field. The handler receives the decoded params but no response is written, and return values are ignored.

**Parameters:**
- `name` (`str`): JSON-RPC notification name.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

def on_progress(params):
    # Side effects only; no response is written.
    pass

runtime.jsonrpc.notification("progress", "handlers.on_progress")
```

### `error(code, message, data=None)`

Builds a structured JSON-RPC error response. Return this from a method handler to emit a JSON-RPC error response with a custom code.

**Parameters:**
- `code` (`int`): JSON-RPC error code (e.g. `-32602` for invalid params).
- `message` (`str`): Human-readable error message.
- `data` (any, optional): Optional structured data attached to the error. Default: `None`.

**Returns:** `JSONRPCError`: instance recognized by the server and converted into a JSON-RPC error response.

```python
import scriptling.runtime as runtime

def divide(params):
    if params["b"] == 0:
        return runtime.jsonrpc.error(-32602, "division by zero", {"field": "b"})
    return params["a"] / params["b"]
```

### `get_request()`

Returns the HTTP request this call is being served for, when the JSON-RPC server is mounted over HTTP (`POST /json-rpc`): the same [Request object](/reference/libraries/scriptling/runtime/http/#request-object) the middleware saw, with `method`, `path`, `headers`, `query`, `remote_addr` and `context`. Over the stdio transport there is no HTTP request, so it returns `None`.

**Returns:** `Request` or `None`

```python
import scriptling.runtime as runtime

def who(params):
    req = runtime.jsonrpc.get_request()
    if req != None:
        return {"ip": req.remote_addr}
    return {"ip": "stdio"}
```

### `request_context()`

Returns the context dict the [middleware](/reference/libraries/scriptling/runtime/http/#middlewarehandler) populated for this request — e.g. `request.context["user"] = name` after authenticating. It is always a dict: empty when no middleware ran or it set nothing, so `.get(name, default)` is always safe. Each call gets its own copy, so writes from the handler are local — with a batch dispatching concurrently, one element's writes are never visible to the others.

**Returns:** `dict`

```python
import scriptling.runtime as runtime

def who(params):
    user = runtime.jsonrpc.request_context().get("user", "anonymous")
    return {"user": user}
```

### `transport()`

Returns `"http"` when serving at `POST /json-rpc` (also from method handlers mid-request), `"stdio"` for the `--json-rpc` stdio server, and `None` when the script is not being served at all — so one setup script can work in every mode, since middleware never runs over stdio.

**Returns:** `str` or `None`

```python
import scriptling.runtime as runtime

if runtime.jsonrpc.transport() == "stdio":
    # No middleware over stdio: treat every caller alike.
    ...
```

## Concurrency Model

Each request is dispatched on its own goroutine with a fresh Scriptling evaluator, mirroring `runtime.http`, MCP, and WebSocket serving. Handlers cannot share in-memory state across requests; coordinate through `runtime.kv` or `runtime.sync` instead.

## Stdio Wire Format

- Requests are newline-delimited JSON objects (NDJSON), one per line.
- Batches (JSON arrays) are supported: each element is dispatched concurrently and a single JSON array of responses is returned.
- Notifications (requests with no `id`) produce no response.
- Integer precision is preserved (numbers are not coerced to floats).

## HTTP Wire Format

- Send a single JSON-RPC object or batch array with `POST /json-rpc`.
- Requests return `200 application/json`.
- Notifications and all-notification batches return `204 No Content`.
- Notifications inside a mixed batch are handled but omitted from the response array.
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

### Sample stdio session

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

### Sample HTTP session

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

- Methods/notifications are registered during setup script execution, then frozen.
- The `JSONRPCError` class is exposed as `runtime.jsonrpc.JSONRPCError` for type checks.
- Use `--json-rpc` together with `--kv-storage` or `--libpath` exactly as you would for the HTTP `--server` mode.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.runtime.jsonrpc` is server-only: it registers method/notification handlers for an incoming JSON-RPC stream and never issues outbound JSON-RPC calls itself. The risk shape matches `runtime.http`: registering a method exposes that handler to any peer that can reach the stdio stream or `POST /json-rpc` endpoint, so treat every registered method as a network-reachable entry point and validate `params` defensively. For a full risk breakdown across all libraries, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.runtime.http](../http/): HTTP route registration sharing the same per-request evaluator model
- [scriptling.runtime.plugin](../plugin/): full plugin protocol server (functions, constants, and classes)
- [scriptling.runtime.kv](../kv/): share state across JSON-RPC handlers
- [Security Guide](/docs/security/)
