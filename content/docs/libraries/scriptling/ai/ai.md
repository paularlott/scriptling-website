---
title: scriptling.ai
linkTitle: ai
weight: 1
---

AI and LLM functions for interacting with OpenAI-compatible APIs. This library provides:

1. **[AI Client](client/)** - Create clients and make completions, embeddings, and Responses API calls
2. **Tool Registry** - Build tool schemas for AI agents
3. **Response Helpers** - Extract text and thinking blocks from AI responses

## Quick Start

```python
import scriptling.ai as ai

# Create a client and make a completion
client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "What is 2+2?")
print(response.choices[0].message.content)

# Extract text
print(ai.text(response))
```

For the full client method reference (completion, streaming, parallel, embeddings, Responses API, background processing), see [AI Client](client/).

## Available Functions

| Function                     | Description                               |
| ---------------------------- | ----------------------------------------- |
| `Client(base_url, **kwargs)` | Create AI client for API interactions     |
| `text(response)`             | Extract text content from response        |
| `thinking(response)`         | Extract thinking blocks from response     |
| `extract_thinking(text)`     | Extract thinking blocks from text string  |
| `tool_calls(input)`          | Extract normalized tool calls             |
| `execute_tool_calls(...)`    | Execute tool calls with a tool registry   |
| `collect_stream(...)`        | Aggregate a chat stream into one result   |
| `estimate_tokens(req, resp=None)` | Estimate token counts for request/response|
| `cosine_similarity(a, b)`    | Compare two vectors (e.g. embeddings)     |
| `ToolRegistry()`             | Create tool registry for building schemas |

## Creating an AI Client

The first step is to create an AI client instance. See [AI Client](client/) for the full constructor reference and all client methods.

```python
import scriptling.ai as ai

# OpenAI API with defaults
client = ai.Client("", api_key="sk-...")

# With custom settings
client = ai.Client(
    "https://api.openai.com/v1",
    api_key="sk-...",
    max_tokens=2048,
    temperature=0.7
)

# Claude (max_tokens defaults to 4096 if not specified)
client = ai.Client(
    "https://api.anthropic.com",
    provider=ai.CLAUDE,
    api_key="sk-ant-..."
)

# Local LLM (LM Studio, Ollama, etc.)
client = ai.Client("http://127.0.0.1:1234/v1")
```

## Response Helpers

### ai.text(response)

Extracts the text content from a completion response, automatically removing any thinking blocks.

**Parameters:**

- `response` (dict): Chat completion response from `client.completion()`

**Returns:** str - The response text with thinking blocks removed

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "What is 2+2?")

# Get just the text, without thinking blocks
text = ai.text(response)
print(text)  # "4"
```

### ai.thinking(response)

Extracts thinking/reasoning blocks from a completion response.

**Parameters:**

- `response` (dict): Chat completion response from `client.completion()`

**Returns:** list - List of thinking block strings (empty if no thinking blocks)

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")
response = client.completion("gpt-4", "Explain step by step")

# Get thinking blocks separately
thoughts = ai.thinking(response)
for thought in thoughts:
    print("Reasoning:", thought)

# Get clean text
text = ai.text(response)
print("Answer:", text)
```

## Thinking Extractor

### ai.extract_thinking(text)

Extracts thinking/reasoning blocks from AI model responses. Many models include their reasoning in special blocks (like `<think>...</think>`) which you may want to process separately from the main response.

**Supported Formats:**

- XML-style: `<think>...</think>`, `<thinking>...</thinking>`
- OpenAI style: `<Thought>...</Thought>`
- Markdown blocks: ` ```thinking\n...\n``` `, ` ```thought\n...\n``` `
- Claude style: `<antThinking>...</antThinking>`

**Parameters:**

- `text` (str): The AI response text to process

**Returns:** dict - Contains:

- `thinking` (list): List of extracted thinking block strings
- `content` (str): The cleaned response text with thinking blocks removed

**Example:**

```python
import scriptling.ai as ai

response_text = """<think>
Let me analyze this step by step.
The user wants to know about Python.
</think>

Python is a high-level programming language known for its readability."""

result = ai.extract_thinking(response_text)

# Access the thinking blocks
for thought in result["thinking"]:
    print("Model reasoning:", thought)

# Get the cleaned response
print("Response:", result["content"])
# Output: "Python is a high-level programming language known for its readability."
```

**With Agent Responses:**

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent

bot = agent.Agent(client, tools=tools, system_prompt="...")
response = bot.trigger("Explain Python")

# Extract and display thinking separately
result = ai.extract_thinking(response.content)

