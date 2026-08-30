---
title: Using Plugins
description: Load plugin directories and use plugin libraries from Scriptling code.
tags: [plugins]
weight: 1
---

## CLI Loading

Use `--plugin-dir` to load executable plugins from a directory, or `--plugin`
to load a single executable directly:

```bash
scriptling --plugin-dir ./plugins script.py
scriptling --plugin-dir ./plugins --plugin-dir ./more-plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
scriptling --plugin ./plugins/hello script.py
```

Both flags can be repeated. Scriptling scans executable files directly inside each `--plugin-dir` directory; subdirectories are ignored. A `--plugin` value is an executable path, used literally, so paths containing spaces need nothing special — or the `http://`/`https://` URL of a plugin server, which speaks the same protocol over JSON-RPC POST instead of stdio (`--plugin-insecure` accepts a self-signed certificate). Arguments come from `--plugin-arg`, and environment entries for an executable plugin from `--plugin-env KEY=VALUE`; both bind the same way, bare with one plugin or `<plugin>=` qualified with several:

```bash
scriptling --plugin /usr/local/bin/knot \
           --plugin-arg scriptling-server --plugin-arg=--alias=testing \
           script.py
```

Values that begin with `-` need the `--plugin-arg=value` form. With one
`--plugin`, every `--plugin-arg` belongs to it; with several, qualify each as
`<plugin>=<arg>`. See
[loading plugins](/docs/cli/command-line-options/#loading-plugins) for the full
rules.

Explicit `--plugin` entries load before `--plugin-dir` scans, and the same
executable discovered in a directory loses to the explicit entry and its
arguments. Plugins register under the library name they declare in their
handshake however they are loaded.

Configuration options:

| Source | Key |
| --- | --- |
| CLI | `--plugin-dir ./plugins` |
| Environment | `SCRIPTLING_PLUGIN_DIR=./plugins` |
| Config file | `plugins.dirs = ["./plugins"]` |
| CLI | `--plugin ./plugins/hello` |
| Environment | `SCRIPTLING_PLUGIN=./plugins/hello` |
| Config file | `plugins.paths = ["./plugins/hello"]` |
| CLI | `--plugin-arg scriptling-server` |
| Environment | `SCRIPTLING_PLUGIN_ARG=scriptling-server` |
| Config file | `plugins.args = ["scriptling-server"]` |

Plugin loading is eager. Startup failures are reported as warnings. A loaded plugin that fails while a script is running produces an execution error. Commands that never evaluate a script (`--lint`, `--list-libs`, and the `pack`, `unpack` and `cache` subcommands) skip plugin loading entirely.

Plugins that serve [fetcher](/docs/plugins/fetchers/) schemes are loaded the
same way; their sources then work as packages and scripts (`--package
knot://libs`).

## Importing Plugin Libraries

A plugin declares a name in its handshake, and the name decides where the
library lands:

- A **bare name** registers in the plugin namespace. A plugin declaring
  `hello` becomes `plugin.hello`; one declaring `knot` becomes `plugin.knot`.
  Every function and class is a member of that module: `plugin.hello.greet()`,
  `plugin.hello.Config(...)`.
- A **name containing a dot** is the author's namespace and is used verbatim.
  A plugin declaring `myplugin.hello` imports as `myplugin.hello`, and the first-party
  database plugins declare `scriptling.sqlite`, `scriptling.sql`,
  `scriptling.valkey` and `scriptling.badgerdb` so their imports match
  compiled-in builds exactly.

```python
import plugin.hello
print(plugin.hello.greet("Ada"))

import scriptling.sqlite as sqlite
conn = sqlite.connect()
```

Because verbatim names can collide, registration guards them: a plugin whose
dotted name matches a library the host already has (a built-in, a stdlib
library, or a compiled-in driver) is skipped with a warning at load instead
of shadowing it. A plugin can never take over `json`, `scriptling.runtime`,
or a compiled-in driver's name. Bare names cannot collide with built-ins by
construction, since built-in names are single words.

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

Prefer explicit `release()` for deterministic cleanup. Embedded Go applications can call `plugin.ReleaseWithContext(ctx, obj)` when release should follow a request context. The contextless `plugin.Release(obj)` and GC finalizer fallback use `plugin.DefaultReleaseTimeout`. All class instances with `__del__` get a GC finalizer installed automatically, both in-process and plugin objects, as a best-effort fallback.

## Loading JSON-RPC Peers at Runtime

The `--plugin-dir` flag loads plugins eagerly at startup. For ad-hoc loading
from inside a script, use `scriptling.plugin.load` and `unload`. These can
spawn executable peers over stdio or connect to HTTP(S) JSON-RPC endpoints.
They are always available: even without `--plugin-dir`: in run, server, and
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

Use the `args` keyword to pass command-line arguments to the executable: for
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
  name must not collide with any existing plugin library, including ones
  discovered via `--plugin-dir`.
- A dotted (verbatim) name that matches a library already registered on the
  interpreter is refused at registration with a warning, so plugins cannot
  shadow built-in or compiled-in libraries.
- `unload(name)` sends a best-effort shutdown, closes the process, removes the
  client, and removes any dynamic `plugin.*` proxy registered for that peer.
  The same name+path can be `load()`-ed again afterwards.
- All loaded executables appear in `scriptling.plugin.list()` alongside any
  plugins discovered via `--plugin-dir`.
