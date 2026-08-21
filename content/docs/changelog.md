---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## August 2026

{{< version "v0.21.0" >}}

{{< changelog-item "added" >}}
**Script network policies.** Hosts can keep scripts off the private LAN and away from cloud metadata endpoints. Registering `requests`, `wait_for`, or `websocket` with a policy blocks loopback, link-local, private, and IP-literal addresses by default, with allow/deny host lists, CIDRs, https-only, and custom DNS servers for the exceptions you grant. Checks run at connect time, so DNS-rebinding and redirect tricks don't get through. The CLI takes a TOML policy file — `--network-policy=policy.toml`, format in the CLI guide — and `--no-subprocess` leaves the subprocess library out entirely. No policy configured means no restrictions.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**One resolver for all script DNS.** A policy's `dns_servers` — or a resolver injected by the host — now serves every script network path, `scriptling.net.resolve` included, so lookups and connections always see the same answers. Without either, the host's system resolver is used as before.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`sys.stdout` and `sys.stderr`.** Scripts had no way to write to stderr, so warnings and errors shared stdout with the report. Both streams are now available with `write()`, `writelines()`, `flush()`, `isatty()`, and `with` support, and `print(..., file=...)` now accepts any object with a `write` method — `sys.stderr`, `sys.stdout`, or your own class. The streams follow output capture, host writers, and sandbox discarding just like `print()` does, and Go hosts get a matching `SetErrorWriter(io.Writer)`.

```python
import sys

sys.stderr.write("warning: retrying (attempt 2)\n")
print("fatal: disk full", file=sys.stderr)
print('{"status": "ok"}')   # stdout stays report-only
```
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Booleans now display as `True`/`False`, matching Python 3.** `print(True)`, `str()`, `repr()`, and f-strings used to render lowercase; the literals themselves were always `True`/`False`. Machine-facing output is unchanged — `json.dumps`, query parameters, and tool responses still use lowercase. Scripts that compare boolean text (for example `str(flag) == "true"`) need updating, and Go hosts stringifying booleans for the wire should use the new `object.CoerceWireString`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`toon.decode` accepts block lists and rejects malformed input.** Lists written as `- item` lines under a key (`tags:` / `- python`) were silently decoded as an empty object; they now decode as lists. Invalid lines that were silently dropped now raise an error in strict mode (the default).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`create_leader_election` now takes `min_cluster_size`.** A leader can only be elected while at least that many nodes are visible, so a split cluster can no longer elect two leaders. This replaces `quorum_percentage` — set `min_cluster_size` to the majority of your smallest cluster (`2` for three nodes, `1` for single-node) and leave it alone as the cluster grows. Upgrading gossip also brings adaptive quorum sizing and automatic retirement of dead nodes' votes.
{{< /changelog-item >}}

---

{{< version "v0.20.1" >}}

{{< changelog-item "fixed" >}}
**bug fixes**
{{< /changelog-item >}}

---

## July 2026

{{< version "v0.20.0" >}}

{{< changelog-item "fixed" >}}
**`ZeroDivisionError` is now catchable.** Division by zero raised an error that no `except` clause could name, only a bare `except Exception` caught it, even though `ZeroDivisionError` already existed as a builtin. `/`, `//`, and `%` now raise a `ZeroDivisionError` that `except ZeroDivisionError:` matches, for both integer and float operands. Uncaught behaviour is unchanged (same message, file, and line), and `except Exception` still catches it, so existing scripts are unaffected.
```python
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print("caught:", e)
```
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`math.fmod(x, 0)` now raises a catchable `ValueError`.** It had the same problem: an error no `except` clause could name. CPython reports a zero divisor here as `ValueError` ("math domain error") rather than `ZeroDivisionError`, and `math.fmod` now matches. The message is unchanged and `except Exception` still catches it.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Iterating a dict directly now yields its keys, matching Python.** `for k in d`, comprehensions (`[k for k in d]`, `{k for k in d}`), and `*d` unpacking all raised `type error: expected iterable, got DICT`; they now iterate the keys like CPython. `list(d)` and `tuple(d)` already worked. The view methods `d.keys()` / `d.values()` / `d.items()` are unchanged, and `dict_keys` still has no `.sort()` (use `sorted(d.keys())`), also matching CPython.
```python
d = {"b": 2, "a": 1}
for k in d:          # "b", then "a"
    print(k, d[k])
```
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Substantially faster evaluation, with far fewer allocations.** Four changes to the evaluator, all measured against v0.19.0:

