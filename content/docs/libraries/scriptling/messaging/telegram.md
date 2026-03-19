---
title: scriptling.messaging.telegram
linkTitle: telegram
weight: 1
---

Telegram Bot API client for building bots on the Telegram platform.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(token, allowed_users=[])` | Create a Telegram bot client |
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
| `answer_callback(bot, id, text="")` | Acknowledge a callback |
| `download(bot, ref)` | Download a file by ID |
| `capabilities(bot)` | Get platform capabilities |

## Creating a Client

### telegram.client(token, allowed_users=[])

Creates a new Telegram bot client.

**Parameters:**
- `token` (str): Telegram bot token from @BotFather
- `allowed_users` (list, optional): List of user IDs allowed to use the bot

**Returns:** TelegramClient instance

**Example:**

```python
import scriptling.messaging.telegram as telegram

# Basic client
bot = telegram.client("123456789:ABCdefGHIjklMNOpqrsTUVwxyz")

# With allowed users restriction
bot = telegram.client(
    "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    allowed_users=["123456789", "987654321"]
)
```

## Event Handlers

### telegram.command(bot, name, help_text, handler)

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `name` (str): Command name (without /)
- `help_text` (str): Help text for the command
- `handler` (callable): Function receiving context dict

**Example:**

```python
import scriptling.messaging.telegram as telegram

bot = telegram.client("TOKEN")

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

telegram.command(bot, "start", "Start the bot", handle_start)
telegram.command(bot, "help", "Show help", lambda ctx: ctx.reply("Help text..."))

telegram.run(bot)
```

### telegram.on_callback(bot, handler)

Registers a handler for button callback events.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()  # Acknowledge the button press
    ctx.reply(f"You clicked: {data}")

telegram.on_callback(bot, handle_button)
```

### telegram.on_message(bot, handler)

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

telegram.on_message(bot, handle_message)
```

### telegram.on_file(bot, handler)

Registers a handler for file/photo uploads.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")
    data = ctx.download()  # Returns base64 encoded data

telegram.on_file(bot, handle_file)
```

### telegram.auth(bot, handler)

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `handler` (callable): Function returning True to allow, False to deny

**Example:**

```python
allowed_ids = {"123456789", "987654321"}

def check_auth(ctx):
    return ctx.user.id in allowed_ids

telegram.auth(bot, check_auth)
```

## Sending Messages

### telegram.send_message(bot, dest, text, parse_mode="", keyboard=None)

Sends a text message.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID to send to
- `text` (str or dict): Message text or rich message dict
- `parse_mode` (str, optional): "Markdown" or "HTML"
- `keyboard` (list, optional): Button keyboard from `keyboard()`

**Example:**

```python
# Simple text message
telegram.send_message(bot, chat_id, "Hello!")

# With keyboard
kb = telegram.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
telegram.send_message(bot, chat_id, "Choose:", keyboard=kb)
```

### telegram.send_rich_message(bot, dest, msg)

Sends a rich/embed message.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID to send to
- `msg` (dict): Rich message dict with title, body, color, image, url

**Example:**

```python
telegram.send_rich_message(bot, chat_id, {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000",
    "image": "https://example.com/image.png"
})
```

### telegram.edit_message(bot, dest, msg_id, text)

Edits an existing message.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID
- `msg_id` (str): Message ID to edit
- `text` (str): New message text

**Example:**

```python
telegram.edit_message(bot, chat_id, message_id, "Updated text")
```

### telegram.delete_message(bot, dest, msg_id)

Deletes a message.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID
- `msg_id` (str): Message ID to delete

**Example:**

```python
telegram.delete_message(bot, chat_id, message_id)
```

## Sending Files

### telegram.send_file(bot, dest, source, filename="", caption="", base64=False)

Sends a file to a chat.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID to send to
- `source` (str): File path or base64 data
- `filename` (str, optional): Filename to display
- `caption` (str, optional): File caption
- `base64` (bool, optional): True if source is base64 data

**Example:**

```python
# Send from file path
telegram.send_file(bot, chat_id, "/path/to/file.pdf", filename="document.pdf")

# Send from base64 data
telegram.send_file(bot, chat_id, base64_data, filename="image.png", base64=True)
```

## Utilities

### telegram.typing(bot, dest)

Sends a typing indicator to the chat.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `dest` (str): Chat ID

**Example:**

```python
telegram.typing(bot, chat_id)
# Do some work...
telegram.send_message(bot, chat_id, "Done!")
```

### telegram.answer_callback(bot, id, text="")

Acknowledges a button callback.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `id` (str): Callback ID from context
- `text` (str, optional): Text to show as notification

**Example:**

```python
def handle_callback(ctx):
    telegram.answer_callback(bot, ctx.callback_id, "Processing...")
    # Do work...
```

### telegram.download(bot, ref)

Downloads a file by its ID/reference.

**Parameters:**
- `bot` (TelegramClient): Bot instance
- `ref` (str): File ID or reference

**Returns:** str - Base64 encoded file data

**Example:**

```python
def handle_file(ctx):
    data = telegram.download(bot, ctx.file.id)
    # Process base64 data...
```

### telegram.capabilities(bot)

Returns list of platform capabilities.

**Parameters:**
- `bot` (TelegramClient): Bot instance

**Returns:** list - List of capability strings

**Example:**

```python
caps = telegram.capabilities(bot)
# ["send_message", "edit_message", "delete_message", "typing", ...]
```

### telegram.keyboard(rows)

Builds a button keyboard grid.

**Parameters:**
- `rows` (list): List of button rows, each row is a list of button dicts

**Button Dict:**
- `text` (str): Button label
- `data` (str): Callback data (for callback buttons)
- `url` (str): URL (for URL buttons)

**Example:**

```python
kb = telegram.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}],
    [{"text": "Visit Website", "url": "https://example.com"}]
])
```

## Running the Bot

### telegram.run(bot)

Starts the bot event loop. This blocks until the bot is stopped.

**Parameters:**
- `bot` (TelegramClient): Bot instance

**Example:**

```python
import scriptling.messaging.telegram as telegram

bot = telegram.client("TOKEN")
telegram.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
telegram.run(bot)  # Blocks here
```

## Complete Example

```python
import scriptling.messaging.telegram as telegram

# Create bot
bot = telegram.client("YOUR_BOT_TOKEN")

# Register commands
telegram.command(bot, "start", "Start the bot", lambda ctx: (
    ctx.reply("Welcome! Use /help for commands.")
))

telegram.command(bot, "help", "Show help", lambda ctx: (
    ctx.reply("Commands: /start, /help, /echo")
))

telegram.command(bot, "echo", "Echo your message", lambda ctx: (
    ctx.reply(" ".join(ctx.args) if ctx.args else "Usage: /echo <message>")
))

# Handle button callbacks
telegram.on_callback(bot, lambda ctx: (
    ctx.answer() or ctx.reply(f"You selected: {ctx.callback_data}")
))

# Handle regular messages
telegram.on_message(bot, lambda ctx: ctx.reply(f"You said: {ctx.text}"))

# Start the bot
telegram.run(bot)
```
