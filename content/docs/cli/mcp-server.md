---
title: MCP Server Mode
description: Running Scriptling as a Model Context Protocol (MCP) server for AI integration.
tags: [cli, mcp, ai]
weight: 7
---

Scriptling can run as an MCP (Model Context Protocol) server, enabling AI assistants to use your tools and execute scripts.

## MCP Server Overview

When running in MCP server mode, Scriptling provides:

1. **Custom MCP Tools**: Your own tools defined in `--mcp-tools` directory
2. **Script Execution Tool**: Allow AI to execute Scriptling code directly (`--mcp-exec-script`)
3. **Resources**: Files served by URI from `--mcp-resources` (a `{var}` + `.py` path is a template), plus built-in server/script resources
4. **Prompts**: Static `.md` or dynamic `.toml` + `.py` prompts from `--mcp-prompts`, plus a built-in `write_script` prompt
5. **Live reload & notifications**: All three folders hot-reload on change and push `listChanged` notifications so clients refresh automatically

## Starting an MCP Server

### Basic MCP Server with Custom Tools

```bash
# Start HTTP server with MCP tools
scriptling --server :8000 --mcp-tools ./tools setup.py
```

### With Script Execution Enabled

```bash
# Enable script execution tool (allows AI to run code)
scriptling --server :8000 --mcp-exec-script setup.py
```

### Combined Setup

```bash
# Both custom tools and script execution
scriptling --server :8000 --mcp-tools ./tools --mcp-exec-script setup.py

# With authentication
scriptling --server :8000 --mcp-tools ./tools --mcp-exec-script \
  --bearer-token my-secret-token setup.py

# With filesystem restrictions
scriptling --server :8000 --mcp-tools ./tools --mcp-exec-script \
  --allowed-paths "/tmp/sandbox,./data" setup.py
```

### Choosing the transport: HTTP vs stdio

The MCP tool flags (`--mcp-tools` and/or `--mcp-exec-script`) enable the MCP
server; the presence of `--server` selects the transport:

- **With `--server`** — MCP is served over HTTP at `/mcp` (as shown above).
- **Without `--server`** — MCP is served over **stdio** (stdin/stdout,
  newline-delimited JSON-RPC 2.0), the transport MCP hosts use to launch a
  server as a subprocess.

This mirrors `--json-rpc`, which serves over stdio by default and over HTTP at
`/json-rpc` when combined with `--server`.

```bash
# Serve tools over stdio
scriptling --mcp-tools ./tools

# Or the built-in script execution tool
scriptling --mcp-exec-script
```

> **Logging goes to stderr** in stdio mode so it never corrupts the protocol
> stream on stdout, exactly like `--json-rpc`. Some MCP hosts (e.g. the MCP
> Inspector) forward every stderr line to the client before the connection is
> fully established, which can cause errors. Use `--log-format null` to suppress
> all log output when this is an issue.

Configure it in an MCP host (e.g. Claude Desktop) as a command rather than a URL:

```json
{
  "mcpServers": {
    "scriptling": {
      "command": "scriptling",
      "args": ["--mcp-tools", "/absolute/path/to/tools"]
    }
  }
}
```

Test it by piping requests in:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | scriptling --mcp-exec-script
```

## MCP Options

| Flag                | Environment Variable       | Description                              | Default    |
| ------------------- | -------------------------- | ---------------------------------------- | ---------- |
| `--mcp-tools`       | `SCRIPTLING_MCP_TOOLS`     | Directory of MCP tools (`name.toml` + `name.py`) | (disabled) |
| `--mcp-resources`   | `SCRIPTLING_MCP_RESOURCES` | Directory of MCP resources (files served verbatim; `{var}` + `.py` = template, optional `.toml` metadata) | (disabled) |
| `--mcp-prompts`     | `SCRIPTLING_MCP_PROMPTS`   | Directory of MCP prompts (`name.md` static, or `name.toml` + `name.py` dynamic) | (disabled) |
| `--mcp-exec-script` | -                          | Enable MCP script execution tool         | false      |

Any of these flags enables the MCP server. Add `--server <addr>` to serve over
HTTP at `/mcp`; without it, the server runs over stdio.

## Script Execution Tool

The `--mcp-exec-script` flag enables a built-in MCP tool that allows AI assistants to execute Scriptling code directly.

### Enabling Script Execution

```bash
scriptling --server :8000 --mcp-exec-script setup.py
```

### Tool Details

- **Name:** `execute_script`
- **Description:** Execute Scriptling code and return the result
- **Parameters:**
  - `code` (string, required): Scriptling code to execute

### Return Behavior

The `execute_script` tool captures output in the following order of priority:

1. **Explicit return functions** - If you use `tool.return_string()`, `tool.return_object()`, etc., that value is returned
2. **Script return value** - If the script returns a value (e.g., calling a function that returns a string), it's automatically captured and returned
3. **Print output** - Output from `print()` statements is captured and returned if no other return method is used

```python
# Example: Direct return value
def greet():
    return "Hello, World!"