- **Integer arithmetic is no longer boxed per operator.** An expression such as `total + i * 2 - 1` allocated an integer object for every operator, even though only the final value is ever observed. Side-effect-free integer arithmetic and comparisons now evaluate without boxing intermediates.
- **Attribute reads no longer allocate.** `obj.attr` is indexing by a string literal internally, so every field read was allocating its own copy of the field name. String literals now reuse one immutable value.
- **Builtin calls no longer allocate a context.** Each call built a throwaway context to carry the environment; it is now derived once per evaluation.
- **`a + b + c` chains no longer allocate scratch slices.** The chain path collected its operands into two slices before discovering whether they were strings, so numeric and list chains paid for a string path they never used. Operands are now folded as they are evaluated.

| Workload                          | Time  | Allocations |
| --------------------------------- | ----- | ----------- |
| Integer `+` chains                | −75%  | −100%       |
| Integer loops                     | −35%  | −50%        |
| String `+` chains                 | −25%  | −50%        |
| Mixed-type `+` chains             | −45%  | −44%        |
| `if`/`while`/`try` control flow   | −28%  | —           |
| List and dict manipulation        | −24%  | −44%        |
| Recursive calls                   | −9%   | —           |
| String building                   | −17%  | −36%        |
| Method calls and attribute access | −21%  | −70%        |
| Comprehensions                    | —     | —           |

Measured on operation-dense workloads (loops doing real work inside a single evaluation), these average roughly a 30% reduction in run time, with per-operation allocations down 40–100% — integer chains and loops, which previously boxed every operator, now allocate almost nothing. The gains are largest for scripts that loop over arithmetic, attribute access, or string/list building. Short one-shot `Eval` calls see smaller gains because the per-call interpreter setup dominates them; parse and compile times are unchanged.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`is` on a repeated string literal.** Because a string literal now yields one shared value, evaluating the same literal twice returns the same object — so `f() is f()`, where `f` returns a string literal longer than 20 characters, is now `true` where it was `false`. This matches CPython, which interns literal constants. Strings of 20 characters or fewer were already compared by value and are unaffected. Use `==` rather than `is` to compare string contents.
{{< /changelog-item >}}

{{< version "v0.19.0" >}}

{{< changelog-item "breaking" >}}
**`scriptling.net.unicast` and `scriptling.net.multicast` `receive()` now return `data` as `bytes`** (was `str`). It matches Python's `socket.recv()` semantics and fixes silent corruption of binary data sent over UDP/TCP. Existing text-only scripts need `msg["data"].decode()` where they previously used `msg["data"]` directly in string operations.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`bytes` type** — a dedicated binary data type mirroring Python's `bytes`: an immutable sequence of byte values (0–255) with the usual operator support (`len()`, indexing, slicing, `+`/`*`, comparison, `in`, iteration, truthiness). Mixing `bytes` with `str` in concatenation or comparison raises a `TypeError` — call `.decode()` to convert. It is a global builtin with the Python-compatible constructor `bytes(source, encoding="utf-8")`, plus `bytes.fromhex()` and `bytes.frombase64()` static constructors. Methods on values: `.decode()`, `.hex()`, `.base64()`, `.length()`.

```python
b = bytes("hi")          # b'hi'
b = bytes([104, 105])    # b'hi'
assert b.decode() == "hi"
assert b.hex() == "6869"
assert b + bytes("!") == bytes("hi!")
```
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`msgpack` library** — MessagePack binary serialisation, the compact counterpart to `json`. Mirrors Python's `msgpack` module: `packb(obj)` returns `bytes`, `unpackb(packed)` accepts `bytes`, with `pack`/`unpack` aliases. `bytes` round-trips as msgpack `bin`; `str` as msgpack `str`. The default codec is `shamaton-msgpack`, also used by `gossip.DefaultConfig()`, so a fresh instance and cluster agree on the wire format without explicit wiring.

