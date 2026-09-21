---
description: Linking a tool to an interactive UI resource, from any tool registration style.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/mcp/mcp-apps/
sources:
    - resource: https://scriptling.dev/reference/libraries/mcp/mcp-apps/
status: stable
tags:
    - libraries
    - mcp
title: MCP Apps
type: API Reference
---
# MCP Apps

[MCP Apps](https://github.com/modelcontextprotocol/ext-apps) (SEP-1865) is an MCP extension that lets a tool link to a companion interactive HTML UI, which a compliant host renders in a sandboxed iframe instead of (or alongside) the tool's text result. Linking a tool only **declares** the connection — nothing renders it server-side, and a host that doesn't support the extension just ignores it and the tool behaves exactly as it would without one.

All three tool registration styles support it:

| Style | How | Docs |
|---|---|---|
| Folder (`.toml` + `.py`) | `[ui]` table in the tool's `.toml` | [Writing MCP Tools](https://scriptling.dev/okf/scriptling-libraries/mcp/writing-mcp-tools.md#linking-a-ui-resource-ui) |
| Decorated (`@mcp.tool`) | `ui=` keyword argument | below |
| Dynamic (`register_request_tool`) | `ui=` keyword argument | below |

## The `ui` Dict

Wherever it appears — a decorator kwarg, a `register_request_tool` kwarg, or (as TOML) a `[ui]` table — the shape is the same:

| Field | Required | Description |
|---|---|---|
| `resourceUri` | No\* | URI of the paired `ui://` resource |
| `visibility` | No\* | Array of `"model"` and/or `"app"`; who can see the tool (default: both) |

\* At least one of the two must be present, or `ui` shouldn't be set at all. `resourceUri` names the view a compliant host renders **when this tool is called** — an `"app"`-only *action* tool that's only ever called by a view that's already open (a form submission, a "claim" button) has no rendering purpose of its own and should omit it, declaring `visibility` alone. Use `resourceUri` on an `"app"`-only tool only when calling it should *also* refresh a view — see `add_sale` below for the plain-action case.

`resourceUri`, when given, must point at a resource served with mimeType `text/html;profile=mcp-app` — see [The Paired Resource](#the-paired-resource) below.

## Decorated Tools

```python
import scriptling.runtime.mcp as mcp

@mcp.tool("Get the sales report",
          ui={"resourceUri": "ui://sales-dashboard/dashboard.html"})
def sales_report():
    return {"records": [...]}

@mcp.tool("Add a sale record (called by the dashboard's own form, not the model)",
          ui={"visibility": ["app"]})
def add_sale(date, product, amount):
    ...
```

`add_sale` is `visibility: ["app"]`: a compliant host still sees it in `tools/list` (the natural way for a host to learn it exists, so it can let the view call it), but hides it from the model — it's meant to be called by the dashboard's own form, not requested by the AI. It has no `resourceUri`: the dashboard is already open by the time this gets called, so there's no view of its own for it to render.

## Dynamic (Per-Request) Tools

```python
import scriptling.runtime.mcp as mcp

def auth(request):
    mcp.register_request_tool("sales_report", handler="reportmod.report",
        description="Get the sales report",
        ui={"resourceUri": "ui://sales-dashboard/dashboard.html"})
    return None
```

Same `ui` dict, same rules — see [Request-Scoped Registration](https://scriptling.dev/okf/scriptling-libraries/runtime/mcp.md#request-scoped-registration) for the rest of `register_request_tool`'s parameters.

## The Paired Resource

`resourceUri` names a normal Scriptling resource — no code changes needed on the resource side, since resources already support arbitrary URI schemes and mimetypes via a `_{stem}.toml` sidecar:

```
resources/ui/sales-dashboard/dashboard.html      # The UI itself
resources/ui/sales-dashboard/_dashboard.toml     # mimeType + optional CSP
```

```toml
# resources/ui/sales-dashboard/_dashboard.toml
mimeType = "text/html;profile=mcp-app"
name = "Sales Dashboard"

[ui.csp]
resourceDomains = ["https://cdn.jsdelivr.net"]
```

The `[ui.csp]` table (and its siblings `[ui.permissions]`, `ui.domain`, `ui.prefersBorder`) tell a compliant host what the sandboxed iframe is allowed to reach — omit it entirely to accept the host's restrictive same-origin/inline-only default. See [Resources and Prompts](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md#resources-and-prompts) for how the resource scanner derives a URI from a file's path.

## Returning Structured Data

A UI typically wants its data as `structuredContent`, not JSON buried in a text block:

```python
import scriptling.mcp.tool as tool

tool.return_structured({"records": [...]})
```

`return_structured` requires a dict (structuredContent must be a JSON object per the MCP spec) and, for backwards compatibility with clients that don't read `structuredContent`, still includes the same JSON as a text block — see [Returning Results](https://scriptling.dev/okf/scriptling-libraries/mcp/writing-mcp-tools.md#returning-results) for how it compares to `return_object`.

## Icons

Any tool — with or without a `ui` link — can carry visual identifiers via `icons`, a list of dicts:

```python
@mcp.tool("Get the weather",
          icons=[{"src": "https://example.com/weather.png", "mimeType": "image/png", "sizes": ["48x48"]}])
def weather():
    ...
```

| Field | Required | Description |
|---|---|---|
| `src` | Yes | An `https://` URL or `data:` URI |
| `mimeType` | No | Media type, e.g. `image/png` — useful when it can't be inferred from `src` |
| `sizes` | No | Size hints such as `"48x48"`, or `"any"` for a scalable format like SVG |
| `theme` | No | `"light"` or `"dark"` — omit for a theme-neutral icon |

Icons aren't required on every tool — a plain `"app"`-only action tool like `add_sale` above typically doesn't need one. All three registration styles accept `icons` the same way:

```toml
# Folder style (.toml)
[[icons]]
src = "https://example.com/weather.png"
mimeType = "image/png"
```

```python
# Dynamic (register_request_tool) — same shape as the decorator
mcp.register_request_tool("weather", handler="weathermod.forecast",
    description="Get the weather",
    icons=[{"src": "https://example.com/weather.png", "mimeType": "image/png"}])
```

Scriptling only carries this metadata on the wire — it never fetches or renders icon bytes itself. A host that does render icons is responsible for the MCP spec's security precautions (treat `src` and any fetched bytes as untrusted, require an `https://` or `data:` URI, reject unsafe schemes and cross-origin redirects, fetch without credentials, verify content type from magic bytes, and guard against oversized images).

## See Also

- [Writing MCP Tools](https://scriptling.dev/okf/scriptling-libraries/mcp/writing-mcp-tools.md) — the three registration styles in full
- [MCP Apps extension specification](https://github.com/modelcontextprotocol/ext-apps)
