---
title: scriptling.console
linkTitle: console
weight: 1
---

The `scriptling.console` library provides console I/O with a built-in TUI. Scripts can register handlers, stream output, control the status bar, and call `console.run()` to start the interactive event loop — the TUI starts automatically on demand.

> **Note:** When embedded without the scriptling CLI, `input` and `print` fall back to plain stdin/stdout. All other functions are no-ops unless a custom backend is registered via `SetBackend`.

## Import

```python
import scriptling.console as console
```

## Functions

| Function                              | Description                                                        |
| ------------------------------------- | ------------------------------------------------------------------ |
| `input([prompt])`                     | Read a line from input                                             |
| `print(*args, [label=])`              | Write a message to the output area, optionally with a custom label |
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
| `register_command(name, desc, fn)`    | Register a slash command with the backend                          |
| `remove_command(name)`                | Remove a registered slash command                                  |
| `on_submit(fn)`                       | Register handler called when user submits input                    |
| `on_escape(fn)`                       | Register a callback for Esc key                                    |
| `on_init(fn)`                         | Register a callback invoked once when the console starts           |
| `run()`                               | Start the console event loop (blocks until exit)                   |

## Output

```python
console.print("Hello", "world")               # adds a message to the output area
console.print("result here", label="Tool")    # message with a custom label
console.clear_output()                         # clears all messages
```

## Styling

`console.styled(color, text)` applies a foreground color to text and returns the styled string for use with `console.print` or anywhere text is displayed.

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
console.styled(console.PRIMARY, "ScriptlingCoder")
console.styled(console.DIM, "type /exit to quit")
console.styled(console.ERROR, "WARNING: executes AI-generated code")

# Using name strings
console.styled("primary", "ScriptlingCoder")

# Hex colors (#RRGGBB or RRGGBB)
console.styled("#ff6600", "orange text")
console.styled("4eb8c8", "teal text")

# Combine with print
console.print(
    console.styled(console.PRIMARY, "MyApp") + " — " +
    console.styled(console.DIM, "type /exit to quit")
)
```

Falls back to plain text when no TUI backend is active.

## Streaming

Use streaming to display text as it arrives (e.g. LLM token output).

```python
console.stream_start()                    # default label
console.stream_start(label="Assistant")   # custom label
for chunk in response_chunks:
    console.stream_chunk(chunk)
console.stream_end()
```

## Spinner

```python
console.spinner_start("Thinking")
result = do_work()
console.spinner_stop()
```

## Progress

```python
console.set_progress("Downloading", 0.5)   # 50%
console.set_progress("", -1)               # clear
```

## Status bar

```python
console.set_status("myapp", "v1.0")   # set both
console.set_status_left("myapp")      # left only
console.set_status_right("v1.0")      # right only
```

## Slash commands

Register a slash command with the backend. Under the TUI this adds the command to the palette (accessible by typing `/`).

```python
def cmd_clear(args):
    console.clear_output()

console.register_command("clear", "Clear output", cmd_clear)
console.remove_command("clear")  # remove when no longer needed
```

## Event loop

Scripts that want to drive the TUI register their handlers then call `console.run()` to hand control to the event loop:

```python
def on_submit(text):
    console.stream_start()
    console.stream_chunk("You said: " + text)
    console.stream_end()

def on_ready():
    console.print(console.styled("primary", "MyApp") + " ready!")

console.on_submit(on_submit)
console.on_escape(lambda: console.spinner_stop())
console.on_init(on_ready)  # called once after TUI starts, before blocking
console.run()  # blocks until /exit or Ctrl+C
```

`on_init` is useful for printing a welcome message or setting initial state. It fires after the TUI backend is live so `console.print`, `console.set_status`, etc. all work correctly.

## Labels

Set the display labels used for user, assistant, and system messages:

```python
console.set_labels("You", "Assistant", "")  # empty string leaves that label unchanged
```

## Plain fallback behaviour

When running embedded without the scriptling CLI and no custom backend is registered:

| Function                                              | Behaviour               |
| ----------------------------------------------------- | ----------------------- |
| `input`                                               | Reads a line from stdin |
| `print`                                               | Writes to stdout        |
| `stream_start` / `stream_chunk` / `stream_end`        | No-op                   |
| `spinner_start` / `spinner_stop`                      | No-op                   |
| `set_progress`                                        | No-op                   |
| `set_labels`                                          | No-op                   |
| `set_status` / `set_status_left` / `set_status_right` | No-op                   |
| `register_command` / `remove_command`                 | No-op                   |
| `on_submit` / `on_escape` / `on_init`                 | No-op                   |
| `clear_output`                                        | No-op                   |
| `run`                                                 | Returns immediately     |
| `styled`                                              | Returns text unchanged  |

## Go integration

Register the library with a scriptling interpreter:

```go
import "github.com/paularlott/scriptling/extlibs/console"

console.Register(p) // p is *scriptling.Scriptling
```

To use the TUI backend (from `github.com/paularlott/cli/tui`), implement `ConsoleBackend` and call `SetBackend` before running the script:

```go
console.SetBackend(myBackend) // call before p.Eval(...)
```

The `ConsoleBackend` interface:

```go
type ConsoleBackend interface {
    Input(prompt string, env *object.Environment) (string, error)
    Print(text string, env *object.Environment)
    PrintAs(label, text string, env *object.Environment)
    StreamStart()
    StreamStartAs(label string)  // called when label kwarg is provided to stream_start
    StreamChunk(chunk string)
    StreamEnd()
    SpinnerStart(text string)
    SpinnerStop()
    SetProgress(label string, pct float64)
    SetLabels(user, assistant, system string)
    SetStatus(left, right string)
    SetStatusLeft(left string)
    SetStatusRight(right string)
    RegisterCommand(name, description string, handler func(args string))
    RemoveCommand(name string)
    OnSubmit(fn func(ctx context.Context, text string))
    OnEscape(fn func())
    ClearOutput()
    Run() error
}
```

The `OnSubmit` callback receives a `context.Context` that is cancelled when the user presses Esc. Pass this context to any cancellable operations (e.g. streaming AI completions) so they stop immediately on Esc.

The scriptling CLI wires the TUI automatically — scripts running under `scriptling-cli` get the full TUI backend without any extra setup.

## See Also

- [scriptling.ai.agent.interact](interact/) — interactive agent loop using this library
