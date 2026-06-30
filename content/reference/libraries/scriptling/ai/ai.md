---
title: scriptling.ai
linkTitle: ai
weight: 1
---

AI and LLM functions for interacting with OpenAI-compatible APIs: clients, completions, embeddings, the Responses API, and tool-calling helpers for building agents.

## Submodules

- [scriptling.ai.Client](../client/): Create clients and make completions, embeddings, and Responses API calls
- [scriptling.ai.agent](../agent/): Agentic AI loop with automatic tool execution
- [scriptling.ai.agent.interact](../interact/): Interactive terminal session for agents
- [scriptling.ai.memory](../memory/): Long-term memory store for AI agents

The `scriptling.ai` namespace itself also exposes a handful of functions directly: response helpers, token estimation, vector similarity, and a `ToolRegistry` for building tool schemas (see below).

## Quick Start

```python
import scriptling.ai as ai

# Create a client and make a completion
client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "What is 2+2?")
print(response.choices[0].message.content)

# Extract text (thinking blocks stripped)
print(ai.text(response))
```

For the full client method reference (completion, streaming, parallel, embeddings, Responses API, background processing), see [scriptling.ai.Client](../client/).

## Available Functions

| Function | Description |
|----------|-------------|
| `Client(base_url, **kwargs)` | Create an AI client for API interactions: see [scriptling.ai.Client](../client/) |
| `text(response)` | Extract text content from a response |
| `thinking(response)` | Extract thinking blocks from a response |
| `extract_thinking(text)` | Extract thinking blocks from a text string |
| `tool_calls(input)` | Extract normalized tool calls |
| `execute_tool_calls(registry, tool_calls)` | Execute tool calls with a tool registry |
| `collect_stream(stream, **kwargs)` | Aggregate a chat stream into one result |
| `estimate_tokens(request, response=None)` | Estimate token counts for a request/response |
| `cosine_similarity(a, b)` | Compare two vectors (e.g. embeddings) |
| `ToolRegistry()` | Create a tool registry for building tool schemas |

## Functions

### `ai.text(response)`

Extracts the text content from a completion response, automatically removing any thinking blocks.

**Parameters:**

- `response` (`dict`): Chat completion response from `client.completion()`.

**Returns:** `str`: the response text with thinking blocks removed.

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "What is 2+2?")

text = ai.text(response)
print(text)  # "4"
```

### `ai.thinking(response)`

Extracts thinking/reasoning blocks from a completion response.

**Parameters:**

- `response` (`dict`): Chat completion response from `client.completion()`.

**Returns:** `list`: list of thinking block strings (empty if no thinking blocks).

```python
client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "Explain step by step")

thoughts = ai.thinking(response)
for thought in thoughts:
    print("Reasoning:", thought)

text = ai.text(response)
print("Answer:", text)
```

### `ai.extract_thinking(text)`

Extracts thinking/reasoning blocks from AI model response text. Many models include their reasoning in special blocks (like `<think>...</think>`) which you may want to process separately from the main response.

**Supported formats:**

- XML-style: `<think>...</think>`, `<thinking>...</thinking>`
- OpenAI style: `<Thought>...</Thought>`
- Markdown blocks: ` ```thinking\n...\n``` `, ` ```thought\n...\n``` `
- Claude style: `<antThinking>...</antThinking>`

**Parameters:**

- `text` (`str`): The AI response text to process.

**Returns:** `dict`: contains:
- `thinking` (`list`): List of extracted thinking block strings.
- `content` (`str`): The cleaned response text with thinking blocks removed.

```python
response_text = """<think>
Let me analyze this step by step.
The user wants to know about Python.
</think>

Python is a high-level programming language known for its readability."""

result = ai.extract_thinking(response_text)

for thought in result["thinking"]:
    print("Model reasoning:", thought)

print("Response:", result["content"])
# Output: "Python is a high-level programming language known for its readability."
```

### `ai.tool_calls(response_or_message)`

Extracts normalized tool calls from a completion response, assistant message dict, or raw tool call list.

**Parameters:**

- `response_or_message` (`dict` or `list`): Completion response, assistant message, or tool call list.

**Returns:** `list`: normalized tool call dicts with `id`, `type`, and `function` fields.

```python
client = ai.Client("http://127.0.0.1:11434/v1")

tools = ai.ToolRegistry()
tools.add("echo_tool", "Echo a message", {"message": "string"}, lambda args: args["message"])
schemas = tools.build()

response = client.completion("gemma4:e4b", "Call echo_tool with the message hello", tools=schemas)
tool_calls = ai.tool_calls(response)

for tool_call in tool_calls:
    print(tool_call["function"]["name"])
    print(tool_call["function"]["arguments"].get("message", "missing"))
```

### `ai.execute_tool_calls(registry, tool_calls)`

Executes normalized tool calls using handlers from a `ToolRegistry`.

**Parameters:**

- `registry` (`ToolRegistry`): Tool registry containing handlers.
- `tool_calls` (`list`): Tool call dicts, typically from `ai.tool_calls(...)`.

**Returns:** `list`: tool result message dicts with `role`, `tool_call_id`, and `content`.

```python
tools = ai.ToolRegistry()
tools.add("echo_tool", "Echo a message", {"message": "string"}, lambda args: "echo:" + args["message"])

tool_calls = [{
    "id": "call_1",
    "type": "function",
    "function": {"name": "echo_tool", "arguments": {"message": "hello"}}
}]

