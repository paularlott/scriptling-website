---
description: Serve Scriptling's documentation as OKF bundles to AI agents through the OKF MCP server.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/quick-start/documentation-mcp/
sources:
    - resource: https://scriptling.dev/docs/quick-start/documentation-mcp/
status: stable
tags:
    - quick-start
    - mcp
    - ai
title: Documentation MCP Server
type: Guide
---
# Documentation MCP Server

Scriptling's documentation can be published as [OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) knowledge bundles and exposed to AI agents through an MCP server. An LLM can then browse and search the docs, list bundles and folders, read individual pages, and run semantic or keyword search without scraping the website.

The MCP server is a separate, generic project — [okf-server](https://github.com/paularlott/okf-server) — that works with any OKF bundles. Scriptling ships prebuilt bundles, so there is no need to clone or build anything.

The same bundles are also hosted as plain markdown at [scriptling.dev/okf/](https://scriptling.dev/okf/) — if your agent can fetch URLs it can read the docs directly (each bundle's `index.md` lists its concepts), and the MCP server is only needed for search and write access.

## Prerequisites

- **Scriptling 0.18.0 or later** installed and on your `PATH` (`scriptling --version`). See [CLI Getting Started](https://scriptling.dev/okf/scriptling-docs/quick-start/cli.md) to install.

## 1. Download the bundles

Grab the latest OKF bundles archive and unzip it into a `bundles/` folder:

```bash
curl -L -o okf-bundles.zip \
  https://github.com/paularlott/scriptling-website/releases/latest/download/scriptling-okf-bundles.zip
unzip okf-bundles.zip -d bundles && rm okf-bundles.zip
```

This gives three bundles under `bundles/`:

| Bundle | Contents |
|--------|----------|
| `bundles/scriptling-docs/` | Guides and tutorials. |
| `bundles/scriptling-reference/` | CLI and language reference. |
| `bundles/scriptling-libraries/` | Standard library API reference. |

The `latest/download` URL always fetches the newest release. To pin a specific version, replace it with `releases/download/v0.18.0/scriptling-okf-bundles.zip`.

Per-bundle search indexes (`.vectors.json`, `.tags.json`, `.types.json`) are built automatically by the server on first use, so they are not shipped with the bundles.

## 2. Start the MCP server

Run the [okf-server](https://github.com/paularlott/okf-server) package with `scriptling`, pointing `--bundles` at the downloaded bundles:

**Over HTTP** (for HTTP-based MCP clients):

```bash
scriptling --server :8765 \
  --package https://github.com/paularlott/okf-server/releases/latest/download/okf-server.zip \
  -- --bundles ./bundles
# → http://127.0.0.1:8765/mcp
```

**Over stdio** (for MCP hosts such as Claude Desktop, which launch the server as a subprocess):

```bash
scriptling \
  --package https://github.com/paularlott/okf-server/releases/latest/download/okf-server.zip \
  -- --bundles ./bundles
```

As with the bundles, the `latest/download` URL always fetches the newest okf-server release. To pin a specific version instead, use `releases/download/v0.1.0/okf-server.zip`.

For a host such as Claude Desktop, configure it to spawn `scriptling`. Download and unzip the [okf-server package](https://github.com/paularlott/okf-server/releases/latest) once, then reference it by absolute path. Most hosts support an `env` block:

```json
{
  "mcpServers": {
    "okf": {
      "command": "scriptling",
      "args": ["--package", "/abs/path/to/okf-server"],
      "env": { "OKF_BUNDLES": "/abs/path/to/bundles" }
    }
  }
}
```

If your client doesn't support `env`, pass `--bundles` as an argument after `--` instead:

```json
{
  "mcpServers": {
    "okf": {
      "command": "scriptling",
      "args": ["--package", "/abs/path/to/okf-server", "--", "--bundles", "/abs/path/to/bundles"]
    }
  }
}
```

## Write mode

By default the server is read-only. Add `--allow-write` (after `--`) to let agents create or delete concepts — useful when maintaining the bundles:

```bash
scriptling --server :8765 \
  --package https://github.com/paularlott/okf-server/releases/latest/download/okf-server.zip \
  -- --bundles ./bundles --allow-write
```

## Tools

| Tool | Purpose |
|------|---------|
| `okf_get` | Read a concept; synthesizes a listing when given a folder (empty path lists the bundles). |
| `okf_search` | Semantic search ranked by natural-language query. |
| `okf_grep` | Exact, fast keyword search. |
| `okf_facets` | List the tags and types present, with concept counts. |

See the [okf-server README](https://github.com/paularlott/okf-server) for the full tool list, faceted filtering, and the `okf_concept_write` / `okf_concept_delete` write tools.
