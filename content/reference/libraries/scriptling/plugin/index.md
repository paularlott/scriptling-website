---
title: scriptling.plugin
linkTitle: Plugin
weight: 95
---

Control library for listing, inspecting, calling, and loading executable plugins at runtime.

## Overview

The `scriptling.plugin` library is the built-in control library for executable plugins. Normal code usually imports plugin libraries directly with `import plugin.<name>`, but this library is useful for diagnostics, custom wrappers, explicit calls, resource cleanup, and loading executables on demand.

The library is always available in the CLI even without `--plugin-dir`.

## Available Functions

| Function | Description |
|----------|-------------|
| `list()` | Return metadata for all loaded executables |
| `describe(name)` | Return metadata for one plugin library |
| `call_function(library, name, *args, **kwargs)` | Call a plugin function directly |
| `batch_call(library, calls)` | Call multiple functions on one executable in a JSON-RPC batch |
| `call_method(obj, name, *args, **kwargs)` | Call a method on a remote plugin object |
| `load(name, path, scriptling=False)` | Spawn an executable and register it under `name` |
| `unload(name)` | Close a loaded executable and remove it from the registry |
| `release(obj)` | Explicitly release a remote plugin object |

## list

```python
list() -> list[dict]
```

Returns a list of metadata dictionaries for every loaded plugin.

### Returns

`list[dict]` — each entry contains keys such as `name` and `functions`.

### Example

```python
import scriptling.plugin

for meta in scriptling.plugin.list():
    print(meta["name"])
```

## describe

```python
describe(name: str) -> dict
```

Returns a metadata dictionary for a single plugin library.

### Returns

`dict` — contains keys such as `name` and `functions`.

### Example

```python
import scriptling.plugin

meta = scriptling.plugin.describe("plugin.hello")
print(meta["functions"])
```

## call_function

```python
call_function(library: str, name: str, *args, **kwargs) -> any
```

Calls a function on a loaded executable. The dispatch mode is automatic based
on how the executable was loaded:

- **Plugin protocol** (`scriptling=True`): sends `function.call` with typed
  plugin transport values. Arguments and return values preserve int/float
  distinction.
- **Raw JSON-RPC** (`scriptling=False`, the default): sends the function name
  directly as the JSON-RPC method. A single dict positional arg becomes the
  `params` object; multiple positional args become a `params` array; kwargs
  become a `params` object. Return values are raw JSON (numbers come back as
  floats).

This means `call_function` works for both plugin peers and `--json-rpc` peers
without the caller needing to know which protocol the peer speaks.

### Returns

The return value of the called function.

### Example

```python
import scriptling.plugin

# Plugin protocol peer
name = scriptling.plugin.load("widgets", "/opt/widget", scriptling=True)
scriptling.plugin.call_function(name, "build", "chair")

# Raw JSON-RPC peer (e.g. scriptling --json-rpc)
rpc = scriptling.plugin.load("rpc", "scriptling", args=["--json-rpc", "./setup.py"])
scriptling.plugin.call_function(rpc, "search", {"query": "hello"})
```

## batch_call

```python
batch_call(library: str, calls: list[dict]) -> list
```

Calls multiple functions on one loaded executable by sending a JSON-RPC batch
over that executable's stdio connection. Results are returned in the same order
as the input calls.

Each call dictionary supports:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `name` | `str` | yes | Function name, or raw JSON-RPC method name for non-plugin peers. |
| `args` | `list` or `tuple` | no | Positional arguments. |
| `kwargs` | `dict[str, any]` | no | Keyword arguments. |

For `scriptling=True` clients, each item is sent as a typed plugin
`function.call` request. For `scriptling=False` clients, each `name` is sent
directly as the raw JSON-RPC method. Callback arguments are not supported in
`batch_call`.

If any item returns a JSON-RPC error, `batch_call` raises an error for the
whole batch and includes the failing item index and method name.

### Returns

`list` — return values in the same order as `calls`.

### Example

```python
import scriptling.plugin

rpc = scriptling.plugin.load("rpc", "scriptling", args=["--json-rpc", "./setup.py"])

results = scriptling.plugin.batch_call(rpc, [
    {"name": "ping"},
    {"name": "add", "args": [20, 22]},
    {"name": "search", "kwargs": {"query": "scriptling"}},
])
```

## call_method

```python
call_method(obj: any, name: str, *args, **kwargs) -> any
```

Calls a method on a remote plugin object. Plugin-supplied class wrappers use this internally.

### Returns

The return value of the called method.

### Example

```python
import plugin.hello
import scriptling.plugin

cfg = plugin.hello.Config({"name": "Ada"})
result = scriptling.plugin.call_method(cfg, "get", "name")
```

## load

```python
load(name: str, path: str, *, scriptling: bool = False, args: list[str] = []) -> str
```

Spawns an executable and registers it under `name`. With `scriptling=False`
(the default), `call_function` sends the requested function name directly as a
raw JSON-RPC method. With `scriptling=True`, the executable must implement the
Scriptling plugin handshake and `function.call` dispatch method. The loaded
client is reachable via `call_function`, `describe`, and `list`; no proxy
library is generated.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | — | Library name to register under. Normalised into the `plugin.*` namespace (e.g. `"widgets"` becomes `"plugin.widgets"`). Must not collide with an existing plugin library name. |
| `path` | `str` | — | Filesystem path to the executable. |
| `scriptling` | `bool` | `False` | If `True`, perform the plugin protocol handshake so `describe()` / `list()` report version and schema from the executable. If `False`, the handshake is skipped; `transport` is still reported as `"json"`. |
| `args` | `list[str]` | `[]` | Command-line arguments passed to the executable (e.g. `["--json-rpc", "./setup.py"]`). |

### Short names

`call_function`, `batch_call`, `call_method`, `describe`, and `unload` all
accept either the normalised name (`"plugin.widgets"`) or the short name
(`"widgets"`).

### Identity and collisions

Identity is by absolute path. A second `load()` of the same path with the same
name is a no-op (returns the existing client, ignoring `scriptling`/`args`).
Loading an already-loaded path under a different name, or loading a new path
under a name already in use, raises an error.

### Returns

`str` — the normalised library name (e.g. `"plugin.widgets"`).

### Example

```python
import scriptling.plugin

name = scriptling.plugin.load("widgets", "/opt/widgets/widget", scriptling=True)
chair = scriptling.plugin.call_function(name, "build", "chair")

# Short name also works:
scriptling.plugin.call_function("widgets", "build", "chair")

# Pass command-line arguments:
rpc = scriptling.plugin.load("rpc", "scriptling",
                             args=["--json-rpc", "./setup.py"])
```

## unload

```python
unload(name: str) -> None
```

Closes a loaded executable's process (best-effort `plugin.shutdown` plus stdin
close) and removes it from the registry. The name is freed for re-use; the
same `name` + `path` can be `load()`-ed again afterwards.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Library name returned by `load()`, or a discovered plugin name. Short or normalised form accepted. |

### Returns

`None`

### Example

```python
import scriptling.plugin

name = scriptling.plugin.load("temp", "/tmp/worker")
scriptling.plugin.unload(name)
```

## release

```python
release(obj: any) -> None
```

Explicitly releases a remote plugin object, freeing server-side resources. Objects are released automatically when garbage collected, but this function allows deterministic cleanup.

### Returns

`None`

### Example

```python
import plugin.hello
import scriptling.plugin

cfg = plugin.hello.Config({"name": "Ada"})
scriptling.plugin.release(cfg)
```

## See Also

- [Plugins](/docs/plugins/) - Loading and writing executable plugins
