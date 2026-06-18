---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
---


## June 2026

{{< version "v0.12.0" >}}

{{< changelog-item "added" >}}
### JSON-RPC stdio server

- Added `scriptling.runtime.jsonrpc`, a concurrent stdin/stdout JSON-RPC 2.0
  server. Handlers are referenced by string (`"library.function"`) and run on a
  fresh, isolated evaluator per request. Supports batches, notifications, and structured errors. Start with
  `scriptling --jsonrpc setup.py`; logs are redirected to stderr so the stdout
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
**Language — ImportError handling:**

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
- GC finalizers installed automatically on all class instances with `__del__` — both in-process and plugin objects are cleaned up when unreachable
- Custom wrapper class source for full control over the host-side proxy
- `scriptling.plugin` control library: `list()`, `describe()`, `call_function()`, `call_method()`, `release()`
- Concurrent plugin server — multiple requests are dispatched in parallel so slow calls from one environment don't block another
- `plugin.RegisterScriptFunc` / `plugin.RegisterScriptClass` for host-side Scriptling code within plugin libraries
- Plugin callbacks — plugins can call host-provided functions via `plugin.Callback` interface during RPC calls, enabling streaming, event handlers, and other bidirectional patterns
- `object.GCReleaseHook` for best-effort cleanup when GC collects plugin-owned objects
- Evaluator installs `runtime.SetFinalizer` on instances of classes that define `__del__`, calling the destructor automatically on garbage collection

**Class Builder:**

- `object.ClassBuilder.Constructor(fn)` for typed receiver classes — constructor returns a Go struct, methods receive it directly
- `object.ClassBuilder.Property(name, getter)` and `PropertyWithSetter(name, getter, setter)` for exposing private Go struct fields as readable/writable Scriptling properties
{{< /changelog-item >}}

---

{{< version "v0.9.3" >}}

{{< changelog-item "added" >}}
**AI Library — Vector Similarity:**

- New `ai.cosine_similarity(a, b)` for comparing two embedding vectors; returns a score from -1.0 to 1.0

**Networking Library — DNS Resolve:**

- New `scriptling.net.resolve` library with `lookup_ip`, `lookup_srv`, and `resolve_srv_http` for DNS resolution

**Provisioning Library — File:**

- New `scriptling.provision.file` library with `ensure(path, content, mode=0o644)` for idempotent file provisioning
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**MCP Server — `tool.return_error()` messages lost:**

- When a tool called `return_error()`, the error message was discarded and replaced with a generic `Tool execution failed: script execution failed: SystemExit: 1`; the actual error message from the script is now correctly returned to the MCP client

**MCP Server — Tool script changes not auto-reloading:**

- The file watcher only triggered a reload on `.toml` changes; editing a tool's `.py` script now also triggers an automatic reload
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**CLI — Server Logging:**

- The HTTP and MCP servers now emit `trace`/`debug`-level diagnostics for incoming requests, dispatched handlers, middleware execution, MCP tool invocations, and WebSocket lifecycle events, controlled by `--log-level` / `SCRIPTLING_LOG_LEVEL` and `--log-format` / `SCRIPTLING_LOG_FORMAT`

**Docs — AI Client reference split:**

- The AI Client method reference (completion, streaming, embeddings, Responses API, Pipeline, etc.) has been split into its own [Client](reference/libraries/scriptling/ai/client/) page for easier navigation
{{< /changelog-item >}}

---

{{< version "v0.9.2" >}}

{{< changelog-item "added" >}}
**Filesystem Libraries — Pathlib copy, rename, iterdir, glob:**

- New `pathlib.Path.copy(target)` to copy a file or directory tree to a target path, returning a new `Path` pointing to the target
- New `pathlib.Path.rename(target)` to rename or move a file or directory, returning a new `Path` pointing to the target
- New `pathlib.Path.iterdir()` to list directory contents as `Path` objects
- New `pathlib.Path.glob(pattern)` to match a shell-style wildcard pattern (`*`, `?`, `**`) within a directory and return matching `Path` objects
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Language — Constant Folding:**

