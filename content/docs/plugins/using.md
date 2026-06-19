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

Prefer explicit `release()` for deterministic cleanup. Embedded Go applications can call `plugin.ReleaseWithContext(ctx, obj)` when release should follow a request context. The contextless `plugin.Release(obj)` and GC finalizer fallback use `plugin.DefaultReleaseTimeout`. All class instances with `__del__` get a GC finalizer installed automatically — both in-process and plugin objects — as a best-effort fallback.

## Loading Executables at Runtime

The `--plugin-dir` flag loads plugins eagerly at startup. For ad-hoc loading
from inside a script, use `scriptling.plugin.load` and `unload`. These are
always available — even without `--plugin-dir` — in run, server, and
`--json-rpc` modes.

`load` takes the library `name` first and the executable `path` second. The
loaded client is driven through `call_function` — no proxy library is
generated.

```python
import scriptling.plugin

# Spawn an executable and register it as "plugin.mine". Returns the normalised
# name. Identity is by absolute path: calling load() again with the same
# name+path is a no-op.
name = scriptling.plugin.load("mine", "/opt/myext/bin")

# Call functions on it via call_function. The short name also works:
# call_function("mine", "do_thing", "hello").
result = scriptling.plugin.call_function(name, "do_thing", "hello")

# Close the process and free the name for re-use.
scriptling.plugin.unload(name)
```

### Batch calls

Use `batch_call` to send several function calls to the same executable in one
JSON-RPC batch frame. The result list matches the input order.

```python
import scriptling.plugin

name = scriptling.plugin.load("myrpc", "scriptling",
                              args=["--json-rpc", "./setup.py"])

results = scriptling.plugin.batch_call(name, [
    {"name": "ping"},
    {"name": "add", "args": [20, 22]},
    {"name": "search", "kwargs": {"query": "hello"}},
])
```

Each call is a dictionary with `name`, optional `args`, and optional `kwargs`.
For raw JSON-RPC peers, `name` is sent directly as the JSON-RPC method. For
`scriptling=True` peers, each item is sent as a typed plugin `function.call`.
Callback arguments are not supported in `batch_call`.

### Passing command-line arguments

Use the `args` keyword to pass command-line arguments to the executable — for
example when loading `scriptling` itself in `--json-rpc` mode:

```python
import scriptling.plugin

name = scriptling.plugin.load("myrpc", "scriptling",
                              args=["--json-rpc", "./setup.py"])
result = scriptling.plugin.call_function(name, "echo", "hello")
```

### The `scriptling` flag

The flag controls whether the full Scriptling plugin protocol is used:

| Mode | Behaviour |
| --- | --- |
| `scriptling=False` (default) | No handshake. `call_function` sends the function name directly as the JSON-RPC method; `describe()` / `list()` report `transport: "json"` but no version or schema. |
| `scriptling=True` | Performs the plugin protocol handshake and uses `function.call`, so `describe()` / `list()` report version and schema from the executable. |

```python
# With handshake — describe() will show version, schema, etc.
name = scriptling.plugin.load("widgets", "/opt/widgets/widget", scriptling=True)
scriptling.plugin.call_function(name, "build", "chair")
```

### Identity, collisions, and unload

- `load()` is idempotent on path + name: calling it twice with the same
  absolute path and the same name returns the same client (the `scriptling`
  flag is ignored on the second call).
- Loading an already-loaded path under a **different** name raises an error.
- Loading a **new** path under a name already in use raises an error. The
  name must not collide with any existing plugin library — including ones
  discovered via `--plugin-dir`.
- `unload(name)` sends a best-effort shutdown, closes the process, and
  removes the client. The same name+path can be `load()`-ed again afterwards.
- All loaded executables appear in `scriptling.plugin.list()` alongside any
  plugins discovered via `--plugin-dir`.