tool_results = ai.execute_tool_calls(tools, tool_calls)
print(tool_results[0]["content"])  # "echo:hello"
```

### `ai.collect_stream(stream, **kwargs)`

Consumes a `ChatStream`, aggregates reasoning, content, tool calls, and finish status, and optionally emits events while chunks are processed.

**Parameters:**

- `stream` (`ChatStream`): Stream returned by `client.completion_stream()`.
- `chunk_timeout` (`int`, optional): Per-chunk timeout in seconds. Default: `0`.
- `first_chunk_timeout` (`int`, optional): Timeout for the first chunk only (models may need time to load). Falls back to `chunk_timeout`. Default: `0`.
- `on_event` (`callable`, optional): Callback invoked with event dicts during collection.

**Returns:** `dict`: aggregated result with `content`, `reasoning`, `tool_calls`, `finish_reason`, `timed_out`, `assistant_message`, and `error` (only present when `timed_out` is true).

```python
events = []

def on_event(event):
    events.append(event["type"])

client = ai.Client("http://127.0.0.1:11434/v1")
stream = client.completion_stream("gemma4:e4b", "hello")
result = ai.collect_stream(stream, first_chunk_timeout=30, chunk_timeout=4, on_event=on_event)

print(result["content"])
print(events)
```

### `ai.estimate_tokens(request, response=None)`

Estimates the number of tokens in request messages and/or a completion response using a character-based heuristic (~4 characters per token). Provides a fast, reproducible approximation useful for cost estimation and context window management. Character-based estimation is ~70x faster than using tiktoken and provides reasonable approximations across model families (GPT, Claude, Gemini).

**Parameters:**

- `request` (`str`, `list`, `dict`, or `None`): The messages sent to the AI. Can be a string (user message), a list of message dicts with `role`/`content` keys, a completion request dict with a `messages` key, or `None` to estimate only response tokens.
- `response` (`dict`, optional): The completion response from `client.completion()` or `client.response_create()`. Default: `None` (estimate only request tokens).

**Returns:** `dict`: token usage estimates with keys:
- `prompt_tokens` (`int`): Estimated tokens in the request messages.
- `completion_tokens` (`int`): Estimated tokens in the response.
- `total_tokens` (`int`): Sum of prompt and completion tokens.

```python
client = ai.Client("", api_key="sk-...")

messages = [{"role": "user", "content": "Hello!"}]
response = client.completion("gpt-4", messages)
usage = ai.estimate_tokens(messages, response)
print(f"Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}")

# Estimate a request before sending it
usage = ai.estimate_tokens(messages)

# Estimate only a response
usage = ai.estimate_tokens(None, response)

# With string shorthand
response = client.completion("gpt-4", "What is 2+2?")
usage = ai.estimate_tokens("What is 2+2?", response)
print(f"Total: {usage.total_tokens} tokens")
```

### `ai.cosine_similarity(a, b)`

Computes the cosine similarity between two vectors. Primarily used to compare embedding vectors from `client.embedding()` to find semantically similar texts.

**Parameters:**

- `a` (`list`): First vector (list of numbers).
- `b` (`list`): Second vector (list of numbers, same length as `a`).

**Returns:** `float`: cosine similarity score from `-1.0` (opposite direction) to `1.0` (identical direction). `0.0` means the vectors are orthogonal (no similarity), and is also returned if either vector has zero magnitude.

```python
client = ai.Client("", api_key="sk-...")

emb1 = client.embedding("text-embedding-3-small", "Hello world")
emb2 = client.embedding("text-embedding-3-small", "Hi world")
emb3 = client.embedding("text-embedding-3-small", "Goodbye")

score = ai.cosine_similarity(emb1.data[0].embedding, emb2.data[0].embedding)
print(score)  # High similarity (~0.9+)

score = ai.cosine_similarity(emb1.data[0].embedding, emb3.data[0].embedding)
print(score)  # Lower similarity
```

### `ai.ToolRegistry()`

Creates a new tool registry for building OpenAI-compatible tool schemas for AI agents. This is a re-export of the `Registry` class from [scriptling.ai.tools](../tools/): `ai.ToolRegistry()` and `scriptling.ai.tools.Registry()` both return a `Registry` instance.

**Returns:** `ToolRegistry`: a registry object with `add()`, `build()`, and `get_handler()` methods.

```python
registry = ai.ToolRegistry()
```

See [scriptling.ai.tools](../tools/) for the `add()`, `build()`, and `get_handler()` method reference and the full list of accepted parameter types. For automatic tool execution with an agent loop, see [scriptling.ai.agent](../agent/).

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.ai` and its submodules make outbound HTTP requests to AI provider APIs (and, via `agent`, can drive multi-step tool-calling loops). API keys and endpoints are supplied by the embedder when creating a client: scripts don't see them directly unless explicitly passed. For a full risk breakdown, see the [Security Guide](/docs/security/#library-security) and [Library Registration](/docs/go-integration/library-registration/#ai--agent).

## See Also

- [scriptling.ai.Client](../client/): Full client method reference (completion, streaming, embeddings, Responses API)
- [scriptling.ai.agent](../agent/): Agentic AI loop with automatic tool execution
- [scriptling.ai.memory](../memory/): Long-term memory store for AI agents
- [scriptling.ai.tools](../tools/): Tool schema builder (`Registry` / `ai.ToolRegistry`)
- [scriptling.mcp](../mcp/): MCP client for connecting to MCP servers
