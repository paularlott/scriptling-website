---
description: AI integration libraries for building intelligent agents.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/ai/
sources:
    - resource: https://scriptling.dev/reference/libraries/ai/
status: stable
tags:
    - libraries
    - ai
title: AI
type: API Reference
---
# AI

Libraries for interacting with AI/LLM APIs and building intelligent agents with automatic tool execution.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/ai/ai.md) | AI and LLM functions and helpers |
| [AI Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md) | Client class reference (completion, embedding, Responses API) |
| [scriptling.ai.agent](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md) | Agentic AI loop with automatic tool execution |
| [scriptling.ai.agent.interact](https://scriptling.dev/okf/scriptling-libraries/ai/interact.md) | Interactive terminal interface for AI agents |
| [scriptling.ai.memory](https://scriptling.dev/okf/scriptling-libraries/ai/memory.md) | Long-term memory store for AI agents |
| [scriptling.ai.tools](https://scriptling.dev/okf/scriptling-libraries/ai/tools.md) | Tool schema builder for AI agents |

## Quick Start

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

# Create AI client
client = ai.Client("http://127.0.0.1:1234/v1")

# Simple completion
response = client.completion("gpt-4", "Hello!")
print(response.choices[0].message.content)

# With agent and tools
tools = ai.ToolRegistry()
tools.add("get_time", "Get current time", {}, lambda args: "12:00 PM")

bot = agent.Agent(client, tools=tools, system_prompt="You are helpful", model="gpt-4")
response = bot.trigger("What time is it?")
print(response)
```

## See Also

- [scriptling.mcp](https://scriptling.dev/okf/scriptling-libraries/./mcp.md) - MCP protocol client and tool authoring for AI agents
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#library-security) - Security guidance for AI and network-enabled libraries
