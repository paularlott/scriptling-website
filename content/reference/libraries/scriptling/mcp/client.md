---
title: scriptling.mcp
linkTitle: mcp
weight: 1
---

MCP (Model Context Protocol) client library. This library provides functions for connecting to MCP servers and interacting with the tools they expose for AI models to use.

For MCP integration with AI clients, see the `remote_servers` parameter on [scriptling.ai.Client](../../ai/client/).

## Available Functions

| Function | Description |
|----------|-------------|
| `decode_response(response)` | Decode a raw MCP tool response |
| `Client(base_url, **kwargs)` | Create an MCP client for connecting to servers |

## MCPClient Methods

| Method | Description |
|--------|-------------|
| `client.tools()` | List available tools |
| `client.call_tool(name, arguments)` | Execute a tool by name |
| `client.call_tools_parallel(calls)` | Execute multiple tools concurrently |
| `client.refresh_tools()` | Refresh cached tool list |
| `client.tool_search(query, **kwargs)` | Search for tools by query |
| `client.execute_discovered(name, arguments)` | Execute a discovered tool |
| `client.execute_discovered_parallel(calls)` | Execute multiple discovered tools concurrently |

## Functions

### `mcp.decode_response(response)`

Decodes a raw MCP tool response into scriptling objects.

**Parameters:**

- `response` (`dict`): Raw tool response dict.

**Returns:** `object`: decoded response (parsed JSON or string).

```python
import scriptling.mcp as mcp

decoded = mcp.decode_response(raw_response)
```

```python
raw_response = {
    "content": [{"type": "text", "text": '{"temp": 15}'}]
}

decoded = mcp.decode_response(raw_response)
print(decoded)  # {"temp": 15}
```

### `mcp.Client(base_url, **kwargs)`

Creates a new MCP client for connecting to a remote MCP server.

**Parameters:**

- `base_url` (`str`): URL of the MCP server.
- `namespace` (`str`, optional): Namespace for tool names (e.g. `"scriptling"` makes tools available as `"scriptling/tool_name"`). Default: `""`.
- `bearer_token` (`str`, optional): Bearer token for authentication. Default: `""`.

**Returns:** `MCPClient`: a client instance with methods for interacting with the server.

```python
import scriptling.mcp as mcp

# Without namespace or auth
client = mcp.Client("https://api.example.com/mcp")

# With namespace only
client = mcp.Client("https://api.example.com/mcp", namespace="scriptling")

# With bearer token only
client = mcp.Client("https://api.example.com/mcp", bearer_token="your-token-here")

# With both namespace and bearer token
client = mcp.Client(
    "https://api.example.com/mcp",
    namespace="scriptling",
    bearer_token="your-token-here"
)
```

When using a namespace, all tool names are prefixed. For example, if the server has a tool called `execute_code` and you use namespace `scriptling`, the tool is available as `scriptling/execute_code`. The namespace is automatically added to all tool names and stripped when calling tools.

## MCPClient Class

### `client.tools()`

Lists all tools available from this MCP server.

**Returns:** `list`: tool dicts with `name`, `description`, `inputSchema`.

```python
client = mcp.Client("https://api.example.com/mcp")
tools = client.tools()

for tool in tools:
    print(f"{tool.name}: {tool.description}")
    if "inputSchema" in tool:
        print(f"  Schema: {tool.inputSchema}")
```

### `client.call_tool(name, arguments)`

Executes a tool by name with the provided arguments.

**Parameters:**

- `name` (`str`): Tool name to execute.
- `arguments` (`dict`): Tool arguments.

**Returns:** `dict`: decoded tool response.

```python
client = mcp.Client("https://api.example.com/mcp")

result = client.call_tool("search", {
    "query": "golang programming",
    "limit": 10
})

print(result)
```

### `client.refresh_tools()`

Explicitly refreshes the cached list of tools from the server.

**Returns:** `None`

```python
client = mcp.Client("https://api.example.com/mcp")

# Tools are cached, refresh to get latest
client.refresh_tools()

tools = client.tools()
```

### `client.tool_search(query, **kwargs)`

Searches for tools using the `tool_search` MCP tool. Useful when the server has many tools registered via a discovery registry.

**Parameters:**

- `query` (`str`): Search query for tool names, descriptions, and keywords.
- `max_results` (`int`, optional): Maximum number of results. Default: `10`.

**Returns:** `list`: matching tool dicts.

```python
client = mcp.Client("https://api.example.com/mcp")

# Search for weather-related tools (default: up to 10 results)
results = client.tool_search("weather")

# Search with custom limit
results = client.tool_search("database", max_results=5)

for tool in results:
    print(f"{tool.name}: {tool.description}")
```

### `client.call_tools_parallel(calls)`

Executes multiple tools concurrently and returns results in the same order as the input.

**Parameters:**

- `calls` (`list`): List of dicts, each with `name` (`str`) and `arguments` (`dict`) keys.

**Returns:** `list`: result dicts with `name`, `result`, and `error` keys. `error` is an empty string on success.

```python
client = mcp.Client("https://api.example.com/mcp")

results = client.call_tools_parallel([
    {"name": "search", "arguments": {"query": "golang"}},
    {"name": "weather", "arguments": {"city": "London"}},
])

for r in results:
    if r.error:
        print(f"{r.name} failed: {r.error}")
    else:
        print(f"{r.name}: {r.result}")
```

