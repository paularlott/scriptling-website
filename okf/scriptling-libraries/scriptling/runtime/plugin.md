---
description: Declare a Scriptling script as a first-class plugin server exposing functions, constants, and classes to remote clients.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/runtime/plugin/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/runtime/plugin/
status: stable
tags:
    - libraries
    - runtime
    - plugins
title: scriptling.runtime.plugin
type: API Reference
---
# scriptling.runtime.plugin

## Overview

The `scriptling.runtime.plugin` library lets a setup script expose itself via the full Scriptling plugin protocol: the same protocol used by compiled Go or C plugin executables. When the server starts, clients can load it with `scriptling=True` and receive auto-generated `plugin.<name>` proxy libraries with wrappers for every registered function, constant, and class.

Available only in the **agent variant** of Scriptling, registered alongside `scriptling.ai.agent`.

## Available Functions

| Function | Description |
|----------|-------------|
| `serve(name, version="", description="")` | Declare this script as a plugin server |
| `register_function(name, handler)` | Register a callable function |
| `register_constant(name, value)` | Register a read-only constant |
| `register_class(handler)` | Register a class with full object lifecycle |

## Functions

### `serve(name, version="", description="")`

Declares this script as a Scriptling plugin server. Must be called before `runtime.start_server()`; a warning is printed to stderr if called after the server has started.

**Parameters:**
- `name` (`str`): Library name. Clients import it as `plugin.<name>`.
- `version` (`str`, optional): Version string (e.g. `"1.0.0"`). Default: `""`.
- `description` (`str`, optional): Human-readable description surfaced in plugin metadata. Default: `""`.

**Returns:** `None`

```python
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic operations")
plugin_srv.register_function("add", "handlers.add")
runtime.start_server()
```

### `register_function(name, handler)`

Registers a function for the plugin server. The handler receives individual positional arguments decoded from the plugin transport: not a raw params blob. Each call runs on a fresh, isolated evaluator (the same concurrency model as `runtime.http` and `runtime.jsonrpc` handlers). Raise an exception from the handler to produce an error response on the client side.

If a client passes a callable (function or lambda) as an argument, the handler receives it as a callable object and can invoke it normally. Callbacks are only supported over the **stdio transport**; HTTP connections are request/response only.

**Parameters:**
- `name` (`str`): Function name exposed to plugin clients.
- `handler` (`str`): Handler as `"library.function"` string.

**Returns:** `None`

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv

plugin_srv.register_function("add", "handlers.add")
plugin_srv.register_function("multiply", "handlers.multiply")
```

```python
# handlers.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

### `register_constant(name, value)`

Registers a constant exported by the plugin server. Constants are included in the `scriptling.handshake` schema and delivered to clients as part of the auto-generated proxy library. Clients read them as plain attributes: `plugin.myservice.VERSION`.

**Parameters:**
- `name` (`str`): Constant name exposed to plugin clients.
- `value` (any): Any JSON-serialisable value: `bool`, `int`, `float`, `str`, `list`, `dict`, or `None`.

**Returns:** `None`

```python
import scriptling.runtime.plugin as plugin_srv

plugin_srv.register_constant("VERSION", "1.0.0")
plugin_srv.register_constant("MAX_RETRIES", 5)
```

### `register_class(handler)`

Registers a class exported by the plugin server. The exposed class name is taken from the last segment of `handler` (e.g. `"mymodule.Config"` → `"Config"`). The class and its method closures are resolved once at server startup; must be called before `runtime.start_server()`.

The server handles the complete object lifecycle:

- **`object.new`**: calls the constructor (`__init__`), stores the instance server-side, returns a remote handle.
- **`object.call_method`**: calls a method on the stored instance.
- **`object.destroy`**: calls `__del__` (if defined) and removes the instance.

**Parameters:**
- `handler` (`str`): Class as `"library.ClassName"` string.

**Returns:** `None`

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

## Transports

| Transport | Functions | Constants | Classes | Callbacks |
|-----------|-----------|-----------|---------|-----------|
| **stdio** | ✓ | ✓ | ✓ | ✓ |
| **HTTP** | ✓ | ✓ | ✓ | partial, request/response only |

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
# client script
import scriptling.plugin as plugin

plugin.load("calculator", "scriptling", scriptling=True, args=["--json-rpc", "setup.py"])
import plugin.calculator

print(plugin.calculator.VERSION)           # "1.0.0"
print(plugin.calculator.add(3, 4))         # 7
print(plugin.calculator.multiply(3, 4))    # 12
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

Use `runtime.start_server(wait=False)` with a `server_running()` loop when the setup script needs to maintain state or perform cleanup on shutdown:

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

- `runtime.start_server()` is optional. If the setup script exits without calling it, the server starts automatically (backward-compatible behaviour). Call it explicitly when you need `wait=False` lifecycle control.
- All registration calls (`serve`, `register_function`, `register_constant`, `register_class`) must happen before `runtime.start_server()`. Calls after server start are silently ignored with a stderr warning.
- Handler functions run on fresh evaluators and cannot share in-memory state. Use `runtime.kv` for cross-request state.

## Security Considerations

This is an extended library, requiring registration in Go via `RegisterRuntimePluginLibrary` (called after `RegisterRuntimeLibraryAll`), see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries).

`scriptling.runtime.plugin` does not execute arbitrary code strings the way `runtime.sandbox` does: `RegisterRuntimePluginLibrary` only registers a transport that decodes plugin-protocol calls and dispatches them to functions, constants, and classes the script explicitly registered. The risk shape is the same as `runtime.http` and `runtime.jsonrpc`: declaring `serve()` and registering handlers turns the process into a network-reachable (or stdio-reachable) RPC server, so every `register_function`/`register_class` call is a new entry point reachable by any connected plugin client. Registered classes additionally hand the server full object lifecycle control (construct, call methods, destroy) over server-side instances, so treat registered classes with the same care as any other exposed API surface. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [scriptling.runtime.jsonrpc](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/jsonrpc.md): lower-level JSON-RPC method registration without the full plugin handshake
- [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/http.md): HTTP route registration sharing the same per-request evaluator model
- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/runtime.md): `start_server()` lifecycle shared with the plugin server
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md)
