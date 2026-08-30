---
description: Control library for listing, inspecting, calling, and loading executable plugins at runtime.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/plugin/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/plugin/
status: stable
tags:
    - libraries
    - plugins
title: scriptling.plugin
type: API Reference
---
# scriptling.plugin

The `scriptling.plugin` library is the built-in control library for executable plugins. Normal code usually imports plugin libraries directly with `import plugin.<name>`, but this library is useful for diagnostics, custom wrappers, explicit calls, resource cleanup, and loading executables on demand.

It is always available in the CLI even without `--plugin-dir`.

## Available Functions

| Function | Description |
|----------|-------------|
| `list()` | Return metadata for all loaded executables |
| `describe(name)` | Return metadata for one plugin library |
| `call_function(library, name, *args, **kwargs)` | Call a plugin function directly |
| `batch_call(library, calls)` | Call multiple functions on one executable in a JSON-RPC batch |
| `call_method(obj, name, *args, **kwargs)` | Call a method on a remote plugin object |
| `load(name, path, scriptling=False, args=None, insecure_skip_tls=False, headers=None)` | Register an executable or HTTP(S) JSON-RPC peer under `name` |
| `unload(name)` | Close a loaded executable and remove it from the registry |
| `release(obj)` | Explicitly release a remote plugin object |

## Functions

### `list()`

Returns a list of metadata dictionaries for every loaded plugin.

**Returns:** `list` of `dict`: each entry contains keys such as `name` and `functions`.

```python
import scriptling.plugin

for meta in scriptling.plugin.list():
    print(meta["name"])
```

### `describe(name)`

Returns a metadata dictionary for a single plugin library.

**Parameters:**
- `name` (`str`): Library name, short or normalised form.

**Returns:** `dict`: contains keys such as `name` and `functions`.

```python
import scriptling.plugin

meta = scriptling.plugin.describe("plugin.hello")
print(meta["functions"])
```

### `call_function(library, name, *args, **kwargs)`

Calls a function on a loaded JSON-RPC peer. The dispatch mode is automatic based on how the peer was loaded:

- **Plugin protocol** (`scriptling=True`): sends `function.call` with typed plugin transport values. Arguments and return values preserve int/float distinction.
- **Raw JSON-RPC** (`scriptling=False`, the default): sends the function name directly as the JSON-RPC method. A single dict positional arg becomes the `params` object; multiple positional args become a `params` array; kwargs become a `params` object. Return values are raw JSON (numbers come back as floats).

This means `call_function` works for plugin peers, stdio `--json-rpc` peers, and HTTP(S) JSON-RPC peers without the caller needing to know which protocol the peer speaks.

**Parameters:**
- `library` (`str`): Library name returned by `load()`, short or normalised form.
- `name` (`str`): Function name to call (or raw JSON-RPC method name for non-plugin peers).
- `*args`: Positional arguments to pass.
- `**kwargs`: Keyword arguments to pass.

**Returns:** The return value of the called function.

```python
import scriptling.plugin

# Plugin protocol peer
name = scriptling.plugin.load("widgets", "/opt/widget", scriptling=True)
scriptling.plugin.call_function(name, "build", "chair")

# Raw JSON-RPC peer (e.g. scriptling --json-rpc)
rpc = scriptling.plugin.load("rpc", "scriptling", args=["--json-rpc", "./setup.py"])
scriptling.plugin.call_function(rpc, "search", {"query": "hello"})

# HTTP JSON-RPC peer
remote = scriptling.plugin.load(
    "remote",
    "http://127.0.0.1:8000/json-rpc",
    headers={"Authorization": "Bearer token"},
)
scriptling.plugin.call_function(remote, "search", {"query": "hello"})
```

### `batch_call(library, calls)`

Calls multiple functions on one loaded JSON-RPC peer by sending a JSON-RPC batch over its stdio or HTTP transport. Results are returned in the same order as the input calls.

For `scriptling=True` clients, each item is sent as a typed plugin `function.call` request. For `scriptling=False` clients, each `name` is sent directly as the raw JSON-RPC method. Callback arguments are not supported in `batch_call`. If any item returns a JSON-RPC error, `batch_call` raises an error for the whole batch and includes the failing item index and method name.

**Parameters:**
- `library` (`str`): Library name returned by `load()`, short or normalised form.
- `calls` (`list` of `dict`): Each dict supports:
  - `name` (`str`, required): Function name, or raw JSON-RPC method name for non-plugin peers.
  - `args` (`list` or `tuple`, optional): Positional arguments.
  - `kwargs` (`dict`, optional): Keyword arguments.

**Returns:** `list`: return values in the same order as `calls`.

**Raises:** `Error`: if any call in the batch returns a JSON-RPC error; includes the failing item's index and method name.

```python
import scriptling.plugin

rpc = scriptling.plugin.load("rpc", "scriptling", args=["--json-rpc", "./setup.py"])

results = scriptling.plugin.batch_call(rpc, [
    {"name": "ping"},
    {"name": "add", "args": [20, 22]},
    {"name": "search", "kwargs": {"query": "scriptling"}},
])
```

### `call_method(obj, name, *args, **kwargs)`

Calls a method on a remote plugin object. Plugin-supplied class wrappers use this internally.

