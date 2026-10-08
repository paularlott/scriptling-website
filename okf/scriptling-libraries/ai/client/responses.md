---
description: Create, stream, fetch, cancel, delete, and compact OpenAI Responses API responses with scriptling.ai.Client.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/ai/client/responses/
sources:
    - resource: https://scriptling.dev/reference/libraries/ai/client/responses/
status: stable
tags:
    - libraries
    - ai
title: Responses API
type: API Reference
---
# Responses API

Part of [scriptling.ai.Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md). These methods use the OpenAI Responses API rather than chat completions.

OpenAI and Grok use the provider's own Responses API, which stores responses at the provider. Every other provider emulates it over chat completions: responses are kept in the scriptling process, expire after 15 minutes idle and are lost on restart. `client.supports("responses")` tells you which you have. Either way, responses are only visible to clients with the same provider, base URL and API key.

## Functions

### `client.response_create(model, input, **kwargs)`

Creates a response using the OpenAI Responses API (newer structured API). It supports multi-turn conversations, tool calling, background processing, streaming, and compaction.

**Provider support:**

| Provider | Support | Notes |
|----------|---------|-------|
| OpenAI | Native | Direct API calls |
| Grok | Native | Direct API calls; background responses run in the client, as xAI doesn't support them |
| Claude | Emulated | Transparently emulated via chat completions |
| Gemini | Emulated | Transparently emulated via chat completions |
| Ollama / ZAI / Mistral | Emulated | Transparently emulated via chat completions |

**Parameters:**

- `model` (`str`): Model identifier (e.g. `"gpt-4o"`, `"gpt-4"`).
- `input` (`str` or `list`): Either a string (user message content) or a list of input items (messages).
- `system_prompt` (`str`, optional): System prompt to use when `input` is a string.
- `instructions` (`str`, optional): Instructions for this request. They are not carried over when a later request continues the conversation.
- `previous_response_id` (`str`, optional): Continue the conversation of this response, without resending it.
- `tools` (`list`, optional): Tool definitions, e.g. from `ToolRegistry.build()`. The model's tool calls are returned as `function_call` items in `output` for the script to run: see the tool calling example below.
- `store` (`bool`, optional): Set `False` to keep nothing: the response can't be retrieved or continued. Default: `True`.
- `background` (`bool`, optional): If `True`, runs asynchronously and returns immediately with `in_progress` status. Default: `False`.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.

**Returns:** `dict`: response object with `id`, `status`, `output`, `usage`, etc. Use `ai.text(response)` for its text and `ai.tool_calls(response)` for its tool calls.

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

# Multi-turn: continue a conversation by ID
first = client.response_create("gpt-4o", "My name is Zorblat.")
second = client.response_create("gpt-4o", "What is my name?", previous_response_id=first.id)
print(ai.text(second))  # "Your name is Zorblat."
```

**Tool calling:** pass `tools`, run the calls the model asks for, and send the results back with `ai.tool_outputs()`, continuing from the response that asked:

```python
import scriptling.ai as ai

def get_weather(args):
    return "Sunny, 21C in " + args["city"]

tools = ai.ToolRegistry()
tools.add("get_weather", "Current weather for a city", {"city": "string"}, get_weather)

client = ai.Client("", provider=ai.GROK, api_key="xai-...")
response = client.response_create("grok-4.7", "What's the weather in Paris?", tools=tools.build())
while True:
    calls = ai.tool_calls(response)
    if not calls:
        break
    results = ai.execute_tool_calls(tools, calls)
    response = client.response_create("grok-4.7", ai.tool_outputs(results),
                                      previous_response_id=response.id, tools=tools.build())
print(ai.text(response))
```

Tools from the client's `remote_servers` are run by the client itself and never appear in `output`.

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
- `instructions`, `previous_response_id`, `tools`, `store` (optional): As for `response_create()`.
- `extra_body` (`dict`, optional): Provider-specific fields to merge into the request body.

**Returns:** `ResponseStream`: a stream object with a `next()` method.

**Event types:**

| Event type | Key fields |
|---|---|
| `response.created` | `response` |
| `response.output_item.added` | `item`, `output_index` |
| `response.output_text.delta` | `delta`, `item_id`, `output_index`, `content_index` |
| `response.output_text.done` | `text`, `item_id`, `output_index`, `content_index` |
| `response.function_call_arguments.delta` | `delta`, `item_id`, `output_index` (tool calls, when `tools` is passed) |
| `response.function_call_arguments.done` | `arguments`, `name`, `item_id`, `output_index` |
| `response.output_item.done` | `item` (a finished message or `function_call` item), `output_index` |
| `response.completed` | `response` (full ResponseObject; pass it to `ai.tool_calls()`) |
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

### `client.response_compact(model, previous_response_id=None, input=None, instructions=None)`

Compacts a long conversation into a short `output` to use in its place: the conversation of `previous_response_id`, if given, followed by `input`. Pass the result's `output` as the input of the next `response_create()` call, adding the new message, instead of `previous_response_id`.

OpenAI and Grok use the provider's compaction endpoint (Grok needs `input` and doesn't accept `previous_response_id`). Other providers have the model summarise the conversation into a single message.

**Parameters:**

- `model` (`str`): Model used for compaction.
- `previous_response_id` (`str`, optional): Response whose conversation to compact.
- `input` (`str` or `list`, optional): Further conversation to include.
- `instructions` (`str`, optional): Instructions the conversation was run under.

At least one of `previous_response_id` and `input` is required.

**Returns:** `dict`: compaction with `id`, `object` (`"response.compaction"`), `output` and `usage`.

```python
client = ai.Client("", api_key="sk-...")
response = client.response_create("gpt-4o", "My name is Zorblat. Let's talk about tea.")
compacted = client.response_compact("gpt-4o", previous_response_id=response.id)
response = client.response_create("gpt-4o", compacted.output + [
    {"role": "user", "content": "What is my name?"}
])
print(ai.text(response))
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

- [scriptling.ai.Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md): creating a client, completions, `ask()`, parallel requests, pipelines, embeddings, and message format
- [Streaming Completions](https://scriptling.dev/okf/scriptling-libraries/ai/client/streaming.md): `completion_stream()` and the `ChatStream` object
