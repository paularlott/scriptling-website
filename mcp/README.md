# Scriptling KB — MCP Server

Browse and search Scriptling's documentation (OKF knowledge bundles) from any
MCP-compatible AI client. Ships three bundles — `scriptling-docs`, `scriptling-reference`,
`scriptling-libraries` — exposed as four tools.

## Requirements

- The `scriptling` CLI, **0.17.4 or later**, installed and on your `PATH` (`scriptling --version`).

## Install

Unzip the archive anywhere, then `cd` into it:

```bash
unzip scriptling-kb.zip -d scriptling-kb
cd scriptling-kb
```

You should have:

```
scriptling-kb/
├── tools/           # the skb_* MCP tools (+ okf_lib.py helper)
└── okf/             # the knowledge bundles (scriptling-docs/, scriptling-reference/, scriptling-libraries/)
```

The tools read the bundles from `$OKF_ROOT`, so every command below sets it to
this folder's `okf/`. Substitute your real absolute path where shown.

## Tools

| Tool          | What it does                                                             |
| ------------- | ------------------------------------------------------------------------ |
| `skb_list`    | List what's at a path: a folder's contents, a file's metadata, or the bundles (empty path). |
| `skb_get`     | Read a concept file as markdown; synthesizes a listing for a folder.     |
| `skb_search`  | Semantic search: rank concepts by relevance to a natural-language query. |
| `skb_grep`    | Exact/fast keyword search (parallel grep, OR, case-insensitive).         |

The bundles also carry a per-bundle vector index (`.vector.json`) computed by
`make okf`, which powers `skb_search`. It's a hidden file, ignored by `skb_list`.

## Option A — stdio (for MCP hosts like Claude Desktop)

With no `--server`, `--mcp-tools` serves MCP over **stdio** (newline-delimited
JSON-RPC on stdin/stdout) — the transport hosts use to launch the server as a
subprocess. Configure your host to spawn `scriptling` directly, passing
`OKF_ROOT` so the tools find the bundles:

```json
{
  "mcpServers": {
    "scriptling-kb": {
      "command": "scriptling",
      "args": ["--mcp-tools", "/absolute/path/to/scriptling-kb/tools"],
      "env": { "OKF_ROOT": "/absolute/path/to/scriptling-kb/okf" }
    }
  }
}
```

Smoke test from a shell (after `cd scriptling-kb`):

```bash
export OKF_ROOT="$PWD/okf"
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"skb_list","arguments":{"path":""}}}' \
  | scriptling --mcp-tools "$PWD/tools"
```

> Logging goes to stderr so it can't corrupt the stdio stream. If your host
> forwards stderr before the handshake completes and errors, suppress it with
> `--log-format null` (add it to `args` above).

## Option B — HTTP

Add `--server <addr>` to serve MCP over HTTP at `/mcp`:

```bash
export OKF_ROOT="$PWD/okf"
scriptling --server :8765 --mcp-tools "./tools"
# → http://127.0.0.1:8765/mcp
```

Call it with curl (JSON-RPC 2.0):

```bash
# list tools
curl -s -X POST http://127.0.0.1:8765/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# list the bundles (empty path)
curl -s -X POST http://127.0.0.1:8765/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"skb_list","arguments":{"path":""}}}'

# search everywhere for "sandbox"
curl -s -X POST http://127.0.0.1:8765/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"skb_search","arguments":{"path":"","terms":["sandbox"]}}}'
```

Point any HTTP-based MCP client at `http://<host>:8765/mcp`.

## Updating

The knowledge in `okf/` is generated from the Scriptling website's `content/`
with `make okf` (see the website repo). Regenerate, then rebuild the archive
with `make pack` to produce a fresh `scriptling-kb.zip`.
