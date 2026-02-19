---
title: scriptling.ai.agent.interact
linkTitle: ai.agent.interact
weight: 2
---

Interactive terminal interface for AI agents. This library extends the `Agent` class with an `interact()` method that provides a REPL-like interface for conversing with AI agents.

## Import

```python
import scriptling.ai.agent.interact
```

## Overview

The `interact` library enhances the `scriptling.ai.agent.Agent` class with an interactive terminal session. After importing, your Agent instances will have an additional `interact()` method.

## Usage

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.agent.interact  # Adds interact() to Agent

# Create client and tools
client = ai.client("https://api.openai.com/v1", api_key="your-key")

# Create agent with tools
my_agent = agent.Agent(
    client=client,
    model="gpt-4",
    system_prompt="You are a helpful assistant."
)

# Register tools
my_agent.tool("get_weather", get_weather, "Get current weather for a location")

# Start interactive session
my_agent.interact()
```

## Interactive Commands

| Command | Description |
|---------|-------------|
| `/q` or `exit` | Exit the interactive session |
| `/c` | Clear conversation history |

## Features

### Color-Coded Output

The interface uses ANSI colors for better readability:

- User prompts in blue
- AI responses in cyan
- Thinking blocks in purple
- Code blocks in gray

### Thinking Block Extraction

When the AI model outputs thinking/reasoning blocks (using `<think/>` or similar tags), they are automatically extracted and displayed separately.

### Code Formatting

Inline code and code blocks are automatically formatted with distinct colors.

## Example Session

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.agent.interact

client = ai.client("https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY"))

my_agent = agent.Agent(
    client=client,
    model="gpt-4o",
    system_prompt="You are a coding assistant. Help users write and debug code."
)

# Define tools
def run_python(code):
    # Execute code safely
    return eval_result

my_agent.tool("run_python", run_python, "Execute Python code and return the result")

# Start interactive session
my_agent.interact()
```

Session output:
```
--------------------------------------------------------------------------------
❯ Write a function to calculate fibonacci numbers
--------------------------------------------------------------------------------

⏺ Here's a recursive Fibonacci function:

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

Would you like me to test it?

--------------------------------------------------------------------------------
❯ /c
⏺ Cleared conversation

--------------------------------------------------------------------------------
❯ /q
```

## Configuration

The `interact()` method uses the following defaults:

- Maximum iterations: 20
- Conversation history is preserved until cleared with `/c`
- System prompt is re-added when conversation is cleared

## See Also

- [scriptling.ai](ai/) - AI client and tool registry
- [scriptling.ai.agent](agent/) - Agent class and tool execution
- [scriptling.console](console/) - Console I/O functions
