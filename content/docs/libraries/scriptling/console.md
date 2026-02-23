---
title: scriptling.console
linkTitle: console
weight: 1
---

The `scriptling.console` library provides a TUI (terminal UI) console. Import the library and create a `Console` instance — the TUI is created at construction time and all interaction happens through the instance.

> **Note:** This library is for TUI use only. For plain stdin/stdout I/O, use the built-in `print()` and `input()` functions.

## Import

```python
import scriptling.console as console
c = console.Console()
```

## Constructor

```python
c = console.Console()
```

Creates a new Console instance backed by a TUI. Each instance is independent.

## Methods

| Method                                | Description                                                        |
| ------------------------------------- | ------------------------------------------------------------------ |
| `add_message(*args, [label=])`        | Add a message to the output area, optionally with a custom label   |
| `styled(color, text)`                 | Apply a color to text; returns the styled string                   |
| `clear_output()`                      | Clear the output area                                              |
| `stream_start([label=])`              | Begin a streaming message, optionally with a custom label          |
| `stream_chunk(text)`                  | Append a chunk to the current stream                               |
| `stream_end()`                        | Finalise the current stream                                        |
| `spinner_start([text])`               | Show a spinner                                                     |
| `spinner_stop()`                      | Hide the spinner                                                   |
| `set_progress(label, pct)`            | Set progress bar (0.0–1.0, or <0 to clear)                         |
| `set_labels(user, assistant, system)` | Set default role labels; empty string leaves label unchanged       |
| `set_status(left, right)`             | Set both status bar texts                                          |
| `set_status_left(text)`               | Set left status bar text only                                      |
| `set_status_right(text)`              | Set right status bar text only                                     |
| `register_command(name, desc, fn)`    | Register a slash command with the TUI                              |
| `remove_command(name)`                | Remove a registered slash command                                  |
| `on_submit(fn)`                       | Register handler called when user submits input                    |
| `on_escape(fn)`                       | Register a callback for Esc key                                    |
| `run()`                               | Start the console event loop (blocks until exit)                   |

## Output

```python
c.add_message("Hello", "world")               # adds a message to the output area
c.add_message("result here", label="Tool")    # message with a custom label
c.clear_output()                               # clears all messages
```

## Styling

`c.styled(color, text)` applies a foreground color to text and returns the styled string.

The `color` argument accepts a constant, a theme color name string, or a hex color.

### Color constants

| Constant            | Name string   | Description                        |
| ------------------- | ------------- | ---------------------------------- |
| `console.PRIMARY`   | `"primary"`   | Accent color (prompts, highlights) |
| `console.SECONDARY` | `"secondary"` | Secondary accent                   |
| `console.ERROR`     | `"error"`     | Error / warning color              |
| `console.DIM`       | `"dim"`       | Muted / hint text                  |
| `console.USER`      | `"user"`      | User message text color            |
| `console.TEXT`      | `"text"`      | Normal content text                |

```python
# Using constants (recommended)
c.styled(console.PRIMARY, "ScriptlingCoder")
c.styled(console.DIM, "type /exit to quit")
c.styled(console.ERROR, "WARNING: executes AI-generated code")

# Using name strings
c.styled("primary", "ScriptlingCoder")

# Hex colors (#RRGGBB or RRGGBB)
c.styled("#ff6600", "orange text")
c.styled("4eb8c8", "teal text")

# Combine with add_message
c.add_message(
    c.styled(console.PRIMARY, "MyApp") + " — " +
    c.styled(console.DIM, "type /exit to quit")
)
```

## Streaming

Use streaming to display text as it arrives (e.g. LLM token output).

```python
c.stream_start()                    # default label
c.stream_start(label="Assistant")   # custom label
for chunk in response_chunks:
    c.stream_chunk(chunk)
c.stream_end()
```

## Spinner

```python
c.spinner_start("Thinking")
result = do_work()
c.spinner_stop()
```

## Progress

```python
c.set_progress("Downloading", 0.5)   # 50%
c.set_progress("", -1)               # clear
```

## Status bar

```python
c.set_status("myapp", "v1.0")   # set both
c.set_status_left("myapp")      # left only
c.set_status_right("v1.0")      # right only
```

## Slash commands

```python
def cmd_clear(args):
    c.clear_output()

c.register_command("clear", "Clear output", cmd_clear)
c.remove_command("clear")  # remove when no longer needed
```

## Event loop

Register handlers then call `run()` to hand control to the event loop:

```python
import scriptling.console as console

c = console.Console()

def on_submit(text):
    c.stream_start()
    c.stream_chunk("You said: " + text)
    c.stream_end()

c.set_status("MyApp", "v1.0")
c.add_message(c.styled(console.PRIMARY, "MyApp") + " ready!")
c.on_submit(on_submit)
c.on_escape(lambda: c.spinner_stop())
c.run()  # blocks until /exit or Ctrl+C
```

## Labels

```python
c.set_labels("You", "Assistant", "")  # empty string leaves that label unchanged
```

## Go integration

Register the library with a scriptling interpreter:

```go
import "github.com/paularlott/scriptling/extlibs/console"

console.Register(p) // p is *scriptling.Scriptling
```

The `Console()` constructor creates a TUI instance directly — no backend registration or `SetBackend` call is needed.

The `on_submit` callback receives a `context.Context` that is cancelled when the user presses Esc. Pass this context to any cancellable operations (e.g. streaming AI completions) so they stop immediately on Esc.

## See Also

- [scriptling.ai.agent.interact](interact/) — interactive agent loop using this library
