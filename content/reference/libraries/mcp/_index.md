---
title: MCP Protocol
description: MCP (Model Context Protocol) client and tool authoring libraries.
tags: [libraries, mcp]
weight: 12

aliases:
  - /reference/libraries/scriptling/mcp/
---

MCP (Model Context Protocol) is a protocol for AI models to interact with external tools and data sources. These libraries connect to MCP servers and author MCP tools that can be used by AI agents: a client for calling server-exposed tools, and helpers for creating tools.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.mcp](client/) | MCP client for connecting to MCP servers |
| [scriptling.mcp.tool](tool/) | Helper library for authoring MCP tools |
| [Writing MCP Tools Guide](writing-mcp-tools/) | Guide for creating MCP tools |

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

- [scriptling.ai](../ai/) - AI and agent libraries that consume MCP tools
- [Libraries](../) - Full library reference index
- [Security Guide](/docs/security/#network-security) - Network-enabled libraries risk breakdown
