---
title: scriptling.ai.agent.interact
linkTitle: ai.agent.interact
weight: 2
---

Interactive terminal interface for AI agents. This library extends the `Agent` class with an `interact()` method that provides a REPL-like interface for conversing with AI agents using the TUI console.

## Import

```python
import scriptling.ai.agent.interact
```

## Overview

The `interact` library enhances the `scriptling.ai.agent.Agent` class with an interactive terminal session. After importing, your Agent instances will have an additional `interact()` method.

When `interact()` is called it uses the shared console singleton, registers commands and handlers, then calls `console.run()` to start the TUI event loop.

## Usage

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.agent.interact  # Adds interact() to Agent

client = ai.client("https://api.openai.com/v1", api_key="your-key")

my_agent = agent.Agent(
    client=client,
    model="gpt-4",
    system_prompt="You are a helpful assistant."
)

# Start interactive session
my_agent.interact()
```

## Pre-configuring the console

You can set up the console before calling `interact()` using module-level functions:

```python
import scriptling.console as console
import scriptling.ai.agent.interact as agent

console.set_status("MyApp", "v1.0")
main = console.main_panel()
main.add_message(
    console.styled(console.PRIMARY, "MyApp") + " — type your requests.\n" +
    console.styled(console.DIM, "Type '/exit' to quit.")
)

bot = agent.Agent(client, model="gpt-4o", system_prompt="You are helpful.")
bot.interact()
```

The console is a singleton, so any configuration applied before `interact()` will be preserved.

## Max Iterations

The `interact()` method accepts a `max_iterations` parameter to limit the number of tool call rounds per user message. This prevents infinite loops if the agent gets stuck.

```python
# Default: 25 iterations per message
bot.interact()

# Custom limit for complex tasks
bot.interact(max_iterations=50)

# Lower limit for faster responses
bot.interact(max_iterations=10)
```

When the iteration limit is reached, a message is displayed:

```
[Reached max iterations (25). Type 'continue' or ask me to proceed.]
```

You can then type "continue" or ask the agent to proceed, and it will continue from where it left off.

## Interactive Commands

Commands are registered with the TUI palette when `interact()` is called. Type `/` to open the command palette.

| Command | Description |
|---------|-------------|
| `/clear` | Clear conversation history and screen |
| `/model <name>` | Switch model (`none` to reset to default) |
| `/history` | Show conversation history |
| `/exit` | Exit (registered by the CLI) |
| Esc | Cancel the current request |

> **Note:** `scriptling.ai.agent.interact` requires `scriptling.console` to be registered. It is designed for use with the scriptling CLI.

## See Also

- [scriptling.ai](./) - AI client and tool registry
- [scriptling.ai.agent](agent/) - Agent class and tool execution
- [scriptling.console](../console/) - Console TUI library