```python
import msgpack

payload = msgpack.packb({"user": "alice", "id": 42})
data = msgpack.unpackb(payload)
print(data["user"])  # "alice"
```
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`hashlib.digest()`, `hmac.digest()`, and `base64.b64decode()` now return `bytes`** instead of `str`. The previous behaviour stuffed raw binary through a UTF-8 string, silently corrupting any non-ASCII byte. Call `.decode()` on the result for a string; `hexdigest()`, `compare_digest()`, `b64encode()`, and the `hashlib`/`hmac` constructors are unchanged. `b64encode`, `hashlib`, and `hmac` now also accept `bytes` as input. `pathlib.Path.read_bytes()` and `pathlib.Path.write_bytes()` had the same bug and are fixed in the same way.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Binary interop across file I/O, HTTP, and sockets** — `bytes` is now a first-class participant in every I/O surface, mirroring Python 3's split between `str` and `bytes`:

- **Files** — new `os.read_bytes(path)` returns `bytes`; `os.read_lines(path)` iterates lines lazily for large files; `os.write_file` and `os.append_file` accept `bytes`.
- **HTTP** — responses gain a `.content` field (`bytes`), matching Python's `requests`; the request `data=` accepts `bytes` for binary bodies. `.text` and `.body` remain `str`.
- **Sockets** — `scriptling.net.unicast` and `scriptling.net.multicast` `send()` accepts `bytes`; `receive()` returns `data` as `bytes` (see breaking change above).
- **Packages** — new `scriptling.package.read_bytes(name, path)`.

```python
import os, msgpack

# Pack to bytes, persist, read back, unpack — zero corruption.
os.write_file("/tmp/data.msgpack", msgpack.packb({"k": "v"}))
data = msgpack.unpackb(os.read_bytes("/tmp/data.msgpack"))
```
{{< /changelog-item >}}

{{< version "v0.18.0" >}}

{{< changelog-item "added" >}}
**`scriptling.package` library** — read-only access to files inside loaded packages (app bundles and library bundles). Works identically in directory and zip mode. Every function takes the package name (from `manifest.toml`) as its first argument.

```python
import scriptling.package as package

spec = package.read_file("myapp", "data/spec.md")
files = package.list("myapp", "tools/")
py = package.glob("myapp", "**/*.py")
```

Functions: `read_file`, `file_exists`, `list`, `glob`, `exists`, `version`, `names`. Package name uniqueness is enforced at load time.

**`additional_files` manifest field** — ship extra files or directories in a package zip. A trailing `/` includes the entire directory tree; a bare path includes a single file.

```toml
additional_files = ["data/", "LICENSE"]
```
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Decorator-based HTTP and JSON-RPC handler registration** — attach routes directly to handler functions with `@http.get("/path")`, `@http.post(...)`, `@http.route(...)`, `@http.websocket(...)`, `@http.middleware`, `@http.not_found`, and `@jsonrpc.method("name")`, `@jsonrpc.notification("name")`, plus `@plugin.register_function` and `@plugin.register_class` for plugin servers. No separate setup-script registration block needed; the route lives right above the function.

```python
import scriptling.runtime.http as http

@http.get("/health")
def health(request):
    return http.json(200, {"status": "ok"})

@http.post("/api/users")
def create_user(request):
    return http.json(201, {"name": request.json()["name"]})
```

The module name is auto-resolved from `__name__` (falling back to `__file__` for the setup script). The imperative API (`runtime.http.get("/path", "lib.func")`) continues to work; both forms coexist.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**App bundles** — ship MCP tools, HTTP routes, JSON-RPC methods and static assets in a single package (folder or zip). A `manifest.toml` with a `serve` field declares the app's protocols; the CLI provides only the transport. Dev folders and production zips run the same code path.

```toml
name    = "myapp"
version = "1.0.0"
main    = "setup.py"
libs    = ["lib", "vendor"]
serve   = ["http", "mcp"]
```

```bash
scriptling --server :8000 --package ./myapp       # dev (folder)
scriptling --server :8000 --package myapp.zip     # prod (zip)
```

See `examples/app-bundle/` for a complete working example.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Decorator-based MCP tool registration** — define tools with `@mcp.tool()` in a single `.py` file, no `.toml` sidecar needed. Parameters, types and descriptions live alongside the implementation. Multiple tools per file are supported.

```python
import scriptling.runtime.mcp as mcp

@mcp.tool("Calculate an expression", params={"expr": "Math expression"})
def calc(expr):
    return f"{expr} = {eval(expr)}"
```

