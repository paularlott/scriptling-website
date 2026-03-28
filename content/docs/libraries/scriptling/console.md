---
title: scriptling.console
linkTitle: console
weight: 1
---

The `scriptling.console` library provides a TUI (terminal UI) console. Import the library and use module-level functions to interact with it. There is a single shared TUI instance — no constructor needed.

> **Note:** This library is for TUI use only. For plain stdin/stdout I/O, use the built-in `print()` and `input()` functions.

## Import

```python
import scriptling.console as console
```

## Overview

The console uses a module-level API. Everything is accessed through the `console` module directly — there is no `Console()` constructor. The TUI is a singleton shared across your entire application.

**Module-level** — TUI control, layout, overlays, callbacks:

```python
console.panel("logs")        # get a named panel
console.main_panel()         # get the main chat panel
console.create_panel(...)    # create a panel
console.add_left(panel)      # layout
console.add_right(panel)     # layout
console.clear_layout()       # layout
console.has_panels()         # check layout state
console.styled(color, text)  # theme helper
console.set_status(l, r)     # status bar
console.spinner_start(text)  # overlay
console.set_progress(l, pct) # overlay
console.on_submit(fn)        # callback
console.on_escape(fn)        # callback
console.run()                # event loop
```

**Panel** — all content operations:

```python
main = console.main_panel()
main.add_message("Hello")
main.stream_start()
main.stream_chunk("chunk")
main.stream_end()
main.clear()

logs = console.panel("logs")
logs.write("entry\n")
logs.set_content("full content")
```

## Module Functions

| Function                                | Description                                                        |
| --------------------------------------- | ------------------------------------------------------------------ |
| `panel([name])`                         | Get a Panel by name (default: `"main"`)                            |
| `main_panel()`                          | Get the main chat panel                                            |
| `create_panel([name], **kwargs)`        | Create a new panel (independent of layout)                         |
| `add_left(panel)`                       | Add a panel to the left of main                                    |
| `add_right(panel)`                      | Add a panel to the right of main                                   |
| `clear_layout()`                        | Remove layout tree but keep all panels                             |
| `has_panels()`                          | Return `True` if multi-panel layout is active                      |
| `styled(color, text)`                   | Apply a color to text; returns the styled string                   |
| `set_status(left, right)`               | Set both status bar texts                                          |
| `set_status_left(text)`                 | Set left status bar text only                                      |
| `set_status_right(text)`                | Set right status bar text only                                     |
| `set_labels(user, assistant, system)`   | Set default role labels; empty string leaves label unchanged       |
| `register_command(name, desc, fn)`      | Register a slash command with the TUI                              |
| `remove_command(name)`                  | Remove a registered slash command                                  |
| `spinner_start([text])`                 | Show a spinner (TUI overlay, not per-panel)                       |
| `spinner_stop()`                        | Hide the spinner                                                   |
| `set_progress(label, pct)`              | Set progress bar (0.0–1.0, or <0 to clear)                         |
| `on_submit(fn)`                         | Register handler called when user submits input                    |
| `on_escape(fn)`                         | Register a callback for Esc key                                    |
| `run()`                                 | Start the console event loop (blocks until exit)                   |

## Styling

`console.styled(color, text)` applies a foreground color to text and returns the styled string.

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

# Combine with add_message
main = console.main_panel()
main.add_message(
    console.styled(console.PRIMARY, "MyApp") + " — " +
    console.styled(console.DIM, "type /exit to quit")
)
```

## Output (Main Panel)

```python
main = console.main_panel()
main.add_message("Hello", "world")               # adds a message to the main area
main.add_message("result here", label="Tool")    # message with a custom label
main.clear()                                     # clears all messages
```

## Streaming

Use streaming to display text as it arrives (e.g. LLM token output).

```python
main = console.main_panel()
main.stream_start()                    # default label
main.stream_start(label="Assistant")   # custom label
for chunk in response_chunks:
    main.stream_chunk(chunk)
