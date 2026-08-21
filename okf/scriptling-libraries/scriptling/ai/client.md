---
description: Primary client interface for calling AI providers like OpenAI, Claude, and Gemini.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/ai/client/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/ai/client/
status: stable
tags:
    - libraries
    - ai
title: scriptling.ai.Client
type: API Reference
---
# scriptling.ai.Client

The AI Client is the primary interface for making API calls to AI providers: OpenAI, Claude, Gemini, Ollama, Z AI, and Mistral. Create a client with `ai.Client()`, then call methods like `completion()`, `embedding()`, or `response_create()` on it.

## Available Functions

| Function | Description |
|----------|-------------|
| `Client(base_url, **kwargs)` | Create an AI client for API calls |

## Client Methods

| Method | Description |
|--------|-------------|
| `completion(model, messages, **kwargs)` | Chat completion |
| `completion_stream(model, messages, **kwargs)` | Streaming chat completion |
| `ask(model, messages, **kwargs)` | Quick completion returning text directly |
| `completion_parallel(model, messages_list, **kwargs)` | Concurrent completions |
| `ask_parallel(model, messages_list, **kwargs)` | Concurrent ask completions |
| `Pipeline(model, **kwargs)` | Streaming completion pipeline |
| `embedding(model, input)` | Create embedding vectors |
| `models()` | List available models |
| `response_create(model, input, **kwargs)` | Create a Responses API response |
| `response_get(id)` | Get a response by ID |
| `response_stream(model, input, **kwargs)` | Stream a Responses API response |
| `response_cancel(id)` | Cancel an in-progress response |
| `response_delete(id)` | Delete a response by ID |
| `response_compact(id)` | Compact a response (remove reasoning) |

## Constants

| Constant | Description |
|----------|-------------|
| `ai.OPENAI` | OpenAI provider (default) |
| `ai.CLAUDE` | Anthropic Claude provider |
| `ai.GEMINI` | Google Gemini provider |
| `ai.OLLAMA` | Ollama provider |
| `ai.ZAI` | Z AI provider |
| `ai.MISTRAL` | Mistral provider |

## Functions

### `Client(base_url, **kwargs)`

Creates a new AI client instance for making API calls to a supported provider.

**Parameters:**

- `base_url` (`str`): Base URL of the API. Default: `https://api.openai.com/v1` if empty.
- `provider` (`str`, optional): Provider type: one of the constants above. Default: `ai.OPENAI`.
- `api_key` (`str`, optional): API key for authentication.
- `max_tokens` (`int`, optional): Default `max_tokens` applied to all requests from this client. Claude defaults to `4096` if not set.
- `temperature` (`float`, optional): Default sampling temperature (`0.0`-`2.0`) applied to all requests.
- `top_p` (`float`, optional): Default nucleus sampling threshold (`0.0`-`1.0`) applied to all requests.
- `headers` (`dict`, optional): Extra HTTP headers to include with every AI API request.
- `remote_servers` (`list`, optional): List of remote MCP server config dicts, each with:
  - `base_url` (`str`, required): URL of the MCP server.
  - `namespace` (`str`, optional): Namespace prefix for tools from this server.
  - `bearer_token` (`str`, optional): Bearer token for authentication.
- `max_retries` (`int`, optional): Max retries for retryable errors (429, 5xx). Default: `3`. Set `-1` to disable.
- `retry_backoff` (`float`, optional): Base backoff in seconds between retries (doubles each attempt). Default: `1.0`.
- `retry_on_rate_limit` (`bool`, optional): Retry on 429 rate limit errors. Default: `True`.
- `retry_on_server_error` (`bool`, optional): Retry on 5xx server errors. Default: `True`.

**Returns:** `AIClient`: a client instance with methods for API calls.

```python
import scriptling.ai as ai

# OpenAI API with defaults, top_p=0.9
client = ai.Client("", api_key="sk-...", max_tokens=2048, temperature=0.7)

# Claude (max_tokens defaults to 4096 if not specified)
client = ai.Client(
    "https://api.anthropic.com",
    provider=ai.CLAUDE,
    api_key="sk-ant-...",
    max_tokens=4096,
    temperature=0.7
)

# LM Studio / local LLM
client = ai.Client("http://127.0.0.1:1234/v1")

# With custom request headers
client = ai.Client("", api_key="sk-...", headers={"X-Project": "docs-bot"})

# With MCP servers configured
client = ai.Client("http://127.0.0.1:1234/v1", remote_servers=[
    {"base_url": "http://127.0.0.1:8080/mcp", "namespace": "scriptling"},
    {"base_url": "https://api.example.com/mcp", "namespace": "search", "bearer_token": "secret"},
])
```

