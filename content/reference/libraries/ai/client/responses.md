---
title: Responses API
description: Create, stream, fetch, cancel, delete, and compact OpenAI Responses API responses with scriptling.ai.Client.
tags: [libraries, ai]
weight: 2
---

Part of [scriptling.ai.Client](../). These methods use the OpenAI Responses API rather than chat completions.

## Functions

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

## See Also

- [scriptling.ai.Client](../): creating a client, completions, `ask()`, parallel requests, pipelines, embeddings, and message format
- [Streaming Completions](../streaming/): `completion_stream()` and the `ChatStream` object