main.stream_end()
```

## Spinner

Spinner is a TUI-level overlay — it's not tied to any specific panel.

```python
console.spinner_start("Thinking")
result = do_work()
console.spinner_stop()
```

## Progress

Progress is a TUI-level overlay — it's not tied to any specific panel.

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

```python
def cmd_clear(args):
    console.main_panel().clear()

console.register_command("clear", "Clear output", cmd_clear)
console.remove_command("clear")  # remove when no longer needed
```

## Event loop

Register handlers then call `run()` to hand control to the event loop:

```python
import scriptling.console as console

main = console.main_panel()

def on_submit(text):
    main.stream_start()
    main.stream_chunk("You said: " + text)
    main.stream_end()

console.set_status("MyApp", "v1.0")
main.add_message(console.styled(console.PRIMARY, "MyApp") + " ready!")
console.on_submit(on_submit)
console.on_escape(lambda: console.spinner_stop())
console.run()  # blocks until /exit or Ctrl+C
```

## Labels

```python
console.set_labels("You", "Assistant", "")  # empty string leaves that label unchanged
```

## Panels

The console supports a multi-panel layout with a main chat area in the center, plus optional left and right side panels. Use the two-step builder pattern: **create panels first**, then **add them to the layout**.

### Layout

```
┌──────────┬─────────────────────┬──────────────┐
│  Left    │      Main Chat      │  Right Top   │
│  Panel   │                     ├──────────────┤
│          │                     │ Right Bottom │
└──────────┴─────────────────────┴──────────────┘
```

### Builder API

Use `create_panel` to create panels with configuration, then attach them to the layout with `add_left`, `add_right`, `add_row`, and `add_column`.

#### console.create_panel(name="", **kwargs)

Create a new panel. Panels exist independently of the layout — they can be added and removed without losing their content.

**Parameters:**
- `name` (str, optional): Panel identifier
- `width` (int): Positive = columns, negative = percentage (e.g. -25 = 25%)
- `height` (int): Positive = rows, negative = percentage (e.g. -50 = 50%)
- `min_width` (int): Minimum width to render; panel hides if narrower
- `scrollable` (bool): `True` = content scrolls, `False` = fixed viewport
- `title` (str): Title shown in the border
- `no_border` (bool): `True` = hide border
- `skip_focus` (bool): `True` = exclude from Tab focus cycle

**Returns:** `Panel` — a panel instance

#### console.add_left(panel)

Add a panel to the left of the main panel.

**Parameters:**
- `panel` (Panel): Panel to add

#### console.add_right(panel)

Add a panel to the right of the main panel.

**Parameters:**
- `panel` (Panel): Panel to add

#### console.clear_layout()

Remove the layout tree but keep all panels and their content. Panels can be re-added with `add_left`/`add_right` to toggle layouts.

#### panel.add_row(child)

Add a child panel as a vertical row (appends top to bottom). A panel cannot mix rows and columns — adding a row to a panel that already has columns is a no-op.

**Parameters:**
- `child` (Panel): Child panel to add

#### panel.add_column(child)

Add a child panel as a horizontal column (appends left to right). A panel cannot mix rows and columns — adding a column to a panel that already has rows is a no-op.

**Parameters:**
- `child` (Panel): Child panel to add

### Basic example

```python
# Create panels
logs = console.create_panel("logs", width=-25, min_width=15, scrollable=True, title="Logs")
right = console.create_panel(width=-30, min_width=16)
cpu_panel = console.create_panel("cpu", height=-50, title="CPU")
mem_panel = console.create_panel("mem", height=-50, title="Memory")

# Build layout tree
right.add_row(cpu_panel)
right.add_row(mem_panel)

# Attach to console
console.add_left(logs)
console.add_right(right)
```

### Toggle layout

Panels persist across layout changes — their content and scroll state are preserved when you clear and re-add them:

```python
def cmd_layout(args):
    if console.has_panels():
        console.clear_layout()
    else:
        console.add_left(logs)
        console.add_right(right)

console.register_command("layout", "Toggle panel layout", cmd_layout)
```

### Full dashboard example

```python
import scriptling.console as console
import scriptling.runtime as runtime
import time

