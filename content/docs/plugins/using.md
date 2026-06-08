---
title: Using Plugins
description: Load plugin directories and use plugin libraries from Scriptling code.
weight: 1
---

## CLI Loading

Use `--plugin-dir` to load executable plugins from a directory:

```bash
scriptling --plugin-dir ./plugins script.py
scriptling --plugin-dir ./plugins --plugin-dir ./more-plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

The flag can be repeated. Scriptling scans executable files directly inside each directory. Subdirectories are ignored.

Configuration options:

| Source | Key |
| --- | --- |
| CLI | `--plugin-dir ./plugins` |
| Environment | `SCRIPTLING_PLUGIN_DIR=./plugins` |
| Config file | `plugins.dirs = ["./plugins"]` |

Plugin loading is eager. Startup failures are reported as warnings. A loaded plugin that fails while a script is running produces an execution error.

## Importing Plugin Libraries

A plugin declares a short name, for example `hello`, and Scriptling exposes it as `plugin.hello`:

```python
import plugin.hello

print(plugin.hello.greet("Ada"))
```

## Inspecting Plugins

Use the built-in `scriptling.plugin` library for metadata and direct calls:

```python
import scriptling.plugin

for meta in scriptling.plugin.list():
    print(meta["name"])

meta = scriptling.plugin.describe("plugin.hello")
print(meta["functions"])

result = scriptling.plugin.call_function("plugin.hello", "greet", "Ada")
```

## Remote Objects

Plugin classes create remote objects inside the plugin process. The Scriptling object is a proxy:

```python
import plugin.hello
import scriptling.plugin

cfg = plugin.hello.Config("Ada")
print(cfg.get("name"))
scriptling.plugin.release(cfg)
```

Prefer explicit `release()` for deterministic cleanup. Embedded Go applications can call `plugin.ReleaseWithContext(ctx, obj)` when release should follow a request context. All class instances with `__del__` get a GC finalizer installed automatically — both in-process and plugin objects — as a best-effort fallback.
