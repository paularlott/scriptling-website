---
title: scriptling.messaging.slack
linkTitle: slack
weight: 3
---

Slack Bot API client for building bots on the Slack platform.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(bot_token, app_token, allowed_users=[])` | Create a Slack bot client |
| `open_dm(bot, user_id)` | Open a DM channel with a user |
| `keyboard(rows)` | Build a button keyboard |
| `command(bot, name, handler)` | Register a command handler |
| `on_callback(bot, handler)` | Register callback handler |
| `on_message(bot, handler)` | Register message handler |
| `on_file(bot, handler)` | Register file handler |
| `auth(bot, handler)` | Register auth handler |
| `run(bot)` | Start the bot event loop |
| `send_message(bot, dest, text, ...)` | Send a message |
| `send_rich_message(bot, dest, msg)` | Send a rich/embed message |
| `edit_message(bot, dest, msg_id, text)` | Edit a message |
| `delete_message(bot, dest, msg_id)` | Delete a message |
| `send_file(bot, dest, source, ...)` | Send a file |
| `typing(bot, dest)` | Send typing indicator |
| `answer_callback(bot, id, token, text="")` | Acknowledge a callback |
| `download(bot, ref)` | Download a file by ID |
| `capabilities(bot)` | Get platform capabilities |

## Creating a Client

### slack.client(bot_token, app_token, allowed_users=[])

Creates a new Slack bot client. Unlike other platforms, Slack requires two tokens.

**Parameters:**
- `bot_token` (str): Slack bot token (starts with `xoxb-`)
- `app_token` (str): Slack app-level token (starts with `xapp-`)
- `allowed_users` (list, optional): List of user IDs allowed to use the bot

**Returns:** SlackClient instance

**Getting Your Tokens:**

1. Go to https://api.slack.com/apps
2. Create or select your app
3. **Bot Token**: Go to "OAuth & Permissions" → copy the "Bot User OAuth Token" (starts with `xoxb-`)
4. **App Token**: Go to "Basic Information" → "App-Level Tokens" → create or copy a token (starts with `xapp-`)

**Example:**

```python
import scriptling.messaging.slack as slack

# Basic client with both tokens
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

## Slack-Specific Functions

### slack.open_dm(bot, user_id)

Opens or retrieves a DM channel with a user. This is Slack-specific because you need a DM channel ID to send direct messages.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `user_id` (str): Slack user ID (starts with `U`)

**Returns:** str - DM channel ID (starts with `D`)

**Example:**

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")

# Open DM channel with a user
dm_channel = slack.open_dm(bot, "U1234567890")

# Send a direct message
slack.send_message(bot, dm_channel, "Hello directly!")
```

## Event Handlers

### slack.command(bot, name, help_text, handler)

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `name` (str): Command name (without /)
- `help_text` (str): Help text for the command
- `handler` (callable): Function receiving context dict

**Example:**

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

slack.command(bot, "start", "Start the bot", handle_start)
slack.command(bot, "help", "Show help", lambda ctx: ctx.reply("Help text..."))

slack.run(bot)
```

### slack.on_callback(bot, handler)

Registers a handler for button callback events.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

slack.on_callback(bot, handle_button)
```

### slack.on_message(bot, handler)

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

slack.on_message(bot, handle_message)
```

### slack.on_file(bot, handler)

Registers a handler for file uploads.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

