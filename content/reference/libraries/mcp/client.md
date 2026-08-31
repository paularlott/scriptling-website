---
title: scriptling.mcp
linkTitle: mcp
description: MCP client library for connecting to MCP servers and invoking the tools they expose.
tags: [libraries, mcp]
weight: 1

aliases:
  - /reference/libraries/scriptling/mcp/client/
---

MCP (Model Context Protocol) client library. This library provides functions for connecting to MCP servers and interacting with the tools they expose for AI models to use.

For MCP integration with AI clients, see the `remote_servers` parameter on [scriptling.ai.Client](../../ai/client/).

## Available Functions

| Function | Description |
|----------|-------------|
| `decode_response(response)` | Decode a raw MCP tool response |
| `Client(target, **kwargs)` | Create an MCP client over HTTP or stdio |

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
| `client.list_resources()` | List resources exposed by the server |
| `client.list_resource_templates()` | List resource templates (URIs with `{var}` placeholders) |
| `client.read_resource(uri)` | Read a resource by URI (static or expanded from a template) |
| `client.list_prompts()` | List prompts exposed by the server |
| `client.get_prompt(name, arguments)` | Render a prompt by name into messages |
| `client.close()` | Close the client (shuts a stdio subprocess down) |

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

### `mcp.Client(target, **kwargs)`

Creates a new MCP client. The transport is chosen from `target`: an `http://` or
`https://` URL connects over **HTTP**; any other value is treated as a local
executable that is launched as a **stdio** MCP server subprocess.

**Parameters:**

- `target` (`str`): HTTP(S) URL of the server, or the path/command of a stdio server.
- `namespace` (`str`, optional): Namespace for tool names (e.g. `"scriptling"` makes tools available as `"scriptling__tool_name"`). Default: `""`.
- `bearer_token` (`str`, optional): Bearer token for authentication. **HTTP only.** Default: `""`.
- `args` (`list`, optional): Command-line arguments for the stdio server. **stdio only.**
- `env` (`list`, optional): Extra `KEY=value` environment variables for the stdio subprocess. **stdio only.** Merged on top of the inherited environment, so `PATH`, `HOME`, etc. are preserved.

Passing `args` or `env` with an HTTP URL, or `bearer_token` with a command, raises an error.

**Returns:** `MCPClient`: a client instance with methods for interacting with the server.

```python
import scriptling.mcp as mcp

# HTTP server
client = mcp.Client("https://api.example.com/mcp", namespace="scriptling", bearer_token="your-token-here")

# stdio server: launch a local executable as a subprocess
client = mcp.Client("/usr/local/bin/thebinary", args=["--server"], namespace="t1")

# stdio server with extra environment variables (merged on top of the inherited env)
client = mcp.Client("npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/data"], env=["FS_ROOT=/data", "LOG_LEVEL=debug"])

# Scriptling itself can be a stdio MCP server
client = mcp.Client("scriptling", args=["--mcp-exec-script"], namespace="local")
```

When using a namespace, all tool names are prefixed. For example, if the server has a tool called `execute_code` and you use namespace `scriptling`, the tool is available as `scriptling__execute_code`. The namespace is automatically added to all tool names and stripped when calling tools.

> **Close stdio clients.** A stdio client owns a subprocess; call `client.close()` when finished to shut it down. For HTTP clients `close()` is a harmless no-op.

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

## Resources and Prompts

As well as tools, an MCP server may expose **resources** (addressable data read
by URI) and **prompts** (reusable message templates rendered into messages for
the model). Scriptling's client can read both.

### `client.list_resources()`

Lists the static resources exposed by the server.

**Returns:** `list`: resource dicts with `uri`, `name`, `description`, `mimeType`.

```python
client = mcp.Client("https://api.example.com/mcp")
for res in client.list_resources():
    print(res.uri, res.name, res.mimeType)
```

### `client.list_resource_templates()`

Lists resource **templates** — URIs containing `{var}` placeholders that the
client expands before reading. Expand a template by substituting the variable
and pass the result to `read_resource`.

**Returns:** `list`: dicts with `uriTemplate`, `name`, `description`, `mimeType`.

