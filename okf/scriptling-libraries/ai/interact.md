---
description: Interactive terminal interface for conversing with AI agents via a REPL-style loop.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/ai/interact/
sources:
    - resource: https://scriptling.dev/reference/libraries/ai/interact/
status: stable
tags:
    - libraries
    - ai
    - agents
title: scriptling.ai.agent.interact
type: API Reference
---
# scriptling.ai.agent.interact

Interactive terminal interface for AI agents. This library extends the `Agent` class with an `interact()` method that provides a REPL-like interface for conversing with AI agents using the TUI console.

## Availability

CLI registration is mode-dependent: the ordinary non-server CLI execution path adds `scriptling.ai.agent.interact`, while evaluator factories and server-style execution do not add it automatically. Embedders must register it explicitly, together with `scriptling.console`. Importing `scriptling.ai.agent` alone does not provide `interact()`.

## Available Functions

| Function | Description |
|----------|-------------|
| `agent.interact(max_iterations=25)` | Added to the `Agent` class: starts an interactive TUI session |

Importing `scriptling.ai.agent.interact` enhances the `scriptling.ai.agent.Agent` class with an `interact()` method; it does not add any standalone module-level functions of its own.

## Overview

After importing, your `Agent` instances gain an additional `interact()` method. When `interact()` is called it uses the shared console singleton, registers commands and handlers, then calls `console.run()` to start the TUI event loop.

During each turn, the interactive loop:

- Streams reasoning and assistant text into the main panel as it arrives.
- Keeps the spinner running until the turn is fully complete.
- Shows tool call and result messages with status and preview.
- Uses `ai.collect_stream()` for streaming with configurable timeouts.
- Preserves conversation state for follow-up requests.

## Functions

### `agent.interact(max_iterations=25)`

Runs an interactive CLI session for the agent. Requires `scriptling.console` to be registered, and is designed for use with the scriptling CLI.

**Parameters:**

- `max_iterations` (`int`, optional): Maximum number of tool call rounds per user message. Prevents infinite loops if the agent gets stuck. Default: `25`.

**Returns:** `None`

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.agent.interact  # Adds interact() to Agent

client = ai.Client("https://api.openai.com/v1", api_key="your-key")

my_agent = agent.Agent(
    client=client,
    model="gpt-4",
    system_prompt="You are a helpful assistant."
)

# Start interactive session
my_agent.interact()

# Custom limit for complex tasks
my_agent.interact(max_iterations=50)
```

When the iteration limit is reached, a message is displayed:

```
[Reached max iterations (25). Type 'continue' or ask me to proceed.]
```

You can then type "continue" or ask the agent to proceed, and it will continue from where it left off.

## Pre-configuring the Console

You can set up the console before calling `interact()` using module-level functions from `scriptling.console`:

```python
import scriptling.console as console
import scriptling.ai.agent.interact as agent

console.set_status("MyApp", "v1.0")
main = console.main_panel()
main.add_message(
    console.styled(console.PRIMARY, "MyApp") + ": type your requests.\n" +
    console.styled(console.DIM, "Type '/exit' to quit.")
)

bot = agent.Agent(client, model="gpt-4o", system_prompt="You are helpful.")
bot.interact()
```

The console is a singleton, so any configuration applied before `interact()` will be preserved.

## Interactive Commands

Commands are registered with the TUI palette when `interact()` is called. Type `/` to open the command palette.

| Command | Description |
|---------|-------------|
| `/clear` | Clear conversation history and screen |
| `/model <name>` | Switch model (`none` to reset to default) |
| `/history` | Show conversation history |
| `/exit` | Exit (registered by the CLI) |
| Esc | Cancel the current request |

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.ai.agent.interact` inherits the network and agentic-execution risk of `scriptling.ai.agent`: it streams completions from the configured AI provider and runs the same tool-calling loop, just with a terminal UI on top. Never register it for untrusted code. See [Security Considerations](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md#security-considerations) on the `ai.agent` page, the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#library-security), and [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#ai--agent).

## See Also

- [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/ai.md): AI client and tool registry
- [scriptling.ai.agent](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md): Agent class and tool execution
- [scriptling.console](https://scriptling.dev/okf/scriptling-libraries/utilities/console.md): Console TUI library