**Parameters:**
- `obj`: Remote plugin object returned by a `plugin.*` proxy library.
- `name` (`str`): Method name to call.
- `*args`: Positional arguments to pass.
- `**kwargs`: Keyword arguments to pass.

**Returns:** The return value of the called method.

```python
import plugin.hello
import scriptling.plugin

cfg = plugin.hello.Config({"name": "Ada"})
result = scriptling.plugin.call_method(cfg, "get", "name")
```

### `load(name, path, scriptling=False, args=None, insecure_skip_tls=False, headers=None)`

Registers a JSON-RPC peer under `name`. The peer can be a filesystem executable using stdio JSON-RPC, or an `http://` / `https://` JSON-RPC endpoint. With `scriptling=False` (the default), `call_function` sends the requested function name directly as a raw JSON-RPC method. With `scriptling=True`, the peer must implement the Scriptling plugin handshake and `function.call` dispatch method; handshaken peers also register an importable `plugin.*` proxy library. With `scriptling=False`, the loaded client is helper-only and reachable via `call_function`, `describe`, and `list`.

HTTP(S) transport is request/response only. It supports calls, objects, generated `plugin.*` proxies, and batches, but the server cannot initiate callbacks back to the client. Use stdio plugins when host callbacks or `plugin.Logger(ctx)` are required.

`call_function`, `batch_call`, `call_method`, `describe`, and `unload` all accept either the normalised name (`"plugin.widgets"`) or the short name (`"widgets"`).

Identity is by absolute path for executables and by URL for HTTP endpoints. A second `load()` of the same path or URL with the same name is a no-op (returns the existing client, ignoring `scriptling`/`args`/`insecure_skip_tls`/`headers`). Loading an already-loaded peer under a different name, or loading a new peer under a name already in use, raises an error.

**Parameters:**
- `name` (`str`): Library name to register under. Normalised into the `plugin.*` namespace (e.g. `"widgets"` becomes `"plugin.widgets"`). Must not collide with an existing plugin library name.
- `path` (`str`): Filesystem path to the executable, or `http://` / `https://` JSON-RPC endpoint.
- `scriptling` (`bool`, optional): If `True`, perform the plugin protocol handshake, register an importable `plugin.*` proxy library, and fill `describe()` / `list()` from peer metadata. If `False`, the handshake and proxy registration are skipped; `transport` is still reported as `"json"`. Default: `False`.
- `args` (`list`, optional): Command-line arguments passed to executable peers, e.g. `["--json-rpc", "./setup.py"]`. Ignored for HTTP endpoints. Default: `None`.
- `insecure_skip_tls` (`bool`, optional): Skip HTTPS certificate verification for HTTP endpoints. Intended for local or trusted self-signed servers. Default: `False`.
- `headers` (`dict`, optional): Additional HTTP headers sent with every HTTP(S) JSON-RPC request, including handshake, calls, and batches. Default: `None`.

**Returns:** `str`: the normalised library name (e.g. `"plugin.widgets"`).

**Raises:** `Error`: if `name` collides with an existing plugin under a different path/URL, or the peer's handshake fails.

```python
import scriptling.plugin

name = scriptling.plugin.load("widgets", "/opt/widgets/widget", scriptling=True)
chair = scriptling.plugin.call_function(name, "build", "chair")

# Short name also works:
scriptling.plugin.call_function("widgets", "build", "chair")

# Pass command-line arguments:
rpc = scriptling.plugin.load("rpc", "scriptling",
                             args=["--json-rpc", "./setup.py"])

# Connect to an HTTP JSON-RPC endpoint:
remote = scriptling.plugin.load("remote", "https://127.0.0.1:8443/json-rpc",
                                insecure_skip_tls=True,
                                headers={"Authorization": "Bearer token"})
```

### `unload(name)`

Closes a loaded executable's process (best-effort `plugin.shutdown` plus stdin close) and removes it from the registry. The name is freed for re-use; the same `name` + `path` can be `load()`-ed again afterwards.

**Parameters:**
- `name` (`str`): Library name returned by `load()`, or a discovered plugin name. Short or normalised form accepted.

**Returns:** `None`

```python
import scriptling.plugin

name = scriptling.plugin.load("temp", "/tmp/worker")
scriptling.plugin.unload(name)
```

### `release(obj)`

Explicitly releases a remote plugin object, freeing server-side resources. Objects are released automatically when garbage collected, but this function allows deterministic cleanup.

**Parameters:**
- `obj`: Remote plugin object to release.

**Returns:** `None`

```python
import plugin.hello
import scriptling.plugin

cfg = plugin.hello.Config({"name": "Ada"})
scriptling.plugin.release(cfg)
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.plugin.load()` can register any executable on the filesystem (or any HTTP(S) endpoint) as a callable plugin, then run it as a child process via stdio JSON-RPC. If the `path` argument is influenced by untrusted input rather than controlled by the embedder, this is process-execution-adjacent: equivalent in risk to letting a script choose what to run on the host. Only allow `load()` with paths and URLs the host trusts. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [Plugins](https://scriptling.dev/okf/scriptling-docs/./plugins.md) - Loading and writing executable plugins
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for host-provided libraries