```python
client = mcp.Client("https://api.example.com/mcp")
for t in client.list_resource_templates():
    print(t.uriTemplate, t.name)

# Expand a template and read it
data = client.read_resource("scriptling://script/greet")  # from scriptling://script/{name}
```

### `client.read_resource(uri)`

Reads a resource by URI. The URI may be a static resource or a template already
expanded by the caller.

**Parameters:**

- `uri` (`str`): The resource URI to read.

**Returns:** `dict` (single content block) or `list` of dicts. Each content dict
has `uri`, `mimeType`, and either `text` (parsed JSON if valid, else a string)
or `blob` (base64).

```python
client = mcp.Client("https://api.example.com/mcp")

data = client.read_resource("config://app")
print(data.uri, data.mimeType)
print(data.text)  # parsed JSON object, or plain string
```

### `client.list_prompts()`

Lists the prompts exposed by the server.

**Returns:** `list`: prompt dicts with `name`, `description`, and `arguments`
(each argument has `name`, `description`, `required`).

```python
client = mcp.Client("https://api.example.com/mcp")
for p in client.list_prompts():
    print(p.name, p.description)
    for a in getattr(p, "arguments", []):
        print("  -", a.name, "(required)" if a.required else "(optional)")
```

### `client.get_prompt(name, arguments)`

Renders a prompt by name with the given arguments into messages for the model.
Prompt arguments are always strings; non-string values are coerced.

**Parameters:**

- `name` (`str`): Prompt name.
- `arguments` (`dict`): Argument values.

**Returns:** `dict` with `description` and `messages` (a list of
`{role, content}` where `content` is a decoded content block).

```python
client = mcp.Client("https://api.example.com/mcp")

out = client.get_prompt("write_script", {"task": "greet a user by name"})
for m in out.messages:
    print(m.role, m.content)
```

### `client.close()`

Closes the client and releases its transport. For a **stdio** client this shuts
down the launched server subprocess; for an **HTTP** client it is a no-op. Safe
to call more than once.

**Returns:** `None`

```python
client = mcp.Client("scriptling", args=["--mcp-exec-script"], namespace="local")
try:
    result = client.call_tool("local__execute_script", {"code": "print(6 * 7)"})
    print(result)
finally:
    client.close()
```

## Stdio Servers

`mcp.Client()` can launch a local executable as an MCP server communicating over
stdin/stdout (newline-delimited JSON-RPC 2.0), the transport MCP hosts use for
local servers. Pass the command as `target` and any flags as `args`:

```python
import scriptling.mcp as mcp

# Launch a stdio MCP server subprocess
client = mcp.Client("scriptling", args=["--mcp-tools", "./tools"], namespace="tools")

for tool in client.tools():
    print(tool.name)

result = client.call_tool("tools__greet", {"name": "Ada"})
print(result)

client.close()  # shut the subprocess down
```

Pass `env` to set extra environment variables on the subprocess. Entries use the
`KEY=value` form and are merged on top of the inherited environment, so
`PATH`, `HOME`, and other defaults remain available:

```python
client = mcp.Client("npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/data"],
    env=["FS_ROOT=/data", "LOG_LEVEL=debug"],
    namespace="fs",
)
```

Scriptling can itself run as a stdio MCP server (`scriptling --mcp-exec-script`
or `--mcp-tools <dir>`, without `--server`) — see
[MCP Server Mode](../../../../docs/cli/mcp-server/).

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

`scriptling.mcp` makes outbound network connections to MCP servers (and via `client.call_tool()`, executes whatever tools that server exposes). The trust boundary is the MCP server itself: a malicious or compromised server can expose tools that do anything its own implementation allows. When `target` is a command rather than a URL, `mcp.Client()` also **launches a local subprocess** — treat the command and its arguments as trusted input, since they run with the same permissions as the interpreter. For a full risk breakdown, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.mcp.tool](../tool/): Helper library for authoring MCP tools
- [scriptling.ai](../../ai/): AI client and completion functions
- [scriptling.ai.agent](../../ai/agent/): Building AI agents with automatic tool execution