greet()  # Returns: "Hello, World!"

# Example: Print output
print("Hello, World!")  # Returns: "Hello, World!"

# Example: Explicit return (stops execution)
import scriptling.mcp.tool as tool
tool.return_string("Hello, World!")  # Returns immediately
```

For structured data (JSON), use `tool.return_object(data)`. For complex types returned directly (dict, list), they're automatically converted to JSON.

### Example: Using the Tool

```bash
# Call the execute_script tool via MCP
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/call",
    "params":{
      "name":"execute_script",
      "arguments":{
        "code":"for i in range(1, 21, 3):\n    print(i)"
      }
    }
  }'
```

### Returning Structured Data

When you need to return JSON instead of text:

```python
import scriptling.mcp.tool as tool

# Return JSON object
data = {"users": ["Alice", "Bob"], "count": 2}
tool.return_object(data)

# Or return text
tool.return_string("Operation completed successfully")
```

### Discovering Available Functions

The tool description instructs AI assistants to use `help(topic)` to discover available functions:

```python
# Get help on built-in functions
help('builtins')

# Get help on string methods
help('str')

# Get help on a library
import json
help('json')
```

## Custom MCP Tools

Custom tools are loaded from the directory specified by `--mcp-tools`. Each tool consists of two files:

- `toolname.toml`: Metadata (description, parameters)
- `toolname.py`: Implementation script

### Directory Structure

```
./tools/
  hello.toml      # Metadata for "hello" tool
  hello.py        # Implementation for "hello" tool
  add.toml        # Metadata for "add" tool
  add.py          # Implementation for "add" tool
```

### Starting with Custom Tools

```bash
scriptling --server :8000 --mcp-tools ./tools setup.py
```

For details on creating custom tools, see [Writing MCP Tools](../../../reference/libraries/scriptling/mcp/writing-mcp-tools/).

### Conditional Tool Registration

The MCP scanner *evaluates* each `.py` file to find `@mcp.tool` decorators —
it doesn't just parse the AST. This means decorators inside a conditional
only fire when the condition is true, so you can gate tools behind CLI flags
or environment checks.

`sys.argv` is available in tool evaluators and contains extra args passed
after `--` on the command line:

```python
# tools/files.py
import scriptling.runtime.mcp as mcp
import sys

@mcp.tool("Read a file", params={"path": "File path"})
def read_file(path):
    return "contents"

if "--allow-write" in getattr(sys, "argv", []):
    @mcp.tool("Write a file", params={"path": "File path", "content": "Content"})
    def write_file(path, content):
        return "wrote " + path

    @mcp.tool("Delete a file", params={"path": "File path"})
    def delete_file(path):
        return "deleted " + path
```

```sh
# Read-only — only read_file is visible
scriptling --mcp-tools tools

# Read + write — all three tools are visible
scriptling --mcp-tools tools -- --allow-write
```

The same pattern works in app bundles:

```sh
scriptling --package . -- --allow-write
```

`sys.argv` is set once at startup and is the same at scan time and request
time, so the condition is consistent across all tool invocations.

## MCP Endpoints

When running as an MCP server, the following endpoints are available:

### List Tools

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Call a Tool

```bash
# Native tool (appears in tools/list)
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"hello",
      "arguments":{"name":"Alice","times":2}
    }
  }'

# Script execution tool
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":3,
    "method":"tools/call",
    "params":{
      "name":"execute_script",
      "arguments":{"code":"print(2 + 2)"}
    }
  }'
