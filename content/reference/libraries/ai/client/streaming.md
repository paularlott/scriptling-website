---
title: Streaming Completions
description: Stream chat completions from scriptling.ai.Client with completion_stream() and the ChatStream object.
tags: [libraries, ai]
weight: 1
---

Part of [scriptling.ai.Client](../). `completion_stream()` takes the same arguments as [`completion()`](../#clientcompletionmodel-messages-kwargs) but returns a `ChatStream` that yields chunks as they arrive.

## Functions

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

## See Also

- [scriptling.ai.Client](../): creating a client, completions, `ask()`, parallel requests, pipelines, embeddings, and message format
- [Responses API](../responses/): `response_stream()` and the `ResponseStream` object
