---
title: scriptling.runtime.plugin
linkTitle: runtime.plugin
weight: 4
---

Declare a Scriptling script as a first-class plugin server.

`scriptling.runtime.plugin` lets a setup script expose itself via the full
Scriptling plugin protocol — the same protocol used by compiled Go or C plugin
executables. When the server starts, clients can load it with `scriptling=True`
and receive auto-generated `plugin.<name>` proxy libraries with wrappers for
every registered function, constant, and class.

Available in the **agent variant** of Scriptling only (registered alongside
`scriptling.ai.agent`).

## Available Functions

| Function | Description |
|----------|-------------|
| `serve(name, version="", description="")` | Declare this script as a plugin server |
| `register_function(name, handler)` | Register a callable function |
| `register_constant(name, value)` | Register a read-only constant |
| `register_class(handler)` | Register a class with full object lifecycle |

## Function Reference

### scriptling.runtime.plugin.serve(name, version="", description="")

Declare this script as a Scriptling plugin server.

**Parameters:**

- `name` (str): Library name. Clients import it as `plugin.<name>`.
- `version` (str, optional): Version string (e.g. `"1.0.0"`).
- `description` (str, optional): Human-readable description surfaced in plugin metadata.

Must be called before `runtime.start_server()`. A warning is printed to stderr
if called after the server has started.

### scriptling.runtime.plugin.register_function(name, handler)

Register a function for the plugin server.

**Parameters:**

- `name` (str): Function name exposed to plugin clients.
- `handler` (str): Handler as `"library.function"` string.

The handler receives individual positional arguments decoded from the plugin
transport — not a raw params blob. Each call runs on a fresh, isolated
evaluator (the same concurrency model as `runtime.http` and `runtime.jsonrpc`
handlers).

**Callbacks:** If a client passes a callable (function or lambda) as an
argument, the handler receives it as a callable object and can invoke it
normally. Callbacks are only supported over the **stdio transport**; HTTP
connections are request/response only.

Raise an exception from the handler to produce an error response on the
client side.

### scriptling.runtime.plugin.register_constant(name, value)

Register a constant exported by the plugin server.

**Parameters:**

- `name` (str): Constant name exposed to plugin clients.
- `value` (any): Any JSON-serialisable value: `bool`, `int`, `float`, `str`, `list`, `dict`, or `None`.

Constants are included in the `scriptling.handshake` schema and delivered to
clients as part of the auto-generated proxy library. Clients read them as plain
attributes: `plugin.myservice.VERSION`.

### scriptling.runtime.plugin.register_class(handler)

Register a class exported by the plugin server.

**Parameters:**

- `handler` (str): Class as `"library.ClassName"` string.

The exposed class name is taken from the last segment of `handler`
(e.g. `"mymodule.Config"` → `"Config"`). The server handles the complete
object lifecycle:

- **`object.new`** — calls the constructor (`__init__`), stores the instance server-side, returns a remote handle.
- **`object.call_method`** — calls a method on the stored instance.
- **`object.destroy`** — calls `__del__` (if defined) and removes the instance.

The class and its method closures are resolved once at server startup. Must be
called before `runtime.start_server()`.

## Transports

| Transport | Functions | Constants | Classes | Callbacks |
|-----------|-----------|-----------|---------|-----------|
| **stdio** | ✓ | ✓ | ✓ | ✓ |
| **HTTP** | ✓ | ✓ | ✓ | — (request/response only) |

Run as a stdio plugin server:

```bash
scriptling --json-rpc setup.py
```

Run as an HTTP plugin server (plugin protocol served at `POST /json-rpc`):

```bash
scriptling --server :8000 --json-rpc setup.py
```

## Examples

### Basic function server

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic operations")
plugin_srv.register_function("add", "handlers.add")
plugin_srv.register_function("multiply", "handlers.multiply")
plugin_srv.register_constant("VERSION", "1.0.0")

runtime.start_server()
```

```python
# handlers.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

```python
# client script
import scriptling.plugin as plugin

plugin.load("calculator", "scriptling", scriptling=True, args=["--json-rpc", "setup.py"])
import plugin.calculator

print(plugin.calculator.VERSION)           # "1.0.0"
print(plugin.calculator.add(3, 4))         # 7
print(plugin.calculator.multiply(3, 4))    # 12
```

### Classes

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("formatter", "1.0")
plugin_srv.register_class("handlers.Template")
runtime.start_server()
```

```python
# handlers.py
class Template:
    def __init__(self, prefix):
        self.prefix = prefix

    def render(self, name):
        return self.prefix + name
```

```python
# client script
import plugin.formatter

t = plugin.formatter.Template("Hello, ")
print(t.render("world"))    # "Hello, world"
```

### Callbacks (stdio only)

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("transform", "1.0")
plugin_srv.register_function("apply", "handlers.apply")
runtime.start_server()
```

```python
# handlers.py
def apply(fn, items):
    return [fn(x) for x in items]
```

```python
# client script
import plugin.transform

result = plugin.transform.apply(lambda x: x * 2, [1, 2, 3])
print(result)   # [2, 4, 6]
```

### Keeping the setup script alive

Use `runtime.start_server(wait=False)` with a `server_running()` loop when the
setup script needs to maintain state or perform cleanup on shutdown:

```python
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("stateful", "1.0")
plugin_srv.register_function("greet", "handlers.greet")
plugin_srv.register_constant("VERSION", "1.0.0")

runtime.start_server(wait=False)
while runtime.server_running():
    yield_now()
# cleanup runs here after shutdown signal
```

## Comparison with Go Plugins

| | Go plugin | Scriptling plugin server |
|---|---|---|
| **Language** | Go | Scriptling (Python-like) |
| **Distribution** | Compiled binary | Script file |
| **Handler isolation** | Shared process state | Fresh evaluator per call |
| **Type safety** | Typed via `FunctionBuilder` | Duck-typed |
| **Functions** | `RegisterFunc` | `register_function` |
| **Constants** | `Constant` | `register_constant` |
| **Classes** | `RegisterClass` | `register_class` |
| **Callbacks** | stdio and HTTP | stdio only |

## Notes

- `runtime.start_server()` is optional. If the setup script exits without
  calling it, the server starts automatically (backward-compatible behaviour).
  Call it explicitly when you need `wait=False` lifecycle control.
- All registration calls (`register_function`, `register_constant`,
  `register_class`) must happen before `runtime.start_server()`. Calls after
  server start are silently ignored with a stderr warning.
- Handler functions run on fresh evaluators and cannot share in-memory state.
  Use `runtime.kv` for cross-request state.