slack.on_file(bot, handle_file)
```

### slack.auth(bot, handler)

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `handler` (callable): Function returning True to allow, False to deny

**Example:**

```python
allowed_ids = {"U1234567890", "U0987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

slack.auth(bot, check_auth)
```

## Sending Messages

### slack.send_message(bot, dest, text, parse_mode="", keyboard=None)

Sends a text message.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID (starts with `C`) or DM channel ID (starts with `D`)
- `text` (str or dict): Message text or rich message dict
- `parse_mode` (str, optional): Not used for Slack
- `keyboard` (list, optional): Button keyboard from `keyboard()`

**Example:**

```python
# Simple text message to channel
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

### slack.send_rich_message(bot, dest, msg)

Sends a rich/embed message (Slack Block Kit).

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID or DM channel ID
- `msg` (dict): Rich message dict with title, body, color, image, url

**Example:**

```python
slack.send_rich_message(bot, "C1234567890", {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### slack.edit_message(bot, dest, msg_id, text)

Edits an existing message.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID
- `msg_id` (str): Timestamp of the message (Slack uses timestamps as IDs)
- `text` (str): New message text

**Example:**

```python
slack.edit_message(bot, "C1234567890", "1234567890.123456", "Updated text")
```

### slack.delete_message(bot, dest, msg_id)

Deletes a message.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID
- `msg_id` (str): Timestamp of the message

**Example:**

```python
slack.delete_message(bot, "C1234567890", "1234567890.123456")
```

## Sending Files

### slack.send_file(bot, dest, source, filename="", caption="", base64=False)

Sends a file to a channel.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID or DM channel ID
- `source` (str): File path or base64 data
- `filename` (str, optional): Filename to display
- `caption` (str, optional): File caption/message
- `base64` (bool, optional): True if source is base64 data

**Example:**

```python
# Send from file path
slack.send_file(bot, "C1234567890", "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
slack.send_file(bot, "C1234567890", base64_data, filename="image.png", base64=True)
```

## Utilities

### slack.typing(bot, dest)

Sends a typing indicator to the channel.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `dest` (str): Channel ID

**Example:**

```python
slack.typing(bot, "C1234567890")
# Do some work...
slack.send_message(bot, "C1234567890", "Done!")
```

### slack.answer_callback(bot, id, token, text="")

Acknowledges a button callback.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `id` (str): Callback ID from context
- `token` (str): Callback token from context
- `text` (str, optional): Text to show as notification

**Example:**

```python
def handle_callback(ctx):
    slack.answer_callback(bot, ctx.callback_id, ctx.callback_token, "Processing...")
    # Do work...
```

### slack.download(bot, ref)

Downloads a file by its ID/reference.

**Parameters:**
- `bot` (SlackClient): Bot instance
- `ref` (str): File ID or URL

**Returns:** str - Base64 encoded file data

**Example:**

```python
def handle_file(ctx):
    data = slack.download(bot, ctx.file.url)
    # Process base64 data...
```

### slack.capabilities(bot)

Returns list of platform capabilities.

**Parameters:**
- `bot` (SlackClient): Bot instance

**Returns:** list - List of capability strings

**Example:**

```python
caps = slack.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

### slack.keyboard(rows)

Builds a button keyboard grid.

**Parameters:**
- `rows` (list): List of button rows, each row is a list of button dicts

**Button Dict:**
- `text` (str): Button label
- `data` (str): Callback data (for callback buttons)
- `url` (str): URL (for URL buttons)

**Example:**

```python
kb = slack.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

## Running the Bot

### slack.run(bot)

Starts the bot event loop. This blocks until the bot is stopped.

**Parameters:**
- `bot` (SlackClient): Bot instance

**Example:**

```python
import scriptling.messaging.slack as slack

bot = slack.client("xoxb-...", "xapp-...")
slack.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
slack.run(bot)  # Blocks here
```

## Complete Example

```python
import scriptling.messaging.slack as slack

# Create bot with both tokens
bot = slack.client(
    "xoxb-your-bot-token",
    "xapp-your-app-token"
)

# Register commands
slack.command(bot, "start", "Start the bot", lambda ctx: (
    ctx.reply("Welcome! Use /help for commands.")
))

slack.command(bot, "help", "Show help", lambda ctx: (
    ctx.reply("Commands: /start, /help, /echo, /dm")
))

slack.command(bot, "echo", "Echo your message", lambda ctx: (
    ctx.reply(" ".join(ctx.args) if ctx.args else "Usage: /echo <message>")
))

slack.command(bot, "dm", "Send a DM", lambda ctx: (
    slack.send_message(bot, slack.open_dm(bot, ctx.user.id), "Hello via DM!")
))

# Handle button callbacks
slack.on_callback(bot, lambda ctx: (
    ctx.answer() or ctx.reply(f"You selected: {ctx.callback_data}")
))

# Handle regular messages
slack.on_message(bot, lambda ctx: ctx.reply(f"You said: {ctx.text}"))

# Start the bot
slack.run(bot)
```

## Slack-Specific Notes

### Two Token Requirement

Slack requires two tokens:
- **Bot Token (`xoxb-`)**: Used for most API calls (sending messages, etc.)
- **App Token (`xapp-`)**: Used for WebSocket connections to receive events

### Message IDs are Timestamps

Slack uses timestamps as message IDs. These look like `1234567890.123456`.

### DM Channels

Unlike Telegram, Slack requires you to open a DM channel before sending direct messages. Use `open_dm()` to get the channel ID.

### Channel Types

- `C...` - Public channels
- `G...` - Private channels (groups)
- `D...` - Direct message channels
- `U...` - User IDs (use with `open_dm()`)

### Workspace App

The bot must be installed to your Slack workspace with the appropriate OAuth scopes for the features you use.
