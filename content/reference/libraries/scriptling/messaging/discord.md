---
title: scriptling.messaging.discord
linkTitle: discord
weight: 2
---

Discord Bot API client for building bots on the Discord platform.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(token, allowed_users=[])` | Create a Discord bot client |
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

### discord.client(token, allowed_users=[])

Creates a new Discord bot client.

**Parameters:**
- `token` (str): Discord bot token from the Developer Portal
- `allowed_users` (list, optional): List of user IDs allowed to use the bot

**Returns:** DiscordClient instance

**Example:**

```python
import scriptling.messaging.discord as discord

# Basic client
bot = discord.client("YOUR_DISCORD_BOT_TOKEN")

# With allowed users restriction
bot = discord.client(
    "YOUR_DISCORD_BOT_TOKEN",
    allowed_users=["123456789", "987654321"]
)
```

## Event Handlers

### discord.command(bot, name, help_text, handler)

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `name` (str): Command name (without /)
- `help_text` (str): Help text for the command
- `handler` (callable): Function receiving context dict

**Example:**

```python
import scriptling.messaging.discord as discord

bot = discord.client("TOKEN")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

discord.command(bot, "start", "Start the bot", handle_start)
discord.command(bot, "help", "Show help", lambda ctx: ctx.reply("Help text..."))

discord.run(bot)
```

### discord.on_callback(bot, handler)

Registers a handler for button callback events.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

discord.on_callback(bot, handle_button)
```

### discord.on_message(bot, handler)

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

discord.on_message(bot, handle_message)
```

### discord.on_file(bot, handler)

Registers a handler for file/photo uploads.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

discord.on_file(bot, handle_file)
```

### discord.auth(bot, handler)

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `handler` (callable): Function returning True to allow, False to deny

**Example:**

```python
allowed_ids = {"123456789", "987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

discord.auth(bot, check_auth)
```

## Sending Messages

### discord.send_message(bot, dest, text, parse_mode="", keyboard=None)

Sends a text message.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID to send to
- `text` (str or dict): Message text or rich message dict
- `parse_mode` (str, optional): Not used for Discord
- `keyboard` (list, optional): Button keyboard from `keyboard()`

**Example:**

```python
# Simple text message
discord.send_message(bot, channel_id, "Hello!")

# With keyboard (buttons)
kb = discord.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
discord.send_message(bot, channel_id, "Choose:", keyboard=kb)
```

### discord.send_rich_message(bot, dest, msg)

Sends a rich/embed message.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID to send to
- `msg` (dict): Rich message dict with title, body, color, image, url

**Example:**

```python
discord.send_rich_message(bot, channel_id, {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### discord.edit_message(bot, dest, msg_id, text)

Edits an existing message.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID
- `msg_id` (str): Message ID to edit
- `text` (str): New message text

**Example:**

```python
discord.edit_message(bot, channel_id, message_id, "Updated text")
```

### discord.delete_message(bot, dest, msg_id)

Deletes a message.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID
- `msg_id` (str): Message ID to delete

**Example:**

```python
discord.delete_message(bot, channel_id, message_id)
```

## Sending Files

### discord.send_file(bot, dest, source, filename="", caption="", base64=False)

Sends a file to a channel.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID to send to
- `source` (str): File path or base64 data
- `filename` (str, optional): Filename to display
- `caption` (str, optional): File caption/message
- `base64` (bool, optional): True if source is base64 data

**Example:**

```python
# Send from file path
discord.send_file(bot, channel_id, "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
discord.send_file(bot, channel_id, base64_data, filename="image.png", base64=True)
```

## Utilities

### discord.typing(bot, dest)

Sends a typing indicator to the channel.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `dest` (str): Channel ID

**Example:**

```python
discord.typing(bot, channel_id)
# Do some work...
discord.send_message(bot, channel_id, "Done!")
```

### discord.answer_callback(bot, id, token, text="")

Acknowledges a button callback.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `id` (str): Callback ID from context
- `token` (str): Callback token from context
- `text` (str, optional): Text to show as notification

**Example:**

```python
def handle_callback(ctx):
    discord.answer_callback(bot, ctx.callback_id, ctx.callback_token, "Processing...")
    # Do work...
```

### discord.download(bot, ref)

Downloads a file by its ID/reference.

**Parameters:**
- `bot` (DiscordClient): Bot instance
- `ref` (str): File ID or reference

**Returns:** str - Base64 encoded file data

**Example:**

```python
def handle_file(ctx):
    data = discord.download(bot, ctx.file.id)
    # Process base64 data...
```

### discord.capabilities(bot)

Returns list of platform capabilities.

**Parameters:**
- `bot` (DiscordClient): Bot instance

**Returns:** list - List of capability strings

**Example:**

```python
caps = discord.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

### discord.keyboard(rows)

Builds a button keyboard grid.

**Parameters:**
- `rows` (list): List of button rows, each row is a list of button dicts

**Button Dict:**
- `text` (str): Button label
- `data` (str): Callback data (for callback buttons)
- `url` (str): URL (for URL buttons)

**Example:**

```python
kb = discord.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

## Running the Bot

### discord.run(bot)

Starts the bot event loop. This blocks until the bot is stopped.

**Parameters:**
- `bot` (DiscordClient): Bot instance

**Example:**

```python
import scriptling.messaging.discord as discord

bot = discord.client("TOKEN")
discord.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
discord.run(bot)  # Blocks here
```

## Complete Example

```python
import scriptling.messaging.discord as discord

# Create bot
bot = discord.client("YOUR_DISCORD_BOT_TOKEN")

# Register commands
discord.command(bot, "start", "Start the bot", lambda ctx: (
    ctx.reply("Welcome! Use /help for commands.")
))

discord.command(bot, "help", "Show help", lambda ctx: (
    ctx.reply("Commands: /start, /help, /echo")
))

discord.command(bot, "echo", "Echo your message", lambda ctx: (
    ctx.reply(" ".join(ctx.args) if ctx.args else "Usage: /echo <message>")
))

# Handle button callbacks
discord.on_callback(bot, lambda ctx: (
    ctx.answer() or ctx.reply(f"You selected: {ctx.callback_data}")
))

# Handle regular messages
discord.on_message(bot, lambda ctx: ctx.reply(f"You said: {ctx.text}"))

# Start the bot
discord.run(bot)
```

## Discord-Specific Notes

### Gateway Connection

Discord uses WebSocket Gateway connections for real-time events. The `run()` function establishes this connection and maintains it.

### Intents

The bot automatically requests the necessary gateway intents for receiving messages and interactions.

### Rate Limits

Discord has rate limits. The client handles basic rate limiting automatically, but be aware of Discord's API limits when sending many messages quickly.
