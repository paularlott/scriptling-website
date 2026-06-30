---
title: Plugin Server Mode
description: Run a Scriptling script as a first-class plugin that clients can load with scriptling=True.
weight: 4
---

`runtime.plugin` lets a Scriptling script expose itself as a **first-class plugin
peer**: one that implements the full plugin handshake protocol. When loaded by
another Scriptling process with `scriptling=True`, the host generates proxy
libraries automatically, just as if you had built a Go or C plugin executable.

This is available in the **agent variant** of Scriptling only (registered
alongside `scriptling.ai.agent`).

## How It Works

Instead of a compiled binary, the plugin server is an ordinary Scriptling
setup script:

1. The setup script calls `runtime.plugin.serve(name, version, description)` to
   declare a plugin identity.
2. It registers functions, constants, and classes with `runtime.plugin.register_function`,
   `runtime.plugin.register_constant`, and `runtime.plugin.register_class`.
3. It calls `runtime.start_server()`: the CLI switches from the plain JSON-RPC
   loop to the full plugin protocol, serving `scriptling.handshake`,
   `function.call`, `object.*`, and constants over stdio or HTTP.
4. A host process loads it with `scriptling.plugin.load(..., scriptling=True)`,
   or via `--plugin-dir` if the script is wrapped in a thin shell shim, and gets
   an auto-generated `plugin.<name>` proxy library.

## Basic Example

```python
# setup.py  (the plugin server script)
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic operations")
plugin_srv.register_function("add", "handlers.add")
plugin_srv.register_function("multiply", "handlers.multiply")
plugin_srv.register_constant("VERSION", "1.0.0")
plugin_srv.register_class("handlers.Config")

runtime.start_server()
```

```python
# handlers.py  (loaded on demand per request)
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Config:
    def __init__(self, prefix):
        self.prefix = prefix

    def greeting(self, name):
        return self.prefix + name
```

Run it as a stdio plugin server:

```bash
scriptling --json-rpc setup.py
```

Load it from another Scriptling process:

```python
import scriptling.plugin as plugin

plugin.load("calculator", "http://127.0.0.1:8000/json-rpc", scriptling=True)
import plugin.calculator
print(plugin.calculator.VERSION)           # "1.0.0"
print(plugin.calculator.add(3, 4))         # 7
cfg = plugin.calculator.Config("Hello, ")
print(cfg.greeting("world"))               # "Hello, world"
```

Or as a subprocess over stdio:

```python
import scriptling.plugin as plugin

plugin.load("calculator", "scriptling", scriptling=True, args=["--json-rpc", "setup.py"])
import plugin.calculator
print(plugin.calculator.add(3, 4))
```

## API

### `runtime.plugin.serve(name, version="", description="")`

Declare this script as a Scriptling plugin server.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Library name. Clients import it as `plugin.<name>`. |
| `version` | str | Optional version string (e.g. `"1.0.0"`). |
| `description` | str | Optional human-readable description. |

Must be called before `runtime.start_server()`. A warning is printed to stderr
if called after the server has started.

### `runtime.plugin.register_function(name, handler)`

Register a function for the plugin server.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Function name exposed to plugin clients. |
| `handler` | str | Handler as `"library.function"` string. |

The handler receives individual positional arguments decoded from the plugin
transport: not a raw params blob like `runtime.jsonrpc` handlers do. Each call
runs on a fresh, isolated evaluator (the same concurrency model as HTTP and
JSON-RPC handlers).

**Callbacks:** If a client passes a callable (function, lambda, or builtin) as
an argument, the handler receives it as a callable object and can invoke it with
normal call syntax:

```python
# handlers.py
def apply(fn, x):
    return fn(x)   # fn is a callback: calling it sends callback.call back to the client
```

```python
# client script
import plugin.myservice
result = plugin.myservice.apply(lambda x: x * 2, 5)  # returns 10
```

Callbacks are only valid during the lifetime of the handler call and are only
supported over the **stdio transport**. HTTP connections are request/response
only and cannot carry server→client callback calls.

Must be called before `runtime.start_server()`.

### `runtime.plugin.register_constant(name, value)`

Register a constant exported by the plugin server.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Constant name exposed to plugin clients. |
| `value` | any | Any JSON-serialisable value: `bool`, `int`, `float`, `str`, `list`, `dict`, or `None`. |

Constants are included in the `scriptling.handshake` schema and delivered to
clients as part of the plugin library. Clients read them as plain attributes:

```python
import plugin.myservice
print(plugin.myservice.VERSION)    # "1.0.0"
print(plugin.myservice.MAX_RETRIES)  # 5
```

Must be called before `runtime.start_server()`.

### `runtime.plugin.register_class(handler)`

Register a class exported by the plugin server.

| Parameter | Type | Description |
|-----------|------|-------------|
| `handler` | str | Class as `"library.ClassName"` string. |

The exposed class name is taken from the last segment of `handler`
(e.g. `"mymodule.Config"` → `"Config"`). The server handles the complete
object lifecycle:

- **`object.new`**: calls the class constructor (`__init__`), stores the
  instance server-side, returns a remote handle to the client.
- **`object.call_method`**: calls a method on the stored instance.
- **`object.destroy`**: calls `__del__` (if defined) and removes the instance.

Clients use the class as if it were local:

```python
cfg = plugin.myservice.Config("Hello, ")
print(cfg.greeting("world"))   # "Hello, world"
```

The class and its method closures are resolved once at server startup and held
for the lifetime of the server. Must be called before `runtime.start_server()`.

## Keeping the Setup Script Alive

Use `runtime.start_server(wait=False)` with a `server_running()` loop to let
the setup script maintain state or perform graceful shutdown work while the
plugin server runs:

```python
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("stateful", "1.0", "Plugin with shared state")
plugin_srv.register_function("greet", "handlers.greet")
plugin_srv.register_constant("VERSION", "1.0.0")

runtime.start_server(wait=False)
while runtime.server_running():
    yield_now()
# cleanup happens here after shutdown signal
```

## Comparison with Go Plugins

| | Go plugin | Scriptling plugin server |
|---|---|---|
| **Language** | Go | Scriptling (Python-like) |
| **Distribution** | Compiled binary | Script file |
| **Handler isolation** | Shared process state | Fresh evaluator per call |
| **Type safety** | Typed via `FunctionBuilder` | Duck-typed |
| **Functions** | `RegisterFunc` | `runtime.plugin.register_function` |
| **Constants** | `Constant` | `runtime.plugin.register_constant` |
| **Classes** | `RegisterClass` | `runtime.plugin.register_class` |
| **Callbacks** | Supported over stdio; HTTP is request/response only | Supported over stdio; HTTP is request/response only |

## See Also

- [`scriptling.plugin.load()`](../../plugins/using/): Load a plugin peer.
- [JSON-RPC Server Mode](../jsonrpc-server/): Plain JSON-RPC without the plugin handshake.
- [Go Plugins](../../plugins/go-plugins/): Compiled plugin executables with full class and callback support.
