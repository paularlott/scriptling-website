---
description: Run a Scriptling script as a first-class plugin that clients can load with scriptling=True.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/cli/plugin-server/
sources:
    - resource: https://scriptling.dev/docs/cli/plugin-server/
status: stable
tags:
    - cli
    - plugins
    - json-rpc
title: Plugin Server Mode
type: Guide
---
# Plugin Server Mode

`runtime.plugin` lets a Scriptling script expose itself as a **first-class plugin
peer**: one that implements the full plugin handshake protocol. When loaded by
another Scriptling process with `scriptling=True`, the host generates proxy
libraries automatically, just as if you had built a Go or C plugin executable.

This mode uses the standard `scriptling` CLI and its existing JSON-RPC transports; there is no `plugin-server` subcommand.

## How It Works

Instead of a compiled binary, the plugin server is an ordinary Scriptling
setup script:

1. The setup script calls `runtime.plugin.serve(name, version, description)` to
   declare a plugin identity.
2. It registers functions, constants, and classes with `runtime.plugin.register_function`,
   `runtime.plugin.register_constant`, and `runtime.plugin.register_class` — and may
   register a fetcher with `runtime.plugin.register_fetcher` to serve sources
   (a host's declared assets) from the script itself.
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

Run and load it over stdio from another Scriptling process:

```python
import scriptling.plugin as plugin

plugin.load("calculator", "scriptling", scriptling=True,
            args=["--json-rpc", "setup.py"])
import plugin.calculator
print(plugin.calculator.VERSION)           # "1.0.0"
print(plugin.calculator.add(3, 4))         # 7
cfg = plugin.calculator.Config("Hello, ")
print(cfg.greeting("world"))               # "Hello, world"
```

For HTTP, start an HTTP server explicitly:

```bash
scriptling --server :8000 --json-rpc setup.py
```

Then load that endpoint:

```python
import scriptling.plugin as plugin

plugin.load("calculator", "http://127.0.0.1:8000/json-rpc", scriptling=True)
import plugin.calculator
print(plugin.calculator.add(3, 4))
```

## Decorator Syntax

Instead of registering functions and classes separately in the setup script,
attach them directly with decorators:

```python
# handlers.py
import scriptling.runtime.plugin as plugin

@plugin.register_function("add")
def add(a, b):
    return a + b

# Bare form uses the function name as the plugin function name
@plugin.register_function
def multiply(a, b):
    return a * b

@plugin.register_class
class Config:
    def __init__(self, prefix):
        self.prefix = prefix

    def greeting(self, name):
        return self.prefix + name
```

The setup script imports the handler library, which fires the decorators:

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic")
plugin_srv.register_constant("VERSION", "1.0.0")

import handlers  # decorators fire, functions and classes registered

runtime.start_server()
```

The imperative API (`register_function("add", "handlers.add")`,
`register_class("handlers.Config")`) continues to work unchanged. Constants
remain imperative — they aren't functions or classes and don't support
decorators.

## API

### `runtime.plugin.serve(name, version="", description="", *, metadata=None)`

Declare this script as a Scriptling plugin server.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Library name. Clients import it as `plugin.<name>`. |
| `version` | str | Optional version string (e.g. `"1.0.0"`). |
| `description` | str | Optional human-readable description. |
| `metadata` | dict | Optional opaque, host-defined manifest data carried verbatim in the handshake — the channel for a host to learn plugin-specific declarations without running plugin code. Keep it static. |

Must be called before `runtime.start_server()`. A warning is printed to stderr
if called after the server has started.

### `runtime.plugin.register_function(name, handler=None)`

Register a function for the plugin server. Supports three forms:

| Form | Syntax | Description |
|------|--------|-------------|
| Named decorator | `@plugin.register_function("add")` | Uses the given name |
| Bare decorator | `@plugin.register_function` | Uses the function's own name |
| Imperative | `register_function("add", "handlers.add")` | String reference |

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Function name exposed to plugin clients. |
| `handler` | str | Handler as `"library.function"` string (imperative only). |

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

### `runtime.plugin.register_fetcher(scheme, read_handler, glob_handler=None)`

Register a fetcher so the host can ask this peer for files on demand — how a script peer serves a host's declared assets (an icon, a logo) from strings or bytes inside the script itself, with no asset files on disk. The scriptling equivalent of a Go peer's embedded assets.

| Parameter | Type | Description |
|-----------|------|-------------|
| `scheme` | str | The source scheme to serve, e.g. `"notes"` (the host asks for `notes://<path>`). Not `http`, `https` or `file`. |
| `read_handler` | str | Handler ref called as `fn(source, path)`. Return the contents (string or bytes); `None` is a miss (not found); any other error fails the read. |
| `glob_handler` | str | Optional ref called as `fn(source, pattern)`, returning a list of `{name, is_dir}` dicts. Without it the fetcher reports no glob matches. |

```python
# setup script
import scriptling.runtime.plugin as plugin_srv

plugin_srv.register_fetcher("notes", "impl.fetch_read")

# impl.py
ASSETS = {
    "assets/icon.svg": "<svg ...>",
}

def fetch_read(source, path):
    return ASSETS.get(path)   # None answers a miss
```

A host reads declared assets peer-first and falls back to disk on a miss, so a scriptling peer can be a single-file plugin. Must be called before `runtime.start_server()`.

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

Register a class exported by the plugin server. Supports two forms:

| Form | Syntax | Description |
|------|--------|-------------|
| Bare decorator | `@plugin.register_class` | Uses the class name |
| Imperative | `register_class("handlers.Config")` | String reference |

| Parameter | Type | Description |
|-----------|------|-------------|
| `handler` | str | Class as `"library.ClassName"` string (imperative only). |

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

## Serving sources (fetchers)

`register_fetcher` turns the peer into an on-demand source server: the host asks for files as it needs them, and your handlers answer from anywhere a script can read — strings in the script, bytes, or files on disk. The common use is serving a host's declared assets (an icon, a logo) so the peer needs no asset files beside it. The fetcher contract itself — schemes, the glob language, error kinds — is [Plugin Fetchers](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md); this section is how to write the handlers in scriptling.

Both handlers are ordinary plugin handlers: `"library.function"` refs, run on a fresh evaluator per call, receiving the full source string and a slash path relative to it.

| Handler | Called as | Returns |
|---------|-----------|---------|
| `read_handler` | `fn(source, path)` | The file's contents — a string or `bytes`. `None` is a **miss** (the host falls back or reports not found); any other error fails the read. |
| `glob_handler` | `fn(source, pattern)` | A list of `{name, is_dir}` dicts. No matches is an empty list. |

### Inlined assets

The single-file pattern — the scriptling equivalent of a Go peer's `go:embed`:

```python
# impl.py
ASSETS = {
    "assets/icon.svg": "<svg xmlns=\"http://www.w3.org/2000/svg\">...</svg>",
    "assets/logo.png": bytes([0x89, 0x50, 0x4e, 0x47]),  # binary survives the wire (base64)
}

def fetch_read(source, path):
    return ASSETS.get(path)   # None answers a miss

def fetch_glob(source, pattern):
    # Simplest useful matcher: treat the pattern as a prefix. Hosts that
    # only read declared assets never call this; match however suits you.
    return [{"name": name, "is_dir": False}
            for name in ASSETS if name.startswith(pattern.rstrip("*"))]
```

```python
# setup script
plugin_srv.register_fetcher("notes", "impl.fetch_read", "impl.fetch_glob")
```

### Serving files from disk

A fetcher may also front real files — here a `files/` folder beside the peer, with the path shape checked so a request can never escape the root:

```python
# impl.py
import os
import os.path
import sys
import pathlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "files")

def fetch_read(source, path):
    # A miss, not an error, for anything that is not a file inside ROOT.
    if path == "" or path.startswith("/") or path.startswith(".."):
        return None
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    return pathlib.Path(full).read_text()
```

Return `None` for anything the peer does not serve — the host treats it as not-found exactly like a missing file, and a host such as knot falls back to the plugin folder on disk. Raise (or return an error) only when the peer genuinely failed: hosts retry or degrade, they do not treat it as a miss.

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

- [`scriptling.plugin.load()`](https://scriptling.dev/okf/scriptling-docs/plugins/using.md): Load a plugin peer.
- [JSON-RPC Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/jsonrpc-server.md): Plain JSON-RPC without the plugin handshake.
- [Go Plugins](https://scriptling.dev/okf/scriptling-docs/plugins/go-plugins.md): Compiled plugin executables with full class and callback support.
