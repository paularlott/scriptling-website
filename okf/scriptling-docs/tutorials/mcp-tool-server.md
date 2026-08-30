---
description: Create a Model Context Protocol server with custom tools for AI assistants.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/tutorials/mcp-tool-server/
sources:
    - resource: https://scriptling.dev/docs/tutorials/mcp-tool-server/
status: stable
tags:
    - tutorials
    - mcp
    - ai
title: Building an MCP Tool Server
type: Guide
---
# Building an MCP Tool Server

This tutorial walks through building an MCP (Model Context Protocol) server with custom tools that AI assistants like Claude can discover and call.

## Prerequisites

- Scriptling CLI installed ([Installation](https://scriptling.dev/okf/scriptling-docs/quick-start/cli.md))
- An MCP-compatible AI client (e.g., Claude Desktop)

## What You'll Build

A tool server that exposes three tools:
1. **time_now**: returns the current time in a given timezone format
2. **data_summary**: generates a summary of a list of numbers
3. **format_report**: formats key-value data as a structured report

## Step 1: Create the Tool Directory

```bash
mkdir -p my-tools
cd my-tools
```

## Step 2: Define the time_now Tool

Create `my-tools/time_now.toml`:

```toml
description = "Get the current date and time"
keywords = ["time", "date", "now"]

[[parameters]]
name = "format"
type = "string"
description = "Time format string (e.g. '%Y-%m-%d' for date, '%H:%M:%S' for time)"
required = false
```

Create `my-tools/time_now.py`:

```python
import time

def call(args, kwargs):
    fmt = kwargs.get("format", "%Y-%m-%d %H:%M:%S")
    return time.strftime(fmt, time.localtime())
```

## Step 3: Define the data_summary Tool

Create `my-tools/data_summary.toml`:

```toml
description = "Calculate summary statistics for a list of numbers"
keywords = ["statistics", "stats", "average", "mean", "data"]

[[parameters]]
name = "numbers"
type = "array:number"
description = "List of numbers to summarize"
required = true
```

Create `my-tools/data_summary.py`:

```python
import statistics

def call(args, kwargs):
    numbers = kwargs["numbers"]

    if not numbers:
        return {"error": "Empty list provided"}

    result = {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }

    if len(numbers) > 1:
        result["stdev"] = statistics.stdev(numbers)
        result["median"] = statistics.median(numbers)

    return result
```

## Step 4: Define the format_report Tool

Create `my-tools/format_report.toml`:

```toml
description = "Format a dictionary of data as a structured text report"
keywords = ["format", "report", "text", "display"]

[[parameters]]
name = "title"
type = "string"
description = "Report title"
required = true

[[parameters]]
name = "data"
type = "string"
description = "JSON string of key-value pairs to include in the report"
required = true
```

Create `my-tools/format_report.py`:

```python
import json

def call(args, kwargs):
    title = kwargs["title"]
    data = json.loads(kwargs["data"])

    lines = []
    lines.append("=" * 50)
    lines.append(f"  {title}")
    lines.append("=" * 50)
    lines.append("")

    for key, value in data.items():
        lines.append(f"  {key}:")
        lines.append(f"    {value}")
        lines.append("")

    lines.append("-" * 50)
    return "\n".join(lines)
```

## Step 5: Start the MCP Server

Scriptling serves MCP over HTTP. Start the server with the tools directory:

```bash
scriptling --server :8000 --mcp-tools ./my-tools setup.py
```

The MCP endpoint is mounted at `http://127.0.0.1:8000/mcp`. See [MCP Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md) for the full set of options.

## Step 6: Configure Claude Desktop

Add the tool server to your Claude Desktop configuration (`claude_desktop_config.json`) using the HTTP endpoint:

```json
{
  "mcpServers": {
    "scriptling-tools": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Restart Claude Desktop. The AI will discover the tools automatically and can call them when needed.

## Step 7: Test Tools from the CLI

Call individual tools directly against the `/mcp` endpoint with a `tools/call` request:

```bash
# Test time_now
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"my-tools/time_now","arguments":{"format":"%H:%M"}}}'

# Test data_summary
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"my-tools/data_summary","arguments":{"numbers":[10,20,30,40,50]}}}'
```

To list all available tools, send a `tools/list` request:

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/list"}'
```

## Step 8: Add Discoverable Tools

For tools that need to be explicitly registered via script (e.g., tools that depend on runtime state), set `discoverable = false` in the TOML file:

```toml
description = "Query the internal database"
discoverable = false

[[parameters]]
name = "query"
type = "string"
description = "SQL-like query string"
required = true
```

Then register them in your setup script:

```python
import scriptling.mcp.tool as mcp

# Register the tool with a custom handler
mcp.register("db_query", "internal/db_query.py")
```

## Tool Directory Structure

The final directory structure:

```
my-tools/
  time_now.toml
  time_now.py
  data_summary.toml
  data_summary.py
  format_report.toml
  format_report.py
```

## What You Learned

- Defining MCP tools with TOML metadata files
- Implementing tool logic in Scriptling scripts
- Starting Scriptling as an MCP server
- Configuring Claude Desktop to use custom tools
- Testing tools from the command line
- Discoverable vs manually-registered tools

## See Also

- [Writing MCP Tools](https://scriptling.dev/okf/scriptling-libraries/mcp/writing-mcp-tools.md) - Complete MCP tool reference
- [MCP Client Library](https://scriptling.dev/okf/scriptling-libraries/mcp/client.md) - Connecting to MCP servers from scripts
- [CLI MCP Server](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md) - CLI server mode documentation
- [Statistics Library](https://scriptling.dev/okf/scriptling-libraries/math-numbers/statistics.md) - Stats functions used in this tutorial
