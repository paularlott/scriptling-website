---
title: scriptling.messaging.telegram
linkTitle: telegram
weight: 1
---

Telegram Bot API client for building bots on the Telegram platform.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(token, allowed_users=[])` | Create a Telegram bot client. |
| `keyboard(rows)` | Build a button keyboard. |
| `command(bot, name, help_text, handler)` | Register a command handler for `/command` style messages. |
| `on_callback(bot, prefix, handler)` | Register a handler for button callback events. |
| `on_message(bot, handler)` | Register a handler for non-command messages. |
| `on_file(bot, handler)` | Register a handler for file/photo uploads. |
| `auth(bot, handler)` | Register an authentication handler. |
| `run(bot)` | Start the bot event loop. |
| `send_message(bot, dest, text, parse_mode="", keyboard=None)` | Send a text or rich message. |
| `send_rich_message(bot, dest, msg)` | Send a rich/embed message. |
| `edit_message(bot, dest, msg_id, text)` | Edit a previously sent message. |
| `delete_message(bot, dest, msg_id)` | Delete a message. |
| `send_file(bot, dest, source, filename="", caption="", base64=False)` | Send a file to a chat. |
| `typing(bot, dest)` | Send a typing indicator. |
| `answer_callback(bot, id, text="")` | Acknowledge a button callback. |
| `download(bot, ref)` | Download a file by ID. |
| `capabilities(bot)` | Get the platform's capability list. |

## Functions

### `client(token, allowed_users=[])`

Creates a new Telegram bot client.

**Parameters:**
- `token` (`str`): Telegram bot token from [@BotFather](https://t.me/BotFather).
- `allowed_users` (`list`, optional): List of user IDs allowed to use the bot. Default: `[]` (no restriction).

**Returns:** `TelegramClient`: a bot client instance.

```python
import scriptling.messaging.telegram as telegram