### `client.execute_discovered(name, arguments)`

Executes a tool by name using the `execute_tool` MCP tool. This is the only way to call tools that were discovered via `tool_search()`.

**Parameters:**

- `name` (`str`): Tool name to execute.
- `arguments` (`dict`): Tool arguments.

**Returns:** `dict`: tool response.

```python
client = mcp.Client("https://api.example.com/mcp")

# First search for tools
results = client.tool_search("weather")
if results:
    # Then execute a discovered tool
    result = client.execute_discovered(results[0].name, {
        "location": "San Francisco"
    })
    print(result)
```

### `client.execute_discovered_parallel(calls)`

Executes multiple discovered tools concurrently and returns results in the same order as the input.

**Parameters:**

- `calls` (`list`): List of dicts, each with `name` (`str`) and `arguments` (`dict`) keys.

**Returns:** `list`: result dicts with `name`, `result`, and `error` keys. `error` is an empty string on success.

```python
client = mcp.Client("https://api.example.com/mcp")

results = client.execute_discovered_parallel([
    {"name": "tool_a", "arguments": {"x": 1}},
    {"name": "tool_b", "arguments": {"y": 2}},
])

for r in results:
    if r.error:
        print(f"{r.name} failed: {r.error}")
    else:
        print(f"{r.name}: {r.result}")
```

## Authentication

```python
import scriptling.mcp as mcp

# Bearer token only
client = mcp.Client(
    "https://api.example.com/mcp",
    bearer_token="your-api-token"
)

# Namespace and bearer token can be in any order
client = mcp.Client(
    "https://api.example.com/mcp",
    namespace="myservice",
    bearer_token="your-api-token"
)

# No authentication
client = mcp.Client("https://public-api.example.com/mcp")
```

## Tool Schema

Tools may include an input schema defining their parameters, and an output schema describing the response structure:

```python
client = mcp.Client("https://api.example.com/mcp")
tools = client.tools()

for tool in tools:
    if tool.name == "search":
        schema = tool.inputSchema
        # Example schema:
        # {
        #     "type": "object",
        #     "properties": {
        #         "query": {"type": "string"},
        #         "limit": {"type": "integer"}
        #     },
        #     "required": ["query"]
        # }
        if "output_schema" in tool:
            print(f"Output schema: {tool.output_schema}")
```

## Using MCP Tools with AI

MCP servers can be configured during AI client creation using the `remote_servers` parameter. This allows AI models to automatically call MCP tools during completions.

```python
import scriptling.ai as ai
import scriptling.mcp as mcp

# Create AI client with MCP servers configured
ai_client = ai.Client("http://127.0.0.1:1234/v1", remote_servers=[
    {"base_url": "http://127.0.0.1:8080/mcp", "namespace": "scriptling"},
])

# AI can now automatically use tools from the MCP server
response = ai_client.completion(
    "gpt-4",
    [{"role": "user", "content": "Calculate 15 + 27 using the execute_code tool"}]
)
print(response.choices[0].message.content)
```

You can use both an MCP client and an AI client together: one for direct tool access and one for AI completions:

```python
# Create MCP client for direct tool access
mcp_client = mcp.Client("http://127.0.0.1:8080/mcp", namespace="scriptling")

tools = mcp_client.tools()
print(f"Available tools: {len(tools)}")
for tool in tools:
    print(f"  - {tool.name}: {tool.description}")
```

When using MCP tools with AI, tools are prefixed with the namespace: with `namespace="scriptling"`, tools become `scriptling/tool_name`:

```python
ai_client = ai.Client("http://127.0.0.1:1234/v1", remote_servers=[
    {"base_url": "http://127.0.0.1:8080/mcp", "namespace": "scriptling"},
])

response = ai_client.completion(
    "gpt-4",
    [{"role": "user", "content": "Use scriptling/execute_code to calculate 15 + 27"}]
)
```

You can configure multiple MCP servers for the AI client:

```python
ai_client = ai.Client("http://127.0.0.1:1234/v1", remote_servers=[
    {"base_url": "http://127.0.0.1:8080/mcp", "namespace": "scriptling"},
    {"base_url": "http://127.0.0.1:8081/mcp", "namespace": "database"},
    {"base_url": "https://api.example.com/mcp", "namespace": "search", "bearer_token": "secret"},
])
```

## Error Handling

```python
import scriptling.mcp as mcp

try:
    client = mcp.Client("https://api.example.com/mcp")
    result = client.call_tool("search", {"query": "golang"})
    print(result)
except Exception as e:
    print("Tool execution failed:", e)
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.mcp` makes outbound network connections to MCP servers (and via `client.call_tool()`, executes whatever tools that server exposes). The trust boundary is the MCP server itself: a malicious or compromised server can expose tools that do anything its own implementation allows. For a full risk breakdown, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.mcp.tool](../tool/): Helper library for authoring MCP tools
- [scriptling.ai](../../ai/): AI client and completion functions
- [scriptling.ai.agent](../../ai/agent/): Building AI agents with automatic tool execution
