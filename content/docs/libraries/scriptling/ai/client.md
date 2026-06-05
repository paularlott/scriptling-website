---
title: scriptling.ai.Client
linkTitle: ai.Client
weight: 1
---

The AI Client is the primary interface for making API calls to AI providers. Create a client with `ai.Client()`, then call methods like `completion()`, `embedding()`, or `response_create()` on it.

## Creating a Client

### ai.Client(base_url, \*\*kwargs)

Creates a new AI client instance for making API calls to supported services.

**Parameters:**

- `base_url` (str): Base URL of the API (defaults to https://api.openai.com/v1 if empty)
- `provider` (str, optional): Provider type (defaults to `ai.OPENAI`). Use constants:

  | Constant     | Provider         |
  | ------------ | ---------------- |
  | `ai.OPENAI`  | OpenAI           |
  | `ai.CLAUDE`  | Anthropic Claude |
  | `ai.GEMINI`  | Google Gemini    |
  | `ai.OLLAMA`  | Ollama           |
  | `ai.ZAI`     | Z AI             |
  | `ai.MISTRAL` | Mistral          |

- `api_key` (str, optional): API key for authentication
- `max_tokens` (int, optional): Default max_tokens for all requests. Claude defaults to 4096 if not set
- `temperature` (float, optional): Default temperature for all requests (0.0-2.0)
- `top_p` (float, optional): Default nucleus sampling threshold for all requests (0.0-1.0)
- `headers` (dict, optional): Extra HTTP headers to include with every AI API request
- `remote_servers` (list, optional): List of remote MCP server configs, each a dict with:
  - `base_url` (str, required): URL of the MCP server
  - `namespace` (str, optional): Namespace prefix for tools from this server
  - `bearer_token` (str, optional): Bearer token for authentication
- `max_retries` (int, optional): Max retries for retryable errors (429, 5xx). Default: `3`. Set `-1` to disable
- `retry_backoff` (float, optional): Base backoff in seconds between retries (doubles each attempt). Default: `1.0`
- `retry_on_rate_limit` (bool, optional): Retry on 429 rate limit errors. Default: `True`
- `retry_on_server_error` (bool, optional): Retry on 5xx server errors. Default: `True`

**Returns:** AIClient - A client instance with methods for API calls

**Example:**

```python
import scriptling.ai as ai

# OpenAI API with defaults, top_p=0.9
client = ai.Client("", api_key="sk-...", max_tokens=2048, temperature=0.7)

# Claude (max_tokens defaults to 4096 if not specified)
client = ai.Client(
    "https://api.anthropic.com",
    provider=ai.CLAUDE,
    api_key="sk-ant-...",
    max_tokens=4096,  # Optional, defaults to 4096 for Claude
    temperature=0.7
)

# LM Studio / Local LLM
client = ai.Client("http://127.0.0.1:1234/v1")

# With custom request headers
client = ai.Client(
    "",
    api_key="sk-...",
    headers={"X-Project": "docs-bot"}
)

# With MCP servers configured
client = ai.Client("http://127.0.0.1:1234/v1", remote_servers=[
    {"base_url": "http://127.0.0.1:8080/mcp", "namespace": "scriptling"},
    {"base_url": "https://api.example.com/mcp", "namespace": "search", "bearer_token": "secret"},
])
```

**Default Parameters:**

When you set `max_tokens`, `temperature`, and `top_p` at the client level, they apply to all requests unless overridden:

```python
# Set defaults at client creation
client = ai.Client("", api_key="sk-...", max_tokens=2048, temperature=0.7, top_p=0.9)

# Uses client defaults (2048 tokens, 0.7 temperature, 0.9 top_p)
response = client.completion("gpt-4", "Hello!")

# Override per request
response = client.completion("gpt-4", "Hello!", max_tokens=4096, temperature=0.9, top_p=1.0)
```

## Client Methods

| Method | Description |
|--------|-------------|
| [`completion(model, messages, **kwargs)`](#clientcompletion) | Chat completion |
| [`completion_stream(model, messages, **kwargs)`](#clientcompletion_stream) | Streaming chat completion |
| [`ask(model, messages, **kwargs)`](#clientask) | Quick completion returning text directly |
| [`completion_parallel(model, messages_list, **kwargs)`](#clientcompletion_parallel) | Concurrent completions |
| [`ask_parallel(model, messages_list, **kwargs)`](#clientask_parallel) | Concurrent ask completions |
| [`Pipeline(model, **kwargs)`](#clientpipeline) | Streaming completion pipeline |
| [`embedding(model, input)`](#clientembedding) | Create embedding vectors |
| [`models()`](#clientmodels) | List available models |
| [`response_create(model, input, **kwargs)`](#clientresponse_create) | Create a Responses API response |
| [`response_get(id)`](#clientresponse_get) | Get a response by ID |
| [`response_stream(model, input, **kwargs)`](#clientresponse_stream) | Stream a Responses API response |
| [`response_cancel(id)`](#clientresponse_cancel) | Cancel an in-progress response |
| [`response_delete(id)`](#clientresponse_delete) | Delete a response by ID |
| [`response_compact(id)`](#clientresponse_compact) | Compact a response (remove reasoning) |

## Chat Completions

### client.completion(model, messages, \*\*kwargs)

Creates a chat completion using this client's configuration.

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages` (str or list): Either a string (user message) or a list of message dicts with "role" and "content" keys
- `system_prompt` (str, optional): System prompt to use when messages is a string
- `tools` (list, optional): List of tool schema dicts from ToolRegistry.build()
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `max_tokens` (int, optional): Maximum tokens to generate
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body
- `timeout` (int, optional): Request timeout in seconds

**Returns:** dict - Response containing id, choices, usage, etc.

**Examples:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# String shorthand - simple user message
response = client.completion("gpt-4", "What is 2+2?")
print(response.choices[0].message.content)

# String shorthand with system prompt
response = client.completion("gpt-4", "What is 2+2?", system_prompt="You are a helpful math tutor")
print(response.choices[0].message.content)

# Full messages array
response = client.completion("gpt-4", [{"role": "user", "content": "What is 2+2?"}])
print(response.choices[0].message.content)

# Provider-specific request body fields
response = client.completion(
    "glm-4.7",
    "Think through this task",
    extra_body={
        "thinking": {
            "type": "enabled",
            "clear_thinking": False
        }
    }
)
```

**With Tool Calling:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# Create tools registry
tools = ai.ToolRegistry()
tools.add("get_time", "Get current time", {}, lambda args: "12:00 PM")
tools.add("read_file", "Read a file", {"path": "string"}, lambda args: os.read_file(args["path"]))

# Build schemas and pass to completion
schemas = tools.build()
response = client.completion("gpt-4", [{"role": "user", "content": "What time is it?"}], tools=schemas)
```

**Note:** In non-streaming completion responses, `tool_call.function.arguments` is exposed as a dict, so you can access fields with `args["name"]` or `args.get("name", default)`.

### client.completion_stream(model, messages, \*\*kwargs)

Creates a streaming chat completion using this client's configuration. Returns a ChatStream object that can be iterated over.

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages` (str or list): Either a string (user message) or a list of message dicts with "role" and "content" keys
- `system_prompt` (str, optional): System prompt to use when messages is a string
- `tools` (list, optional): List of tool schema dicts from ToolRegistry.build()
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `max_tokens` (int, optional): Maximum tokens to generate
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body
- `timeout` (int, optional): Overall request timeout in seconds

**Returns:** ChatStream - A stream object with a `next()` method

**Examples:**

```python
# String shorthand - simple user message
client = ai.Client("", api_key="sk-...")
stream = client.completion_stream("gpt-4", "Count to 10")
while True:
    chunk = stream.next()
    if chunk is None:
        break
    if chunk.choices and len(chunk.choices) > 0:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="")
print()

# String shorthand with system prompt
stream = client.completion_stream("gpt-4", "Explain quantum physics", system_prompt="You are a physics professor")
# ... iterate as above

# Full messages array
stream = client.completion_stream("gpt-4", [{"role": "user", "content": "Count to 10"}])
# ... iterate as above
```

**With Tool Calling:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

tools = ai.ToolRegistry()
tools.add("get_weather", "Get weather for a city", {"city": "string"}, weather_handler)
schemas = tools.build()

stream = client.completion_stream("gpt-4", [{"role": "user", "content": "What's the weather in Paris?"}], tools=schemas)
# Stream chunks...
```

### client.ask(model, messages, \*\*kwargs)

Quick completion method that returns text directly, with thinking blocks automatically removed. This is a convenience method for simple queries where you don't need the full response object.

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages` (str or list): Either a string (user message) or a list of message dicts
- `system_prompt` (str, optional): System prompt to use when messages is a string
- `tools` (list, optional): List of tool schema dicts from ToolRegistry.build()
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `max_tokens` (int, optional): Maximum tokens to generate

**Returns:** str - The response text with thinking blocks removed

**Examples:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# Simple query
answer = client.ask("gpt-4", "What is 2+2?")
print(answer)  # "4"

# With system prompt
answer = client.ask("gpt-4", "Explain quantum physics", system_prompt="You are a physics professor")
print(answer)

# Full messages array
answer = client.ask("gpt-4", [{"role": "user", "content": "Hello!"}])
print(answer)
```

## Parallel Completions

### client.completion_parallel(model, messages_list, \*\*kwargs)

Runs multiple chat completions concurrently and returns a list of responses in the same
order as the input `messages_list`. Each element of `messages_list` is passed to `completion()`.

Includes **adaptive concurrency**: when a rate limit (429) is detected, the parallelism is
automatically halved and workers pause briefly before continuing. This reduces pressure on
the API without manual intervention. Rate limit retries are handled automatically by the
client (see `max_retries` on `ai.Client`).

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages_list` (list): List of messages, where each element is a string or list of message dicts
- `max_parallel` (int, optional): Maximum number of concurrent requests. Default: `1`
- `system_prompt` (str, optional): System prompt to use when messages is a string
- `tools` (list, optional): List of tool schema dicts from ToolRegistry.build()
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `max_tokens` (int, optional): Maximum tokens to generate
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body
- `timeout` (int, optional): Request timeout in seconds

**Returns:** list - List of response dicts in the same order as `messages_list`. Each response
may include a `retry` dict if the client retried the request: `{"attempts": 2, "rate_limit_hit": true, "total_backoff": 1.0}`

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...", max_retries=3)

questions = ["What is 2+2?", "What is the capital of France?", "Explain gravity"]
results = client.completion_parallel("gpt-4", questions, max_parallel=3)
for result in results:
    if "retry" in result:
        print(f"  (retried {result['retry']['attempts']}x)")
    print(result["choices"][0]["message"]["content"])
```

### client.ask_parallel(model, messages_list, \*\*kwargs)

Runs multiple chat completions concurrently and returns a list of text responses in the
same order as the input `messages_list`. Thinking blocks are automatically removed.

Includes **adaptive concurrency**: when a rate limit (429) is detected, the parallelism is
automatically halved and workers pause briefly before continuing. Rate limit retries are
handled automatically by the client (see `max_retries` on `ai.Client`).

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages_list` (list): List of messages, where each element is a string or list of message dicts
- `max_parallel` (int, optional): Maximum number of concurrent requests. Default: `1`
- `system_prompt` (str, optional): System prompt to use when messages is a string
- `tools` (list, optional): List of tool schema dicts from ToolRegistry.build()
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `max_tokens` (int, optional): Maximum tokens to generate
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body
- `timeout` (int, optional): Request timeout in seconds

**Returns:** list - List of response text strings in the same order as `messages_list`

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

questions = ["What is 2+2?", "What is the capital of France?", "Explain gravity"]
answers = client.ask_parallel("gpt-4", questions, max_parallel=3)
for answer in answers:
    print(answer)
```

### client.Pipeline(model, \*\*kwargs)

Creates a **Pipeline** that starts processing requests immediately as they are added via
`add()`, overlapping prompt generation with inference. Call `complete()` to wait for all
results. The Pipeline is the more general primitive behind `completion_parallel` and
`ask_parallel`.

Includes the same **adaptive concurrency** as the parallel methods: on a rate limit (429)
the concurrency is automatically halved and workers pause before continuing.

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
- `max_parallel` (int, optional): Maximum concurrent requests. Default: `1`
- `ask` (bool, optional): If `True`, return plain text strings instead of response dicts. Default: `False`
- `system_prompt` (str, optional): System prompt applied to each string message
- `tools` (list, optional): List of tool schema dicts from `ToolRegistry.build()`
- `temperature` (float, optional): Sampling temperature (0.0-2.0)
- `top_p` (float, optional): Nucleus sampling threshold (0.0-1.0)
- `max_tokens` (int, optional): Maximum tokens to generate
- `extra_body` (dict, optional): Provider-specific fields merged into every request body
- `timeout` (int, optional): Request timeout in seconds

**Returns:** `Pipeline` — a pipeline object with `add()` and `complete()` methods.

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("http://localhost:1234/v1")

# Completion pipeline (ask=False, default) — results are full response dicts
pipe = client.Pipeline("gpt-4", max_parallel=4)
for row in dataset:
    pipe.add(build_prompt(row))            # string shorthand; inference starts immediately
pipe.add([                                 # or a full message list
    {"role": "system", "content": "Be concise."},
    {"role": "user",   "content": "Explain gravity."},
])
results = pipe.complete()                  # ordered list of response dicts
for r in results:
    print(r["choices"][0]["message"]["content"])

# Ask pipeline (ask=True) — results are plain text strings
pipe = client.Pipeline("gpt-4", max_parallel=4, ask=True)
for q in questions:
    pipe.add(q)
answers = pipe.complete()                  # ordered list of str
for answer in answers:
    print(answer)
```

### Pipeline.add(message)

Queues a message for completion. Processing starts immediately as concurrency slots are
available — you do not need to wait until `complete()` is called.

`add()` accepts exactly the same message formats as `completion()` and `ask()`:

| Format | When to use |
|---|---|
| `str` | Simple user question; the pipeline's `system_prompt` (if set) is applied automatically |
| `list` of message dicts | Full conversation turn with explicit `role`/`content` keys; `system_prompt` is ignored |

**Parameters:**

- `message` (str or list): User message string, or list of message dicts with `role` and `content` keys

**Returns:** `None`

**Example:**

```python
# String shorthand
pipe.add("What is the capital of France?")

# Full message list
pipe.add([
    {"role": "system", "content": "You are a geography expert."},
    {"role": "user",   "content": "What is the capital of France?"},
])
```

### Pipeline.complete()

Closes the pipeline to new additions, waits for all in-flight requests to finish, and
returns results in the same order as the `add()` calls.

`complete()` may only be called once. Calling `add()` after `complete()` raises an error.

**Returns:** list

- When `ask=False` (default — **completion mode**): ordered list of response dicts, identical in structure to a single `completion()` response. Access content with `result["choices"][0]["message"]["content"]`.
- When `ask=True` (**ask mode**): ordered list of plain text strings with thinking blocks already removed, identical to what `ask()` returns.

## Embeddings

### client.embedding(model, input)

Creates an embedding vector for the given input text(s) using the specified model.

**Provider Support:**

| Provider | Support | Notes |
|----------|---------|-------|
| OpenAI | Native | POST /embeddings |
| Gemini | Native | Translates to embedContent API |
| Ollama / ZAI / Mistral | Native | OpenAI-compatible endpoint |
| Claude | Not supported | Returns error |

**Parameters:**

- `model` (str): Model identifier (e.g., "text-embedding-3-small", "text-embedding-3-large")
- `input` (str or list): Input text(s) to embed - can be a string or list of strings

**Returns:** dict - Response containing data (list of embeddings with index, embedding, object), model, and usage

**Example:**

```python
client = ai.Client("", api_key="sk-...")

# Single text embedding
response = client.embedding("text-embedding-3-small", "Hello world")
print(response.data[0].embedding)

# Batch embedding
response = client.embedding("text-embedding-3-small", ["Hello", "World"])
for emb in response.data:
    print(emb.embedding)
```

## Models

### client.models()

Lists all models available for this client configuration.

**Returns:** dict - Response object with `object` and `data` fields. `data` contains the list of model objects.

**Example:**

```python
client = ai.Client("", api_key="sk-...")
models_response = client.models()
for model in models_response.data:
    print(model.id)
```

## Responses API

The Responses API is OpenAI's newer structured API for creating AI responses. It supports background processing, streaming, and compaction.

**Provider Support:**

| Provider | Support | Notes |
|----------|---------|-------|
| OpenAI | Native | Direct API calls |
| Claude | Emulated | Transparently emulated via chat completions |
| Gemini | Emulated | Transparently emulated via chat completions |
| Ollama / ZAI / Mistral | Emulated | Transparently emulated via chat completions |

### client.response_create(model, input, \*\*kwargs)

Creates a response using the OpenAI Responses API (new structured API).

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4o", "gpt-4")
- `input` (str or list): Either a string (user message content) or a list of input items (messages)
- `system_prompt` (str, optional): System prompt to use when input is a string
- `background` (bool, optional): If true, runs asynchronously and returns immediately with `in_progress` status
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body

**Returns:** dict - Response object with id, status, output, usage, etc.

**Examples:**

```python
# String shorthand - simple user message
client = ai.Client("", api_key="sk-...")
response = client.response_create("gpt-4o", "Hello!")
print(response.output)

# String shorthand with system prompt
response = client.response_create("gpt-4o", "What is AI?", system_prompt="You are a helpful assistant")
print(response.output)

# Background processing
response = client.response_create("gpt-4o", "What is AI?", background=True)
print(response.status)  # "queued" or "in_progress"
# Poll for completion
import time
while response.status in ["queued", "in_progress"]:
    time.sleep(0.5)
    response = client.response_get(response.id)
print(response.status)  # "completed"
print(response.output)

# Full input array (Responses API format)
response = client.response_create("gpt-4o", [
    {"type": "message", "role": "user", "content": "Hello!"}
])
print(response.output)

# Provider-specific request body fields
response = client.response_create(
    "glm-4.7",
    "Think through this task",
    extra_body={
        "thinking": {
            "type": "enabled",
            "clear_thinking": False
        }
    }
)
```

### client.response_get(id)

Retrieves a previously created response by its ID.

**Parameters:**

- `id` (str): Response ID

**Returns:** dict - Response object with id, status, output, usage, etc.

**Example:**

```python
client = ai.Client("", api_key="sk-...")
response = client.response_get("resp_123")
print(response.status)
```

### client.response_stream(model, input, \*\*kwargs)

Streams a response using the OpenAI Responses API, returning a `ResponseStream` object that yields SSE events.

**Parameters:**

- `model` (str): Model identifier (e.g., "gpt-4o", "gpt-4")
- `input` (str or list): Either a string (user message content) or a list of input items
- `system_prompt` (str, optional): System prompt to use when input is a string
- `extra_body` (dict, optional): Provider-specific fields to merge into the request body

**Returns:** ResponseStream - A stream object with a `next()` method

**Event types:**

| Event type                   | Key fields                                          |
| ---------------------------- | --------------------------------------------------- |
| `response.created`           | `response`                                          |
| `response.output_item.added` | `item`, `output_index`                              |
| `response.output_text.delta` | `delta`, `item_id`, `output_index`, `content_index` |
| `response.output_text.done`  | `text`, `item_id`, `output_index`, `content_index`  |
| `response.completed`         | `response` (full ResponseObject)                    |
| `error`                      | `message`                                           |

**Examples:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# Stream text deltas
stream = client.response_stream("gpt-4o", "Count to 5")
while True:
    event = stream.next()
    if event is None:
        break
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
print()

# With system prompt
stream = client.response_stream("gpt-4o", "Explain AI", system_prompt="You are a helpful assistant")
# ... iterate as above

# Access the completed response object
final_response = None
stream = client.response_stream("gpt-4o", "Hello!")
while True:
    event = stream.next()
    if event is None:
        break
    if event.type == "response.completed":
        final_response = event.response
if final_response:
    print(final_response.status)
```

### client.response_cancel(id)

Cancels a currently in-progress response.

**Parameters:**

- `id` (str): Response ID to cancel

**Returns:** dict - Cancelled response object

**Example:**

```python
client = ai.Client("", api_key="sk-...")
response = client.response_cancel("resp_123")
```

### client.response_delete(id)

Deletes a response by ID, removing it from storage.

**Parameters:**

- `id` (str): Response ID to delete

**Returns:** None

**Example:**

```python
client = ai.Client("", api_key="sk-...")
client.response_delete("resp_123")
```

### client.response_compact(id)

Compacts a response by removing intermediate reasoning steps, returning a more concise version with only the final output.

**Parameters:**

- `id` (str): Response ID to compact

**Returns:** dict - Compacted response object with reasoning removed

**Example:**

```python
client = ai.Client("", api_key="sk-...")

# Create a response with reasoning
response = client.response_create("gpt-4o", "Solve this complex problem: 2+2")

# Compact it to remove reasoning steps
compacted = client.response_compact(response.id)
print(compacted.output)  # Output without reasoning blocks
```

## ChatStream Class

Returned by `client.completion_stream()`. Iterates over response chunks from a streaming chat completion.

### stream.next()

Advances to the next response chunk and returns it.

**Returns:** dict - The next response chunk, or null if the stream is complete

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")
stream = client.completion_stream("gpt-4", [{"role": "user", "content": "Hello!"}])
while True:
    chunk = stream.next()
    if chunk is None:
        break
    if chunk.choices and len(chunk.choices) > 0:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="")
```

### stream.retry()

Returns retry metadata if the connection was retried before streaming began, or `None` if no retries occurred. Blocks until retry metadata is available.

**Returns:** dict or None - Retry metadata with keys:

- `attempts` (int): Total number of connection attempts (including the initial one)
- `rate_limit_hit` (bool): Whether a 429 rate limit error was encountered
- `total_backoff` (float): Total seconds spent waiting between retries

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...", max_retries=3)
stream = client.completion_stream("gpt-4", "Hello!")
result = ai.collect_stream(stream)

retry = stream.retry()
if retry:
    print(f"Retried {retry['attempts']}x, backoff: {retry['total_backoff']:.1f}s")
```

## ResponseStream Class

Returned by `client.response_stream()`. Iterates over SSE events from the Responses API.

### stream.next()

Advances to the next SSE event and returns it as a dict, or `None` when the stream is complete.

**Returns:** dict - Event dict with a `type` field plus event-specific fields, or null if complete

**Example:**

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")
stream = client.response_stream("gpt-4o", "Hello!")
while True:
    event = stream.next()
    if event is None:
        break
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
print()
```

## Error Handling

```python
import scriptling.ai as ai

try:
    client = ai.Client("", api_key="sk-...")
    response = client.completion("gpt-4", [{"role": "user", "content": "Hello!"}])
    print(response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
```

## Message Format

Messages are dictionaries with the following keys:

- `role` (str): "system", "user", "assistant", or "tool"
- `content` (str): The message content
- `tool_calls` (list, optional): Tool calls made by the assistant
- `tool_call_id` (str, optional): ID for tool response messages

```python
message = {
    "role": "user",
    "content": "What is the weather like?"
}
```