**Default parameters:** When you set `max_tokens`, `temperature`, and `top_p` at client creation, they apply to all requests unless overridden per call:

```python
client = ai.Client("", api_key="sk-...", max_tokens=2048, temperature=0.7, top_p=0.9)

# Uses client defaults (2048 tokens, 0.7 temperature, 0.9 top_p)
response = client.completion("gpt-4", "Hello!")

# Override per request
response = client.completion("gpt-4", "Hello!", max_tokens=4096, temperature=0.9, top_p=1.0)
```

### `client.completion(model, messages, **kwargs)`

Creates a chat completion using this client's configuration.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `messages` (`str` or `list`): Either a string (user message) or a list of message dicts with `role` and `content` keys.
- `system_prompt` (`str`, optional): System prompt to use when `messages` is a string. Raises if combined with a list.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.
- `timeout` (`int`, optional): Request timeout in seconds.

**Returns:** `dict`: response containing `id`, `choices`, `usage`, etc.

**Raises:** `Error`: if `messages` is malformed, or `system_prompt` is passed together with a list `messages`.

```python
import scriptling.ai as ai

client = ai.Client("", api_key="sk-...")

# String shorthand
response = client.completion("gpt-4", "What is 2+2?")
print(response.choices[0].message.content)

# String shorthand with system prompt
response = client.completion("gpt-4", "What is 2+2?", system_prompt="You are a helpful math tutor")

# Full messages array
response = client.completion("gpt-4", [{"role": "user", "content": "What is 2+2?"}])

# Provider-specific request body fields
response = client.completion(
    "glm-4.7",
    "Think through this task",
    extra_body={"thinking": {"type": "enabled", "clear_thinking": False}}
)
```

In non-streaming completion responses, `tool_call.function.arguments` is exposed as a dict, so you can access fields with `args["name"]` or `args.get("name", default)`:

```python
tools = ai.ToolRegistry()
tools.add("get_time", "Get current time", {}, lambda args: "12:00 PM")
tools.add("read_file", "Read a file", {"path": "string"}, lambda args: os.read_file(args["path"]))

schemas = tools.build()
response = client.completion("gpt-4", [{"role": "user", "content": "What time is it?"}], tools=schemas)
```

### `client.completion_stream(model, messages, **kwargs)`

Creates a streaming chat completion using this client's configuration.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `messages` (`str` or `list`): Either a string (user message) or a list of message dicts with `role` and `content` keys.
- `system_prompt` (`str`, optional): System prompt to use when `messages` is a string.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.
- `timeout` (`int`, optional): Overall request timeout in seconds.

**Returns:** `ChatStream`: a stream object with `next()`, `next_timeout()`, `err()`, and `retry()` methods.

```python
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
```

With tool calling:

```python
tools = ai.ToolRegistry()
tools.add("get_weather", "Get weather for a city", {"city": "string"}, weather_handler)
schemas = tools.build()

stream = client.completion_stream("gpt-4", [{"role": "user", "content": "What's the weather in Paris?"}], tools=schemas)
```

### `client.ask(model, messages, **kwargs)`

Quick completion that returns text directly, with thinking blocks automatically removed. A convenience wrapper around `completion()` for simple queries where you don't need the full response object.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `messages` (`str` or `list`): Either a string (user message) or a list of message dicts.
- `system_prompt` (`str`, optional): System prompt to use when `messages` is a string.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.

**Returns:** `str`: the response text with thinking blocks removed.

```python
client = ai.Client("", api_key="sk-...")

answer = client.ask("gpt-4", "What is 2+2?")
print(answer)  # "4"

answer = client.ask("gpt-4", "Explain quantum physics", system_prompt="You are a physics professor")
```

### `client.completion_parallel(model, messages_list, **kwargs)`

Runs multiple chat completions concurrently and returns a list of responses in the same order as the input `messages_list`. Each element of `messages_list` is passed to `completion()`.

