---
description: Discord Bot API client using a WebSocket Gateway connection for real-time events.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/messaging/discord/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/messaging/discord/
status: stable
tags:
    - libraries
    - messaging
title: scriptling.messaging.discord
type: API Reference
---
# scriptling.messaging.discord

Discord Bot API client for building bots on the Discord platform, using a WebSocket Gateway connection for real-time events.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(token, allowed_users=[])` | Create a Discord bot client. |
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
| `send_file(bot, dest, source, filename="", caption="", base64=False)` | Send a file to a channel. |
| `typing(bot, dest)` | Send a typing indicator. |
| `answer_callback(bot, id, token, text="")` | Acknowledge a button callback. |
| `download(bot, ref)` | Download a file by ID. |
| `capabilities(bot)` | Get the platform's capability list. |

## Functions

### `client(token, allowed_users=[])`

Creates a new Discord bot client.

**Parameters:**
- `token` (`str`): Discord bot token from the Developer Portal.
- `allowed_users` (`list`, optional): List of user IDs allowed to use the bot. Default: `[]` (no restriction).

**Returns:** `DiscordClient`: a bot client instance.

**Raises:** `Error`: if `token` is empty.

```python
import scriptling.messaging.discord as discord

bot = discord.client("YOUR_DISCORD_BOT_TOKEN")

# With allowed users restriction
bot = discord.client(
    "YOUR_DISCORD_BOT_TOKEN",
    allowed_users=["123456789", "987654321"]
)
```

### `keyboard(rows)`

Builds a button keyboard grid.

**Parameters:**
- `rows` (`list`): List of button rows, each row a list of button dicts with `text` (`str`) and either `data` (`str`, for callback buttons) or `url` (`str`, for URL buttons).

**Returns:** `list`: the keyboard structure, passed to `send_message()`'s `keyboard` parameter.

```python
kb = discord.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

### `command(bot, name, help_text, handler)`

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `name` (`str`): Command name, without the leading `/`.
- `help_text` (`str`, optional): Short description shown in the platform's help/command list. May be omitted, in which case call as `command(bot, name, handler)`. Default: `""`.
- `handler` (`callable`): Function called with a context dict when the command is invoked.

**Returns:** `None`

```python
import scriptling.messaging.discord as discord

bot = discord.client("TOKEN")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

discord.command(bot, "start", "Start the bot", handle_start)
discord.run(bot)
```

### `on_callback(bot, prefix, handler)`

Registers a handler for button callback events.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `prefix` (`str`, optional): Callback prefix to filter on. Omit to register a catch-all. Default: `""` (catch-all).
- `handler` (`callable`): Function called with a context dict when a callback fires.

**Returns:** `None`

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

discord.on_callback(bot, handle_button)
```

### `on_message(bot, handler)`

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict for each plain message.

**Returns:** `None`

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

discord.on_message(bot, handle_message)
```

### `on_file(bot, handler)`

Registers a handler for file/photo uploads.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict when a file is received.

**Returns:** `None`

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

discord.on_file(bot, handle_file)
```

### `auth(bot, handler)`

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict; return `True` to allow, `False` to deny.

**Returns:** `None`

```python
allowed_ids = {"123456789", "987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

discord.auth(bot, check_auth)
```

### `run(bot)`

Starts the bot event loop, establishing and maintaining the Discord Gateway WebSocket connection. Blocks until the bot is stopped. The client requests the gateway intents needed to receive messages and interactions automatically.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.

**Returns:** `None`

```python
import scriptling.messaging.discord as discord

bot = discord.client("TOKEN")
discord.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
discord.run(bot)  # Blocks here
```

### `send_message(bot, dest, text, parse_mode="", keyboard=None)`

Sends a text or rich message to a channel.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID to send to.
- `text` (`str` or `dict`): Message text, or a rich message dict (see `send_rich_message()`).
- `parse_mode` (`str`, optional): Not used by Discord. Default: `""`.
- `keyboard` (`list`, optional): Button keyboard from `keyboard()`. Default: `None`.

**Returns:** `None`

```python
discord.send_message(bot, channel_id, "Hello!")

kb = discord.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
discord.send_message(bot, channel_id, "Choose:", keyboard=kb)
```

### `send_rich_message(bot, dest, msg)`

Sends a rich/embed message to a channel.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID to send to.
- `msg` (`dict`): Rich message dict with `title`, `body`, `color`, `image`, `url` keys.

**Returns:** `None`

```python
discord.send_rich_message(bot, channel_id, {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### `edit_message(bot, dest, msg_id, text)`

Edits an existing message.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID.
- `msg_id` (`str`): ID of the message to edit.
- `text` (`str`): New message text.

**Returns:** `None`

```python
discord.edit_message(bot, channel_id, message_id, "Updated text")
```

### `delete_message(bot, dest, msg_id)`

Deletes a message.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID.
- `msg_id` (`str`): ID of the message to delete.

**Returns:** `None`

```python
discord.delete_message(bot, channel_id, message_id)
```

### `send_file(bot, dest, source, filename="", caption="", base64=False)`

Sends a file to a channel.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID to send to.
- `source` (`str`): File path, or base64-encoded data if `base64=True`.
- `filename` (`str`, optional): Filename to display. Default: `""`.
- `caption` (`str`, optional): Caption/message to send alongside the file. Default: `""`.
- `base64` (`bool`, optional): Whether `source` is base64-encoded data rather than a path. Default: `False`.

**Returns:** `None`

```python
discord.send_file(bot, channel_id, "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
discord.send_file(bot, channel_id, base64_data, filename="image.png", base64=True)
```

### `typing(bot, dest)`

Sends a typing indicator to a channel.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `dest` (`str`): Channel ID.

**Returns:** `None`

```python
discord.typing(bot, channel_id)
# Do some work...
discord.send_message(bot, channel_id, "Done!")
```

### `answer_callback(bot, id, token, text="")`

Acknowledges a button callback.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `id` (`str`): Callback ID from the context.
- `token` (`str`): Callback token from the context.
- `text` (`str`, optional): Text to show as a notification. Default: `""`.

**Returns:** `None`

```python
def handle_callback(ctx):
    discord.answer_callback(bot, ctx.callback_id, ctx.callback_token, "Processing...")
    # Do work...

discord.on_callback(bot, handle_callback)
```

### `download(bot, ref)`

Downloads a file by its ID/reference.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.
- `ref` (`str`): File ID or reference, typically `ctx.file.id`.

**Returns:** `str`: base64-encoded file data.

```python
def handle_file(ctx):
    data = discord.download(bot, ctx.file.id)
    # Process base64 data...

discord.on_file(bot, handle_file)
```

### `capabilities(bot)`

Returns the list of capabilities the Discord platform supports.

**Parameters:**
- `bot` (`DiscordClient`): Bot instance.

**Returns:** `list`: list of capability strings.

```python
caps = discord.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

This library sends and receives messages via the Discord Bot API using the bot token supplied to `client()`. The token is held by the embedder: typically passed in via `Register(p, logger)` when embedding in Go: and is not directly exposed to scripts; scripts can send and receive messages on the bot's behalf but cannot read the token back out. Treat the bot token as a secret: anyone who obtains it can act as your bot. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

## See Also

- [scriptling.messaging.telegram](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/telegram.md): Telegram Bot API client
- [scriptling.messaging.slack](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/slack.md): Slack Bot API client
- [scriptling.messaging.console](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/console.md): terminal-based client for local testing
