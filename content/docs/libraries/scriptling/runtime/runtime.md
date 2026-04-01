---
title: scriptling.runtime
linkTitle: runtime
weight: 1
---

Background tasks and concurrency for scripts and HTTP servers.

## Available Functions

| Function                                   | Description                                      |
| ------------------------------------------ | ------------------------------------------------ |
| `background(name, handler, *args, **kwargs)` | Start a background task, returns a Promise |

## Setup

```go
import "github.com/paularlott/scriptling/extlibs"

// Register only the core runtime library (background function)
extlibs.RegisterRuntimeLibrary(p)

// Optionally register sub-libraries individually
extlibs.RegisterRuntimeHTTPLibrary(p)   // HTTP routes and responses
extlibs.RegisterRuntimeKVLibrary(p)     // Key-value store
extlibs.RegisterRuntimeSyncLibrary(p)   // Concurrency primitives

// Or register everything at once (core + all sub-libraries)
extlibs.RegisterRuntimeLibraryAll(p)
```

## Functions

### scriptling.runtime.background(name, handler, *args, **kwargs)

Start a background task in a goroutine. Returns a `Promise` that can be used to wait for the result.

**Parameters:**

- `name` (string): Unique name for the task
- `handler` (string): Function name to execute — either a local function (`"my_func"`) or a library function (`"lib.func"`)
- `*args`: Positional arguments passed to the function
- `**kwargs`: Keyword arguments passed to the function

**Returns:** A `Promise` object (in script mode) or `None` (in server mode, where tasks are fire-and-forget).

**Promise methods:**

| Method   | Description                                      |
| -------- | ------------------------------------------------ |
| `get()`  | Block until the task completes and return its result |
| `wait()` | Block until the task completes, discard the result |

**Argument cloning:** Arguments must be transferable types and are deep-copied before the task starts to prevent data races between the caller and background task:

- Scalars (`None`, `bool`, `int`, `float`, `str`) are passed by value
- Containers (`list`, `dict`, `set`, `tuple`) are recursively validated and deep-copied — all elements must also be transferable
- Not allowed: instances, classes, functions, builtins, or any other runtime-backed objects
- Circular references in containers are rejected

For ongoing coordination between tasks, use `runtime.sync` primitives (`Shared`, `Atomic`, `Queue`, `WaitGroup`).

## Sub-Libraries

- [scriptling.runtime.http](../http/) - HTTP route registration and response helpers
- [scriptling.runtime.kv](../kv/) - Thread-safe key-value store
- [scriptling.runtime.sync](../sync/) - Named cross-environment concurrency primitives
- [scriptling.runtime.sandbox](../sandbox/) - Isolated script execution environments

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

- In script mode, `background()` starts the task immediately and returns a `Promise`
- In server mode, tasks are queued during script execution and started after setup completes; `background()` returns `None`
- Background tasks run in isolated environments — use named sync primitives to share state
- **Always look up sync primitives by name inside the task** — do not rely on closure variables from the outer script. The task runs in a clean environment with only sibling functions; libraries must be re-imported inside the task
- Local function handlers copy only sibling functions (not other globals) from the caller's scope — data must be passed via args or `runtime.sync` primitives