if result["thinking"]:
    print("=== Model Reasoning ===")
    for thought in result["thinking"]:
        print(thought)
    print()

print("=== Response ===")
print(result["content"])
```

## Token Estimation

### ai.estimate_tokens(request, response=None)

Estimates the number of tokens in request messages and/or a completion response using a character-based heuristic (~4 characters per token). This provides a fast, reproducible approximation useful for cost estimation and context window management.

**Parameters:**

- `request` (str, list, dict, or None): The messages sent to the AI. Can be:
  - A string (user message)
  - A list of message dicts with "role" and "content" keys
  - A completion request dict with a "messages" key
  - `None` to estimate only response tokens
- `response` (dict or None, optional): The completion response from `client.completion()` or `client.response_create()`. Use `None` or omit it to estimate only request tokens.

**Returns:** dict - Token usage estimates with keys:

- `prompt_tokens` (int): Estimated tokens in the request messages
- `completion_tokens` (int): Estimated tokens in the response
- `total_tokens` (int): Sum of prompt and completion tokens

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# With messages array
messages = [{"role": "user", "content": "Hello!"}]
response = client.completion("gpt-4", messages)
usage = ai.estimate_tokens(messages, response)
print(f"Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}")

# Estimate a request before sending it
usage = ai.estimate_tokens(messages)
print(f"Prompt: {usage.prompt_tokens}")

# Estimate only a response
usage = ai.estimate_tokens(None, response)
print(f"Completion: {usage.completion_tokens}")

# With string shorthand
response = client.completion("gpt-4", "What is 2+2?")
usage = ai.estimate_tokens("What is 2+2?", response)
print(f"Total: {usage.total_tokens} tokens")
```

**Performance:** Character-based estimation is ~70x faster than using tiktoken and provides reasonable approximations across model families (GPT, Claude, Gemini).

## Vector Similarity

### ai.cosine_similarity(a, b)

Computes the cosine similarity between two vectors, returning a score from -1.0 (opposite direction) to 1.0 (identical direction). A score of 0.0 means the vectors are orthogonal (no similarity).

Primarily used to compare embedding vectors from `client.embedding()` to find semantically similar texts.

**Parameters:**

- `a` (list): First vector (list of numbers)
- `b` (list): Second vector (list of numbers, same length as `a`)

**Returns:** float - Cosine similarity score from -1.0 to 1.0. Returns 0.0 if either vector has zero magnitude.

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# Embed multiple texts
emb1 = client.embedding("text-embedding-3-small", "Hello world")
emb2 = client.embedding("text-embedding-3-small", "Hi world")
emb3 = client.embedding("text-embedding-3-small", "Goodbye")

# Compare similarity
score = ai.cosine_similarity(emb1.data[0].embedding, emb2.data[0].embedding)
print(score)  # High similarity (~0.9+)

score = ai.cosine_similarity(emb1.data[0].embedding, emb3.data[0].embedding)
print(score)  # Lower similarity
```

**Finding the most similar text:**

```python
texts = ["Python is great", "I love coding", "The weather is nice"]
query = "programming language"

query_emb = client.embedding("text-embedding-3-small", query)
query_vec = query_emb.data[0].embedding

text_embs = client.embedding("text-embedding-3-small", texts)

best_idx = 0
best_score = -1.0
for i, emb in enumerate(text_embs.data):
    score = ai.cosine_similarity(query_vec, emb.embedding)
    if score > best_score:
        best_score = score
        best_idx = i

print(f"Best match: {texts[best_idx]} (score: {best_score:.3f})")
```

## Tool Registry

Build OpenAI-compatible tool schemas for AI agents.

### ai.ToolRegistry()

Creates a new tool registry for building OpenAI-compatible tool schemas.

**Example:**

```python
import scriptling.ai as ai

registry = ai.ToolRegistry()
```

### registry.add(name, description, params, handler)

Adds a tool to the registry.

**Parameters:**

- `name` (str): Tool name
- `description` (str): Tool description for the AI
- `params` (dict): Parameter definitions with types
- `handler` (callable): Function to execute when tool is called

**Parameter Types:**

The value for each parameter is a JSON Schema type name. Append `?` to mark
the parameter as optional.

| Type      | Aliases | Description       |
| --------- | ------- | ----------------- |
| `string`  | `str`   | Text value        |
| `integer` | `int`   | Whole number      |
| `number`  | `float` | Integer or float  |
| `boolean` | `bool`  | `true` or `false` |
| `array`   | `list`  | List of values    |
| `object`  | `dict`  | Key/value mapping |

Unknown type names raise an error at `registry.add()` time.

**Example:**

```python
tools = ai.ToolRegistry()

