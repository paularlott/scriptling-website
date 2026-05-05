---
title: scriptling.ai.agent
linkTitle: ai.agent
weight: 1
---

Agentic AI loop for building AI agents with automatic tool execution. The agent handles the complete agentic loop including tool calling, execution, and response formatting.

## Available Classes & Methods

| Class/Method | Description |
| --- | --- |
| `Agent(client, tools, system_prompt, model, memory, max_tokens, compaction_threshold, request_timeout, extra_body)` | Create AI agent |
| `agent.trigger(message, max_iterations)` | One-shot trigger with response |
| `agent.interact(max_iterations)` | Start interactive session |
| `agent.get_messages()` | Get conversation history |
| `agent.set_messages(messages)` | Set conversation history |

For tool registry documentation, see [AI Library](./#tool-registry).

## Quick Start

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

# Create AI client
client = ai.Client("http://127.0.0.1:1234/v1")

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

### Agent(client, tools=None, system_prompt="", model="", memory=None, max_tokens=32000, compaction_threshold=80, request_timeout=300, extra_body=None)

Creates an AI agent with automatic tool execution.

**Parameters:**

- `client` (AIClient): AI client instance from `ai.Client()`
- `tools` (ToolRegistry, optional): Tool registry with available tools
- `system_prompt` (str, optional): System prompt for the agent
- `model` (str, optional): Model to use
- `memory` (memory object, optional): Memory store from `memory.new()` — see [Memory Integration](#memory-integration)
- `max_tokens` (int, optional): Maximum token budget for the conversation. When estimated token usage reaches the compaction threshold, the conversation history is automatically compacted (summarized). Default: 32000
- `compaction_threshold` (int, optional): Percentage of `max_tokens` at which auto-compaction triggers (0-100). For example, with `max_tokens=32000` and `compaction_threshold=80`, compaction triggers at ~25600 tokens. Default: 80
- `request_timeout` (int, optional): Timeout in seconds for each LLM completion request. LLM calls can be slow, especially with tool-calling loops or large contexts. Default: 300
- `extra_body` (dict, optional): Provider-specific fields to merge into every request body

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

# With custom compaction settings (compact at 50% of 16k tokens)
bot = agent.Agent(
    client,
    tools=tools,
    max_tokens=16000,
    compaction_threshold=50
)

# With provider-specific request body fields
bot = agent.Agent(
    client,
    tools=tools,
    model="glm-4.7",
    extra_body={
        "thinking": {
            "type": "enabled",
            "clear_thinking": False
        }
    }
)
```

### agent.trigger(message, max_iterations=1)

Processes a message with the agent, executing tools as needed.

**Parameters:**

- `message` (str or dict): User message to process
- `max_iterations` (int): Maximum tool call rounds (default: 1)

**Returns:** dict — agent's response message

**Behavior:**

- Strips `<think>...</think>` blocks from responses
- Executes tools automatically
- Maintains conversation history
- Uses configurable request timeout (default: 300 seconds) for LLM calls
- Stops after max_iterations or when no more tool calls

**Example:**

```python
response = bot.trigger("What is 2+2?")
print(response.content)

response = bot.trigger("Reverse the word 'hello'", max_iterations=10)
print(response.content)
```

### agent.interact(max_iterations=25)

Runs an interactive CLI session. Requires `scriptling.console` library.

**Parameters:**

- `max_iterations` (int, optional): Maximum tool call rounds per message. Default: 25

**Behavior:**

- Streams reasoning and assistant text into the main console panel as it arrives
- Keeps the spinner active for the full request lifecycle
- Shows tool call and result messages with status and preview
- Uses streaming via `ai.collect_stream()` with configurable timeouts
- Preserves conversation history between turns

**Example:**

```python
bot = agent.Agent(client, tools=tools, system_prompt="Coding assistant")
bot.interact()
```

### agent.get_messages() / set_messages(messages)

Get or replace the conversation history.

```python
messages = bot.get_messages()
bot.set_messages([
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"},
])
```

## Memory Integration

Pass a memory store to `Agent` via the `memory=` kwarg. The agent automatically:

1. Registers `memory_remember`, `memory_recall`, and `memory_forget` as tools
2. Appends memory usage instructions to the system prompt
3. Pre-loads all stored `preference` memories into the system prompt so the LLM has immediate context on the first message without a tool call round-trip

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.memory as memory
import scriptling.runtime.kv as kv

client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"))

bot = agent.Agent(
    client,
    model="gpt-4",
    system_prompt="You are a helpful assistant.",
    memory=mem
)

bot.interact()
```

You can combine `memory=` with your own tools — the memory tools are added to the existing registry:

```python
tools = ai.ToolRegistry()
tools.add("search", "Search the web", {"query": "string"}, search_handler)

bot = agent.Agent(client, tools=tools, memory=mem, model="gpt-4")
# bot.tool_schemas now contains: search, memory_remember, memory_recall, memory_forget
```

### Memory Tools

When `memory=` is provided, the following tools are registered automatically:

| Tool | Parameters | Description |
|------|-----------|-------------|
| `memory_remember` | `content`, `type?`, `importance?` | Store a fact, preference, event or note |
| `memory_recall` | `query?`, `limit?`, `type?` | Search memories by keyword; omit query for recent context |
| `memory_forget` | `id` | Remove a memory by ID |

### System Prompt Augmentation

The agent appends a `## Memory` block to the system prompt explaining when and how to use the memory tools. It also injects a `## Remembered Preferences` block containing all stored `preference` memories, so the LLM has user preferences available immediately.

The original `system_prompt` you pass is always preserved — the memory content is appended after it.

## Auto-Compaction

The agent automatically compacts conversation history when it grows too large, preventing context window overflow and reducing API costs.

**How it works:**

1. Before each completion call, the agent estimates the token count of the current messages
2. If the estimated tokens reach the compaction threshold (percentage of `max_tokens`), the conversation is compacted
3. Compaction asks the AI to summarize the conversation so far, preserving key facts and context
4. The history is rebuilt as: system prompt + summary + protected recent context
5. Active tool rounds are preserved so assistant tool calls remain paired with their tool results
6. The agent continues normally with the compacted history

**Parameters:**

- `max_tokens` (int): Maximum token budget. Default: 32000
- `compaction_threshold` (int): Percentage of `max_tokens` at which compaction triggers. Default: 80

**Example:**

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

client = ai.Client("http://127.0.0.1:1234/v1")

# Default: compact at 80% of 32000 tokens (25600 tokens)
bot = agent.Agent(client, model="gpt-4")

# Custom: compact at 50% of 16000 tokens (8000 tokens)
bot = agent.Agent(client, model="gpt-4", max_tokens=16000, compaction_threshold=50)
```

**Note:** Set `max_tokens=0` or `compaction_threshold=0` to disable auto-compaction entirely.

### With LLM-based Deduplication

Pass an AI client to `memory.new()` to enable intelligent deduplication. When similar memories are found during `remember()` or `compact()`, the LLM decides whether to merge them or keep them separate:

```python
client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"), ai_client=client, model="qwen3-8b")

bot = agent.Agent(client, model="qwen3-8b", memory=mem)
```

Without an AI client, deduplication is rule-based only (MinHash similarity ≥ 85% auto-merges, otherwise keeps separate).

See [ai.memory](../ai-memory/) for full memory store documentation.

## Complete Example

```python
#!/usr/bin/env scriptling
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.memory as memory
import scriptling.runtime.kv as kv
import os

client = ai.Client("http://127.0.0.1:1234/v1", api_key=os.getenv("OPENAI_API_KEY", ""))

# Tools
tools = ai.ToolRegistry()
tools.add("sqrt", "Calculate square root", {"number": "number"}, lambda args: str(args["number"] ** 0.5))
tools.add("reverse", "Reverse a text string", {"text": "string"}, lambda args: args["text"][::-1])

# Memory
mem = memory.new(kv.open("./memory-db"))

# Agent with tools and memory
bot = agent.Agent(
    client,
    tools=tools,
    memory=mem,
    system_prompt="You are a helpful math and text assistant.",
    model="gpt-4"
)

bot.interact()
```

## Tool Handler Interface

Tool handlers receive a dict of arguments and can return any value — complex types are automatically JSON-encoded for the LLM.

```python
def get_time(args):
    import datetime
    return str(datetime.datetime.now())

def calculate_safe(args):
    try:
        import math
        return str(math.sqrt(args["number"]))
    except ValueError as e:
        return f"Error: {e}"
```

## Thinking Blocks

The agent automatically handles `<think>...</think>` blocks:

- In `trigger()`: strips thinking blocks from responses
- In `interact()`: displays thinking in purple, then strips from final output

### Manual Extraction

```python
import scriptling.ai as ai

result = ai.extract_thinking(response_text)
thinking_blocks = result["thinking"]
clean_content = result["content"]
```

## See Also

- [AI Library](./) — AI client and completion functions
- [ai.memory](memory/) — Long-term memory store
- [ai.agent.interact](interact/) — Interactive terminal session
