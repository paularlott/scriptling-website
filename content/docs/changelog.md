---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
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