Includes **adaptive concurrency**: when a rate limit (429) is detected, the parallelism is automatically halved and workers pause briefly before continuing. Rate limit retries are handled automatically by the client (see `max_retries` on `ai.Client`).

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `messages_list` (`list`): List of messages, where each element is a string or list of message dicts.
- `max_parallel` (`int`, optional): Maximum number of concurrent requests. Default: `1`.
- `system_prompt` (`str`, optional): System prompt to use when an element of `messages_list` is a string.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.
- `timeout` (`int`, optional): Request timeout in seconds.

**Returns:** `list`: response dicts in the same order as `messages_list`. Each response may include a `retry` dict if the client retried the request: `{"attempts": 2, "rate_limit_hit": true, "total_backoff": 1.0}`.

```python
client = ai.Client("", api_key="sk-...", max_retries=3)

questions = ["What is 2+2?", "What is the capital of France?", "Explain gravity"]
results = client.completion_parallel("gpt-4", questions, max_parallel=3)
for result in results:
    if "retry" in result:
        print(f"  (retried {result['retry']['attempts']}x)")
    print(result["choices"][0]["message"]["content"])
```

### `client.ask_parallel(model, messages_list, **kwargs)`

Runs multiple chat completions concurrently and returns a list of text responses in the same order as the input `messages_list`. Thinking blocks are automatically removed.

Includes the same **adaptive concurrency** behavior as `completion_parallel()`.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `messages_list` (`list`): List of messages, where each element is a string or list of message dicts.
- `max_parallel` (`int`, optional): Maximum number of concurrent requests. Default: `1`.
- `system_prompt` (`str`, optional): System prompt to use when an element of `messages_list` is a string.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.
- `timeout` (`int`, optional): Request timeout in seconds.

**Returns:** `list`: response text strings in the same order as `messages_list`.

```python
client = ai.Client("", api_key="sk-...")

questions = ["What is 2+2?", "What is the capital of France?", "Explain gravity"]
answers = client.ask_parallel("gpt-4", questions, max_parallel=3)
for answer in answers:
    print(answer)
```

### `client.Pipeline(model, **kwargs)`

Creates a Pipeline that starts processing requests immediately as they are added via `add()`, overlapping prompt generation with inference. Call `complete()` to wait for all results. The Pipeline is the more general primitive behind `completion_parallel()` and `ask_parallel()`.

Includes the same **adaptive concurrency** as the parallel methods: on a rate limit (429), concurrency is automatically halved and workers pause before continuing.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4"`, `"gpt-3.5-turbo"`).
- `max_parallel` (`int`, optional): Maximum concurrent requests. Default: `1`.
- `ask` (`bool`, optional): If `True`, results are plain text strings instead of response dicts. Default: `False`.
- `system_prompt` (`str`, optional): System prompt applied to each string message.
- `tools` (`list`, optional): List of tool schema dicts from `ToolRegistry.build()`.
- `temperature` (`float`, optional): Sampling temperature (`0.0`-`2.0`).
- `top_p` (`float`, optional): Nucleus sampling threshold (`0.0`-`1.0`).
- `max_tokens` (`int`, optional): Maximum tokens to generate.
- `extra_body` (`dict`, optional): Provider-specific fields merged into every request body.
- `timeout` (`int`, optional): Request timeout in seconds.

**Returns:** `Pipeline`: a pipeline object with `add()` and `complete()` methods.

```python
client = ai.Client("http://localhost:1234/v1")

# Completion pipeline (ask=False, default): results are full response dicts
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

# Ask pipeline (ask=True): results are plain text strings
pipe = client.Pipeline("gpt-4", max_parallel=4, ask=True)
for q in questions:
    pipe.add(q)
answers = pipe.complete()                  # ordered list of str
```

### `pipeline.add(message)`

Queues a message for completion. Processing starts immediately as concurrency slots become available: you do not need to wait until `complete()` is called.

Accepts exactly the same message formats as `completion()` and `ask()`:

| Format | When to use |
|---|---|
| `str` | Simple user question; the pipeline's `system_prompt` (if set) is applied automatically. |
| `list` of message dicts | Full conversation turn with explicit `role`/`content` keys; `system_prompt` is ignored. |

**Parameters:**

- `message` (`str` or `list`): User message string, or list of message dicts with `role` and `content` keys.

**Returns:** `None`

