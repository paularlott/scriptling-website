---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## September 2026

{{< version "v0.28.0" >}}

{{< changelog-item "added" >}}
**Type annotations are accepted.** Function signatures (`def f(a: int, b: str = "x") -> bool:`), annotated assignments (`count: int = 5`), and generic/string annotations (`dict[str, int]`, `int | None`) all parse; the annotations are ignored, matching their runtime meaning in Python, so annotated Python pastes in unchanged — including MCP tool functions. See [Functions](/reference/functions/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Walrus assignment expressions.** `while (chunk := read()):`, `if (n := len(x)) > 10:`, and walrus in comprehension filters, with Python's precedence. A walrus bound inside a comprehension does not leak to the enclosing scope. See [Operators](/reference/operators/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Dict merge operators.** `d1 | d2` builds a new dict with the right operand winning conflicts, and `d |= other` merges in place so aliases observe the update, matching Python (PEP 584). See [Operators](/reference/operators/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**The `...` placeholder.** `def stub(): ...` bodies and `tuple[int, ...]` annotations parse; the expression evaluates to `None`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`json.dumps(data, indent=n)` honors a numeric indent.** The kwarg previously only accepted strings, so `indent=2` silently produced compact output; a number now gives that many spaces and `indent=0` newline-separates. See [json](/reference/libraries/data-formats/json/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`sum()` accepts Python's optional `start` argument.** `sum(iterable, start)` previously failed; it now offsets the total and can seed a float result. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`list.sort()` is as honest as `sorted()`.** Sorting incomparable elements (dicts without a `key`) silently did nothing where `sorted()` raised; both now use one comparator, so `.sort()` errors the same way and also supports `__lt__` on instances. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`repr(e)` prints the exception's class.** `ValueError: bad input` instead of the generic `EXCEPTION:` wrapper, matching `type(e)`. The LLM guide also now states that custom exception classes are not supported. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`type(e)` reports the exception's class.** `type()` on a caught exception now returns the class it was raised as (`"ValueError"`, `"KeyError"`) instead of the generic `"EXCEPTION"`, so `except` blocks can discriminate without message sniffing. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**A failing tool no longer kills the agent turn.** A tool handler that raises — or a tool name the model invented — now comes back as an `Error: ...` tool result the model can see and recover from, and the other tools in the same batch still run. See [Agent](/reference/libraries/ai/agent/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`ToolRegistry.add()` with a duplicate name now replaces the tool.** Previously re-registering a name appended a second identical schema — the model saw two copies of the tool — while silently swapping the handler. `add_schema()` still errors on duplicates.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**The positional-only separator `/` is rejected with a clear parse error.** `def f(a, /, b)` previously parsed with the `/` silently accepted as a parameter named `/`, so every call failed with a confusing argument-count error. The parser now reports `positional-only parameters ('/') are not supported` up front.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**The `@mcp.tool` help example no longer uses `eval()`.** The example used `eval()`, which does not exist in scriptling — copying it produced an error.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`scriptling pack --list <package>`.** Prints what a package contains before you deploy it: the manifest's name, version and protocols, each convention directory with its file count, and the sha256. The [Python differences](/reference/python-differences/) page was also re-verified end to end: nested classes and `bytes()` work and are now listed as supported, and `input()`'s availability and the `type(x).__name__` divergence are documented precisely.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`sys.executable`: the running interpreter's path.** Lets a script relaunch its own binary as a subprocess instead of depending on which `scriptling` resolves to on PATH; the MCP examples now launch their stdio servers this way. See [sys](/reference/libraries/http-process/sys/).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`mcp.Client` HTTP requests time out after 30 seconds by default.** Script-level clients previously inherited the library's 5-minute timeout, so a hung server stalled a script for minutes per call. `mcp.Client(url, timeout=300)` opts a known-slow server back up, and timeouts surface as ordinary catchable exceptions. See [MCP Client](/reference/libraries/mcp/client/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`Agent` can use real MCP servers: the `mcp_servers=` argument.** Pass one or more `mcp.Client` clients and the agent gets their tools (namespaced, so a `search` tool on a client with `namespace="shop"` becomes `shop__search`) and skills alongside its own. Each client needs a distinct namespace. See [Agent](/reference/libraries/ai/agent/#mcp-server-integration).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`tools.Registry.add_schema(name, description, schema, handler)` registers a tool from a full JSON Schema.** For parameter shapes richer than the flat name-to-type map `add()` accepts (nested objects, enums, per-parameter descriptions). Duplicate names are an error instead of a silent overwrite. See [AI Tools](/reference/libraries/ai/tools/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Register resources, prompts and skills from script code: `@mcp.resource`, `@mcp.prompt`, `@mcp.skill`.** The tools folder's decorated `.py` files can now register every MCP entry kind, not just tools. One file can mix all four decorators, everything reloads with the tools folder, and the same registrations work in app bundles. See [runtime.mcp](/reference/libraries/runtime/mcp/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Booleans order like numbers in `min()`, `max()` and `sorted()`.** `sorted([True, False])` previously failed and `min([True, False])` returned the wrong element; booleans now order as 0 and 1, matching Python. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`min()` and `max()` honor the `key` function.** Previously `max(records, key=lambda r: r["amount"])` silently returned the first record instead of the largest. A `default` argument is also supported for the single-iterable form. See [Built-in Functions](/reference/builtins/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**App packages can carry skills.** The `skills/` directory joins `tools/`, `resources/`, `prompts/`, `webroot/` and `docs/` as a package convention directory: present means packed and served. See the [Packaging an MCP App](/tutorials/mcp-app-package/) tutorial.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`client.namespace` on an MCP client.** The client's namespace (empty string when created without one) is now readable as an attribute, so scripts can tell which server a namespaced tool name or skill URI belongs to. See [MCP Client](/reference/libraries/mcp/client/).
{{< /changelog-item >}}

---

{{< version "v0.27.0" >}}

{{< changelog-item "added" >}}
**The MCP server can serve skills (SEP-2640).** `--mcp-skills` (env `SCRIPTLING_MCP_SKILLS`) points at a directory of skills — one per subdirectory containing a `SKILL.md` — served per the MCP skills extension via `skills/list` and `skills/get`, with each file readable as a `skill://` resource. See [MCP Server](/docs/cli/mcp-server/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`mcp.Client` can consume skills: `skills()` and `get_skill(uri)`.** `skills()` lists the skills a server exposes (URI, frontmatter, per-file digests) and `get_skill(uri)` fetches one; the content reads with the existing `read_resource`. Works for HTTP and stdio clients alike. See [MCP Client](/reference/libraries/mcp/client/).
{{< /changelog-item >}}
