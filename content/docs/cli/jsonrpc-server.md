---
title: JSON-RPC Server Mode
description: Running Scriptling as a concurrent stdio JSON-RPC 2.0 server.
weight: 3
---

Scriptling can run as a JSON-RPC 2.0 server over stdin/stdout, letting host
processes (editors, daemons, tool runners) invoke Scriptling handlers as
JSON-RPC methods.

## Starting the Server

Use the `--jsonrpc` flag to start a stdio JSON-RPC server:

```bash
scriptling --jsonrpc setup.py
```

The setup script runs once at startup and registers method and notification
handlers via `scriptling.runtime.jsonrpc`. The server then reads newline-
delimited JSON-RPC 2.0 requests from stdin and writes one response per line to
stdout.

> **Logging goes to stderr.** In `--jsonrpc` mode, all log output is
> automatically redirected to **stderr** so it never corrupts the JSON-RPC
> stream on stdout. You can safely combine `--log-level debug` with piping
> requests on stdin.

## Server Options

| Flag              | Environment Variable       | Description                          | Default    |
| ----------------- | -------------------------- | ------------------------------------ | ---------- |
| `--jsonrpc`       | `SCRIPTLING_JSONRPC`       | Enable stdio JSON-RPC server mode    | false      |
| `--allowed-paths` | `SCRIPTLING_ALLOWED_PATHS` | Allowed filesystem paths             | (none)     |
| `--kv-storage`    | `SCRIPTLING_KV_STORAGE`    | Directory for persistent KV store    | in-memory  |
| `--libpath`       | -                          | Extra library search directories     | none       |
| `--package`       | -                          | Load libraries from a package (zip)  | none       |
| `--plugin-dir`    | -                          | Load plugin libraries                | none       |

`--jsonrpc` and `--server` are mutually exclusive modes.

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

## Talking to the Server

```bash
# Single request
echo '{"jsonrpc":"2.0","method":"echo","params":{"hello":"world"},"id":1}' \
  | scriptling --jsonrpc setup.py
# {"jsonrpc":"2.0","result":{"hello":"world"},"id":1}

# Batch (returned as a single JSON array)
echo '[{"jsonrpc":"2.0","method":"divide","params":{"a":1,"b":0},"id":1},
       {"jsonrpc":"2.0","method":"echo","params":42,"id":2}]' \
  | scriptling --jsonrpc setup.py
# [{"jsonrpc":"2.0","error":{"code":-32602,"message":"division by zero","data":{"field":"b"}},"id":1},
#  {"jsonrpc":"2.0","result":42,"id":2}]

# Notification (no id) — no response is written
echo '{"jsonrpc":"2.0","method":"progress","params":{"done":1}}' \
  | scriptling --jsonrpc setup.py
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
| `-32700` | Parse error | Malformed JSON on stdin |
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