```python
# String shorthand
pipe.add("What is the capital of France?")

# Full message list
pipe.add([
    {"role": "system", "content": "You are a geography expert."},
    {"role": "user",   "content": "What is the capital of France?"},
])
```

### `pipeline.complete()`

Closes the pipeline to new additions, waits for all in-flight requests to finish, and returns results in the same order as the `add()` calls. May only be called once: calling `add()` after `complete()` raises an error.

**Returns:** `list`

- When `ask=False` (default, completion mode): ordered list of response dicts, identical in structure to a single `completion()` response. Access content with `result["choices"][0]["message"]["content"]`.
- When `ask=True` (ask mode): ordered list of plain text strings with thinking blocks already removed, identical to what `ask()` returns.

**Raises:** `Error`: if `add()` is called after `complete()`.

```python
results = pipe.complete()
```

### `client.embedding(model, input)`

Creates an embedding vector for the given input text(s) using the specified model.

**Provider support:**

| Provider | Support | Notes |
|----------|---------|-------|
| OpenAI | Native | `POST /embeddings` |
| Gemini | Native | Translates to embedContent API |
| Ollama / ZAI / Mistral | Native | OpenAI-compatible endpoint |
| Claude | Not supported | Returns error |

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"text-embedding-3-small"`, `"text-embedding-3-large"`).
- `input` (`str` or `list`): Input text(s) to embed: a single string or a list of strings.

**Returns:** `dict`: response containing `data` (list of embeddings with `index`, `embedding`, `object`), `model`, and `usage`.

**Raises:** `Error`: when called against a Claude client (embeddings unsupported).

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

### `client.models()`

Lists all models available for this client configuration.

**Returns:** `dict`: response object with `object` and `data` fields. `data` contains the list of model objects.

```python
client = ai.Client("", api_key="sk-...")
models_response = client.models()
for model in models_response.data:
    print(model.id)
```

### `client.response_create(model, input, **kwargs)`

Creates a response using the OpenAI Responses API (newer structured API). It supports background processing, streaming, and compaction.

**Provider support:**

| Provider | Support | Notes |
|----------|---------|-------|
| OpenAI | Native | Direct API calls |
| Claude | Emulated | Transparently emulated via chat completions |
| Gemini | Emulated | Transparently emulated via chat completions |
| Ollama / ZAI / Mistral | Emulated | Transparently emulated via chat completions |

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4o"`, `"gpt-4"`).
- `input` (`str` or `list`): Either a string (user message content) or a list of input items (messages).
- `system_prompt` (`str`, optional): System prompt to use when `input` is a string.
- `background` (`bool`, optional): If `True`, runs asynchronously and returns immediately with `in_progress` status. Default: `False`.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.

**Returns:** `dict`: response object with `id`, `status`, `output`, `usage`, etc.

```python
client = ai.Client("", api_key="sk-...")
response = client.response_create("gpt-4o", "Hello!")
print(response.output)

# Background processing
response = client.response_create("gpt-4o", "What is AI?", background=True)
print(response.status)  # "queued" or "in_progress"
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
```

### `client.response_get(id)`

Retrieves a previously created response by its ID.

**Parameters:**

- `id` (`str`): Response ID.

**Returns:** `dict`: response object with `id`, `status`, `output`, `usage`, etc.

```python
client = ai.Client("", api_key="sk-...")
response = client.response_get("resp_123")
print(response.status)
```

### `client.response_stream(model, input, **kwargs)`

Streams a response using the OpenAI Responses API, returning a `ResponseStream` object that yields SSE events.

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4o"`, `"gpt-4"`).
- `input` (`str` or `list`): Either a string (user message content) or a list of input items.
- `system_prompt` (`str`, optional): System prompt to use when `input` is a string.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.

**Returns:** `ResponseStream`: a stream object with a `next()` method.

**Event types:**

| Event type | Key fields |
|---|---|
| `response.created` | `response` |
| `response.output_item.added` | `item`, `output_index` |
| `response.output_text.delta` | `delta`, `item_id`, `output_index`, `content_index` |
| `response.output_text.done` | `text`, `item_id`, `output_index`, `content_index` |
| `response.completed` | `response` (full ResponseObject) |
| `error` | `message` |

```python
client = ai.Client("", api_key="sk-...")

stream = client.response_stream("gpt-4o", "Count to 5")
while True:
    event = stream.next()
    if event is None:
        break
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
print()
```

