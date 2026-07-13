---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
---

## July 2026

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

## June 2026

{{< version "v0.16.0" >}}

{{< changelog-item "added" >}}
**MCP server now exposes Resources and Prompts, and pushes listChanged notifications.**

Scriptling's MCP server implements the remaining two MCP primitives alongside
tools, all defined as files in folders — no Go code, no startup registration:

- **Tools** (`--mcp-tools`): `name.toml` + `name.py`, as before.
- **Resources** (`--mcp-resources`): just files — the path is the URI (the first
  directory is the scheme, the rest mirrors the URI). A `{var}` segment with a
  `.py` is a **template** (the script runs with the extracted variable); every
  other file is served verbatim (a `.py` with no `{var}` is served as source
  text). A template or static resource may have an optional `_stem.toml`
  metadata file providing a human-readable name, description, and MIME type
  (`_` prefix files are never served).
- **Prompts** (`--mcp-prompts`): `name.md` for a static prompt, or
  `name.toml` + `name.py` for an arg-driven prompt (args declared in the toml,
  the script returns messages).

A built-in `scriptling://script/{name}` resource template (tool source code)
and a `write_script` prompt are always available. The `scriptling.mcp.Client` class
gained `list_resources`, `list_resource_templates`, `read_resource`,
`list_prompts`, and `get_prompt` for reading them on remote servers.

```bash
# A templated resource from a file: resources/greeting/{name}.py -> greeting://{name}
scriptling --mcp-resources ./resources
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"greeting://Ada"}}'
```

**`scriptling.mcp.Client` can read resources and prompts from MCP servers.**

The MCP client class gained five methods for the resource and prompt primitives:

| Method | Description |
| --- | --- |
| `client.list_resources()` | List static resources (`uri`, `name`, `description`, `mimeType`) |
| `client.list_resource_templates()` | List resource templates (`uriTemplate`, …) |
| `client.read_resource(uri)` | Read a resource (static or expanded from a template) |
| `client.list_prompts()` | List prompts (`name`, `description`, `arguments`) |
| `client.get_prompt(name, arguments)` | Render a prompt into messages |

```python
import scriptling.mcp as mcp

c = mcp.Client("https://example.com/mcp")
data = c.read_resource("config://app")      # -> {uri, mimeType, text|blob}
out = c.get_prompt("write_script", {"task": "greet a user"})
for msg in out.messages:
    print(msg.role, msg.content)
```

**MCP over stdio: Scriptling can run as a stdio MCP server, and consume stdio MCP servers.**

Scriptling can now serve the Model Context Protocol over stdin/stdout
(newline-delimited JSON-RPC 2.0) — the transport MCP hosts use to launch a
server as a subprocess — in addition to HTTP. The MCP tool flags enable the
server; leaving off `--server` serves it over stdio:

```bash
scriptling --mcp-tools ./tools      # serve your tools over stdio
scriptling --mcp-exec-script        # serve the code-execution tool
```

This mirrors `--json-rpc`: stdio by default, HTTP with `--server`. As with
`--json-rpc`, logs are redirected to stderr so stdout stays a clean protocol
stream. With `--server`, the same tools continue to be served over HTTP at
`/mcp`.

**`scriptling.mcp.Client()` now chooses HTTP or stdio from its argument.**

The client transport is selected from the first argument: an `http://` or
`https://` URL connects over HTTP; anything else is launched as a local stdio
MCP server subprocess. A new `args` keyword supplies the server's command-line
arguments, and a new `client.close()` method shuts a stdio subprocess down.

```python
import scriptling.mcp as mcp

# HTTP server
remote = mcp.Client("https://example.com/mcp", namespace="t2", bearer_token="secret")

# stdio server (a local executable)
local = mcp.Client("/usr/local/bin/thebinary", args=["--server"], namespace="t1")
print(local.call_tool("t1__greet", {"name": "Ada"}))
local.close()
```

`bearer_token` is HTTP-only and `args` is stdio-only; using either with the
wrong transport raises an error. This is backward compatible: existing
`mcp.Client("https://…", namespace=…, bearer_token=…)` calls are unchanged.

