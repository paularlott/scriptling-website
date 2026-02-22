---
title: scriptling.console
linkTitle: console
weight: 1
---

The `scriptling.console` library provides console I/O backed by the TUI when running under the scriptling CLI. It is designed for scripts that want to drive the terminal UI — registering commands, handling submissions, streaming output, and controlling the status bar.

> **Note:** `scriptling.console` requires a TUI backend to be active. It is intended for use with the scriptling CLI. In embedded or headless environments the plain fallback is a no-op for most functions.

## Import

```python
import scriptling.console as console
```

## Functions

| Function | Description |
|----------|-------------|
| `input([prompt])` | Read a line from input |
| `print(*args)` | Write a message to the output area |
| `print_as(label, *args)` | Write a message with a custom label |
| `clear_output()` | Clear the output area |
| `stream_start()` | Begin a streaming message |
| `stream_start_as(label)` | Begin a streaming message with a custom label |
| `stream_chunk(text)` | Append a chunk to the current stream |
| `stream_end()` | Finalise the current stream |
| `spinner_start([text])` | Show a spinner |
| `spinner_stop()` | Hide the spinner |
| `set_progress(label, pct)` | Set progress bar (0.0–1.0, or <0 to clear) |
| `set_labels(user, assistant, system)` | Set default role labels; empty string leaves label unchanged |
| `set_status(left, right)` | Set both status bar texts |
| `set_status_left(text)` | Set left status bar text only |
| `set_status_right(text)` | Set right status bar text only |
| `register_command(name, desc, fn)` | Register a slash command with the backend |
| `remove_command(name)` | Remove a registered slash command |
| `on_submit(fn)` | Register handler called when user submits input |
| `on_escape(fn)` | Register a callback for Esc key |
| `run()` | Start the console event loop (blocks until exit) |

## Output

```python
console.print("Hello", "world")          # adds a message to the output area
console.print_as("Tool", "result here")  # message with a custom label
console.clear_output()                    # clears all messages
```

## Streaming

Use streaming to display text as it arrives (e.g. LLM token output).

```python
console.stream_start()                    # default label
console.stream_start_as("Assistant")      # custom label
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

console.on_submit(on_submit)
console.on_escape(lambda: console.spinner_stop())
console.run()  # blocks until /exit or Ctrl+C
```

## Labels

Set the display labels used for user, assistant, and system messages:

```python
console.set_labels("You", "Assistant", "")  # empty string leaves that label unchanged
```

## Plain fallback behaviour

When no TUI backend is registered:

| Function | Behaviour |
|----------|-----------|
| `input` | Reads a line from stdin |
| `print` / `print_as` | Writes to stdout |
| `stream_start` / `stream_start_as` / `stream_chunk` / `stream_end` | No-op |
| `spinner_start` / `spinner_stop` | No-op |
| `set_progress` | No-op |
| `set_labels` | No-op |
| `set_status` / `set_status_left` / `set_status_right` | No-op |
| `register_command` / `remove_command` | No-op |
| `on_submit` / `on_escape` | No-op |
| `clear_output` | No-op |
| `run` | Returns immediately |

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
    StreamStartAs(label string)
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