```

### Search Discoverable Tools

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":4,
    "method":"tools/call",
    "params":{
      "name":"tool_search",
      "arguments":{"query":"math"}
    }
  }'
```

### Execute a Discoverable Tool

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":5,
    "method":"tools/call",
    "params":{
      "name":"execute_tool",
      "arguments":{"name":"add","arguments":{"a":5,"b":3}}
    }
  }'
```

## Resources and Prompts

As well as tools, the MCP server exposes resources and prompts. They are defined
as **files in folders** — no Go code, no startup registration — the same model
as tools.

- **Resources** (`--mcp-resources`): a file is served verbatim at the URI formed
  from its path (first directory = scheme, rest = URI). A path containing a
  `{var}` segment and ending in `.py` is a **template** whose script runs with
  the extracted variable. An optional `_stem.toml` sibling provides a
  human-readable name, description, and MIME type; without it the URI is used as
  the name. Files starting with `_` are metadata, never served.
- **Prompts** (`--mcp-prompts`): `name.md` for a static prompt (one user
  message), or `name.toml` + `name.py` for a dynamic, arg-driven prompt. The
  dynamic `.toml` uses **the same format as a tool's `.toml`** — `description`
  plus an array of tables — but `[[arguments]]` instead of `[[parameters]]`,
  and prompt arguments are string-only (no `type`).

A built-in `scriptling://script/{name}` resource template (tool source code,
when `--mcp-tools` is set) and a `write_script` prompt are always available.

**For a walkthrough of creating resources and prompts** — including the shared
`.toml` format — see the [Building an MCP Resources & Prompts Server tutorial](../../tutorials/mcp-resources-prompts/).
The [tool metadata reference](../../../reference/libraries/scriptling/mcp/writing-mcp-tools/)
covers the `.toml` fields prompts share. To read resources and prompts from a
server in a script, see the [scriptling.mcp client](../../../reference/libraries/scriptling/mcp/client/#resources-and-prompts).

## Live Reload and Change Notifications

When `--mcp-tools`, `--mcp-resources`, or `--mcp-prompts` point at folders,
Scriptling watches them for changes. Adding, editing, or removing a file reloads
that primitive automatically (debounced); `SIGHUP`/`SIGUSR1` force an immediate
reload of all three.

Reloads mutate the live server in place and emit `notifications/tools/listChanged`,
`notifications/resources/listChanged`, and `notifications/prompts/listChanged` so
connected clients drop their cached list and re-fetch — over both HTTP
(Server-Sent Events) and stdio. The server advertises `listChanged` support for
all three primitives in its capabilities.

```bash
# Force a reload
kill -HUP $(pidof scriptling)
```

## Security Considerations

### Script Execution Tool

The `--mcp-exec-script` flag allows AI assistants to execute arbitrary code. Consider:

- Use `--allowed-paths` to restrict filesystem access
- Use `--bearer-token` to require authentication
- Run in a sandboxed environment for untrusted AI systems

```bash
# Secure configuration for script execution
scriptling --server :8000 --mcp-exec-script \
  --allowed-paths "/tmp/sandbox" \
  --bearer-token secure-token setup.py
```

### Custom Tools

Custom tools run with the same permissions as the server process. Validate inputs and restrict file access as needed.

## Complete Example

### Full MCP Server Setup

```bash
# Start server with both custom tools and script execution
scriptling --server :8000 \
  --mcp-tools ./tools \
  --mcp-exec-script \
  --bearer-token my-secret-token \
  --allowed-paths "/tmp/sandbox,./data" \
  setup.py
```

This configuration:
- Loads custom tools from `./tools/`
- Enables the script execution tool
- Requires bearer token authentication
- Restricts file operations to `/tmp/sandbox` and `./data`

## See Also

- [Basic Usage](../basic-usage/) - Running scripts, interactive mode, and lint mode
- [Command Line Options](../command-line-options/) - Every flag and configuration file setting
- [HTTP Server Mode](../http-server/) - HTTP server without MCP
- [Writing MCP Tools](../../../reference/libraries/scriptling/mcp/writing-mcp-tools/) - Creating custom MCP tools
- [MCP Library](../../../reference/libraries/scriptling/mcp/) - MCP library reference
- [MCP Tool Library](../../../reference/libraries/scriptling/mcp/tool/) - Tool implementation API