The JSON-RPC framing for both the stdio server and client is provided by the
reusable [`github.com/paularlott/jsonrpc`](https://github.com/paularlott/jsonrpc)
package via the [`github.com/paularlott/mcp`](https://github.com/paularlott/mcp)
library.
{{< /changelog-item >}}

---

{{< version "v0.15.1" >}}

{{< changelog-item "fixed" >}}
**`re`: `re.sub()` with `count=0` now replaces all matches (Python semantics).**

Previously, `re.sub(pattern, repl, string, count=0)` returned the string unchanged (zero replacements), diverging from Python where `count=0` means "replace all". It now matches Python: `count=0` (the default) replaces all occurrences, and a positive `count` limits the number of replacements. This also makes `sub` consistent with `re.split`, which already treated `maxsplit=0` as "no limit".

**`scriptling.runtime.kv`: `incr()` is now atomic.**

`kv.incr()` performed a non-atomic read-then-write, so concurrent increments on the same key could lose updates. It now performs an atomic read-modify-write against the underlying store, so parallel increments are safe and no updates are lost.
{{< /changelog-item >}}

---

{{< version "v0.15.0" >}}

{{< changelog-item "added" >}}
**`runtime.plugin`: expose a Scriptling script as a first-class plugin peer (agent variant only).**

A Scriptling setup script can now implement the full Scriptling plugin protocol
so that host processes can load it with `scriptling=True` and receive
auto-generated `plugin.<name>` proxy libraries: no compiled binary required.

```python
# setup.py
import scriptling.runtime.plugin as plugin_srv
import scriptling.runtime as runtime

plugin_srv.serve("calculator", "1.0", "Basic arithmetic")
plugin_srv.register_function("add", "handlers.add")
plugin_srv.register_function("multiply", "handlers.multiply")

runtime.start_server()
```

```python
# handlers.py : called on a fresh evaluator per request
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

When a client loads this peer with `scriptling=True`, the host performs the
`scriptling.handshake`, receives the schema, and builds a `plugin.calculator`
proxy library with generated wrappers for `add` and `multiply`. Function
handlers receive individual positional arguments decoded from the plugin
transport (not a raw params blob).

`runtime.plugin` is registered only in the **agent variant** of Scriptling: it
is intentionally absent from the general CLI runtime. See the
[Plugin Server Mode](../cli/plugin-server/) docs.

**`runtime.start_server(wait=True)` and `runtime.server_running()`: keep the setup script alive while the server runs.**

Previously, a setup script registered its routes and then exited; the server started automatically in the background. This made it impossible for the setup script to remain alive alongside the running server (to maintain gossip state, share objects, or run a polling loop that feeds HTTP handlers).

Now the setup script can call `runtime.start_server()` to signal that all routes are registered: the server builds its mux and starts listening: and then continue running for the lifetime of the server:

```python
import scriptling.runtime as runtime
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="0.0.0.0:8001")
cluster.start()

# Register HTTP routes
runtime.http.get("/status", "handle_status")

# Signal the server to start, then stay alive while it runs
runtime.start_server(wait=False)
while runtime.server_running():
    yield_now()
```

Use `wait=True` (the default) to block inside `start_server()` until the server shuts down: equivalent to Flask's `app.run()`. Use `wait=False` with a `server_running()` loop to keep the script running while also doing other work.

**Backward compatibility:** scripts that exit without calling `start_server()` continue to work unchanged: the server starts automatically after the setup script finishes.

The same pattern works for HTTP, JSON-RPC, and MCP servers.

**Interpreter lock (GIL): one environment is now safe to use from many goroutines.**

Each Scriptling environment now has an interpreter lock, acquired automatically
whenever script runs. Any number of goroutines may call into the same
environment: shared-state threads, background handlers, server requests: and
the lock guarantees only one runs script at a time, so shared state can no longer
be corrupted by concurrent access (no locks needed in your handlers). Independent
environments keep independent locks and still run fully in **parallel**, so the
per-request isolation used by the servers keeps its throughput.

Blocking calls release the lock while they wait, so other threads keep making
progress: sleeps, `input()`, file I/O, sockets, WebSocket, subprocess, HTTP, AI
completions/streaming, container calls, plugin calls, provisioning, `wait_for`,
`grep`/`sed`, messaging sends, `runtime.sync` primitives, `Promise.wait()`, and
`gossip send_request()`. For tight CPU-bound loops that never block, the new
global `yield_now()` builtin releases the lock briefly so other threads can run.

**`runtime.background(..., shared=True)`: shared-environment threads.**

`background()` gains a keyword-only `shared` flag. With `shared=True` the handler
runs on a goroutine in the **caller's own environment**, sharing its live
variables; the interpreter lock makes concurrent access safe without locks.
Arguments are passed live (no transferable restriction or copying). The default
(`shared=False`) is unchanged: an isolated, parallel copy. Also fixed docs that
referenced a non-existent `runtime.spawn`: the function is `runtime.background`.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`scriptling.console` handlers run one at a time, to completion:**

`on_submit`, `on_escape`, and `register_command` handlers run sequentially: each
finishes before the next starts. This is for ordering, not safety (the
interpreter lock already makes them memory-safe): a chat conversation is only
coherent if a submit handler completes before the next begins, and serializing
keeps input responsive while a handler runs. A long-running handler delays the
next one; submitting new input or pressing Esc still cancels the in-flight
handler so cooperative handlers can stop early.

**Faster interpreter hot path:**

A set of interpreter optimizations cut per-call and per-statement overhead:

- A call-site **callee cache** resolves functions defined in an enclosing scope
  (recursion, shared helpers) without re-walking the environment chain.
- **Call-frame environments** are recycled through a per-tree free-list instead
  of a global pool.
- **Return values** are now recycled through the same per-tree free-list,
  removing the per-`return` overhead of a global pool while keeping allocations
  flat.
- The **source-file lookup** used for error reporting is no longer performed on
  every block and statement: it is deferred to the error path, removing a
  context lookup from every loop body and function call. The call-depth lookup
  is likewise resolved in a single step per call.
- Hot type checks (`IsError`, exception detection) use direct type assertions
  instead of interface method calls.
- **Integer dictionary keys** (loop indices, ids) allocate far less: small
  keys are now cached and reused, and larger keys take a single allocation
  instead of two. Dict-heavy code does roughly **40% fewer allocations**.
- **Object instances store their fields inline** instead of always allocating a
  map. Most instances have only a handful of fields, so this avoids a heap map
  (and its buckets) per object entirely; fields beyond a small inline capacity
  spill to a map as before. Class-heavy code runs about **13% faster** and uses
  roughly **23% less memory**.

Recursion-heavy workloads (e.g. recursive `fib`) run roughly **16% faster**,
dict-heavy code about **15% faster**, class-heavy code about **13% faster**, and
loop- and call-heavy code is broadly faster too: with fewer allocations across
the board.

**Breaking change (Go embedders / plugin authors only): instance fields are now
accessed through methods, not a map.**

`object.Instance` no longer exposes a public `Fields map[string]Object`. Go code
that read or wrote instance fields directly must switch to the accessor methods:

```go
// Before
v := inst.Fields["name"]
inst.Fields["name"] = object.NewString("x")
delete(inst.Fields, "name")

// After
v, ok := inst.GetField("name")        // or inst.Field("name") for a bare value
inst.SetField("name", object.NewString("x"))
inst.DeleteField("name")
```

Also available: `HasField`, `FieldCount`, `RangeFields`, and `FieldsSnapshot`,
plus the constructors `object.NewInstance(class)`,
`object.NewInstanceWithFields(class, fields)` and
`object.NewInstanceWithData(class, fields, nativeData)`. This decouples the
public API from the storage layout, which is what enabled the inline-field
optimization above. **Scripts are unaffected**: this only touches Go code that
manipulates instances directly.
{{< /changelog-item >}}

---

{{< version "v0.14.1" >}}

{{< changelog-item "added" >}}
**Embeddable server: inject host libraries via `ServerConfig.ExtraLibs`**

The server runtime (`scriptling-cli/server`) now accepts an optional
`ExtraLibs func(*scriptling.Scriptling)` on `ServerConfig`. When set, it runs on
every evaluator the server builds: the setup script and every JSON-RPC, HTTP,
MCP, and WebSocket request handler: after the standard library set. Host
applications embedding the server can use it to expose their own libraries to
served scripts:

```go
cfg := server.ServerConfig{
    ScriptFile: "setup.py",
    ExtraLibs: func(p *scriptling.Scriptling) {
        myapp.RegisterLibraries(p)
    },
}
server.RunJSONRPCServer(ctx, cfg)
```

{{< /changelog-item >}}

{{< version "v0.14.0" >}}

{{< changelog-item "changed" >}}
**Breaking change: `hashlib` now returns hash objects:**

`hashlib.md5()`, `hashlib.sha1()` and `hashlib.sha256()` previously returned a
hexadecimal string directly. They now return **hash objects**, matching Python.
Call `.hexdigest()` (or `.digest()`) on the result:

```python
# Before (v0.12)
h = hashlib.sha256("hello")        # a hex string

# After (v0.14)
h = hashlib.sha256("hello").hexdigest()
```

The hash objects also support `.update(data)`, `.copy()`, and the `.name`,
`.digest_size` and `.block_size` attributes. Constructors accept an optional
initial `data` argument (a string used as a byte buffer, or a list of byte
values such as returned by `str.encode()`).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**New `hmac` standard library** (alongside `hashlib`):

- `hmac.new(key, msg=None, digestmod=None)` returns an HMAC object with
  `.update()`, `.digest()`, `.hexdigest()`, `.copy()` and `.name` /
  `.digest_size` / `.block_size` attributes.
- `digestmod` accepts a string name (`"sha256"` default, `"sha1"`, `"md5"`),
  the omitted value, or a `hashlib` constructor reference (`hashlib.sha256`).
- `hmac.digest(key, msg, digestmod)` is a one-shot helper.
- `hmac.compare_digest(a, b)` performs a constant-time string comparison.

This makes webhook signature verification (GitHub, Stripe, Slack, etc.) a
one-liner:

```python
import hmac, hashlib

def verify(body, signature, secret):
    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

`secrets.compare_digest` now delegates to the shared `hmac.compare_digest`
implementation. Note that scriptling has no `bytes` type: strings are used as
byte buffers and parameter type annotations are not supported, so write
`def verify(body, signature, secret):`.
{{< /changelog-item >}}

---

{{< version "v0.12.3" >}}

{{< changelog-item "added" >}}
**Plugin Manager Scoping:**

- `manager.NewScope(opts ...ScopeOption)` creates a child manager that isolates dynamically loaded plugins from the parent and from sibling scopes.
- Scopes chain for lookup: `Get` and `List` fall back to the parent (and so on up the chain) when a name is not found locally. A child scope may not load a plugin under a name that already exists in any ancestor: attempting this returns an error. Loading the exact same endpoint under the same name is idempotent and returns the ancestor's client unchanged.
- `scope.Close()` shuts down and unloads only the scope-local plugins. The parent and sibling scopes are completely unaffected. The local client map is cleared atomically on close.
- `scope.Unload(name)` removes only scope-local plugins; parent plugins cannot be unloaded from a child scope.
- Scopes can be nested to arbitrary depth. `Get`, `List`, and transport inheritance propagate correctly through the full chain.
- `WithTransport(TransportHTTP)` restricts a scope to HTTP(S) endpoints only: any attempt to load a stdio executable raises an error.
- `WithTransport(TransportStdio)` restricts a scope to stdio executables only: any attempt to load an HTTP(S) URL raises an error.
- `WithTransport(TransportAll)` (default) permits both transport types.

**Pooled, HTTP/2-capable transports:**

- `plugin.NewManager` now creates two shared `*http.Transport` instances: one TLS-verified, one with TLS skip-verify: that are inherited by all child scopes via `NewScope`. Connections to the same endpoint are reused across scopes, reducing TLS handshake overhead and enabling HTTP/2 connection reuse.
- `manager.LoadURL(ctx, name, url, scriptling, insecureSkipTLS=true, ...)` now draws from the manager's pooled skip-verify transport rather than creating a new transport per connection.
- The shared transports use `ForceAttemptHTTP2: true`, `MaxIdleConnsPerHost: 20`, and `IdleConnTimeout: 90s`.
{{< /changelog-item >}}

{{< changelog-item "security" >}}
**Markdown Library:**

- `scriptling.markdown.to_html` no longer passes raw HTML through to the output. Raw HTML blocks and inline HTML are now dropped (replaced with an HTML comment), so untrusted input such as LLM output cannot inject `<script>` tags, event handlers, or other dangerous markup. The rendered HTML is safe for direct insertion into a page. HTML-like syntax inside code spans and fenced code blocks is still rendered, with angle brackets HTML-escaped.
{{< /changelog-item >}}

---

{{< version "v0.12.1" >}}

{{< changelog-item "added" >}}
**Plugins with `scriptling.plugin`:**

- `scriptling.plugin.load(...)` can now load local executables and HTTP(S) JSON-RPC endpoints.
- Works with both plugin styles: typed Scriptling plugin protocol (`scriptling=True`) and raw JSON-RPC methods (`scriptling=False`, default).
- New `scriptling.plugin.batch_call(...)` supports batched calls with ordered results.
- `describe()` / `list()` include handshake metadata for Scriptling plugins, while raw JSON-RPC peers skip handshake metadata.
- Loading is deduplicated by absolute path; conflicting name/path combinations raise an error.
- New `scriptling.plugin.unload(name)` cleanly stops and removes a plugin.
- Go manager support matches this behavior, including HTTP(S) loading.
- `scriptling.plugin` is always available in run, server, and `--json-rpc` modes (even without `--plugin-dir`).

**JSON-RPC over HTTP:**

- `scriptling --server ... --json-rpc ...` now exposes JSON-RPC at `POST /json-rpc`.
- `scriptling --json-rpc ...` still works over stdio when `--server` is not used.
- HTTP JSON-RPC supports single calls, batches, and notifications (`204 No Content` for notification-only requests), and can run alongside existing HTTP routes and MCP tools.

**Provisioning Library: Managed Blocks:**

- New `scriptling.provision.file.ensure_block(...)` manages marker-delimited sections inside a file, updating only the managed block and leaving the rest untouched.
- Supports start/end placement, insertion after a matching line, and multiple independent blocks via unique block ids.
- New `scriptling.provision.file.absent_block(...)` removes a managed block and returns `file.REMOVED` or `file.UNCHANGED`.

**Provisioning Library: Fetch:**

- New `scriptling.provision.fetch.file(...)` downloads HTTP/HTTPS files idempotently, with optional size limits and zip extraction.
- Supports trusted internal endpoints (`insecure=True`) and optional `provides` checks to skip work when expected files already exist.
- Zip extraction is safe against path traversal and keeps executable bits.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Provisioning Library File:**

- `scriptling.provision.file.ensure` now accepts a `create_only=False` keyword argument; when `True`, an existing file is never modified and the call returns `file.UNCHANGED`, while new files are still written normally: useful for seeding config files only on first run
{{< /changelog-item >}}

---

{{< version "v0.12.0" >}}

{{< changelog-item "added" >}}
**JSON-RPC stdio server:**

- Added `scriptling.runtime.jsonrpc`, a concurrent stdin/stdout JSON-RPC 2.0
  server. Handlers are referenced by string (`"library.function"`) and run on a
  fresh, isolated evaluator per request. Supports batches, notifications, and structured errors. Start with
  `scriptling --json-rpc setup.py`; logs are redirected to stderr so the stdout
  stream stays pure JSON-RPC.

{{< /changelog-item >}}

---

{{< version "v0.11.3" >}}

{{< changelog-item "added" >}}
**Markdown Library:**

- New `scriptling.markdown` library with `to_html(markdown_string)` for converting Markdown to HTML
{{< /changelog-item >}}

---

{{< version "v0.11.1" >}}

{{< changelog-item "fixed" >}}
**Language: ImportError handling:**

- Failed `import` and `from ... import ...` statements now raise catchable `ImportError` exceptions inside `try` / `except`, while uncaught import failures still terminate evaluation as before
- `ImportError(...)` is available as a built-in exception constructor and can be used in typed `except ImportError` and tuple `except (..., ImportError)` clauses
{{< /changelog-item >}}

---

{{< version "v0.11.0" >}}

{{< changelog-item "added" >}}
**Plugin System:**

- Plugin class properties are exposed through generated and native proxies, including read-only getters and getter/setter pairs
- Go plugins can emit records to the host logger with `plugin.Logger(ctx)`; host applications pass the manager-lifetime logger to `plugin.NewManager(appLogger, crashHandler)`
- Plugin manager crash handling can be supplied during construction, with `SetCrashHandler()` still available for late wiring
- New runnable plugin examples for properties and host logging
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Version:**

- Scriptling version bumped to `v0.11.0`
{{< /changelog-item >}}

---

{{< version "v0.10.0" >}}

{{< changelog-item "added" >}}
**Plugin System:**

- Go plugin system for extending Scriptling with out-of-process plugins written in Go
- `plugin.NewServer` for building plugin executables that register functions, classes, and constants via RPC
- `plugin.Manager` for loading and managing plugin binaries from directories
- `--plugin-dir` CLI flag and `SCRIPTLING_PLUGIN_DIR` env var for loading plugins in both CLI and server modes
- Auto-generated proxy classes with `__del__` that releases plugin-side objects on garbage collection
- GC finalizers installed automatically on all class instances with `__del__`: both in-process and plugin objects are cleaned up when unreachable
- Custom wrapper class source for full control over the host-side proxy
- `scriptling.plugin` control library: `list()`, `describe()`, `call_function()`, `call_method()`, `release()`
- Concurrent plugin server: multiple requests are dispatched in parallel so slow calls from one environment don't block another
- `plugin.RegisterScriptFunc` / `plugin.RegisterScriptClass` for host-side Scriptling code within plugin libraries
- Plugin callbacks: plugins can call host-provided functions via `plugin.Callback` interface during RPC calls, enabling streaming, event handlers, and other bidirectional patterns
- `object.GCReleaseHook` for best-effort cleanup when GC collects plugin-owned objects
- Evaluator installs `runtime.SetFinalizer` on instances of classes that define `__del__`, calling the destructor automatically on garbage collection

**Class Builder:**

- `object.ClassBuilder.Constructor(fn)` for typed receiver classes: constructor returns a Go struct, methods receive it directly
- `object.ClassBuilder.Property(name, getter)` and `PropertyWithSetter(name, getter, setter)` for exposing private Go struct fields as readable/writable Scriptling properties
{{< /changelog-item >}}

---

{{< version "v0.9.3" >}}

{{< changelog-item "added" >}}
**AI Library: Vector Similarity:**

- New `ai.cosine_similarity(a, b)` for comparing two embedding vectors; returns a score from -1.0 to 1.0

**Networking Library: DNS Resolve:**

- New `scriptling.net.resolve` library with `lookup_ip`, `lookup_srv`, and `resolve_srv_http` for DNS resolution

**Provisioning Library: File:**

- New `scriptling.provision.file` library with `ensure(path, content, mode=0o644)` for idempotent file provisioning
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**MCP Server: `tool.return_error()` messages lost:**

- When a tool called `return_error()`, the error message was discarded and replaced with a generic `Tool execution failed: script execution failed: SystemExit: 1`; the actual error message from the script is now correctly returned to the MCP client

**MCP Server: Tool script changes not auto-reloading:**

- The file watcher only triggered a reload on `.toml` changes; editing a tool's `.py` script now also triggers an automatic reload
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**CLI: Server Logging:**

- The HTTP and MCP servers now emit `trace`/`debug`-level diagnostics for incoming requests, dispatched handlers, middleware execution, MCP tool invocations, and WebSocket lifecycle events, controlled by `--log-level` / `SCRIPTLING_LOG_LEVEL` and `--log-format` / `SCRIPTLING_LOG_FORMAT`

**Docs: AI Client reference split:**

- The AI Client method reference (completion, streaming, embeddings, Responses API, Pipeline, etc.) has been split into its own [Client](../../reference/libraries/scriptling/ai/client/) page for easier navigation
{{< /changelog-item >}}

---

{{< version "v0.9.2" >}}

{{< changelog-item "added" >}}
**Filesystem Libraries: Pathlib copy, rename, iterdir, glob:**

- New `pathlib.Path.copy(target)` to copy a file or directory tree to a target path, returning a new `Path` pointing to the target
- New `pathlib.Path.rename(target)` to rename or move a file or directory, returning a new `Path` pointing to the target
- New `pathlib.Path.iterdir()` to list directory contents as `Path` objects
- New `pathlib.Path.glob(pattern)` to match a shell-style wildcard pattern (`*`, `?`, `**`) within a directory and return matching `Path` objects
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Language: Constant Folding:**

- Constant expressions (arithmetic, string concatenation, comparisons on literals) are now evaluated at compile time, reducing runtime overhead
{{< /changelog-item >}}

---

{{< version "v0.9.1" >}}

{{< changelog-item "added" >}}
**Language: Keyword-only Parameters:**

- Function and lambda signatures now support Python-style keyword-only parameters using a bare `*`, such as `def resize(image, *, width, height=100):`
- Keyword-only parameters are enforced at call time, so values after bare `*` must be supplied by name
- Keyword-only parameters can also follow `*args`, such as `def collect(prefix, *items, sep):`
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Language: Shorthand operators:**

- Shorthand assignment operators (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`, `&=`, `|=`, `^=`, `>>=`, `<<=`) now correctly evaluate the left-hand side expression against objects.
{{< /changelog-item >}}

---

{{< version "v0.9.0" >}}

{{< changelog-item "added" >}}
**AI Library: Parallel Completions:**

- New `client.completion_parallel(model, messages_list, max_parallel=1, **kwargs)`: run multiple chat completions concurrently
- New `client.ask_parallel(model, messages_list, max_parallel=1, **kwargs)`: run multiple ask completions concurrently
- The `max_parallel` parameter controls the number of concurrent API requests (default: 1, sequential)

**AI Library: Automatic Retry & Adaptive Parallel Concurrency:**

- `ai.Client()` now accepts `max_retries` (default 3), `retry_backoff` (default 1.0s), `retry_on_rate_limit` (default True), and `retry_on_server_error` (default True) kwargs
- 429 (rate limit) and 5xx (server error) responses are automatically retried with exponential backoff
- Completion responses now include a `retry` dict when retries occurred: `{"attempts": 2, "rate_limit_hit": true, "total_backoff": 1.0}`
- `completion_parallel()` and `ask_parallel()` now use adaptive concurrency: parallelism is automatically halved when rate limits are detected, reducing API pressure without manual tuning; workers wake immediately when backoff expires

**AI Library: Pipeline:**

- New `client.Pipeline(model, max_parallel=1, ask=False, **kwargs)`: creates a streaming completion pipeline that starts processing requests immediately as they are added, overlapping prompt generation with inference
- `pipe.add(message)`: queues a message; inference begins immediately as concurrency slots are available
- `pipe.complete()`: waits for all in-flight requests and returns results ordered by submission
- `ask=True` mode returns plain text strings; `ask=False` (default) returns full response dicts
- `completion_parallel()` and `ask_parallel()` are now implemented on top of Pipeline internally, giving them the same overlap benefit when items are added faster than they complete

**Requests Library: Parallel HTTP Requests:**

- New `requests.parallel(requests, max_parallel=4)`: execute multiple HTTP requests concurrently and return responses in submission order
- Each request is a dict with `method`, `url`, and optional `data`, `json`, `headers`, `params`, `auth`, `timeout`
- Returns a list of `Response` objects (or objects with an `error` attribute on failure)
- The `max_parallel` parameter controls the concurrency limit (default: 4)

**Filesystem Libraries: Permission Modes:**

- New `os.chmod(path, mode)` and `pathlib.Path.chmod(mode)` for changing file or directory permissions
- `os.mkdir(path, mode=0o777)`, `os.makedirs(path, mode=0o777, exist_ok=False)`, and `pathlib.Path.mkdir(mode=0o777, parents=False, exist_ok=False)` now accept Python-style mode arguments for directory creation
- New `os.removedirs(name)` for pruning empty directory trees
- New `pathlib.Path.read_bytes()` and `pathlib.Path.write_bytes(data)` for byte-oriented file helpers
- `os.write_file(path, content, mode=0o644)` now accepts an optional mode for newly-created files
- `fs.write_bytes(path, offset, data, mode=0o644)` now accepts an optional mode for newly-created files
{{< /changelog-item >}}

{{< changelog-item "removed" >}}
**AI Library: Removed `tool_round` and `tool_round_parallel`:**

- Removed `ai.tool_round()`: use `client.completion()` with `ai.tool_calls()` and `ai.execute_tool_calls()` directly, or use the `Agent` class for full tool loops
- Removed `ai.tool_round_parallel()`: use `client.completion_parallel()` with `ai.execute_tool_calls()` directly
{{< /changelog-item >}}
