---
title: MCP Protocol
description: MCP (Model Context Protocol) client and tool authoring libraries.
weight: 4
---

Libraries for connecting to MCP servers and authoring MCP tools that can be used by AI agents.

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
client = mcp.connect("http://localhost:8080/mcp")

# List available tools
tools = client.list_tools()

# Call a tool
result = client.call_tool("search", {"query": "hello"})
```

## Overview

MCP (Model Context Protocol) is a protocol for AI models to interact with external tools and data sources. These libraries provide:

- **Client**: Connect to MCP servers and use their tools
- **Tool Authoring**: Create MCP tools that can be exposed to AI agents
