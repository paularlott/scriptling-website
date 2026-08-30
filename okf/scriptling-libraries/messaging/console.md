---
description: Console-based messaging client for building and testing interactive terminal bots.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/messaging/console/
sources:
    - resource: https://scriptling.dev/reference/libraries/messaging/console/
status: stable
tags:
    - libraries
    - messaging
title: scriptling.messaging.console
type: API Reference
---
# scriptling.messaging.console

Console-based messaging client for building and testing interactive terminal bots. It wraps a `scriptling.console` instance to provide the same messaging API as the Discord, Slack, and Telegram libraries, so you can develop and test bot logic locally before deploying to a real platform.

## Available Functions

| Function | Description |
|----------|-------------|
| `client()` | Create a console messaging bot client. |
| `keyboard(rows)` | Build a button keyboard (rendered as numbered options). |
| `command(bot, name, help_text, handler)` | Register a command handler for `/command` style input. |
| `on_callback(bot, prefix, handler)` | Register a handler for button callback events. |
| `on_message(bot, handler)` | Register a handler for non-command messages. |
| `on_file(bot, handler)` | Register a handler for file input. |
| `auth(bot, handler)` | Register an authentication handler. |
| `run(bot)` | Start the bot event loop. |
| `send_message(bot, dest, text, parse_mode="", keyboard=None)` | Send a text or rich message. |
| `send_rich_message(bot, dest, msg)` | Send a rich message. |
| `edit_message(bot, dest, msg_id, text)` | Edit a previously sent message. |
| `delete_message(bot, dest, msg_id)` | Delete a message. |
| `send_file(bot, dest, source, filename="", caption="", base64=False)` | Send a file. |
| `typing(bot, dest)` | Show a typing indicator. |
| `answer_callback(bot, id, text="")` | Acknowledge a callback. |
| `download(bot, ref)` | Download a file's data. |
| `capabilities(bot)` | Get the platform's capability list. |

## Functions

### `client()`

Creates a console messaging bot client backed by the shared terminal console, exposing the same API as the other messaging libraries.

**Returns:** `ConsoleClient`: a bot client instance.

```python
import scriptling.messaging.console as console

bot = console.client()
```

### `keyboard(rows)`

Builds a button keyboard grid. In the console, keyboards are rendered as numbered options that the user selects by typing a number or the callback data.

**Parameters:**
- `rows` (`list`): List of button rows, each row a list of button dicts with `text` (`str`) and `data` (`str`) keys.

**Returns:** `list`: the keyboard structure, passed to `send_message()`'s `keyboard` parameter.

```python
kb = console.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
console.send_message(bot, "", "Choose:", keyboard=kb)
```

### `command(bot, name, help_text, handler)`

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `name` (`str`): Command name, without the leading `/`.
- `help_text` (`str`, optional): Short description shown in the platform's help/command list. May be omitted, in which case call as `command(bot, name, handler)`. Default: `""`.
- `handler` (`callable`): Function called with a context dict when the command is invoked.

**Returns:** `None`

```python
import scriptling.messaging.console as console

bot = console.client()

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

console.command(bot, "start", "Start the bot", handle_start)
console.run(bot)
```

### `on_callback(bot, prefix, handler)`

Registers a handler for button callback events. In the console, callbacks are delivered via text input matching a button's number or data.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `prefix` (`str`, optional): Callback prefix to filter on. Omit to register a catch-all. Default: `""` (catch-all).
- `handler` (`callable`): Function called with a context dict when a callback fires.

**Returns:** `None`

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()
    ctx.reply(f"You selected: {data}")

console.on_callback(bot, handle_button)
```

### `on_message(bot, handler)`

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict for each plain message.

**Returns:** `None`

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

console.on_message(bot, handle_message)
```

### `on_file(bot, handler)`

Registers a handler for file input.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict when a file is received.

**Returns:** `None`

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")

console.on_file(bot, handle_file)
```

### `auth(bot, handler)`

Registers an authentication handler for custom access control. The console allows all access by default, so this is mainly useful for testing auth logic before deploying to a real platform.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict; return `True` to allow, `False` to deny.

**Returns:** `None`

```python
def check_auth(ctx):
    return True  # Console always allows access by default

