---
description: Build a complete MCP application with an app view, tools, a prompt and a skill, package it as one artifact, and run it from the package.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/tutorials/mcp-app-package/
sources:
    - resource: https://scriptling.dev/docs/tutorials/mcp-app-package/
status: stable
tags:
    - tutorials
    - mcp
    - ai
    - packaging
title: Packaging an MCP App
type: Guide
---
# Packaging an MCP App

This tutorial builds a complete MCP application, packages it into a single
artifact, and proves every feature works from the package: an MCP Apps view
(a sales dashboard), plain tools, a prompt with arguments, and a skill. No
configuration flags: the package's manifest declares what it serves.

The finished project ships in the scriptling repository as
`examples/mcp-app-package`; you can run every command in this tutorial
against it.

## Prerequisites

- Scriptling CLI installed ([Installation](https://scriptling.dev/okf/scriptling-docs/quick-start/cli.md))
- Basic familiarity with MCP tools (see [Building an MCP Tool Server](https://scriptling.dev/okf/scriptling-docs/tutorials/mcp-tool-server.md))

## What You'll Build

A sales application exposing:

1. **`sales_report`**, an MCP Apps tool: calling it returns the sales records
   and links them to an interactive dashboard view.
2. **`add_sale`**, an app-only action tool the dashboard's own form calls.
3. **`sales_total`** and **`top_product`**, plain model-facing tools.
4. **`sales_insight`**, a prompt with a required `period` argument and an
   optional `region` argument.
5. **`dashboard-ops`**, a skill explaining how to operate the dashboard,
   with a supporting regions reference file.

## Step 1: Project Layout

Create the project directory:

```bash
mkdir sales-app && cd sales-app
mkdir tools prompts skills resources/ui/sales-dashboard
```

Convention directories are auto-discovered: `tools/`, `resources/`,
`prompts/`, `skills/` and `webroot/` are served when present, so the
manifest only needs to say which protocols the package serves.

## Step 2: The Manifest

Create `manifest.toml`:

```toml
name = "sales-dashboard-app"
version = "1.0.0"
description = "Sales dashboard MCP app: an app view tool, plain tools, a prompt and a skill"
main = "setup.py"
serve = ["mcp"]
```

`serve = ["mcp"]` makes the package an MCP server; add `"http"` to also
serve HTTP routes and a `webroot/`. `setup.py` is the entry point that runs
before serving (for auth middleware or per-user registration); this app needs
none, so the file can be just a comment.

## Step 3: The App Tool and Its View

`tools/sales_report.toml` links the tool to its UI resource per the
[MCP Apps](https://github.com/modelcontextprotocol/ext-apps) extension:

```toml
description = "Get the current sales report as a table and chart"

[ui]
resourceUri = "ui://sales-dashboard/dashboard.html"
```

`tools/sales_report.py` returns the records (seeding a few on first call)
from the KV store. The view itself is
`resources/ui/sales-dashboard/dashboard.html`: everything under
`resources/ui/<name>/` is served as a `ui://` resource, with optional
`_dashboard.toml` sidecar declaring CSP domains. Copy both from
`examples/mcp-app-dashboard` rather than writing a dashboard from scratch.

`tools/add_sale.{toml,py}` is the dashboard's write-back tool: its `[ui]`
table sets `visibility = ["app"]` because only the open view calls it, never
the model.

## Step 4: Plain Tools

`tools/sales_total.{toml,py}` takes no parameters and returns the sum; a
`.toml` with just a description is enough. `tools/top_product.{toml,py}`
takes an optional `min_amount` parameter, declared in its `.toml`:

```toml
description = "Name of the product with the highest single sale above a threshold"

[[parameters]]
name = "min_amount"
type = "number"
description = "Only consider sales at or above this amount"
required = false
```

## Step 5: The Prompt

`prompts/sales_insight.toml` declares the arguments per the MCP spec: a
prompt's `prompts/get` takes string arguments, and a missing required one is
rejected with `-32602` before the script runs.

```toml
description = "Ask for insights about a sales period"

[[arguments]]
name = "period"
description = "Period to analyse, e.g. 2026-09"
required = true

[[arguments]]
name = "region"
description = "Region code (see the dashboard-ops skill); default all"
required = false
```

`prompts/sales_insight.py` reads them with `tool.get_string("period")` and
`tool.get_string("region", "all")` and returns a `{"messages": [...]}` dict
for a multi-message prompt. The same rules hold for every prompt style:
decorated `@mcp.prompt` functions infer their arguments from the function
signature (a parameter without a default is required), and middleware's
`register_request_prompt` takes the same `arguments` list.

## Step 6: The Skill

`skills/dashboard-ops/SKILL.md` is the Agent Skills format: YAML frontmatter
whose `name` matches the directory, plus any supporting files:

```markdown
---
name: dashboard-ops
description: Operating the sales dashboard app - reading reports, adding sales, and interpreting the chart
---

# Dashboard Operations
...
```

`skills/dashboard-ops/references/regions.md` rides along and is served as
`skill://dashboard-ops/references/regions.md`. Every file becomes a
`skill://` resource with a digest, listed by `skills/list` per the Skills
extension.

## Step 7: Package It

From the repo root:

```bash
scriptling pack -o sales-app.zip examples/mcp-app-package
```

`pack` prints the package's sha256 (for `#sha256=` pinning when serving from
a URL). Files outside the convention directories, like the verification
client, produce a warning and stay behind.

## Step 8: Run It and Prove It

Over stdio:

```bash
scriptling --package sales-app.zip
```

Over HTTP, for real MCP clients:

```bash
scriptling --server :8080 --package sales-app.zip
# MCP endpoint: http://localhost:8080/mcp
```

The example's `client.py` connects to the package over stdio and checks
everything, using the [MCP client library](https://scriptling.dev/okf/scriptling-libraries/mcp/client.md):

```bash
scriptling examples/mcp-app-package/client.py
```

It proves, from the packaged zip:

| Check | Result |
|-------|--------|
| `sales_report` listed with `is_app: true`, returns records | yes |
| `ui://sales-dashboard/dashboard.html` readable | 11 KB of HTML |
| `sales_total`, `top_product(min_amount=100)` | `450.75`, `Gizmo (210.00)` |
| `sales_insight` with both arguments, optional default | renders |
| `sales_insight` missing required `period` | `-32602 missing required argument` |
| `skills/list` shows `dashboard-ops`; SKILL.md and regions.md readable | yes |

## Key Points

- **One artifact**: tools, resources, prompts, skills and the app view ship
  in a single zip; folder and zip run the same code path (dev equals prod).
- **Convention over configuration**: the manifest declares protocols; the
  directory layout declares content.
- **Every prompt style shares one contract**: string arguments on
  `prompts/get`, required ones validated centrally to `-32602`.
- **Skills are first-class package content**: packed by convention, served
  at startup, and readable file by file as `skill://` resources.
