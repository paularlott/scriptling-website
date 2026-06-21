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

## Loading JSON-RPC Peers at Runtime

The `--plugin-dir` flag loads plugins eagerly at startup. For ad-hoc loading
from inside a script, use `scriptling.plugin.load` and `unload`. These can
spawn executable peers over stdio or connect to HTTP(S) JSON-RPC endpoints.
They are always available — even without `--plugin-dir` — in run, server, and
`--json-rpc` modes.

`load` takes the library `name` first and the executable path or HTTP endpoint
second. With the default `scriptling=False`, the loaded client is helper-only
and is driven through `call_function`. With `scriptling=True`, Scriptling
performs the plugin handshake and registers an importable `plugin.*` proxy
library.

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

HTTP endpoints use the same call surface:

```python
import scriptling.plugin

name = scriptling.plugin.load(
    "remote",
    "http://127.0.0.1:8000/json-rpc",
    headers={"Authorization": "Bearer token"},
)
result = scriptling.plugin.call_function(name, "do_thing", {"value": "hello"})
```

### Batch calls

Use `batch_call` to send several function calls to the same peer in one
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

`args` is ignored for HTTP(S) endpoints. For self-signed HTTPS endpoints, pass
`insecure_skip_tls=True`:

```python
name = scriptling.plugin.load("devrpc", "https://127.0.0.1:8443/json-rpc",
                              insecure_skip_tls=True,
                              headers={"Authorization": "Bearer token"})
```

### The `scriptling` flag

The flag controls whether the full Scriptling plugin protocol is used:

| Mode | Behaviour |
| --- | --- |
| `scriptling=False` (default) | No handshake. `call_function` sends the function name directly as the JSON-RPC method; `describe()` / `list()` report `transport: "json"` but no version or schema. |
| `scriptling=True` | Performs the plugin protocol handshake, uses `function.call`, registers an importable `plugin.*` proxy library, and fills `describe()` / `list()` from the peer. |

```python
# With handshake - import plugin.widgets works and describe() shows metadata.
name = scriptling.plugin.load("widgets", "/opt/widgets/widget", scriptling=True)
scriptling.plugin.call_function(name, "build", "chair")
import plugin.widgets
plugin.widgets.build("desk")
```

HTTP(S) peers can also receive headers on every JSON-RPC request, including
the handshake, calls, and batches:

```python
name = scriptling.plugin.load(
    "widgets",
    "https://plugins.example.test/json-rpc",
    scriptling=True,
    headers={"Authorization": "Bearer token"},
)
```

HTTP plugin transport is request/response only. It supports calls, objects,
generated `plugin.*` proxies, and batches, but the server cannot initiate
callbacks back to the client. Use stdio plugins when host callbacks or
`plugin.Logger(ctx)` are required.

### Identity, collisions, and unload

- `load()` is idempotent on path/URL + name: calling it twice with the same
  absolute path or URL and the same name returns the same client (the
  `scriptling`, `args`, `insecure_skip_tls`, and `headers` options are ignored
  on the second call).
- Loading an already-loaded path or URL under a **different** name raises an error.
- Loading a **new** path or URL under a name already in use raises an error. The
  name must not collide with any existing plugin library — including ones
  discovered via `--plugin-dir`.
- `unload(name)` sends a best-effort shutdown, closes the process, removes the
  client, and removes any dynamic `plugin.*` proxy registered for that peer.
  The same name+path can be `load()`-ed again afterwards.
- All loaded executables appear in `scriptling.plugin.list()` alongside any
  plugins discovered via `--plugin-dir`.
