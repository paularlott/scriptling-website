---
title: Agent Library
weight: 1
---


Agentic AI loop for building AI agents with automatic tool execution. The agent handles the complete agentic loop including tool calling, execution, and response formatting.

## Available Classes & Methods

| Class/Method                                 | Description                          |
| -------------------------------------------- | ------------------------------------ |
| `Agent(client, tools, system_prompt, model)` | Create AI agent                      |
| `agent.trigger(message, max_iterations)`     | One-shot trigger with response       |
| `agent.interact()`                           | Start interactive session            |

For tool registry documentation, see [AI Library](ai.md#tool-registry).

## Quick Start

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

# Create AI client
client = ai.Client("http://127.0.0.1:1234/v1", api_key="sk-...")

# Create tool registry
tools = ai.ToolRegistry()
tools.add("read_file", "Read a file", {"path": "string"}, lambda args: os.read_file(args["path"]))

# Create agent
bot = agent.Agent(client, tools=tools, system_prompt="You are a helpful assistant", model="gpt-4")

# One-shot trigger
response = bot.trigger("What files are in the current directory?", max_iterations=10)
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
tools.add("read", "Read file", {"path": "string"}, read_func)

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
response = bot.trigger("List all Python files", max_iterations=10)
print(response.content)

# With message dict
response = bot.trigger({
    "role": "user",
    "content": "Read config.json"
}, max_iterations=5)
```

### agent.interact()

Runs an interactive CLI session. Requires `scriptling.console` library.

**Features:**

- Reads user input from stdin
- Displays thinking blocks in purple (from `<think>...</think>` tags)
- Strips thinking markers from final output
- Supports commands:
  - `/q` or `exit` - Quit
  - `/c` - Clear conversation history

**Example:**

```python
bot = agent.Agent(client, tools=tools, system_prompt="Coding assistant")
bot.interact()
```

**Output:**

```
────────────────────────────────────────────────────────────────────────────────
❯ List all Python files
────────────────────────────────────────────────────────────────────────────────

Let me search for Python files...

⏺ Found 3 Python files:
- main.py
- utils.py
- test.py

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

def read_file(args):
    content = os.read_file(args["path"])
    lines = content.split("\n")
    offset = args.get("offset", 0)
    limit = args.get("limit", len(lines))
    return "\n".join(lines[offset:offset+limit])

def write_file(args):
    os.write_file(args["path"], args["content"])
    return "ok"

tools.add("read", "Read file with optional offset/limit", {
    "path": "string",
    "offset": "integer?",
    "limit": "integer?"
}, read_file)

tools.add("write", "Write content to file", {
    "path": "string",
    "content": "string"
}, write_file)

# Create agent
bot = agent.Agent(
    client,
    tools=tools,
    system_prompt="Concise coding assistant. cwd: " + os.getcwd(),
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
def read_file_safe(args):
    try:
        return os.read_file(args["path"])
    except Exception as e:
        return f"Error: {e}"

# Handler that returns structured data
def list_files(args):
    files = os.listdir(args.get("path", "."))
    return "\n".join(files)
```

## Thinking Blocks

The agent automatically handles `<think>...</think>` blocks:

- **In `trigger()`**: Strips thinking blocks from responses
- **In `interact()`**: Displays thinking in purple, then strips from final output

This allows models to show their reasoning process in interactive mode while keeping programmatic responses clean.

**Example model output:**

```
<think>
The user wants to list Python files. I should use the glob tool to search for *.py files.
</think>

I'll search for Python files in the current directory.
```

**Interactive display:**

```
The user wants to list Python files. I should use the glob tool to search for *.py files.

⏺ I'll search for Python files in the current directory.
```

**Programmatic response:**

```python
response = bot.trigger("List Python files")
print(response.content)  # "I'll search for Python files in the current directory."
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
