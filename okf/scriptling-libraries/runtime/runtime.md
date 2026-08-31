---
description: Background tasks and concurrency, plus the runtime namespace grouping HTTP, JSON-RPC, KV, MCP, sync, sandbox, and plugin sub-libraries.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/runtime/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/runtime/
status: stable
tags:
    - libraries
    - runtime
title: scriptling.runtime
type: API Reference
---
# scriptling.runtime

## Overview

The `scriptling.runtime` namespace provides background task execution (`background()`, `start_server()`, `server_running()`) for running concurrent work alongside a script or server. It also groups the `scriptling.runtime.*` sub-libraries `http`, `jsonrpc`, `kv`, `mcp`, `plugin`, `sandbox`, and `sync` under a single import.

## Available Functions

| Function | Description |
|----------|-------------|
| `background(name, handler, *args, shared=False, **kwargs)` | Start a background task, returns a Promise |
| `start_server(wait=True)` | Signal the server to start accepting requests |
| `server_running()` | Returns `True` while the server is running |

## Functions

### `start_server(wait=True)`

Signals the server to collect registered routes and begin listening for requests. Call this after all routes and methods have been registered.

**Parameters:**
- `wait` (`bool`, optional): If `True`, blocks until the server receives a shutdown signal (equivalent to Flask's `app.run()`). If `False`, returns immediately so the script can keep running: e.g. to maintain gossip state or run a polling loop. Default: `True`.

**Returns:** `None`

Scripts that exit without calling `start_server()` continue to work unchanged: the server starts automatically after the setup script finishes. Call `start_server()` only when you need the script to stay alive alongside the running server.

```python
import scriptling.runtime as runtime

runtime.http.get("/hello", "hello_handler")

# Block until shutdown (default):
runtime.start_server()

#: or keep running with a loop:
runtime.start_server(wait=False)
while runtime.server_running():
    yield_now()
```

### `server_running()`

Returns `True` while the server is running, `False` once it receives a shutdown signal. Returns `False` in non-server (script) mode. Typically used with `start_server(wait=False)` to keep the setup script alive.

**Returns:** `bool`

```python
import scriptling.runtime as runtime

runtime.start_server(wait=False)
while runtime.server_running():
    yield_now()   # release interpreter lock on each iteration
```

### `background(name, handler, *args, shared=False, **kwargs)`

Starts a background task in a goroutine. Returns a `Promise` that can be used to wait for the result.

**Isolated vs shared environments:**

- **Isolated (default):** the handler runs in a fresh environment with only sibling functions copied in; arguments must be transferable and are deep-copied. Isolated tasks run truly in **parallel** (separate environments don't share the interpreter lock). Use this for stateless work.
- **Shared (`shared=True`):** the handler runs on a goroutine in the **same** environment, so it can read and write the caller's live variables directly. Arguments are passed live (no transferable restriction, no copying). The interpreter lock (GIL) serializes script execution, so access to shared state is safe **without locks**. Only one thread runs script at a time; threads interleave when one blocks (`time.sleep`, `Queue` operations, `Promise.wait()`, I/O). Use this for Python-style threads over shared in-memory state.

**Parameters:**
- `name` (`str`): Unique name for the task.
- `handler` (`str`): Function name to execute: either a local function (`"my_func"`) or a library function (`"lib.func"`).
- `*args` (any): Positional arguments passed to the function.
- `shared` (`bool`, keyword-only, optional): Run the handler in the caller's own environment instead of an isolated copy. Default: `False`.
- `**kwargs` (any): Keyword arguments passed to the function.

**Returns:** `Promise`: in script mode, with `get()` and `wait()` methods. Returns `None` in server mode, where tasks are fire-and-forget.

**Argument cloning:** arguments must be transferable types and are deep-copied before the task starts to prevent data races:

- Scalars (`None`, `bool`, `int`, `float`, `str`) are passed by value.
- Containers (`list`, `dict`, `set`, `tuple`) are recursively validated and deep-copied: all elements must also be transferable.
- Not allowed: instances, classes, functions, builtins, or any other runtime-backed objects.
- Circular references in containers are rejected.

```python
state = {"count": 0}

def worker(n):
    i = 0
    while i < n:
        state["count"] = state["count"] + 1  # shared, GIL-protected
        i = i + 1

t1 = runtime.background("w1", "worker", 1000, shared=True)
t2 = runtime.background("w2", "worker", 1000, shared=True)
t1.wait()
t2.wait()
print(state["count"])  # 2000
```

For ongoing coordination between tasks, use `runtime.sync` primitives (`Shared`, `Atomic`, `Queue`, `WaitGroup`). To yield the interpreter lock from a tight CPU-bound loop, use the global [`yield_now()`](https://scriptling.dev/okf/scriptling-reference/builtins.md#yield_now) builtin: it is always available without importing `runtime`.

## Sub-Libraries

- [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md): HTTP route registration and response helpers
- [scriptling.runtime.jsonrpc](https://scriptling.dev/okf/scriptling-libraries/runtime/jsonrpc.md): JSON-RPC 2.0 server over stdio or HTTP
- [scriptling.runtime.kv](https://scriptling.dev/okf/scriptling-libraries/runtime/kv.md): thread-safe key-value store
- [scriptling.runtime.mcp](https://scriptling.dev/okf/scriptling-libraries/runtime/mcp.md): decorator and request-scoped MCP registration
- [scriptling.runtime.plugin](https://scriptling.dev/okf/scriptling-libraries/runtime/plugin.md): expose a script as a first-class plugin server
- [scriptling.runtime.sync](https://scriptling.dev/okf/scriptling-libraries/runtime/sync.md): named cross-environment concurrency primitives
- [scriptling.runtime.sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md): isolated script execution environments

## Quick Start

```python
import scriptling.runtime as runtime
import scriptling.runtime.kv as kv

# Background task (handler is passed by name)
def my_task():
    print("Running in background")

runtime.background("my_task", "my_task")

# Key-value storage
store = kv.open("./mydata.db")
store.set("key", "value")
print(store.get("key"))
```

## Examples

### Concurrent calculations with Promises

```python
import scriptling.runtime as runtime

def calculate(x, y, operation="add"):
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y

p1 = runtime.background("calc1", "calculate", 10, 5, operation="add")
p2 = runtime.background("calc2", "calculate", 10, 5, operation="multiply")

print(p1.get())  # 15
print(p2.get())  # 50
```

### Coordinating tasks with WaitGroup

```python
import scriptling.runtime as runtime

wg = runtime.sync.WaitGroup("tasks")

def worker(id):
    print(f"Worker {id} done")
    wg.done()

wg.add(3)
runtime.background("w1", "worker", 1)
runtime.background("w2", "worker", 2)
runtime.background("w3", "worker", 3)

wg.wait()
print("All workers finished")
```

### Background task in server mode

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/counter", "handlers.get_counter")
runtime.background("counter_task", "tasks.increment_counter")
```

```python
# tasks.py
import scriptling.runtime as runtime
import time

def increment_counter():
    counter = runtime.sync.Atomic("request_counter", 0)
    while True:
        counter.add(1)
        time.sleep(1)
```

## Notes

- In script mode, `background()` starts the task immediately and returns a `Promise`.
- In server mode, tasks are queued during script execution and started after setup completes; `background()` returns `None`.
- Background tasks run in isolated environments: use named sync primitives to share state.
- **Always look up sync primitives by name inside the task**: do not rely on closure variables from the outer script. The task runs in a clean environment with only sibling functions; libraries must be re-imported inside the task.
- Local function handlers copy only sibling functions (not other globals) from the caller's scope: data must be passed via args or `runtime.sync` primitives.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

Background task execution itself (`background()`, `start_server()`, `server_running()`) carries low direct risk: it schedules existing script functions concurrently rather than exposing new attack surface. The risk lives in the sub-libraries it groups: `runtime.http` turns the process into an HTTP listener, and `runtime.sandbox` executes arbitrary code strings within the same process. See their pages: [HTTP](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md#security-considerations) and [Sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md#security-considerations): for the specifics.

## See Also

- [scriptling.runtime.sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md): isolated code execution
- [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md): HTTP server integration
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries)