The legacy `.toml` + `.py` format continues to work; both formats can coexist in the same `tools/` folder.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`pack build` is manifest-driven** — inclusion follows the manifest (libs dirs, main script, convention dirs). Unknown top-level entries produce warnings; missing declared entries are build errors.

**Tool scripts no longer get implicit sibling imports** — pass `-L ./tools` if sibling imports are needed.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**HTTP ServeMux conflict** between `/mcp` and `GET /` routes resolved by registering MCP/JSON-RPC endpoints with explicit methods.

**Data race on `reloadMCP`** — signal-triggered reload and file-watcher debounce reload are now serialized with a mutex, preventing concurrent mutation of MCP registration maps and entry-tracking slices.

**Setup script panic recovery** — the setup script goroutine now recovers panics, converting them to a clean startup error instead of blocking `NewServer` forever or crashing the process.

**HTTP handler request cancellation** — `runHandler` now passes `r.Context()` to the script evaluator so client disconnects cancel in-flight handler scripts.

**MCP handler socket consistency** — MCP tool/resource/prompt handlers now respect `--docker-host` / `--podman-host` overrides (previously hardcoded to default socket paths).

**Wasted KV store allocation** — `ResetRuntime` no longer opens a throwaway in-memory KV store that `InitKVStore` immediately replaces.

**`pack build` zip close error** — file close failures during `pack build` are now propagated instead of silently swallowed.
{{< /changelog-item >}}

{{< version "v0.17.8" >}}

{{< changelog-item "added" >}}
**`os.symlink` and `os.path.islink`: create and detect symbolic links.**

`os.symlink(src, dst)` creates a symbolic link at `dst` pointing to `src`. `os.path.islink(path)` returns `True` if the path is a symbolic link (using `Lstat` so the link itself is checked, not the target). Both respect the allowed-paths security configuration.

```python
import os
import os.path

os.symlink("../target.js", "node_modules/.bin/tool")
os.path.islink("node_modules/.bin/tool")  # True
```

**`find.entries`: new `include_symlinks` option and `link_target` field.**

When `include_symlinks=True` is passed to `find.entries`, symlink entries are yielded as-is (not followed) with their target in the `link_target` field. Use this to mirror symlink trees without resolving them.

```python
import scriptling.find as find

for e in find.entries("/site", include_symlinks=True):
    if e["link_target"]:
        print(e["path"], "->", e["link_target"])
```

**`find.entries`: new `include_hash` option and `hash` field.**

When `include_hash=True` is passed to `find.entries`, each file entry's content is crc64-hashed and the result is returned in the `hash` field. Use this for definitive change detection — two files with the same hash have identical bytes.

```python
import scriptling.find as find

for e in find.entries("/site", include_hash=True, type="file"):
    print(e["path"], e["hash"])
```

{{< /changelog-item >}}

---

{{< version "v0.17.7" >}}

{{< changelog-item "added" >}}
**`scriptling.find.entries`: matching files and directories with size, mtime, and type.**

`find.path` returns matching paths as a list of strings — convenient for most uses, but callers that need to compare trees (differential sync, change detection, build artefact caching) previously had to stat every match themselves. The new `find.entries` function applies the same filters as `find.path` and returns a `list[dict]` with `path`, `size`, `mtime`, and `is_dir` per entry, stat'ing each match inside the existing worker pool so the metadata arrives in a single pass.

```python
import scriptling.find as find

# Build a {path: mtime} index for differential sync
mtimes = {e["path"]: e["mtime"]
          for e in find.entries("/site", type="file")}

# Walk the matches with their size readily available
for e in find.entries("/logs", name="*.log", size_min=10 * 1024 * 1024):
    print(e["path"], e["size"])
```

`find.path` is unchanged; use it when only the strings are needed, since it skips the per-entry `stat` in the no-filter common case. The Go API gains a matching `extlibs.FindEntries` returning `[]extlibs.FindEntry`.
{{< /changelog-item >}}

---

{{< version "v0.17.6" >}}

{{< changelog-item "fixed" >}}
**`sorted()`, `sum()`, `min()`, `max()`, and `str.join()` now accept any iterable.**

