---
title: Documentation MCP Server
description: Generate Scriptling's documentation as OKF bundles and serve them to AI agents through an MCP server.
weight: 4
---

Scriptling's documentation can be published as [OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) knowledge bundles and exposed to AI agents through a MCP server. An LLM can then browse and search the docs, list bundles and folders, read individual pages, and run semantic or keyword search without scraping the website.

## Prerequisites

- **Scriptling 0.17.4 or later** installed and on your `PATH` (`scriptling --version`). See [CLI Getting Started](./cli/) to install.

## 1. Generate the bundles

Clone the website repository and generate the bundles and MCP tools:

```bash
git clone https://github.com/paularlott/scriptling-website
cd scriptling-website

scriptling scripts/okf.py     # or, if you have make installed: make okf
```

This produces, under `mcp/`:

| Path | Contents |
|------|----------|
| `mcp/okf/scriptling-docs/`, `mcp/okf/scriptling-reference/`, `mcp/okf/scriptling-libraries/` | The three OKF knowledge bundles. |
| `mcp/tools/` | The `skb_*` MCP tools. |
| `mcp/okf/<bundle>/.vector.json` | Per-bundle vector index powering `skb_search`. |

## 2. Start the MCP server

The tools locate the bundles through the `OKF_ROOT` environment variable. From the repository root it defaults to `mcp/okf`, so the commands below work as-is.

**Over HTTP** (for HTTP-based MCP clients):

```bash
OKF_ROOT=mcp/okf scriptling --server :8765 --mcp-tools mcp/tools
# → http://127.0.0.1:8765/mcp
# shortcut: make mcp-server
```

**Over stdio** (for MCP hosts such as Claude Desktop, which launch the server as a subprocess):

```bash
OKF_ROOT=mcp/okf scriptling --mcp-tools mcp/tools
```

Or configure a host directly using absolute paths:

```json
{
  "mcpServers": {
    "scriptling-kb": {
      "command": "scriptling",
      "args": ["--mcp-tools", "/abs/path/to/scriptling-website/mcp/tools"],
      "env": { "OKF_ROOT": "/abs/path/to/scriptling-website/mcp/okf" }
    }
  }
}
```

## Tools

| Tool | Purpose |
|------|---------|
| `skb_list` | List a folder's contents, a file's metadata, or the bundles (empty path). |
| `skb_get` | Read a concept file; synthesizes a listing when given a folder. |
| `skb_search` | Semantic search ranked by natural-language query. |
| `skb_grep` | Exact, fast keyword search. |