### `client.response_cancel(id)`

Cancels a currently in-progress response.

**Parameters:**

- `id` (`str`): Response ID to cancel.

**Returns:** `dict`: cancelled response object.

```python
client = ai.Client("", api_key="sk-...")
response = client.response_cancel("resp_123")
```

### `client.response_delete(id)`

Deletes a response by ID, removing it from storage.

**Parameters:**

- `id` (`str`): Response ID to delete.

**Returns:** `None`

```python
client = ai.Client("", api_key="sk-...")
client.response_delete("resp_123")
```

### `client.response_compact(id)`

Compacts a response by removing intermediate reasoning steps, returning a more concise version with only the final output.

**Parameters:**

- `id` (`str`): Response ID to compact.

**Returns:** `dict`: compacted response object with reasoning removed.

```python
client = ai.Client("", api_key="sk-...")
response = client.response_create("gpt-4o", "Solve this complex problem: 2+2")
compacted = client.response_compact(response.id)
print(compacted.output)  # Output without reasoning blocks
```

## ChatStream Class

Returned by `client.completion_stream()`. Iterates over response chunks from a streaming chat completion.

### `stream.next()`

Advances to the next response chunk and returns it.

**Returns:** `dict`: the next response chunk, or `None` if the stream is complete.

```python
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

### `stream.next_timeout(timeout)`

Advances to the next response chunk, but stops waiting after `timeout` seconds.

**Parameters:**

- `timeout` (`int`): Timeout in seconds.

**Returns:** `dict`: the next response chunk, `{"timed_out": True}` if the timeout elapsed, or `None` if the stream is complete.

```python
chunk = stream.next_timeout(30)
if chunk and chunk.get("timed_out"):
    print("Stream stalled")
```

### `stream.err()`

Returns the error that caused the stream to stop, or `None` if there was no error. A cancellation error indicates the stream was cancelled (e.g. the user pressed Esc).

**Returns:** `str` or `None`: error message, or `None` if no error.

```python
err = stream.err()
if err:
    print("Stream error:", err)
```

### `stream.retry()`

Returns retry metadata if the connection was retried before streaming began, or `None` if no retries occurred. Blocks until retry metadata is available.

**Returns:** `dict` or `None`: retry metadata with keys:

- `attempts` (`int`): Total number of connection attempts (including the initial one).
- `rate_limit_hit` (`bool`): Whether a 429 rate limit error was encountered.
- `total_backoff` (`float`): Total seconds spent waiting between retries.

```python
client = ai.Client("", api_key="sk-...", max_retries=3)
stream = client.completion_stream("gpt-4", "Hello!")
result = ai.collect_stream(stream)

retry = stream.retry()
if retry:
    print(f"Retried {retry['attempts']}x, backoff: {retry['total_backoff']:.1f}s")
```

## ResponseStream Class

Returned by `client.response_stream()`. Iterates over SSE events from the Responses API.

### `stream.next()`

Advances to the next SSE event and returns it as a dict, or `None` when the stream is complete.

**Returns:** `dict`: event dict with a `type` field plus event-specific fields, or `None` if complete.

```python
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

## Message Format

Messages are dictionaries with the following keys:

- `role` (`str`): `"system"`, `"user"`, `"assistant"`, or `"tool"`.
- `content` (`str`): The message content.
- `tool_calls` (`list`, optional): Tool calls made by the assistant.
- `tool_call_id` (`str`, optional): ID for tool response messages.

```python
message = {
    "role": "user",
    "content": "What is the weather like?"
}
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

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](../../../scriptling-docs/go-integration/library-registration.md#extended-libraries).

`ai.Client` makes outbound HTTP requests to the configured AI provider endpoint (and to any `remote_servers` MCP servers configured on it). API keys and base URLs are supplied by the embedder when constructing the client: scripts only see them if the embedder explicitly passes them in. For a full risk breakdown, see the [Security Guide](../../../scriptling-docs/security.md#library-security) and [Library Registration](../../../scriptling-docs/go-integration/library-registration.md#ai--agent).

## See Also

- [scriptling.ai](../ai.md): AI namespace overview, response helpers, and tool registry
- [scriptling.ai.agent](agent.md): Agentic AI loop with automatic tool execution
- [scriptling.ai.memory](memory.md): Long-term memory store for AI agents
