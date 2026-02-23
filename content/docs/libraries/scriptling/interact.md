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

When `interact()` is called it creates a `console.Console()` instance internally (or uses one you provide), registers commands and handlers, then calls `c.run()` to start the TUI event loop.

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

## Passing a pre-configured Console

You can create a `Console` instance yourself and pass it to `interact()`. This lets you add a welcome message, set status, or configure the console before the event loop starts:

```python
import scriptling.console as console
import scriptling.ai.agent.interact as agent

c = console.Console()
c.set_status("MyApp", "v1.0")
c.add_message(
    c.styled(console.PRIMARY, "MyApp") + " — type your requests.\n" +
    c.styled(console.DIM, "Type '/exit' to quit.")
)

bot = agent.Agent(client, model="gpt-4o", system_prompt="You are helpful.")
bot.interact(c)
```

If no console is passed, `interact()` creates one automatically.

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

- [scriptling.ai](ai/) - AI client and tool registry
- [scriptling.ai.agent](agent/) - Agent class and tool execution
- [scriptling.console](console/) - Console TUI library
