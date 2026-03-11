---
title: MCP Server Mode
description: Running Scriptling as a Model Context Protocol (MCP) server for AI integration.
weight: 3
---

Scriptling can run as an MCP (Model Context Protocol) server, enabling AI assistants to use your tools and execute scripts.

## MCP Server Overview

When running in MCP server mode, Scriptling provides:

1. **Custom MCP Tools** — Your own tools defined in `--mcp-tools` directory
2. **Script Execution Tool** — Allow AI to execute Scriptling code directly (`--mcp-exec-script`)

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

## MCP Options

| Flag                | Environment Variable       | Description                              | Default    |
| ------------------- | -------------------------- | ---------------------------------------- | ---------- |
| `--mcp-tools`       | `SCRIPTLING_MCP_TOOLS`     | Directory containing MCP tool files      | (disabled) |
| `--mcp-exec-script` | -                          | Enable MCP script execution tool         | false      |

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

- Output from `print()` statements is automatically captured and returned
- For structured data (JSON), use `import scriptling.mcp.tool` and call `tool.return_object(data)`
- For text output, use `tool.return_string(text)`

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

- `toolname.toml` — Metadata (description, parameters)
- `toolname.py` — Implementation script

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

For details on creating custom tools, see [Writing MCP Tools](../../../libraries/scriptling/writing-mcp-tools/).

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

- [Basic Usage](../basic-usage/) - Installation and command line options
- [HTTP Server Mode](../http-server/) - HTTP server without MCP
- [Writing MCP Tools](../../../libraries/scriptling/writing-mcp-tools/) - Creating custom MCP tools
- [MCP Library](../../libraries/scriptling/mcp/) - MCP library reference
- [MCP Tool Library](../../libraries/scriptling/mcp-tool/) - Tool implementation API
