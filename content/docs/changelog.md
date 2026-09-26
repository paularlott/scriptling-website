---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## September 2026

{{< version "v0.28.0" >}}

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
