---
title: Building an MCP Resources & Prompts Server
linkTitle: Resources & Prompts Server
description: Create MCP resources and prompts as files, alongside tools.
tags: [tutorials, mcp, ai]
weight: 4
---

This tutorial walks through exposing **resources** and **prompts** from a
Scriptling MCP server — the other two MCP primitives alongside tools. Like
tools, they are just files in folders: no Go code, no startup registration.

## Prerequisites

- Scriptling CLI installed ([Installation](../../quick-start/cli/))
- Read [Building an MCP Tool Server](../mcp-tool-server/) first — this tutorial
  mirrors its conventions

## What you'll build

A server exposing four things, each defined as files:

1. A **static resource** — a Markdown file served verbatim.
2. A **templated resource** — a `{var}` path whose `.py` generates content.
3. A **static prompt** — a `.md` file rendered as a single user message.
4. A **dynamic prompt** — a `.toml` + `.py` that declares arguments and renders
   messages.

## Step 1: Create the folders

```bash
mkdir -p mcp/resources/docs mcp/resources/greeting mcp/prompts mcp/tools
cd mcp
```

## Step 2: A static resource (just a file)

Resources are files served verbatim — **no metadata, no script**. The first
directory under `--mcp-resources` is the URI scheme; the rest of the path is the
URI:

```
resources/docs/about.md  ->  docs://about.md
```

Create `resources/docs/about.md`:

```markdown
# About

A static resource: drop a file in the folder and it is readable by URI.
```

That's the whole resource. The MIME type comes from the extension
(`text/markdown`).

### Optional `_` metadata

To give a static resource a human-readable name and description, add a
`_{stem}.toml` sibling (the `_` prefix hides it from listings):

Create `resources/docs/_about.toml`:

```toml
name = "About"
description = "Information about this MCP server example"
mimeType = "text/markdown"
```

All three fields are optional — without metadata, the resource's name defaults
to its full URI (`docs://about.md`), the MIME type is auto-detected from the
file extension, and no description is set. Files starting with `_` are never
served as resources.
## Step 3: A templated resource

A path containing a `{var}` segment and ending in `.py` is a **template**: the
`.py` runs with the extracted variable.

```
resources/greeting/{name}.py  ->  greeting://{name}
```

Create `resources/greeting/{name}.py` (the literal braces are part of the
filename):

```python
import scriptling.mcp.tool as tool

# "name" is the {name} variable extracted from the requested URI.
# Reading greeting://Ada runs this with name = "Ada".
name = tool.get_string("name")
tool.return_string("Hello, " + name + "!")
```

Reading `greeting://Ada` invokes the script with `name = "Ada"`.

### Optional `.toml` metadata

Without metadata, the template's name defaults to its full URI
(`greeting://{name}`). To give it a human-readable name, description, and MIME
type, add a `_{stem}.toml` sibling (the `_` prefix hides it from listings):

Create `resources/greeting/_{name}.toml`:

```toml
name = "Greeting"
description = "A personalized greeting for a name"
mimeType = "text/plain"
```

The `.toml` is optional — if absent the template still works, just with the URI
as its name and no description. Files starting with `_` are never served.

> A `.py` with **no** `{var}` in its path is served as source text, not
> executed. Only templated resources run scripts.

## Step 4: A static prompt

A prompt named `summarize` from a single Markdown file — no metadata:

Create `prompts/summarize.md`:

```markdown
Summarise the following content in three bullet points. Be concise.
```

The whole file becomes one user message.

## Step 5: A dynamic prompt (`.toml` + `.py`)

A dynamic prompt declares its arguments and renders messages in a script. The
`.toml` uses **the same format as a tool's `.toml`** — `description` plus an
array of tables — except it is `[[arguments]]` instead of `[[parameters]]`, and
prompt arguments are always strings (no `type` field):

| Tool `.toml`                         | Prompt `.toml`                       |
| ------------------------------------ | ------------------------------------ |
| `[[parameters]]` with `name`, `type`, `description`, `required` | `[[arguments]]` with `name`, `description`, `required` (strings only) |

Create `prompts/review.toml`:

```toml
description = "Ask the model to review code"

[[arguments]]
name = "language"
description = "Programming language"
required = true

[[arguments]]
name = "code"
description = "The code to review"
required = true
```

Create `prompts/review.py` (reads its arguments with `mcp.tool.get_string` and
returns messages with `mcp.tool.return_object`):

```python
import scriptling.mcp.tool as tool

language = tool.get_string("language")
code = tool.get_string("code")

tool.return_object({
    "messages": [
        {"role": "user", "content": "Review this " + language + " code:\n\n" + code}
    ]
})
```

A bare string returned (via `tool.return_string`) is treated as a single user
message.

## Step 6: Add a tool (optional)

Drop a tool in `tools/` exactly as in the [tool tutorial](../mcp-tool-server/) —
`name.toml` + `name.py`. Tools, resources, and prompts all live side by side.

## Step 7: Run it

```bash
# Over HTTP
scriptling --server :8000 \
  --mcp-tools ./tools \
  --mcp-resources ./resources \
  --mcp-prompts ./prompts

# Or over stdio (drop --server)
```

## Try it

```bash
# Static resource (file served verbatim)
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"docs://about.md"}}'

# Templated resource (.py runs with the {name} var)
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"resources/read","params":{"uri":"greeting://Ada"}}'

# List resources and templates
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"resources/list"}'
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"resources/templates/list"}'

# Static prompt
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":5,"method":"prompts/get","params":{"name":"summarize"}}'

# Dynamic prompt (.py runs with declared arguments)
curl -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":6,"method":"prompts/get","params":{"name":"review","arguments":{"language":"python","code":"print(1)"}}}'
```

## Live reload

Editing, adding, or removing a file in any of the three folders triggers an
automatic reload, and the server emits `listChanged` notifications so connected
clients re-fetch. `SIGHUP` / `SIGUSR1` force a reload.

## Summary

| Primitive | Folder flag | Files |
| --- | --- | --- |
| Tools | `--mcp-tools` | `name.toml` + `name.py` |
| Resources | `--mcp-resources` | files served verbatim; `{var}` + `.py` = template; optional `_stem.toml` for name/description/mimeType |
| Prompts | `--mcp-prompts` | `name.md` static, or `name.toml` + `name.py` dynamic |

## See also

- [Building an MCP Tool Server](../mcp-tool-server/) — the tool tutorial
- [MCP Server Mode](../../cli/mcp-server/) — running the server, flags, transports
- [Writing MCP Tools](../../../reference/libraries/mcp/writing-mcp-tools/) — tool metadata reference (the `.toml` format prompts share)
- [MCP client library](../../../reference/libraries/mcp/client/) — reading resources and prompts from a server
