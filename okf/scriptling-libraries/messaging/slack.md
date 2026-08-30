---
description: Slack Bot API client using Socket Mode for real-time events.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/messaging/slack/
sources:
    - resource: https://scriptling.dev/reference/libraries/messaging/slack/
status: stable
tags:
    - libraries
    - messaging
title: scriptling.messaging.slack
type: API Reference
---
# scriptling.messaging.slack

Slack Bot API client for building bots on the Slack platform, using Socket Mode for real-time events.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(bot_token, app_token, allowed_users=[])` | Create a Slack bot client. |
| `open_dm(bot, user_id)` | Open or retrieve a DM channel with a user. |
| `keyboard(rows)` | Build a button keyboard. |
| `command(bot, name, help_text, handler)` | Register a command handler for `/command` style messages. |
| `on_callback(bot, prefix, handler)` | Register a handler for button callback events. |
| `on_message(bot, handler)` | Register a handler for non-command messages. |
| `on_file(bot, handler)` | Register a handler for file uploads. |
| `auth(bot, handler)` | Register an authentication handler. |
| `run(bot)` | Start the bot event loop. |
| `send_message(bot, dest, text, parse_mode="", keyboard=None)` | Send a text or rich message. |
| `send_rich_message(bot, dest, msg)` | Send a rich/embed message (Slack Block Kit). |
| `edit_message(bot, dest, msg_id, text)` | Edit a previously sent message. |
| `delete_message(bot, dest, msg_id)` | Delete a message. |
| `send_file(bot, dest, source, filename="", caption="", base64=False)` | Send a file to a channel. |
| `typing(bot, dest)` | Send a typing indicator. |
| `answer_callback(bot, id, token, text="")` | Acknowledge a button callback. |
| `download(bot, ref)` | Download a file by ID or URL. |
| `capabilities(bot)` | Get the platform's capability list. |

## Functions

### `client(bot_token, app_token, allowed_users=[])`

Creates a new Slack bot client. Unlike other platforms, Slack requires two tokens: a bot token for API calls and an app-level token for the Socket Mode WebSocket connection.

To get your tokens: go to [api.slack.com/apps](https://api.slack.com/apps), create or select your app, then copy the Bot User OAuth Token (starts with `xoxb-`) from "OAuth & Permissions", and an App-Level Token (starts with `xapp-`) from "Basic Information" → "App-Level Tokens".

**Parameters:**
- `bot_token` (`str`): Slack bot token, starts with `xoxb-`.
- `app_token` (`str`): Slack app-level token, starts with `xapp-`.
- `allowed_users` (`list`, optional): List of user IDs allowed to use the bot. Default: `[]` (no restriction).

**Returns:** `SlackClient`: a bot client instance.

```python
import scriptling.messaging.slack as slack

bot = slack.client(
    "xoxb-your-bot-token-here",
    "xapp-your-app-token-here"
)

# With allowed users restriction
bot = slack.client(
    "xoxb-your-bot-token-here",
    "xapp-your-app-token-here",
    allowed_users=["U1234567890", "U0987654321"]
)
```

### `open_dm(bot, user_id)`

Opens or retrieves a DM channel with a user. Slack requires a DM channel ID before sending direct messages, unlike Telegram and Discord, which send directly to a user ID.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `user_id` (`str`): Slack user ID, starts with `U`.

**Returns:** `str`: DM channel ID, starts with `D`.

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")

dm_channel = slack.open_dm(bot, "U1234567890")
slack.send_message(bot, dm_channel, "Hello directly!")
```

### `keyboard(rows)`

Builds a button keyboard grid.

**Parameters:**
- `rows` (`list`): List of button rows, each row a list of button dicts with `text` (`str`) and either `data` (`str`, for callback buttons) or `url` (`str`, for URL buttons).

**Returns:** `list`: the keyboard structure, passed to `send_message()`'s `keyboard` parameter.

```python
kb = slack.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

### `command(bot, name, help_text, handler)`

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `name` (`str`): Command name, without the leading `/`.
- `help_text` (`str`, optional): Short description shown in the platform's help/command list. May be omitted, in which case call as `command(bot, name, handler)`. Default: `""`.
- `handler` (`callable`): Function called with a context dict when the command is invoked.

**Returns:** `None`

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

slack.command(bot, "start", "Start the bot", handle_start)
slack.run(bot)
```

### `on_callback(bot, prefix, handler)`

Registers a handler for button callback events.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `prefix` (`str`, optional): Callback prefix to filter on. Omit to register a catch-all. Default: `""` (catch-all).
- `handler` (`callable`): Function called with a context dict when a callback fires.

**Returns:** `None`

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

slack.on_callback(bot, handle_button)
```

### `on_message(bot, handler)`

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict for each plain message.

**Returns:** `None`

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

slack.on_message(bot, handle_message)
```

### `on_file(bot, handler)`

Registers a handler for file uploads.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict when a file is received.

**Returns:** `None`

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