These builtins previously accepted only lists and tuples (`sum`/`min`/`max` additionally took flat numeric arrays); anything else raised `type error: expected LIST or TUPLE`. They now iterate any iterable — dict views (`dict_keys`/`dict_values`/`dict_items`), sets, strings, dicts, and iterators — matching Python's semantics. `str.join` likewise accepts any iterable of strings, not just lists and tuples.

```python
d = {"a": 3, "c": 1, "b": 2}

sorted(d.items(), key=lambda x: x[1])   # [(c, 1), (b, 2), (a, 3)]
sum(d.values())                         # 6
min(d.keys())                           # "a"
max(set([5, 2, 8]))                     # 8
sorted("cab")                           # [a, b, c]
"-".join(("x", "y", "z"))               # "x-y-z"
```

The numeric `FloatArray` fast paths are preserved, and `sorted()` does not mutate its input.

**Set algebra operators `&`, `|`, `-`, `^` on sets.**

Sets already supported set algebra via methods (`.intersection()`, `.union()`, `.difference()`, `.symmetric_difference()`); they now support the operator syntax too, matching Python. Both operands must be sets — use the methods for arbitrary iterables.

```python
a = set([1, 2, 3])
b = set([2, 3, 4])

a & b   # {2, 3}   intersection
a | b   # {1, 2, 3, 4}   union
a - b   # {1}   difference
a ^ b   # {1, 4}   symmetric difference
```

Integer bitwise operations are unchanged — the new behaviour only applies when the left operand is a set. The augmented-assignment forms (`&=`, `|=`, `-=`, `^=`) work on sets too, rebinding the name to the resulting set.

**Set value equality (`==` / `!=`) now compares contents.**

Two sets with the same elements previously compared equal only if they were the same object; distinct sets always reported as unequal. `==` and `!=` now compare contents order-independently, so `set([1, 2, 3]) == set([3, 2, 1])` is `true`. Cross-type equality (`set == list`) returns `false` rather than erroring.

**Empty tuples, sets, and dict views are now falsy.**

Truthiness checks (`if`, `and`, `or`, `bool()`) previously treated any value without an explicit rule as truthy, so empty `()`, `set()`, `dict_keys()`, `dict_values()`, and `dict_items()` were all truthy — unlike Python, where empty containers are falsy. They now follow Python's rule (empty → falsy, non-empty → truthy), so `set() and f()` short-circuits and `if my_set:` works as expected. Lists, dicts, strings, and numbers were already correct.
{{< /changelog-item >}}

---

{{< version "v0.17.5" >}}

{{< changelog-item "added" >}}
**`scriptling.template.html` / `scriptling.template.text`: custom action delimiters.**

`Set()` now accepts optional `left` and `right` keyword arguments to override Go's default `{{` `}}` template markers. This lets you render templates that contain literal `{{ }}` — for client-side frameworks (Vue, Handlebars), CSS, JSON, or upstream config files that already use those characters.

```python
import scriptling.template.text as text

# Use {% %} so {{ }} survives into the output untouched
tmpl = text.Set(left="{%", right="%}")
tmpl.add("Hello, {%.Name%}! Upstream var: {{ service.tag }}")
print(tmpl.render({"Name": "Alice"}))
# Output: Hello, Alice! Upstream var: {{ service.tag }}
```

Both arguments default to the standard delimiters (`{{` and `}}`); pass an empty string to fall back to the default for that side.

**`scriptling.mcp.Client`: environment variables for stdio servers.**

`mcp.Client()` now accepts an `env` keyword argument (stdio servers only) — a list of `KEY=value` strings applied to the launched subprocess. Variables are merged on top of the inherited environment, so `PATH`, `HOME`, and other defaults remain available. Passing `env` with an HTTP URL raises an error.

```python
import scriptling.mcp as mcp

client = mcp.Client("npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/data"],
    env=["FS_ROOT=/data", "LOG_LEVEL=debug"],
    namespace="fs",
)
```
{{< /changelog-item >}}

---

{{< version "v0.17.4" >}}

{{< changelog-item "fixed" >}}
**`sorted()` and `list.sort()` now order tuples and lists lexicographically.**

Previously, sorting a list of tuples or lists was a silent no-op (`list.sort()`) or raised `unsupported type for sorting: TUPLE` (`sorted()`), because the comparator only handled numbers and strings. Tuples and lists now compare element-by-element (Python-style), so nested structures sort correctly too.

