---
title: scriptling.console
linkTitle: console
description: TUI (terminal UI) console for building interactive chat-style applications.
weight: 1
---

The `scriptling.console` library provides a TUI (terminal UI) console for building interactive chat-style applications, with support for layout panels, streaming output, and slash commands. There is a single shared TUI instance: no constructor needed; everything is accessed through module-level functions.

> **Note:** This library is for TUI use only. For plain stdin/stdout I/O, use the built-in `print()` and `input()` functions.

## Available Functions

| Function | Description |
|----------|-------------|
| `panel([name])` | Get a Panel by name (default: `"main"`) |
| `main_panel()` | Get the main chat panel |
| `create_panel([name], **kwargs)` | Create a new panel (independent of layout) |
| `add_left(panel)` | Add a panel to the left of main |
| `add_right(panel)` | Add a panel to the right of main |
| `clear_layout()` | Remove the layout tree but keep all panels |
| `has_panels()` | Return `True` if a multi-panel layout is active |
| `styled(color, text)` | Apply a color to text and return the styled string |
| `set_status(left, right)` | Set both status bar texts |
| `set_status_left(text)` | Set left status bar text only |
| `set_status_right(text)` | Set right status bar text only |
| `set_labels(user, assistant, system)` | Set default role labels; empty string leaves a label unchanged |
| `register_command(name, description, fn)` | Register a slash command with the TUI |
| `remove_command(name)` | Remove a registered slash command |
| `spinner_start([text])` | Show a spinner (TUI overlay, not per-panel) |
| `spinner_stop()` | Hide the spinner |
| `set_progress(label, pct)` | Set the progress bar (`0.0`-`1.0`, or `<0` to clear) |
| `on_submit(fn)` | Register a handler called when the user submits input |
| `on_escape(fn)` | Register a callback for the Esc key |
| `run()` | Start the console event loop (blocks until exit) |