bot = telegram.client("123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

# With allowed users restriction
bot = telegram.client(
    "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    allowed_users=["123456789", "987654321"]
)
```

### `keyboard(rows)`

Builds a button keyboard grid.

**Parameters:**
- `rows` (`list`): List of button rows, each row a list of button dicts with `text` (`str`) and either `data` (`str`, for callback buttons) or `url` (`str`, for URL buttons).

**Returns:** `list`: the keyboard structure, passed to `send_message()`'s `keyboard` parameter.

```python
kb = telegram.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

### `command(bot, name, help_text, handler)`

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `name` (`str`): Command name, without the leading `/`.
- `help_text` (`str`, optional): Short description shown in the platform's help/command list. May be omitted, in which case call as `command(bot, name, handler)`. Default: `""`.
- `handler` (`callable`): Function called with a context dict when the command is invoked.

**Returns:** `None`

```python
import scriptling.messaging.telegram as telegram

bot = telegram.client("TOKEN")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

telegram.command(bot, "start", "Start the bot", handle_start)
telegram.run(bot)
```

### `on_callback(bot, prefix, handler)`

Registers a handler for button callback events.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `prefix` (`str`, optional): Callback prefix to filter on. Omit to register a catch-all. Default: `""` (catch-all).
- `handler` (`callable`): Function called with a context dict when a callback fires.

**Returns:** `None`

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

telegram.on_callback(bot, handle_button)
```

### `on_message(bot, handler)`

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict for each plain message.

**Returns:** `None`

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

telegram.on_message(bot, handle_message)
```

### `on_file(bot, handler)`

Registers a handler for file/photo uploads.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict when a file is received.

**Returns:** `None`

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

telegram.on_file(bot, handle_file)
```

### `auth(bot, handler)`

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict; return `True` to allow, `False` to deny.

**Returns:** `None`

```python
allowed_ids = {"123456789", "987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

telegram.auth(bot, check_auth)
```

### `run(bot)`

Starts the bot event loop. Blocks until the bot is stopped.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.

**Returns:** `None`

```python
import scriptling.messaging.telegram as telegram

bot = telegram.client("TOKEN")
telegram.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
telegram.run(bot)  # Blocks here
```

### `send_message(bot, dest, text, parse_mode="", keyboard=None)`

Sends a text or rich message to a chat.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID to send to.
- `text` (`str` or `dict`): Message text, or a rich message dict (see `send_rich_message()`).
- `parse_mode` (`str`, optional): `"Markdown"` or `"HTML"` to enable Telegram message formatting. Default: `""` (plain text).
- `keyboard` (`list`, optional): Button keyboard from `keyboard()`. Default: `None`.

**Returns:** `None`

```python
telegram.send_message(bot, chat_id, "Hello!")

kb = telegram.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
telegram.send_message(bot, chat_id, "Choose:", keyboard=kb)
```

### `send_rich_message(bot, dest, msg)`

Sends a rich/embed message to a chat.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID to send to.
- `msg` (`dict`): Rich message dict with `title`, `body`, `color`, `image`, `url` keys.

**Returns:** `None`

```python
telegram.send_rich_message(bot, chat_id, {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### `edit_message(bot, dest, msg_id, text)`

Edits an existing message.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID.
- `msg_id` (`str`): ID of the message to edit.
- `text` (`str`): New message text.

**Returns:** `None`

```python
telegram.edit_message(bot, chat_id, message_id, "Updated text")
```

### `delete_message(bot, dest, msg_id)`

Deletes a message.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID.
- `msg_id` (`str`): ID of the message to delete.

**Returns:** `None`

```python
telegram.delete_message(bot, chat_id, message_id)
```

### `send_file(bot, dest, source, filename="", caption="", base64=False)`

Sends a file to a chat.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID to send to.
- `source` (`str`): File path, or base64-encoded data if `base64=True`.
- `filename` (`str`, optional): Filename to display. Default: `""`.
- `caption` (`str`, optional): Caption to send alongside the file. Default: `""`.
- `base64` (`bool`, optional): Whether `source` is base64-encoded data rather than a path. Default: `False`.

**Returns:** `None`

```python
telegram.send_file(bot, chat_id, "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
telegram.send_file(bot, chat_id, base64_data, filename="image.png", base64=True)
```

### `typing(bot, dest)`

Sends a typing indicator to a chat.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `dest` (`str`): Chat ID.

**Returns:** `None`

```python
telegram.typing(bot, chat_id)
# Do some work...
telegram.send_message(bot, chat_id, "Done!")
```

### `answer_callback(bot, id, text="")`

Acknowledges a button callback.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `id` (`str`): Callback ID from the context.
- `text` (`str`, optional): Text to show as a notification. Default: `""`.

**Returns:** `None`

```python
def handle_callback(ctx):
    telegram.answer_callback(bot, ctx.callback_id, "Processing...")
    # Do work...

telegram.on_callback(bot, handle_callback)
```

### `download(bot, ref)`

Downloads a file by its ID/reference.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.
- `ref` (`str`): File ID or reference, typically `ctx.file.id`.

**Returns:** `str`: base64-encoded file data.

```python
def handle_file(ctx):
    data = telegram.download(bot, ctx.file.id)
    # Process base64 data...

telegram.on_file(bot, handle_file)
```

### `capabilities(bot)`

Returns the list of capabilities the Telegram platform supports.

**Parameters:**
- `bot` (`TelegramClient`): Bot instance.

**Returns:** `list`: list of capability strings.

```python
caps = telegram.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

This library sends and receives messages via the Telegram Bot API using the bot token supplied to `client()`. The token is held by the embedder: typically passed in via `Register(p, logger)` when embedding in Go: and is not directly exposed to scripts; scripts can send and receive messages on the bot's behalf but cannot read the token back out. Treat the bot token as a secret: anyone who obtains it can act as your bot. See [Security Considerations](/docs/security/#network-security) for a full breakdown of network-enabled libraries.

## See Also

- [scriptling.messaging.discord](../discord/): Discord Bot API client
- [scriptling.messaging.slack](../slack/): Slack Bot API client
- [scriptling.messaging.console](../console/): terminal-based client for local testing