console.auth(bot, check_auth)
```

### `run(bot)`

Starts the bot event loop, reading from the terminal. Blocks until the bot is stopped.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.

**Returns:** `None`

```python
import scriptling.messaging.console as console

bot = console.client()
console.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
console.run(bot)  # Blocks here, reads from terminal
```

### `send_message(bot, dest, text, parse_mode="", keyboard=None)`

Sends a text or rich message to the console.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client; output always goes to the terminal.
- `text` (`str` or `dict`): Message text, or a rich message dict (see `send_rich_message()`).
- `parse_mode` (`str`, optional): Not used by the console client. Default: `""`.
- `keyboard` (`list`, optional): Button keyboard from `keyboard()`, displayed as numbered options. Default: `None`.

**Returns:** `None`

```python
console.send_message(bot, "", "Hello!")

kb = console.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
console.send_message(bot, "", "Choose:", keyboard=kb)
```

### `send_rich_message(bot, dest, msg)`

Sends a rich message to the console, displayed as formatted text.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client.
- `msg` (`dict`): Rich message dict with `title`, `body`, `color`, `image`, `url` keys.

**Returns:** `None`

```python
console.send_rich_message(bot, "", {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000"
})
```

### `edit_message(bot, dest, msg_id, text)`

Updates a previously sent message. In the console, this reprints the message with an edit indicator rather than mutating terminal history.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client.
- `msg_id` (`str`): ID of the message to edit.
- `text` (`str`): New message text.

**Returns:** `None`

```python
console.edit_message(bot, "", message_id, "Updated text")
```

### `delete_message(bot, dest, msg_id)`

Deletes a message. In the console, this prints a deletion notice rather than removing terminal output.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client.
- `msg_id` (`str`): ID of the message to delete.

**Returns:** `None`

```python
console.delete_message(bot, "", message_id)
```

### `send_file(bot, dest, source, filename="", caption="", base64=False)`

Sends a file. In the console, this prints the file's metadata rather than transferring data anywhere.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client.
- `source` (`str`): File path, or base64-encoded data if `base64=True`.
- `filename` (`str`, optional): Filename to display. Default: `""`.
- `caption` (`str`, optional): Caption to display alongside the file. Default: `""`.
- `base64` (`bool`, optional): Whether `source` is base64-encoded data rather than a path. Default: `False`.

**Returns:** `None`

```python
console.send_file(bot, "", "/path/to/file.pdf", filename="document.pdf")
```

### `typing(bot, dest)`

Shows a typing indicator (`"..."`) in the console.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `dest` (`str`): Destination identifier. Ignored by the console client.

**Returns:** `None`

```python
console.typing(bot, "")
# Do some work...
console.send_message(bot, "", "Done!")
```

### `answer_callback(bot, id, text="")`

Acknowledges a callback, optionally displaying a notification text.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `id` (`str`): Callback ID from the context.
- `text` (`str`, optional): Text to display as acknowledgment. Default: `""`.

**Returns:** `None`

```python
def handle_callback(ctx):
    console.answer_callback(bot, ctx.callback_id, "Processing...")

console.on_callback(bot, handle_callback)
```

### `download(bot, ref)`

Downloads a file's data if available.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.
- `ref` (`str`): File reference, typically `ctx.file.id`.

**Returns:** `str`: base64-encoded file data.

```python
def handle_file(ctx):
    data = console.download(bot, ctx.file.id)
    # Process base64 data...

console.on_file(bot, handle_file)
```

### `capabilities(bot)`

Returns the list of capabilities the console platform supports.

**Parameters:**
- `bot` (`ConsoleClient`): Bot instance.

**Returns:** `list`: list of capability strings.

```python
caps = console.capabilities(bot)
# ["send_message", "typing", ...]
```

## See Also

- [scriptling.messaging.telegram](https://scriptling.dev/okf/scriptling-libraries/messaging/telegram.md): Telegram Bot API client
- [scriptling.messaging.discord](https://scriptling.dev/okf/scriptling-libraries/messaging/discord.md): Discord Bot API client
- [scriptling.messaging.slack](https://scriptling.dev/okf/scriptling-libraries/messaging/slack.md): Slack Bot API client
- [scriptling.console](https://scriptling.dev/okf/scriptling-libraries/utilities/console.md): the underlying Console instance wrapped by this library
