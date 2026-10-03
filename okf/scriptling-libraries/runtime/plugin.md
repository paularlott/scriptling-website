---
description: Declare a Scriptling script as a first-class plugin server exposing functions, constants, and classes to remote clients.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/plugin/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/plugin/
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

It is registered as a runtime server surface and is independent of `scriptling.ai.agent`.

## Available Functions

| Function | Description |
|----------|-------------|
| `serve(name, version="", description="", *, metadata=None)` | Declare this script as a plugin server |
| `register_function(name, handler=None)` | Register a callable function (also usable as a decorator) |
| `register_constant(name, value)` | Register a read-only constant |
| `register_class(handler)` | Register a class with full object lifecycle (also usable as a decorator) |
| `register_fetcher(scheme, read_handler, glob_handler=None)` | Serve sources (such as a host's declared assets) on demand |

## Functions

### `serve(name, version="", description="", *, metadata=None)`

Declares this script as a Scriptling plugin server. Must be called before `runtime.start_server()`; a warning is printed to stderr if called after the server has started.

**Parameters:**
- `name` (`str`): Library name. Clients import it as `plugin.<name>`.
- `version` (`str`, optional): Version string (e.g. `"1.0.0"`). Default: `""`.
- `description` (`str`, optional): Human-readable description surfaced in plugin metadata. Default: `""`.
- `metadata` (`dict`, keyword-only, optional): Opaque, host-defined manifest data carried verbatim in the handshake: the channel for a host to learn plugin-specific declarations without running plugin code. Keep it static. Default: `None`.

**Returns:** `None`

```python
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic operations")
plugin_srv.register_function("add", "handlers.add")
runtime.start_server()
```

### `register_function(name, handler=None)`

Registers a function for the plugin server. The handler receives individual positional arguments decoded from the plugin transport: not a raw params blob. Each call runs on a fresh, isolated evaluator (the same concurrency model as `runtime.http` and `runtime.jsonrpc` handlers). Raise an exception from the handler to produce an error response on the client side.

If a client passes a callable (function or lambda) as an argument, the handler receives it as a callable object and can invoke it normally. Callbacks are only supported over the **stdio transport**; HTTP connections are request/response only.

**Parameters:**
- `name` (`str`): Function name exposed to plugin clients.
- `handler` (`str`, optional): Handler as `"library.function"` string. Omitted when used as a decorator.

**Returns:** `None`

It can also be used as a decorator in a handler library: `@plugin.register_function("add")` uses the given name, and bare `@plugin.register_function` uses the function's own name. See [Decorator Syntax](https://scriptling.dev/okf/scriptling-docs/cli/plugin-server.md#decorator-syntax).

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
- `handler` (`str`): Class as `"library.ClassName"` string. Omitted when used as a decorator.

**Returns:** `None`

It can also be used as a bare decorator, `@plugin.register_class`, which uses the class name. See [Decorator Syntax](https://scriptling.dev/okf/scriptling-docs/cli/plugin-server.md#decorator-syntax).

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

### `register_fetcher(scheme, read_handler, glob_handler=None)`

Registers a fetcher so the host can ask this peer for files on demand: how a script peer serves a host's declared assets (an icon, a logo) from strings or bytes inside the script itself, with no asset files on disk. The scriptling equivalent of a Go peer's embedded assets. A host reads declared assets peer-first and falls back to disk on a miss, so a scriptling peer can be a single-file plugin. Must be called before `runtime.start_server()`.

**Parameters:**
- `scheme` (`str`): The source scheme to serve, e.g. `"notes"` (the host asks for `notes://<path>`). Not `http`, `https` or `file`.
- `read_handler` (`str`): Handler ref called as `fn(source, path)`. Return the contents (string or bytes); `None` is a miss (not found); any other error fails the read.
- `glob_handler` (`str`, optional): Handler ref called as `fn(source, pattern)`, returning a list of `{name, is_dir}` dicts. Without it the fetcher reports no glob matches. Default: `None`.

**Returns:** `None`

```python
# setup script
import scriptling.runtime.plugin as plugin_srv

plugin_srv.register_fetcher("notes", "impl.fetch_read")
```

```python
# impl.py
ASSETS = {
    "assets/icon.svg": "<svg ...>",
}

def fetch_read(source, path):
    return ASSETS.get(path)   # None answers a miss
```

See [Serving sources (fetchers)](https://scriptling.dev/okf/scriptling-docs/cli/plugin-server.md#serving-sources-fetchers) for inlined-asset and from-disk patterns, and [Plugin Fetchers](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md) for the fetcher contract.

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

See [Plugin Server Mode: Comparison with Go Plugins](https://scriptling.dev/okf/scriptling-docs/cli/plugin-server.md#comparison-with-go-plugins) for how a script plugin server differs from a compiled Go plugin.

## Notes

- `runtime.start_server()` is optional. If the setup script exits without calling it, the server starts automatically (backward-compatible behaviour). Call it explicitly when you need `wait=False` lifecycle control.
- All registration calls (`serve`, `register_function`, `register_constant`, `register_class`, `register_fetcher`) must happen before `runtime.start_server()`. Calls after server start are silently ignored with a stderr warning.
- Handler functions run on fresh evaluators and cannot share in-memory state. Use `runtime.kv` for cross-request state.

## Security Considerations

This is an extended library, requiring registration in Go via `RegisterRuntimePluginLibrary` (called after `RegisterRuntimeLibraryAll`), see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries).

`scriptling.runtime.plugin` does not execute arbitrary code strings the way `runtime.sandbox` does: `RegisterRuntimePluginLibrary` only registers a transport that decodes plugin-protocol calls and dispatches them to functions, constants, and classes the script explicitly registered. The risk shape is the same as `runtime.http` and `runtime.jsonrpc`: declaring `serve()` and registering handlers turns the process into a network-reachable (or stdio-reachable) RPC server, so every `register_function`/`register_class` call is a new entry point reachable by any connected plugin client. Registered classes additionally hand the server full object lifecycle control (construct, call methods, destroy) over server-side instances, so treat registered classes with the same care as any other exposed API surface. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [scriptling.runtime.jsonrpc](https://scriptling.dev/okf/scriptling-libraries/runtime/jsonrpc.md): lower-level JSON-RPC method registration without the full plugin handshake
- [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md): HTTP route registration sharing the same per-request evaluator model
- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/runtime.md): `start_server()` lifecycle shared with the plugin server
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md)