# Create panels
logs = console.create_panel("logs", width=-25, min_width=15, scrollable=True, title="Logs")
right = console.create_panel(width=-30, min_width=16)
cpu_panel = console.create_panel("cpu", height=-50, title="CPU")
mem_panel = console.create_panel("mem", height=-50, title="Memory")

# Build layout
right.add_row(cpu_panel)
right.add_row(mem_panel)
console.add_left(logs)
console.add_right(right)

# Background task updates the logs panel
shared = runtime.sync.Shared("state", {"count": 0})

def pump_logs():
    while True:
        state = shared.get()
        count = state["count"]
        timestamp = time.strftime("%H:%M:%S")
        line = console.styled(console.DIM, timestamp) + " Log entry #" + str(count)
        logs.write(line + "\n")
        state["count"] = count + 1
        shared.set(state)
        time.sleep(1)

runtime.background("log_pump", "pump_logs")

main = console.main_panel()
console.on_submit(lambda text: main.add_message("Echo: " + text))
console.run()
```

#### console.panel(name)

Get an existing `Panel` instance by name. Returns `None` if the panel doesn't exist. Defaults to `"main"` if no name is given.

**Parameters:**
- `name` (str): Panel name

**Returns:** `Panel` or `None`

```python
logs = console.panel("logs")
if logs:
    logs.write("Application started\n")
```

#### console.has_panels()

Return `True` if a multi-panel layout is active.

```python
if console.has_panels():
    console.clear_layout()  # toggle back to single panel
```

### Panel class

`console.create_panel(name)` and `console.panel(name)` return a `Panel` instance with its own methods. Panels support both raw text content and message-based content.

#### Panel methods

| Method                          | Description                                           |
| ------------------------------- | ----------------------------------------------------- |
| `write(text)`                   | Append text to the panel                              |
| `set_content(text)`             | Replace all panel content                             |
| `clear()`                       | Remove all panel content                              |
| `set_title(title)`              | Set the panel border title                            |
| `set_color(color)`              | Set border/accent color (name or hex)                 |
| `set_scrollable(bool)`          | Set whether content scrolls                           |
| `add_message(*args, [label=])`  | Add a message to the panel                            |
| `stream_start([label=])`        | Begin a streaming message                             |
| `stream_chunk(text)`            | Append a chunk to the current stream                  |
| `stream_end()`                  | Finalise the current stream                           |
| `add_row(panel)`                | Add a child panel as a vertical row                   |
| `add_column(panel)`             | Add a child panel as a horizontal column              |
| `scroll_to_top()`               | Scroll to top of panel content                        |
| `scroll_to_bottom()`            | Scroll to bottom of panel content                     |
| `size()`                        | Return `[width, height]` of the panel                 |
| `styled(color, text)`           | Apply theme color to text                             |
| `write_at(row, col, text)`      | Write text at a specific position                     |
| `clear_line(row)`               | Clear a specific line                                 |

### Focus and navigation

- **Tab** cycles focus through all visible, non-skip-focus panels (left children, main, right children)
- Focused panel border uses the panel's color; unfocused uses the theme's dim color
- Call `clear_layout()` to reset to single-panel mode at any time
- Panels and their content survive `clear_layout()` — re-add them with `add_left`/`add_right`

## Background tasks

Background tasks can access panels without needing a Console instance:

```python
def pump_logs():
    # Look up the panel by name — works from any background task
    logs = console.panel("logs")
    if logs:
        logs.write("Background message\n")
```

## Go integration

Register the library with a scriptling interpreter:

```go
import "github.com/paularlott/scriptling/extlibs/console"

console.Register(p) // p is *scriptling.Scriptling
```

The TUI is created automatically when first accessed. Use `console.TUI()` to get the shared `*tui.TUI` from Go code.

The `on_submit` callback receives a `context.Context` that is cancelled when the user presses Esc. Pass this context to any cancellable operations (e.g. streaming AI completions) so they stop immediately on Esc.

## See Also

- [scriptling.ai.agent.interact](../interact/) — interactive agent loop using this library