Color constants `console.PRIMARY`, `console.SECONDARY`, `console.ERROR`, `console.DIM`, `console.USER`, and `console.TEXT` are also available for use with `styled()`: see [Styling](#styled) below.

Panel objects returned by `panel()` and `create_panel()` have their own methods, documented under [Panel Methods](#panel-methods) below.

## Functions

### `panel(name="main")`

Gets an existing `Panel` instance by name. Returns `None` if the panel doesn't exist.

**Parameters:**
- `name` (`str`, optional): Panel name. Default: `"main"`.

**Returns:** `Panel` or `None`.

```python
import scriptling.console as console

logs = console.panel("logs")
if logs:
    logs.write("Application started\n")
```

### `main_panel()`

Gets the main chat panel.

**Returns:** `Panel`: the main panel instance.

```python
main = console.main_panel()
main.add_message("Hello", "world")
```

### `create_panel(name="", **kwargs)`

Creates a new panel. Panels exist independently of the layout: they can be added and removed without losing their content. Use `add_left`/`add_right` (or `add_row`/`add_column` on a parent panel) to place a created panel into the layout.

**Parameters:**
- `name` (`str`, optional): Panel identifier. Default: `""`.
- `width` (`int`, optional): Positive = columns, negative = percentage (e.g. `-25` = 25%).
- `height` (`int`, optional): Positive = rows, negative = percentage (e.g. `-50` = 50%).
- `min_width` (`int`, optional): Minimum width to render; the panel hides if narrower.
- `scrollable` (`bool`, optional): `True` = content scrolls, `False` = fixed viewport. Default: `False`.
- `title` (`str`, optional): Title shown in the border.
- `no_border` (`bool`, optional): `True` = hide border. Default: `False`.
- `skip_focus` (`bool`, optional): `True` = exclude from the Tab focus cycle. Default: `False`.

**Returns:** `Panel`: a panel instance.

```python
logs = console.create_panel("logs", width=-25, min_width=15, scrollable=True, title="Logs")
right = console.create_panel(width=-30, min_width=16)
cpu_panel = console.create_panel("cpu", height=-50, title="CPU")
mem_panel = console.create_panel("mem", height=-50, title="Memory")

right.add_row(cpu_panel)
right.add_row(mem_panel)

console.add_left(logs)
console.add_right(right)
```

### `add_left(panel)`

Adds a panel to the left of the main panel.

**Parameters:**
- `panel` (`Panel`): Panel to add.

**Returns:** `None`

### `add_right(panel)`

Adds a panel to the right of the main panel.

**Parameters:**
- `panel` (`Panel`): Panel to add.

**Returns:** `None`

### `clear_layout()`

Removes the layout tree but keeps all panels and their content. Panels can be re-added with `add_left`/`add_right` to toggle layouts, preserving scroll state.

**Returns:** `None`

```python
def cmd_layout(args):
    if console.has_panels():
        console.clear_layout()
    else:
        console.add_left(logs)
        console.add_right(right)

console.register_command("layout", "Toggle panel layout", cmd_layout)
```

### `has_panels()`

Returns `True` if a multi-panel layout is currently active.

**Returns:** `bool`: `True` if a multi-panel layout is active.

```python
if console.has_panels():
    console.clear_layout()  # toggle back to single panel
```

### `styled(color, text)`

Applies a foreground color to text and returns the styled string. `color` accepts a constant (`console.PRIMARY`, `console.SECONDARY`, `console.ERROR`, `console.DIM`, `console.USER`, `console.TEXT`), a theme color name string (`"primary"`, `"secondary"`, `"error"`, `"dim"`, `"user"`, `"text"`), or a hex color (`"#ff6600"` or `"ff6600"`).

**Parameters:**
- `color` (`str`): Color constant, theme name string, or hex color.
- `text` (`str`): Text to style.

**Returns:** `str`: the styled text.

```python
console.styled(console.PRIMARY, "ScriptlingCoder")
console.styled(console.DIM, "type /exit to quit")
console.styled(console.ERROR, "WARNING: executes AI-generated code")
console.styled("primary", "ScriptlingCoder")
console.styled("#ff6600", "orange text")

main = console.main_panel()
main.add_message(
    console.styled(console.PRIMARY, "MyApp") + ": " +
    console.styled(console.DIM, "type /exit to quit")
)
```

### `set_status(left, right)`

Sets both status bar texts at once.

**Parameters:**
- `left` (`str`): Left-aligned status text.
- `right` (`str`): Right-aligned status text.

**Returns:** `None`

```python
console.set_status("myapp", "v1.0")
```

### `set_status_left(text)`

Sets the left status bar text only.

**Parameters:**
- `text` (`str`): Left-aligned status text.

**Returns:** `None`

### `set_status_right(text)`

Sets the right status bar text only.

**Parameters:**
- `text` (`str`): Right-aligned status text.

**Returns:** `None`

### `set_labels(user, assistant, system)`

Sets the default role labels used by `add_message`/`stream_start`. An empty string leaves the corresponding label unchanged.

**Parameters:**
- `user` (`str`): Label for user messages.
- `assistant` (`str`): Label for assistant messages.
- `system` (`str`): Label for system messages.

**Returns:** `None`

```python
console.set_labels("You", "Assistant", "")  # empty string leaves system label unchanged
```

### `register_command(name, description, fn)`

Registers a slash command with the TUI. The command is invoked as `/name args...`. Command handlers run on the same serialized handler goroutine as `on_submit`/`on_escape`: see [Handler concurrency](#handler-concurrency).

**Parameters:**
- `name` (`str`): Command name (without the leading `/`).
- `description` (`str`): Short description shown in command help.
- `fn` (`callable`): Function called with the command's argument string.

**Returns:** `None`

```python
def cmd_clear(args):
    console.main_panel().clear()

console.register_command("clear", "Clear output", cmd_clear)
```

### `remove_command(name)`

Removes a previously registered slash command.

**Parameters:**
- `name` (`str`): Command name to remove.

**Returns:** `None`

```python
console.remove_command("clear")
```

### `spinner_start(text="Working")`

Shows a spinner overlay with the given label. The spinner is a TUI-level overlay: it's not tied to any specific panel.

**Parameters:**
- `text` (`str`, optional): Spinner label. Default: `"Working"`.

**Returns:** `None`

```python
console.spinner_start("Thinking")
result = do_work()
console.spinner_stop()
```

### `spinner_stop()`

Hides the spinner overlay.

**Returns:** `None`

### `set_progress(label, pct)`

Sets the progress bar overlay. The progress bar is a TUI-level overlay: it's not tied to any specific panel.

**Parameters:**
- `label` (`str`): Progress label.
- `pct` (`float`): Progress fraction from `0.0` to `1.0`. Pass a negative value to clear the progress bar.

**Returns:** `None`

```python
console.set_progress("Downloading", 0.5)   # 50%
console.set_progress("", -1)               # clear
```

### `on_submit(fn)`

Registers the handler called when the user submits input from the prompt.

**Parameters:**
- `fn` (`callable`): Function called with the submitted text as its single argument.

**Returns:** `None`

```python
def on_submit(text):
    main = console.main_panel()
    main.stream_start()
    main.stream_chunk("You said: " + text)
    main.stream_end()

console.on_submit(on_submit)
```

### `on_escape(fn)`

Registers a callback invoked when the user presses Esc. Submitting new input or pressing Esc cancels any in-flight `on_submit`/`on_escape`/command handler, allowing cooperative handlers to stop early.

**Parameters:**
- `fn` (`callable`): Function called with no arguments.

**Returns:** `None`

```python
console.on_escape(lambda: console.spinner_stop())
```

### `run()`

Starts the console event loop. Blocks the calling thread until the user exits (e.g. via `/exit` or Ctrl+C).

**Returns:** `None`

```python
import scriptling.console as console

main = console.main_panel()
console.set_status("MyApp", "v1.0")
main.add_message(console.styled(console.PRIMARY, "MyApp") + " ready!")
console.on_submit(lambda text: main.add_message("Echo: " + text))
console.run()  # blocks until /exit or Ctrl+C
```

#### Handler concurrency

The interpreter lock (GIL) already makes your handlers memory-safe: you never need locks around shared state. On top of that, `on_submit`, `on_escape`, and `register_command` handlers run **one at a time, to completion** before the next starts. This is deliberate for a TUI: a chat conversation is only coherent if each submit finishes before the next begins (otherwise two handlers would interleave at blocking points and scramble the order). Serializing also keeps input responsive: the input reader enqueues events and keeps reading while a handler runs.

Because handlers are sequential, a long-running handler delays the next one until it returns. If a handler may run for a while, do its work in a loop that checks for cancellation: submitting new input or pressing Esc cancels the in-flight handler (and fires `on_escape`), so cooperative handlers can stop early and let the next one run.

## Panel Methods

`console.create_panel(name)` and `console.panel(name)` return a `Panel` instance with the following methods. Panels support both raw text content and message-based content.

| Method | Description |
|--------|-------------|
| `write(text)` | Append text to the panel |
| `set_content(text)` | Replace all panel content |
| `clear()` | Remove all panel content |
| `set_title(title)` | Set the panel border title |
| `set_color(color)` | Set border/accent color (name or hex) |
| `set_scrollable(bool)` | Set whether content scrolls |
| `add_message(*args, label=, role=)` | Add a message to the panel |
| `stream_start(label=, role=)` | Begin a streaming message |
| `stream_chunk(text)` | Append a chunk to the current stream |
| `stream_end()` | Finalize the current stream |
| `add_row(panel)` | Add a child panel as a vertical row |
| `add_column(panel)` | Add a child panel as a horizontal column |
| `scroll_to_top()` | Scroll to top of panel content |
| `scroll_to_bottom()` | Scroll to bottom of panel content |
| `size()` | Return `[width, height]` of the panel |
| `styled(color, text)` | Apply a theme color to text |
| `write_at(row, col, text)` | Write text at a specific position |
| `clear_line(row)` | Clear a specific line |

### `Panel.write(text)`

Appends text to the panel's raw content buffer.

**Parameters:**
- `text` (`str`): Text to append.

**Returns:** `None`

```python
logs = console.panel("logs")
logs.write("entry\n")
```

### `Panel.set_content(text)`

Replaces all of the panel's raw content.

**Parameters:**
- `text` (`str`): New panel content.

**Returns:** `None`

### `Panel.clear()`

Removes all content (messages and raw text) from the panel.

**Returns:** `None`

```python
main = console.main_panel()
main.clear()
```

### `Panel.set_title(title)`

Sets the panel's border title.

**Parameters:**
- `title` (`str`): New title text.

**Returns:** `None`

### `Panel.set_color(color)`

Sets the panel's border/accent color.

**Parameters:**
- `color` (`str`): Theme color name or hex color.

**Returns:** `None`

### `Panel.set_scrollable(scrollable)`

Sets whether the panel's content scrolls or uses a fixed viewport.

**Parameters:**
- `scrollable` (`bool`): `True` to enable scrolling.

**Returns:** `None`

### `Panel.add_message(*args, label="", role="")`

Adds a message to the panel.

**Parameters:**
- `*args`: Message content parts, joined together.
- `label` (`str`, optional): Custom label shown next to the message. Default: `""`.
- `role` (`str`, optional): Message role, used for default styling. Default: `""`.

**Returns:** `None`

```python
main = console.main_panel()
main.add_message("Hello", "world")               # adds a message to the main area
main.add_message("result here", label="Tool")    # message with a custom label
```

### `Panel.stream_start(label="", role="")`

Begins a streaming message. Use with `stream_chunk` and `stream_end` to display text as it arrives (e.g. LLM token output).

**Parameters:**
- `label` (`str`, optional): Custom label for the streamed message. Default: `""`.
- `role` (`str`, optional): Message role, used for default styling. Default: `""`.

**Returns:** `None`

```python
main = console.main_panel()
main.stream_start()                    # default label
main.stream_start(label="Assistant")   # custom label
for chunk in response_chunks:
    main.stream_chunk(chunk)
main.stream_end()
```

### `Panel.stream_chunk(text)`

Appends a chunk of text to the current stream started by `stream_start`.

**Parameters:**
- `text` (`str`): Chunk of text to append.

**Returns:** `None`

### `Panel.stream_end()`

Finalizes the current stream started by `stream_start`.

**Returns:** `None`

### `Panel.add_row(child)`

Adds a child panel as a vertical row (appends top to bottom). A panel cannot mix rows and columns: adding a row to a panel that already has columns is a no-op.

**Parameters:**
- `child` (`Panel`): Child panel to add.

**Returns:** `None`

### `Panel.add_column(child)`

Adds a child panel as a horizontal column (appends left to right). A panel cannot mix rows and columns: adding a column to a panel that already has rows is a no-op.

**Parameters:**
- `child` (`Panel`): Child panel to add.

**Returns:** `None`

### `Panel.scroll_to_top()`

Scrolls to the top of the panel's content.

**Returns:** `None`

### `Panel.scroll_to_bottom()`

Scrolls to the bottom of the panel's content.

**Returns:** `None`

### `Panel.size()`

Returns the panel's current rendered size.

**Returns:** `list`: `[width, height]` of the panel.

### `Panel.styled(color, text)`

Applies a theme color to text, identical to the module-level `console.styled`.

**Parameters:**
- `color` (`str`): Color constant, theme name string, or hex color.
- `text` (`str`): Text to style.

**Returns:** `str`: the styled text.

### `Panel.write_at(row, col, text)`

Writes text at a specific row/column position within the panel.

**Parameters:**
- `row` (`int`): Row position.
- `col` (`int`): Column position.
- `text` (`str`): Text to write.

**Returns:** `None`

### `Panel.clear_line(row)`

Clears a specific line within the panel.

**Parameters:**
- `row` (`int`): Row to clear.

**Returns:** `None`

## Layout

The console supports a multi-panel layout with a main chat area in the center, plus optional left and right side panels. Use the two-step builder pattern: **create panels first**, then **add them to the layout**.

```
┌──────────┬─────────────────────┬──────────────┐
│  Left    │      Main Chat      │  Right Top   │
│  Panel   │                     ├──────────────┤
│          │                     │ Right Bottom │
└──────────┴─────────────────────┴──────────────┘
```

- **Tab** cycles focus through all visible, non-skip-focus panels (left children, main, right children).
- Focused panel border uses the panel's color; unfocused uses the theme's dim color.
- Call `clear_layout()` to reset to single-panel mode at any time.
- Panels and their content survive `clear_layout()`: re-add them with `add_left`/`add_right`.

Background tasks can access panels by name without needing a Console instance:

```python
def pump_logs():
    logs = console.panel("logs")
    if logs:
        logs.write("Background message\n")
```

## Full dashboard example

```python
import scriptling.console as console
import scriptling.runtime as runtime
import time

logs = console.create_panel("logs", width=-25, min_width=15, scrollable=True, title="Logs")
right = console.create_panel(width=-30, min_width=16)
cpu_panel = console.create_panel("cpu", height=-50, title="CPU")
mem_panel = console.create_panel("mem", height=-50, title="Memory")

right.add_row(cpu_panel)
right.add_row(mem_panel)
console.add_left(logs)
console.add_right(right)

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

## See Also

- [scriptling.ai.agent.interact](../../ai/interact/) - Interactive agent loop using this library