```python
sorted([(3, "c"), (1, "a"), (2, "b")])  # [(1, "a"), (2, "b"), (3, "c")]

rows = [(1, 9), (1, 3), (1, 7)]
rows.sort()                              # in-place: [(1, 3), (1, 7), (1, 9)]
```
{{< /changelog-item >}}

---

{{< version "v0.17.2" >}}

{{< changelog-item "added" >}}
**`scriptling.nomad`: dynamic host volume support.**

The nomad library now covers Nomad's dynamic host volumes (introduced in Nomad 1.8+):

- `host_volumes_list` — list dynamic host volumes, with optional filters for
  namespace, node_id, node_pool, and plugin_id.
- `host_volume_get` — fetch full details for a single host volume.
- `host_volume_register` — register a pre-existing host volume (e.g. a
  pre-mounted CephFS path) with Nomad.
- `host_volume_create` — provision storage via a host volume plugin and
  register it with Nomad.
- `host_volume_delete` — destroy backing storage via the plugin and deregister
  from Nomad.

```python
import scriptling.nomad as nomad

c = nomad.Client("https://nomad.example.com:4646", token="secret")

# List all host volumes
for v in c.host_volumes_list():
    print(v["name"], v["node_id"], v["state"])

# Create a new host volume via plugin
c.host_volume_create("vol-new-01", {
    "Name": "app-data",
    "PluginID": "mkdir",
    "NodePool": "production",
    "RequestedCapacityMinBytes": 50 * 1024 * 1024 * 1024,
    "RequestedCapabilities": [{"AccessMode": "single-node-writer", "AttachmentMode": "file-system"}],
})
```

The nomad library now covers the complete CSI volume lifecycle:

- `csi_volume_create` — provisions new backing storage via the CSI controller
  plugin (e.g. creates a Ceph RBD image) and registers it in Nomad.
- `csi_volume_delete` — destroys backing storage via the CSI controller plugin
  and deregisters the volume from Nomad.

These complement the existing `csi_volume_register` (register pre-existing
storage) and `csi_volume_deregister` (un-track without destroying data).

```python
# Create a new volume with backing storage
c.csi_volume_create("qaprod-data-01", {
    "Name": "qaprod-data-01",
    "PluginID": "ceph-csi",
    "RequestedCapacityMin": 10 * 1024 * 1024 * 1024,
    "RequestedCapabilities": [{"AccessMode": "single-node-writer", "AttachmentMode": "file-system"}],
}, namespace="fortixqa")

# Delete volume and its Ceph backing store
c.csi_volume_delete("qaprod-orphaned-01", namespace="fortixqa")
```

See [scriptling.nomad](/reference/libraries/scriptling/utilities/nomad/) for
the full method reference.
{{< /changelog-item >}}

---

{{< version "v0.17.0" >}}

{{< changelog-item "added" >}}
**New `scriptling.nomad` library: manage HashiCorp Nomad CSI volumes and jobs.**

A `NomadClient` obtained from `nomad.Client(addr, token=...)` talks directly to
the Nomad HTTP API, covering CSI storage volumes and jobs. Requests default to
a 10 second timeout, adjustable via `timeout=` on `Client()`:

- CSI volumes: `csi_volumes_list`, `csi_volume_get`, `csi_volume_register`,
  `csi_volume_deregister`.
- Jobs: `jobs_list`, `job_get`, `job_register`, `job_stop`,
  `wait_job_stopped`, `job_validate`, `job_plan`, `jobs_parse` (HCL to JSON).

This is aimed at cluster housekeeping tasks, such as reconciling CSI volumes
against a source of truth and removing orphaned ones after confirmation.

```python
import scriptling.nomad as nomad

c = nomad.Client("https://nomad.example.com:4646", token="secret")

expected = set(open("expected_volumes.txt").read().split())
for v in c.csi_volumes_list(namespace="*"):
    if v["id"].startswith("qaprod") and v["id"] not in expected:
        c.csi_volume_deregister(v["id"], force=True)
```

See [scriptling.nomad](/reference/libraries/scriptling/utilities/nomad/) for
the full method reference.

**`scriptling.container`: `wait_stopped()` confirms a container has fully stopped.**

