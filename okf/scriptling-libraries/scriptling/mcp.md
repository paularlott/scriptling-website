---
description: MCP (Model Context Protocol) client and tool authoring libraries.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/mcp/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/mcp/
status: stable
tags:
    - libraries
    - mcp
title: MCP Protocol
type: API Reference
---
# MCP Protocol

MCP (Model Context Protocol) is a protocol for AI models to interact with external tools and data sources. These libraries connect to MCP servers and author MCP tools that can be used by AI agents: a client for calling server-exposed tools, and helpers for creating tools.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.mcp](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/client.md) | MCP client for connecting to MCP servers |
| [scriptling.mcp.tool](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/tool.md) | Helper library for authoring MCP tools |
| [Writing MCP Tools Guide](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/writing-mcp-tools.md) | Guide for creating MCP tools |

## Quick Start

```python
import scriptling.mcp as mcp

# Connect to an MCP server
client = mcp.Client("http://localhost:8080/mcp")

# List available tools
tools = client.tools()

# Call a tool
result = client.call_tool("search", {"query": "hello"})
```

## See Also

- [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/scriptling/ai.md) - AI and agent libraries that consume MCP tools
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) - Network-enabled libraries risk breakdown