slack.on_file(bot, handle_file)
```

### `auth(bot, handler)`

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `handler` (`callable`): Function called with a context dict; return `True` to allow, `False` to deny.

**Returns:** `None`

```python
allowed_ids = {"U1234567890", "U0987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

slack.auth(bot, check_auth)
```

### `run(bot)`

Starts the bot event loop over a Socket Mode WebSocket connection. Blocks until the bot is stopped.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.

**Returns:** `None`

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")
slack.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
slack.run(bot)  # Blocks here
```

### `send_message(bot, dest, text, parse_mode="", keyboard=None)`

Sends a text or rich message to a channel or DM.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID (starts with `C`) or DM channel ID (starts with `D`, see `open_dm()`).
- `text` (`str` or `dict`): Message text, or a rich message dict (see `send_rich_message()`).
- `parse_mode` (`str`, optional): Not used by Slack. Default: `""`.
- `keyboard` (`list`, optional): Button keyboard from `keyboard()`. Default: `None`.

**Returns:** `None`

```python
slack.send_message(bot, "C1234567890", "Hello channel!")

# Direct message (need to open DM first)
dm_channel = slack.open_dm(bot, "U1234567890")
slack.send_message(bot, dm_channel, "Hello directly!")

# With keyboard (buttons)
kb = slack.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
slack.send_message(bot, "C1234567890", "Choose:", keyboard=kb)
```

### `send_rich_message(bot, dest, msg)`

Sends a rich/embed message using Slack Block Kit.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID or DM channel ID.
- `msg` (`dict`): Rich message dict with `title`, `body`, `color`, `image`, `url` keys.

**Returns:** `None`

```python
slack.send_rich_message(bot, "C1234567890", {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### `edit_message(bot, dest, msg_id, text)`

Edits an existing message.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID.
- `msg_id` (`str`): Timestamp of the message to edit. Slack uses message timestamps (e.g. `"1234567890.123456"`) as IDs.
- `text` (`str`): New message text.

**Returns:** `None`

```python
slack.edit_message(bot, "C1234567890", "1234567890.123456", "Updated text")
```

### `delete_message(bot, dest, msg_id)`

Deletes a message.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID.
- `msg_id` (`str`): Timestamp of the message to delete.

**Returns:** `None`

```python
slack.delete_message(bot, "C1234567890", "1234567890.123456")
```

### `send_file(bot, dest, source, filename="", caption="", base64=False)`

Sends a file to a channel or DM.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID or DM channel ID.
- `source` (`str`): File path, or base64-encoded data if `base64=True`.
- `filename` (`str`, optional): Filename to display. Default: `""`.
- `caption` (`str`, optional): Caption/message to send alongside the file. Default: `""`.
- `base64` (`bool`, optional): Whether `source` is base64-encoded data rather than a path. Default: `False`.

**Returns:** `None`

```python
slack.send_file(bot, "C1234567890", "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
slack.send_file(bot, "C1234567890", base64_data, filename="image.png", base64=True)
```

### `typing(bot, dest)`

Sends a typing indicator to a channel.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `dest` (`str`): Channel ID.

**Returns:** `None`

```python
slack.typing(bot, "C1234567890")
# Do some work...
slack.send_message(bot, "C1234567890", "Done!")
```

### `answer_callback(bot, id, token, text="")`

Acknowledges a button callback.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `id` (`str`): Callback ID from the context.
- `token` (`str`): Callback token from the context.
- `text` (`str`, optional): Text to show as a notification. Default: `""`.

**Returns:** `None`

```python
def handle_callback(ctx):
    slack.answer_callback(bot, ctx.callback_id, ctx.callback_token, "Processing...")
    # Do work...

slack.on_callback(bot, handle_callback)
```

### `download(bot, ref)`

Downloads a file by its ID or URL.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.
- `ref` (`str`): File ID or URL, typically `ctx.file.url`.

**Returns:** `str`: base64-encoded file data.

```python
def handle_file(ctx):
    data = slack.download(bot, ctx.file.url)
    # Process base64 data...

slack.on_file(bot, handle_file)
```

### `capabilities(bot)`

Returns the list of capabilities the Slack platform supports.

**Parameters:**
- `bot` (`SlackClient`): Bot instance.

**Returns:** `list`: list of capability strings.

```python
caps = slack.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

This library sends and receives messages via the Slack API using the bot and app tokens supplied to `client()`. The tokens are held by the embedder: typically passed in via `Register(p, logger)` when embedding in Go: and are not directly exposed to scripts; scripts can send and receive messages on the bot's behalf but cannot read the tokens back out. Treat both tokens as secrets: anyone who obtains them can act as your bot in your Slack workspace. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

## See Also

- [scriptling.messaging.telegram](https://scriptling.dev/okf/scriptling-libraries/messaging/telegram.md): Telegram Bot API client
- [scriptling.messaging.discord](https://scriptling.dev/okf/scriptling-libraries/messaging/discord.md): Discord Bot API client
- [scriptling.messaging.console](https://scriptling.dev/okf/scriptling-libraries/messaging/console.md): terminal-based client for local testing