`ContainerClient.stop()` already blocks until the container reports stopped
for Docker, Podman, and Apple Containers, but there was no way to
independently re-check that state afterwards. `wait_stopped(name_or_id,
timeout=30)` polls the container's running state until it stops or the
timeout elapses, and treats a container that no longer exists as already
stopped.

```python
c.stop("web")
if not c.wait_stopped("web", timeout=15):
    print("container did not stop in time")
```

**New `scriptling.find` library: locate files and directories by name, type, mtime, and size.**

A new utility library inspired by the Unix `find` command, filling the gap
between `glob` (name matching only) and a hand-rolled `os.walk` loop:

```python
import scriptling.find as find
import time

# Markdown files modified in the last 24 hours
recent = find.path("/docs", name="*.md", type="file",
                   mtime_min=time.time() - 86400)

# Large log files
big = find.path("/var/log", name="*.log", type="file", size_min=104857600)
```

`find.path(path, *, recursive=True, type="any", name="", mtime_min=None,
mtime_max=None, size_min=None, size_max=None, include_hidden=False,
follow_links=False, max_depth=None)` returns matching paths as a list of
strings. Recursive searches stat and filter entries concurrently using a
bounded worker pool, the same model as `scriptling.grep`. See
[scriptling.find](/reference/libraries/scriptling/utilities/find/) for the full
reference.

**New `shlex`, `tempfile`, and `shutil` standard libraries.**

Three new standard libraries fill gaps in filesystem and command-line tooling:

| Library | Key functions | Description |
|---------|--------------|-------------|
| `shlex` | `quote`, `split`, `join` | Shell-style quoting and splitting — safe command-line construction for `subprocess` |
| `tempfile` | `mkstemp`, `mkdtemp`, `gettempdir` | Temporary file and directory creation with restrictive permissions |
| `shutil` | `copy`, `copytree`, `rmtree`, `move`, `disk_usage` | High-level file operations including recursive delete and disk usage |

All three enforce `allowedPaths` restrictions when registered with explicit
paths (except `shlex`, which is pure string processing with no filesystem
access). `tempfile` creates files with mode `0600` and directories with `0700`,
and falls back to the first allowed path when the system temp directory is
outside the sandbox.

```python
import shlex, subprocess
import tempfile, shutil

# Safe command construction
subprocess.run(shlex.split("echo " + shlex.quote(user_input)))

# Atomic write via temp file
tmp = tempfile.mkstemp(suffix=".tmp")
try:
    # ... write to tmp ...
    shutil.move(tmp, "output.final")
except:
    shutil.rmtree(tmp)
```

See [shlex](/reference/libraries/text-processing/shlex/),
[tempfile](/reference/libraries/filesystem/tempfile/), and
[shutil](/reference/libraries/filesystem/shutil/) for the full references.

**New `zipfile` and `tarfile` libraries: read and write compressed archives.**

Two new standard libraries bring archive handling to Scriptling, matching
Python's `zipfile` and `tarfile` modules:

- **`zipfile`** — `ZipFile(path, mode)` with `namelist()`, `read()`, `extract()`,
  `extractall()`, `write()`, `writestr()`, `is_zipfile()`.
- **`tarfile`** — `TarFile(path, mode)` with the same method set plus gzip
  support (`"r:gz"`, `"w:gz"` modes), `add()`, `addstr()`, `is_tarfile()`.

Both enforce `allowedPaths` and block zip/tar-slip (path traversal via crafted
entry names). See
[zipfile](/reference/libraries/filesystem/zipfile/) and
[tarfile](/reference/libraries/filesystem/tarfile/) for the full references.

```python
import tarfile

# Extract a .tar.gz
tf = tarfile.TarFile("release.tar.gz", "r:gz")
tf.extractall("/opt/app")
tf.close()

# Create a zip from files + inline data
import zipfile
zf = zipfile.ZipFile("config.zip", "w")
zf.writestr("version.txt", "1.0.0")
zf.write("/etc/app.conf")
zf.close()
```

**`scriptling.similarity`: vector operations — `cosine_similarity`, `most_similar`, `vectorize`.**

The similarity library gains three vector functions for text-matching workflows:

- **`cosine_similarity(a, b)`** — compare two numeric vectors (-1.0 to 1.0).
  Now exposed in `similarity` (its natural home) in addition to `scriptling.ai`.
  The implementation is shared — no code duplication.