- Constant expressions (arithmetic, string concatenation, comparisons on literals) are now evaluated at compile time, reducing runtime overhead
{{< /changelog-item >}}

---

{{< version "v0.9.1" >}}

{{< changelog-item "added" >}}
**Language — Keyword-only Parameters:**

- Function and lambda signatures now support Python-style keyword-only parameters using a bare `*`, such as `def resize(image, *, width, height=100):`
- Keyword-only parameters are enforced at call time, so values after bare `*` must be supplied by name
- Keyword-only parameters can also follow `*args`, such as `def collect(prefix, *items, sep):`
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Language — Shorthand operators:**

- Shorthand assignment operators (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`, `&=`, `|=`, `^=`, `>>=`, `<<=`) now correctly evaluate the left-hand side expression against objects.
{{< /changelog-item >}}

---

{{< version "v0.9.0" >}}

{{< changelog-item "added" >}}
**AI Library — Parallel Completions:**

- New `client.completion_parallel(model, messages_list, max_parallel=1, **kwargs)` — run multiple chat completions concurrently
- New `client.ask_parallel(model, messages_list, max_parallel=1, **kwargs)` — run multiple ask completions concurrently
- The `max_parallel` parameter controls the number of concurrent API requests (default: 1, sequential)

**AI Library — Automatic Retry & Adaptive Parallel Concurrency:**

- `ai.Client()` now accepts `max_retries` (default 3), `retry_backoff` (default 1.0s), `retry_on_rate_limit` (default True), and `retry_on_server_error` (default True) kwargs
- 429 (rate limit) and 5xx (server error) responses are automatically retried with exponential backoff
- Completion responses now include a `retry` dict when retries occurred: `{"attempts": 2, "rate_limit_hit": true, "total_backoff": 1.0}`
- `completion_parallel()` and `ask_parallel()` now use adaptive concurrency — parallelism is automatically halved when rate limits are detected, reducing API pressure without manual tuning; workers wake immediately when backoff expires

**AI Library — Pipeline:**

- New `client.Pipeline(model, max_parallel=1, ask=False, **kwargs)` — creates a streaming completion pipeline that starts processing requests immediately as they are added, overlapping prompt generation with inference
- `pipe.add(message)` — queues a message; inference begins immediately as concurrency slots are available
- `pipe.complete()` — waits for all in-flight requests and returns results ordered by submission
- `ask=True` mode returns plain text strings; `ask=False` (default) returns full response dicts
- `completion_parallel()` and `ask_parallel()` are now implemented on top of Pipeline internally, giving them the same overlap benefit when items are added faster than they complete

**Requests Library — Parallel HTTP Requests:**

- New `requests.parallel(requests, max_parallel=4)` — execute multiple HTTP requests concurrently and return responses in submission order
- Each request is a dict with `method`, `url`, and optional `data`, `json`, `headers`, `params`, `auth`, `timeout`
- Returns a list of `Response` objects (or objects with an `error` attribute on failure)
- The `max_parallel` parameter controls the concurrency limit (default: 4)

**Filesystem Libraries — Permission Modes:**

- New `os.chmod(path, mode)` and `pathlib.Path.chmod(mode)` for changing file or directory permissions
- `os.mkdir(path, mode=0o777)`, `os.makedirs(path, mode=0o777, exist_ok=False)`, and `pathlib.Path.mkdir(mode=0o777, parents=False, exist_ok=False)` now accept Python-style mode arguments for directory creation
- New `os.removedirs(name)` for pruning empty directory trees
- New `pathlib.Path.read_bytes()` and `pathlib.Path.write_bytes(data)` for byte-oriented file helpers
- `os.write_file(path, content, mode=0o644)` now accepts an optional mode for newly-created files
- `fs.write_bytes(path, offset, data, mode=0o644)` now accepts an optional mode for newly-created files
{{< /changelog-item >}}

{{< changelog-item "removed" >}}
**AI Library — Removed `tool_round` and `tool_round_parallel`:**

- Removed `ai.tool_round()` — use `client.completion()` with `ai.tool_calls()` and `ai.execute_tool_calls()` directly, or use the `Agent` class for full tool loops
- Removed `ai.tool_round_parallel()` — use `client.completion_parallel()` with `ai.execute_tool_calls()` directly
{{< /changelog-item >}}

---

## May 2026

{{< version "v0.8.0" >}}

{{< changelog-item "changed" >}}
**Go API — Private Value fields:**

- `Integer.Value`, `Float.Value`, `Boolean.Value`, and `String.Value` are now private
- Use `object.NewInteger()`, `object.NewFloat()`, `object.NewBoolean()`, `object.NewString()` constructors instead of struct literals
- Use `.IntValue()`, `.FloatValue()`, `.BoolValue()`, `.StringValue()` getters instead of `.Value`
- Small integer caching now prevents accidental mutation of shared singletons
{{< /changelog-item >}}

---

{{< version "v0.7.0" >}}

{{< changelog-item "changed" >}}
**Improved Performance**
{{< /changelog-item >}}

---

{{< version "v0.7.0" >}}

{{< changelog-item "added" >}}
**AI Tool Registry - type aliases:**

- `registry.add()` now accepts Python-style type aliases: `int` → `integer`, `float` → `number`, `str` → `string`, `bool` → `boolean`, `dict` → `object`, `list` → `array`

**MCP Go library:**

- New `mcp.Integer()` and `mcp.IntegerArray()` parameter constructors for tools that require whole numbers
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- `str.upper()` and `str.lower()` now correctly handle strings that mix ASCII letters with non-ASCII Unicode characters (e.g. `"naïve résumé".upper()` now returns `"NAÏVE RÉSUMÉ"`)
- AI Tool Registry: `"number"` is now emitted as JSON Schema `number` (was silently downgraded to `integer`)
- AI Tool Registry: unknown type strings now raise an error at `registry.add()` time instead of producing invalid schemas silently
- MCP tool metadata: `int` / `integer` now emit JSON Schema `integer`; `float` / `number` emit `number` (previously both mapped to `number`)
- MCP tool metadata: `array:int` / `array:integer` now emit array items of type `integer`; `array:float` / `array:number` emit items of type `number`
- MCP tool metadata: unknown type strings in `.toml` tool definitions now produce a registration error instead of silently defaulting to `string`
{{< /changelog-item >}}

---

{{< version "v0.6.5" >}}

{{< changelog-item "changed" >}}
**AI library:**

- `scriptling.ai.Client(..., headers={...})` — Add custom HTTP headers to every AI API request made by that client
- `client.completion(..., extra_body={...})` and `client.completion_stream(..., extra_body={...})` — Merge provider-specific fields into chat completion request bodies, such as Z.ai thinking-mode options
- `scriptling.ai.estimate_tokens(request, response=None)` — Allow request-only and response-only token estimates by omitting `response` or passing `None` for either side
{{< /changelog-item >}}

{{< version "v0.6.4" >}}

{{< changelog-item "added" >}}
**FloatArray enhancements:**

- `.tolist()` method - Convert FloatArray to a plain list (1D returns list of floats, 2D returns list of lists)
- `.shape()` method - Return shape as a list of integers (method equivalent of `math.shape()`)
- `+` operator - Concatenate FloatArrays (1D joins elements, 2D stacks rows with matching columns)
- List comprehension support - Iterate FloatArray in comprehensions with optional filtering (`[v * 2 for v in a]`, `[row[0] for row in m]`)

**Go API:**

- `GetFloatMatrix(obj)` - Typed getter that extracts data, rows, and cols from a 2D FloatArray
{{< /changelog-item >}}

---

{{< version "v0.6.3" >}}

{{< changelog-item "changed" >}}

**Performance improvements**

**Language:**

- `rf"..."` and `fr"..."` raw f-string prefixes now supported (previously only `r` and `f` separately)
- Triple-quoted f-strings: `f"""..."""` and `f'''...'''`
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**FloatArray type:**

- New `FloatArray` type for efficient numerical operations, avoiding per-element boxing overhead
- 1D and 2D arrays with row-major storage
- Supports indexing, slicing, assignment, iteration, equality, `in` operator, `for` loops, `len()`, `list()` conversion
- `math.array(data)` - Create a FloatArray from a list of numbers or list of lists
- `math.shape(a)` - Return the shape of a FloatArray as a list of ints

**Math library:**

- `softmax`, `dot`, `matmul`, `transpose`, `mat_add` now accept `FloatArray` inputs
- Functions return `FloatArray` when given `FloatArray` input, preserving type

**Built-in functions:**

- `sum()`, `min()`, `max()` accept `FloatArray`
- `enumerate()`, `zip()`, `reversed()` accept `FloatArray`
- `list()` converts `FloatArray` to a list of floats
- `for` loop iterates over `FloatArray` elements (1D) or rows (2D)
{{< /changelog-item >}}

---

## April 2026

{{< version "v0.6.2" >}}

{{< changelog-item "added" >}}
**Math library:**

- `tanh(x)` - Hyperbolic tangent
- `erf(x)` / `erfc(x)` - Error function and complementary error function
- `gamma(x)` / `lgamma(x)` - Gamma function and log-gamma
- `cbrt(x)` - Cube root
- `nextafter(x, y)` - Next floating-point value
- `remainder(x, y)` - IEEE 754-style remainder
- `log1p(x)` / `expm1(x)` - Accurate log(1+x) and exp(x)-1 for small x
- `comb(n, k)` - Binomial coefficient
- `perm(n[, k])` - Permutations
- `prod(iterable, start=1)` - Product of all elements
- `dist(p, q)` - Euclidean distance between two points
- `softmax(x)` - Numerically stable softmax
- `dot(a, b)` - Dot product of two vectors
- `matmul(a, b)` - Matrix multiplication
- `transpose(m)` - Matrix transpose
- `mat_add(a, b)` - Element-wise matrix addition
- `tau` constant - 2π (6.283185...)

**Random library:**

- `choices(population, weights, k)` - Weighted random sampling with replacement
- `betavariate(alpha, beta)` - Beta distribution
- `gammavariate(alpha, beta)` - Gamma distribution
- `triangular(low, high[, mode])` - Triangular distribution
- `paretovariate(alpha)` - Pareto distribution
- `weibullvariate(alpha, beta)` - Weibull distribution

**fs extension library:**

- `read_bytes(path, offset, length)` - Read bytes from a file
- `write_bytes(path, offset, data)` - Write bytes to a file
- `unpack(format, data)` / `pack(format, values)` - Binary struct packing/unpacking
- `byte_at(data, index)` - Get unsigned byte value
- `len(data)` - Byte length (not Unicode code points)
- `slice(data, start[, end])` - Byte-safe slicing
{{< /changelog-item >}}

---

{{< version "v0.6.1" >}}

{{< changelog-item "added" >}}
**Container library:**

- `volume_create(name, size=...)` - optional `size` kwarg (e.g. `"20G"`, `"512M"`) sets the volume size on Apple Containers; silently ignored for Docker and Podman
{{< /changelog-item >}}

---

{{< version "v0.6.0" >}}

{{< changelog-item "added" >}}
**HTTP server:**

- `runtime.http.not_found(handler)` - Register a custom 404 handler, called when no route matches or a web root file is not found
- `--web-root <dir|zip>` CLI flag (`SCRIPTLING_WEB_ROOT` / `server.web_root`) - Serve static files from a directory or zip archive; requests fall through to the `not_found` handler if no file is found

**Template library:**

- `scriptling.template.html` - `html/template` rendering with automatic HTML escaping
- `scriptling.template.text` - `text/template` rendering with no escaping
{{< /changelog-item >}}

---

{{< version "v0.5.8" >}}

{{< changelog-item "changed" >}}

**Gossip library updates:**

- `scriptling.text` renamed to `scriptling.sed` to better reflect its in-place editing capabilities
{{< /changelog-item >}}

{{< version "v0.5.7" >}}

{{< changelog-item "added" >}}
**Configuration file:**

- Optional `scriptling.toml` configuration file with search paths (`.`, `$HOME/`, `$HOME/.config/scriptling/`)
- `-C`/`--config` flag to specify a custom config file path
- All flags with a config path column can be set in the file
- Priority order: command-line flag > environment variable > config file > default

**Container management:**

- `scriptling.container` - Container lifecycle management for Docker, Podman, and Apple Containers

**Search:**

- `scriptling.grep` - Fast file content search with concurrent worker pool, glob filtering, binary file detection, and path restriction support
- `scriptling.text` - In-place file content replacement with atomic temp-file rename, concurrent worker pool, and path restriction support
{{< /changelog-item >}}

{{< changelog-item "changed" >}}

**Gossip library updates:**

- Request/reply messaging, node groups, and leader election
{{< /changelog-item >}}

---

{{< version "v0.5.6" >}}

{{< changelog-item "added" >}}
**Networking libraries:**

- `scriptling.net.gossip` - Gossip protocol cluster membership and messaging with failure detection, metadata propagation, tag-based routing, encryption, and compression
- `scriptling.net.multicast` - UDP multicast group messaging for one-to-many communication
- `scriptling.net.unicast` - UDP and TCP point-to-point messaging with client and server support

**Secrets:**

- `scriptling.secret` - Provider-agnostic secret access through host-configured aliases
- `--secret-config` - CLI support for loading Vault and 1Password provider aliases from TOML
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Runtime and tooling:**

- `scriptling.websocket` moved to `scriptling.net.websocket` to consolidate all networking libraries under the `scriptling.net` namespace
{{< /changelog-item >}}

---

{{< version "v0.5.5" >}}

{{< changelog-item "added" >}}
**Language:**

- `del` statement for removing list indices, slices, dict keys, and object attributes (`del items[0]`, `del cache["key"]`, `del obj.attr`)

**AI library:**

- `ai.tool_calls(response)` - Extract and normalize tool calls from a completion response, message dict, or raw list
- `ai.execute_tool_calls(registry, tool_calls)` - Execute tool calls using a `ToolRegistry` and return result messages
- `ai.collect_stream(stream, **kwargs)` - Collect a chat stream into a single aggregated result with optional per-chunk callbacks
- `ai.tool_round(client, model, messages, registry)` - Perform a single tool-use round: complete, execute tool calls, return results
- `ai.estimate_tokens(messages, model)` - Estimate token count for a message list

**Agent framework:**

- Agent constructor gains `max_tokens` and `compaction_threshold` parameters
- Automatic message compaction for long conversations, with configurable threshold
- Improved streaming support with reasoning and content chunk helpers

**Console:**

- Panel `add_message()` now accepts a `role` parameter (`user`, `system`, `thinking`, `tool`, `assistant`) for richer TUI output
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Runtime and tooling:**

- `isinstance()` now accepts a tuple or list of types, matching Python semantics (`isinstance(x, (int, float))`)
- Lexer keyword lookup refactored from map-based to switch-based dispatch for improved performance
- Better concurrency handling in `ChatStreamInstance` with caller cancellation support
- Improved error handling in variadic function calls
- Parser refactored with cleaner initialization and improved regex handling
{{< /changelog-item >}}
