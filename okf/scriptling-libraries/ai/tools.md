---
description: Tool schema builder for AI agents.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/ai/tools/
sources:
    - resource: https://scriptling.dev/reference/libraries/ai/tools/
status: stable
tags:
    - libraries
    - ai
    - agents
title: scriptling.ai.tools
type: API Reference
---
# scriptling.ai.tools

Builds OpenAI-compatible tool schemas from Scriptling functions, so an AI agent can discover and call them. The library exposes the `Registry` class: construct one with `tools.Registry()` (or `ai.ToolRegistry()`, the re-export most scripts use, see [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/ai.md)), then register tools and build schemas to pass to a completion request or an `Agent`.

## Availability

The standalone `scriptling.ai.tools` import is conditionally registered and is not added by normal CLI setup. When `scriptling.ai` is available, prefer its `ai.ToolRegistry()` re-export, which provides the same class without requiring the standalone namespace. Embedders that need `import scriptling.ai.tools` must register that library explicitly.

## Available Functions

| Function | Description |
|----------|-------------|
| `Registry()` | Create a tool registry for building schemas |

## Registry Methods

| Method | Description |
|--------|-------------|
| `add(name, description, params, handler)` | Register a tool. |
| `build()` | Build OpenAI-compatible tool schemas from the registered tools. |
| `get_handler(name)` | Get the handler function for a registered tool. |

## Functions

### `Registry()`

Creates a new, empty `Registry` instance.

**Returns:** `Registry`: a new registry instance.

```python
import scriptling.ai.tools as tools

registry = tools.Registry()

# Same class, re-exported by scriptling.ai:
import scriptling.ai as ai
registry = ai.ToolRegistry()
```

### `registry.add(name, description, params, handler)`

Registers a tool with the registry. Parameter types are validated immediately, so an unknown type raises an error at `add()` time rather than at `build()` time.

**Parameters:**
- `name` (`str`): Tool name.
- `description` (`str`): Tool description, shown to the model.
- `params` (`dict`): Parameter definitions, mapping each parameter name to a type string. Accepted types: `string`, `integer`, `number`, `boolean`, `array`, `object`. Aliases: `int` for `integer`, `float` for `number`, `str` for `string`, `bool` for `boolean`, `dict` for `object`, `list` for `array`. Append `?` to mark a parameter optional (e.g. `"string?"`).
- `handler` (`callable`): Function executed when the tool is called. It receives the decoded arguments as a `dict`.

**Returns:** `None`.

**Raises:** `Error`: if a parameter type is not one of the accepted types or aliases.

```python
import scriptling.ai.tools as tools

registry = tools.Registry()

registry.add("read_file", "Read a file", {"path": "string", "limit": "int?"}, read_file)
registry.add("search", "Search files", {"query": "string", "max_results": "int?"}, search_files)
```

### `registry.build()`

Builds OpenAI-compatible tool schemas from the tools registered via `add()`. The result is suitable to pass directly to a client completion request's `tools` argument, or to an `Agent` via its `tools=` argument.

**Returns:** `list`: a list of tool schema `dict` values, each with `type`, `function.name`, `function.description`, and a JSON-Schema `function.parameters` object (with `required` derived from which parameters were marked optional).

```python
import scriptling.ai as ai

registry = ai.ToolRegistry()
registry.add("get_time", "Get current time", {}, lambda args: "12:00 PM")

schemas = registry.build()

# Pass to a completion request
client = ai.Client("http://127.0.0.1:1234/v1")
response = client.completion("gpt-4", "What time is it?", tools=schemas)
```

### `registry.get_handler(name)`

Returns the handler function registered for a tool. This is how `Agent` and `ai.execute_tool_calls` look up the function to run for a model-emitted tool call.

**Parameters:**
- `name` (`str`): Tool name.

**Returns:** `callable`: the handler function.

**Raises:** `Error`: if no tool with that name is registered.

```python
handler = registry.get_handler("read_file")
result = handler({"path": "/etc/hostname"})
```

## See Also

- [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/ai.md): re-exports the class as `ai.ToolRegistry`, plus completion helpers and `execute_tool_calls`.
- [scriptling.ai.agent](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md): the `Agent` class consumes a `Registry` via its `tools=` argument.
- [scriptling.mcp.tool](https://scriptling.dev/okf/scriptling-libraries/mcp/tool.md): building tools for the MCP protocol instead of direct LLM APIs.