# Simple tool
tools.add("get_time", "Get current time", {}, lambda args: "12:00 PM")

# Tool with required parameters
tools.add("read_file", "Read a file", {
    "path": "string"
}, lambda args: os.read_file(args["path"]))

# Tool with optional parameters
tools.add("search", "Search files", {
    "query": "string",
    "limit": "integer?",
    "path": "string?"
}, lambda args: search_files(args["query"], args.get("limit", 10)))
```

### registry.build()

Builds OpenAI-compatible tool schemas for passing to completion requests.

**Returns:** list - List of tool schema dicts

**Example:**

```python
tools = ai.ToolRegistry()
tools.add("get_time", "Get current time", {}, time_handler)

# Direct completion calls
schemas = tools.build()
response = client.completion("gpt-4", [{"role": "user", "content": "What time is it?"}], tools=schemas)

# With Agent (recommended - tools handled automatically)
# See [Agent Library](../agent/) for details
```

### registry.get_handler(name)

Gets a tool handler by name.

**Parameters:**

- `name` (str): Tool name

**Returns:** callable - Tool handler function

**Example:**

```python
handler = tools.get_handler("read_file")
result = handler({"path": "config.json"})
```

### Using Tools with Completions

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

tools = ai.ToolRegistry()
tools.add("read_file", "Read a file", {"path": "string"}, lambda args: os.read_file(args["path"]))
schemas = tools.build()

# Pass tools directly to completion()
response = client.completion("gpt-4", [{"role": "user", "content": "Read file /data/config.txt"}], tools=schemas)
```

For automatic tool execution with an agent loop, see [Agent Library](../agent/).

## Tool Call Helpers

These helpers make it easier to build manual tool-calling loops without rewriting
the same response parsing and stream aggregation logic each time.

### ai.tool_calls(response_or_message)

Extracts normalized tool calls from a completion response, assistant message dict,
or raw tool call list.

**Parameters:**

- `response_or_message` (dict or list): Completion response, assistant message, or tool call list

**Returns:** list - Normalized tool call dicts with `id`, `type`, and `function` fields

**Example:**

```python
import scriptling.ai as ai

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

### ai.execute_tool_calls(registry, tool_calls)

Executes normalized tool calls using handlers from a `ToolRegistry`.

**Parameters:**

- `registry` (ToolRegistry): Tool registry containing handlers
- `tool_calls` (list): Tool call dicts, typically from `ai.tool_calls(...)`

**Returns:** list - Tool result message dicts with `role`, `tool_call_id`, and `content`

**Example:**

```python
import scriptling.ai as ai

tools = ai.ToolRegistry()
tools.add("echo_tool", "Echo a message", {"message": "string"}, lambda args: "echo:" + args["message"])

tool_calls = [{
    "id": "call_1",
    "type": "function",
    "function": {
        "name": "echo_tool",
        "arguments": {"message": "hello"}
    }
}]

tool_results = ai.execute_tool_calls(tools, tool_calls)
print(tool_results[0]["content"])  # "echo:hello"
```

### ai.collect_stream(stream, \*\*kwargs)

Consumes a `ChatStream`, aggregates reasoning, content, tool calls, and finish
status, and optionally emits events while chunks are processed.

**Parameters:**

- `stream` (ChatStream): Stream returned by `client.completion_stream()`
- `chunk_timeout` (int, optional): Per-chunk timeout in seconds. Default: `0`
- `first_chunk_timeout` (int, optional): Timeout for the first chunk only (models may need time to load). Falls back to `chunk_timeout`. Default: `0`
- `on_event` (callable, optional): Callback invoked with event dicts during collection

**Returns:** dict - Aggregated result with `content`, `reasoning`, `tool_calls`, `finish_reason`, `timed_out`, `assistant_message`, and `error` (only present when `timed_out` is true)

**Example:**

```python
import scriptling.ai as ai

events = []

def on_event(event):
    events.append(event["type"])

client = ai.Client("http://127.0.0.1:11434/v1")
stream = client.completion_stream("gemma4:e4b", "hello")
result = ai.collect_stream(stream, first_chunk_timeout=30, chunk_timeout=4, on_event=on_event)

print(result["content"])
print(events)
```

## See Also

- [AI Client](client/) - Full client method reference (completion, streaming, embeddings, Responses API)
- [Agent Library](../agent/) - Agentic AI loop with automatic tool execution
- [AI Memory](../memory/) - Long-term memory store for AI agents
