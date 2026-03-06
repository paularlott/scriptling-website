---
title: scriptling.ai.agent
linkTitle: ai.agent
weight: 1
---

Agentic AI loop for building AI agents with automatic tool execution. The agent handles the complete agentic loop including tool calling, execution, and response formatting.

## Available Classes & Methods

| Class/Method                                 | Description                    |
| -------------------------------------------- | ------------------------------ |
| `Agent(client, tools, system_prompt, model)` | Create AI agent                |
| `agent.trigger(message, max_iterations)`     | One-shot trigger with response |
| `agent.interact(c, max_iterations)`          | Start interactive session      |

For tool registry documentation, see [AI Library](ai.md#tool-registry).

## Quick Start

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

# Create AI client
client = ai.Client("http://127.0.0.1:1234/v1", api_key="sk-...")

# Create tool registry
tools = ai.ToolRegistry()
tools.add("calculate", "Calculate square root", {"number": "number"}, lambda args: str(args["number"] ** 0.5))

# Create agent
bot = agent.Agent(client, tools=tools, system_prompt="You are a helpful assistant", model="gpt-4")

# One-shot trigger
response = bot.trigger("What is the square root of 144?", max_iterations=10)
print(response.content)

# Interactive session (requires scriptling.console)
bot.interact()
```

## Agent Class

### agent.Agent(client, tools=None, system_prompt="", model="")

Creates an AI agent with automatic tool execution.

**Parameters:**

- `client` (AIClient): AI client instance (from `ai.Client()`)
- `tools` (ToolRegistry, optional): Tool registry with available tools
- `system_prompt` (str, optional): System prompt for the agent
- `model` (str, optional): Model to use (if not provided, client must handle model selection)

**Example:**

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

client = ai.Client("http://127.0.0.1:1234/v1")
tools = ai.ToolRegistry()
tools.add("reverse", "Reverse text", {"text": "string"}, lambda args: args["text"][::-1])

bot = agent.Agent(
    client,
    tools=tools,
    system_prompt="You are a coding assistant",
    model="gpt-4"
)
```

### agent.trigger(message, max_iterations=1)

Processes a message with the agent, executing tools as needed.

**Parameters:**

- `message` (str or dict): User message to process
- `max_iterations` (int): Maximum tool call rounds (default: 1)

**Returns:** dict - Agent's response message

**Behavior:**

- Strips `<think>...</think>` blocks from responses (for non-interactive use)
- Executes tools automatically
- Maintains conversation history
- Stops after max_iterations or when no more tool calls

**Example:**

```python
# Simple query (no tools)
response = bot.trigger("What is 2+2?")
print(response.content)  # "4"

# Query that uses tools
response = bot.trigger("Reverse the word 'hello'", max_iterations=10)
print(response.content)

# With message dict
response = bot.trigger({
    "role": "user",
    "content": "Calculate the square root of 81"
}, max_iterations=5)
print(response.content)
```

### agent.interact(c=None, max_iterations=25)

Runs an interactive CLI session. Requires `scriptling.console` library.

**Parameters:**

- `c` (Console, optional): Pre-configured console instance
- `max_iterations` (int, optional): Maximum tool call rounds per message. Default: 25

**Features:**

- Reads user input from stdin
- Displays thinking blocks in purple (from `<think>...</think>` tags)
- Strips thinking markers from final output
- Shows warning when iteration limit is reached
- Supports commands:
  - `/q` or `exit` - Quit
  - `/c` - Clear conversation history

**Example:**

```python
bot = agent.Agent(client, tools=tools, system_prompt="Coding assistant")
bot.interact()  # Default: 25 iterations

# With custom iteration limit
bot.interact(max_iterations=50)
```

**Output:**

```
────────────────────────────────────────────────────────────────────────────────
❯ Reverse the word 'greeting'
────────────────────────────────────────────────────────────────────────────────

Let me reverse that text for you...

⏺ The reversed text is: gniteerg

────────────────────────────────────────────────────────────────────────────────
❯ /q
```

### agent.get_messages()

Gets the current conversation history.

**Returns:** list - List of message dicts

**Example:**

```python
messages = bot.get_messages()
for msg in messages:
    print(f"{msg['role']}: {msg.get('content', '')}")
```

### agent.set_messages(messages)

Sets the conversation history.

**Parameters:**

- `messages` (list): List of message dicts

**Example:**

```python
# Start with existing conversation
bot.set_messages([
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
])

response = bot.trigger("What's the weather?")
```

## Complete Example

```python
#!/usr/bin/env scriptling
import scriptling.ai as ai
import scriptling.ai.agent as agent
import os

# Create AI client
client = ai.Client("http://127.0.0.1:1234/v1", api_key=os.getenv("OPENAI_API_KEY", ""))

# Create tools
tools = ai.ToolRegistry()

def calculate(args):
    """Calculate square root of a number."""
    import math
    return str(math.sqrt(args["number"]))

def reverse_text(args):
    """Reverse a string."""
    return args["text"][::-1]

def word_count(args):
    """Count words in text."""
    return str(len(args["text"].split()))

tools.add("sqrt", "Calculate square root of a number", {
    "number": "number"
}, calculate)

tools.add("reverse", "Reverse a text string", {
    "text": "string"
}, reverse_text)

tools.add("wordcount", "Count words in text", {
    "text": "string"
}, word_count)

# Create agent
bot = agent.Agent(
    client,
    tools=tools,
    system_prompt="You are a helpful math and text assistant.",
    model="gpt-4"
)

# Interactive session
bot.interact()
```

## Tool Handler Interface

Tool handlers receive a dict of arguments and can:

1. **Return values** - Automatically converted to strings for the AI
2. **Return None** - Treated as empty response
3. **Raise exceptions** - Caught and returned as error messages

```python
# Simple handler
def get_time(args):
    import datetime
    return str(datetime.datetime.now())

# Handler with error handling
def calculate_safe(args):
    try:
        import math
        return str(math.sqrt(args["number"]))
    except ValueError as e:
        return f"Error: {e}"
    except KeyError:
        return "Error: 'number' parameter required"

# Handler that returns structured data
def analyze_text(args):
    text = args.get("text", "")
    return f"Characters: {len(text)}, Words: {len(text.split())}"
```

## Thinking Blocks

The agent automatically handles `<think>...</think>` blocks:

- **In `trigger()`**: Strips thinking blocks from responses
- **In `interact()`**: Displays thinking in purple, then strips from final output

This allows models to show their reasoning process in interactive mode while keeping programmatic responses clean.

**Example model output:**

```
<think>
The user wants to reverse the word 'hello'. I should use the reverse tool to flip the text.
</think>

I'll reverse that text for you.
```

**Interactive display:**

```
The user wants to reverse the word 'hello'. I should use the reverse tool to flip the text.

⏺ I'll reverse that text for you.
```

**Programmatic response:**

```python
response = bot.trigger("Reverse 'hello'")
print(response.content)  # "I'll reverse that text for you."
```

### Manual Extraction

For cases where you need to manually extract thinking blocks from AI responses (e.g., when not using the agent), use the `ai.extract_thinking()` function from the [AI Library](ai.md#thinking-extractor). This function supports multiple thinking block formats including `<think>`, `<thinking>`, `<Thought>`, `<antThinking>`, and markdown code blocks.

```python
import scriptling.ai as ai

result = ai.extract_thinking(response_text)
thinking_blocks = result["thinking"]  # List of extracted blocks
clean_content = result["content"]     # Text with thinking blocks removed
```

## See Also

- [AI Library](ai.md) - AI client and completion functions
- [Thinking Extractor](ai.md#thinking-extractor) - Manual thinking block extraction
- [scriptlingcoder example](../../examples/openai/scriptlingcoder/) - Complete AI coding assistant
