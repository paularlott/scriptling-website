---
title: Plugin Streaming Callbacks
description: Pass a Scriptling callback into a Go plugin and stream events back while the function runs.
linkTitle: Plugin Callbacks
weight: 35
---

This tutorial builds a Go plugin that accepts a Scriptling callback. The plugin calls that callback multiple times before returning, which is useful for streaming LLM tokens, progress updates, or event notifications.

## Plugin Code

Create `main.go`:

```go
package main

import (
    "context"

    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

type tokenEvent struct {
    Token string `json:"token"`
    Index int    `json:"index"`
}

func main() {
    streamBuilder := object.NewFunctionBuilder()
    streamBuilder.Function(func(ctx context.Context, onEvent plugin.Callback) (string, error) {
        tokens := []string{"Hello", ", ", "Ada"}
        for i, token := range tokens {
            if _, err := onEvent.Call(ctx, tokenEvent{Token: token, Index: i}); err != nil {
                return "", err
            }
        }
        if _, err := onEvent.Call(ctx, []any{"done", len(tokens)}); err != nil {
            return "", err
        }
        return "Hello, Ada", nil
    })

    server := plugin.NewServer("callback", "1.0.0", "Callback streaming example")
    server.RegisterFunc("stream", streamBuilder)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Build the plugin executable into a plugin directory:

```bash
mkdir -p ./plugins
go build -o ./plugins/callback .
```

## Scriptling Host Code

```python
import plugin.callback

events = []

def on_event(event):
    events.append(event)
    return "ack"

text = plugin.callback.stream(on_event)
print(text)
print(events[0]["token"])
print(events[3][0])
```

Run it:

```bash
scriptling --plugin-dir ./plugins scriptling_file.sl
```

## Callback Lifetime

The callback id is valid only while `plugin.callback.stream(on_event)` is running. The plugin may call `onEvent.Call(...)` any number of times before returning. After `stream` returns or fails, the callback id expires and any later attempt to use it returns `unknown callback`.

Callbacks run synchronously on the same Scriptling environment call stack that started the plugin call. A callback should do quick work such as collecting events, printing progress, or updating local state.

## Payloads

`Callback.Call` accepts normal Go values. Maps and exported struct fields arrive as Scriptling dictionaries, and slices or arrays arrive as Scriptling lists.

```go
onEvent.Call(ctx, map[string]any{"token": "Hello"})
onEvent.Call(ctx, []any{"done", 3})
onEvent.Call(ctx, tokenEvent{Token: "Hello", Index: 0})
```

If the Scriptling callback raises an error, `Callback.Call` returns that error. Return it from the plugin function to fail the outer plugin call.