- **`most_similar(query, vectors, top_k=5)`** — rank a list of vectors by
  similarity to a query; returns `[{"index": int, "score": float}, …]`.
- **`vectorize(text, dims=256)`** — generate a vector from text using the
  feature-hashing trick. CPU-only, deterministic, no model or API call required.
  Texts sharing words produce similar vectors.

```python
import scriptling.similarity as sim

# CPU-only text matching — no embedding API needed
v1 = sim.vectorize("the quick brown fox")
v2 = sim.vectorize("the quick red fox")
print(sim.cosine_similarity(v1, v2))  # high — shares 3 of 4 words

# Rank documents against a query
docs = [sim.vectorize(d) for d in ["hello world", "quick fox", "goodbye"]]
for r in sim.most_similar(sim.vectorize("hi world"), docs, top_k=2):
    print(r["index"], r["score"])
```

**New `scriptling.csv` library: CSV parsing and formatting (string-based).**

A string-based CSV library backed by Go's `encoding/csv` (RFC 4180 compliant).
Unlike Python's `csv` module (which requires file objects), this operates on
strings — available in all environments including MCP (no filesystem access
needed).

- **`loads(content, delimiter=",")`** — CSV text → list of lists.
- **`loads_dict(content, delimiter=",")`** — CSV text → list of dicts (first row = headers).
- **`dumps(rows, delimiter=",")`** — list of lists → CSV text (auto-quotes values with commas).
- **`dumps_dict(rows, delimiter=",", columns=None)`** — list of dicts → CSV text with header row.

```python
import scriptling.csv as csv
import os

# Read and parse
people = csv.loads_dict(os.read_file("users.csv"))
for p in people:
    print(p["name"], p["email"])

# Write
os.write_file("output.csv", csv.dumps_dict(people, columns=["name", "email"]))
```

See [scriptling.csv](/reference/libraries/scriptling/utilities/csv/) for the full reference.

**New `scriptling.xml` library: XML parsing and formatting (dict-based).**

A simple dict-based XML library (similar to Python's `xmltodict`), using the
`loads`/`dumps` convention consistent with `json`, `yaml`, `toml`, and `csv`.
No filesystem access required — available in all environments including MCP.

- **`loads(content)`** — XML string → nested dict. Element tags become dict
  keys, attributes become `@`-prefixed keys, repeated elements become lists,
  text alongside attributes/children uses `#text`.
- **`dumps(data, indent="")`** — dict → XML string. Supports attributes,
  repeated elements (list values), and optional indentation.

```python
import scriptling.xml as xml

data = xml.loads('<user id="123"><name>Alice</name></user>')
# {"user": {"@id": "123", "name": "Alice"}}

text = xml.dumps({"users": {"user": ["Alice", "Bob"]}}, indent="  ")
# <users>
#   <user>Alice</user>
#   <user>Bob</user>
# </users>
```

See [scriptling.xml](/reference/libraries/scriptling/utilities/xml/) for the full reference.

{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`glob`: `recursive` and `include_hidden` keyword arguments, with bounded parallel recursive search.**

`glob.glob()` and `glob.iglob()` gain two keyword-only parameters, both
defaulting to `False`:

- `recursive=True` makes `**` match files and directories recursively,
  descending into every subdirectory. When `False` (the default), `**` is
  treated as `*`, matching Python's `glob` module.
- `include_hidden=True` matches entries whose name starts with `.`; when
  `False` (the default) dot-files and dot-directories are skipped.

Recursive searches now run as a **bounded parallel directory walk**, using the
same worker-pool model as `scriptling.grep`, so large trees are scanned
concurrently rather than sequentially.

```python
import glob

# Recursively find all Python files (descends into subdirectories)
py_files = glob.glob("**/*.py", recursive=True)

# Include dot-directories such as .github
all_py = glob.glob("**/*.py", recursive=True, include_hidden=True)
```

`glob.iglob()` accepts the same keyword arguments; the recursive path uses the
same parallel walk internally.

Note that with the new default (`include_hidden=False`), dot-files are now
**skipped** by wildcard patterns, matching Python's behaviour. Previously Go's
glob included them; pass `include_hidden=True` to restore the old behaviour.

{{< /changelog-item >}}
