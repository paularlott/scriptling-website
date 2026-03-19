---
title: AI & LLM
description: AI and LLM integration libraries for building intelligent agents.
weight: 1
---

Libraries for interacting with AI/LLM APIs and building intelligent agents with automatic tool execution.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.ai](ai/) | AI and LLM functions for OpenAI-compatible APIs |
| [scriptling.ai.agent](agent/) | Agentic AI loop with automatic tool execution |
| [scriptling.ai.agent.interact](interact/) | Interactive terminal interface for AI agents |
| [scriptling.ai.memory](memory/) | Long-term memory store for AI agents |

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
print(response.content)
```
