---
title: scriptling.plugin
linkTitle: Plugin
weight: 95
---

Control library for listing, inspecting, and calling loaded Scriptling plugins.

## Overview

The `scriptling.plugin` library is the built-in control library for executable plugins. Normal code usually imports plugin libraries directly with `import plugin.<name>`, but this library is useful for diagnostics, custom wrappers, explicit calls, and resource cleanup.

## Available Functions

| Function | Description |
|----------|-------------|
| `list()` | Return metadata for all loaded plugins |
| `describe(name)` | Return metadata for one plugin library |
| `call_function(library, name, *args, **kwargs)` | Call a plugin function directly |
| `call_method(obj, name, *args, **kwargs)` | Call a method on a remote plugin object |
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

Calls a plugin function directly. Plugin-supplied wrappers use this internally to call hidden RPC helpers.

### Returns

The return value of the called function.

### Example

```python
import scriptling.plugin

result = scriptling.plugin.call_function("plugin.hello", "greet", "Ada")
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
