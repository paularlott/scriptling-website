---
title: Messaging
description: Platform-agnostic bot framework for Telegram, Discord, Slack, and Console.
weight: 3
---

Platform-agnostic messaging bot libraries that provide a unified API across multiple chat platforms. Build bots that work on Telegram, Discord, Slack, or even the console with the same code.

## Overview

The messaging libraries share a common architecture:

- **Unified Client Interface** - All platforms use the same API patterns
- **Event Handlers** - Register commands, callbacks, messages, and file handlers
- **Rich Messages** - Send structured content with titles, bodies, colors, and images
- **Keyboards/Buttons** - Interactive button grids with callback handling
- **File Support** - Send and receive files/photos
- **Authentication** - Control who can interact with your bot

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.messaging.telegram](telegram/) | Telegram Bot API client |
| [scriptling.messaging.discord](discord/) | Discord Bot API client |
| [scriptling.messaging.slack](slack/) | Slack Bot API client |
| [scriptling.messaging.console](console/) | Console-based messaging client |

## Shared Concepts

### Client Creation

Each platform has its own `client()` function with platform-specific authentication:

```python
import scriptling.messaging.telegram as telegram
import scriptling.messaging.discord as discord
import scriptling.messaging.slack as slack
import scriptling.messaging.console as console

# Telegram - single token
tg_bot = telegram.client("YOUR_BOT_TOKEN")

# Discord - single token
dc_bot = discord.client("YOUR_BOT_TOKEN")

# Slack - bot token + app token
sl_bot = slack.client("xoxb-YOUR-BOT-TOKEN", "xapp-YOUR-APP-TOKEN")

# Console - wrap an existing Console instance
import scriptling.console as con
cons_bot = console.client(con.create())
```

### Allowed Users

All platforms support an `allowed_users` parameter for simple access control:

```python
bot = telegram.client("TOKEN", allowed_users=["user123", "user456"])
```

### Event Handlers

All platforms support the same event handlers:

```python
# Register a command handler
telegram.command(bot, "/start", "Start the bot", lambda ctx: ctx.reply("Hello!"))

# Handle button callbacks
telegram.on_callback(bot, lambda ctx: ctx.answer("Button pressed!"))

# Handle all messages
telegram.on_message(bot, lambda ctx: ctx.reply(f"You said: {ctx.text}"))

# Handle file uploads
telegram.on_file(bot, lambda ctx: print(f"Received file: {ctx.file.name}"))

# Custom authentication
telegram.auth(bot, lambda ctx: ctx.user.id in allowed_ids)
```

### Running the Bot

```python
# Start the event loop (blocks until stopped)
telegram.run(bot)
```

## Context Object

All handlers receive a context dict with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `dest` | str | Destination ID (chat/channel/user) |
| `message_id` | str | ID of the message |
| `text` | str | Message text content |
| `command` | str | Command name (if message is a command) |
| `args` | list | Command arguments |
| `is_callback` | bool | True if this is a button callback |
| `callback_id` | str | Callback ID (for answering) |
| `callback_token` | str | Callback token (platform-specific) |
| `callback_data` | str | Data attached to the button |
| `user` | dict | User info with `id`, `name`, `platform` |
| `file` | dict or null | File info with `id`, `name`, `mime`, `size`, `url` |

### Context Methods

The context object includes helper methods:

```python
# Reply with text
ctx.reply("Hello!")

# Reply with rich message
ctx.reply({
    "title": "Title",
    "body": "Message body",
    "color": "#FF5733"
})

# Show typing indicator
ctx.typing()

# Acknowledge a callback/button press
ctx.answer("Processing...")

# Download attached file (returns base64)
data = ctx.download()

# Check platform capabilities
caps = ctx.capabilities()
has_edit = ctx.has_capability("edit_message")
```

## Rich Messages

Send structured content with the rich message format:

```python
telegram.send_message(bot, chat_id, {
    "title": "Alert Title",
    "body": "Detailed message body",
    "color": "#FF0000",
    "image": "https://example.com/image.png",
    "url": "https://example.com"
})
```

## Keyboards and Buttons

Create interactive button grids:

```python
# Build a keyboard
kb = telegram.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}],
    [{"text": "Cancel", "data": "cancel"}]
])

# Send with keyboard
telegram.send_message(bot, chat_id, "Choose:", keyboard=kb)

# Handle button presses
telegram.on_callback(bot, lambda ctx: (
    ctx.answer() or ctx.reply(f"You chose: {ctx.callback_data}")
))
```

## Platform Capabilities

Check what features each platform supports:

```python
caps = telegram.capabilities(bot)
# Returns list like: ["send_message", "edit_message", "typing", ...]
```

Common capabilities:

| Capability | Description |
|------------|-------------|
| `send_message` | Can send text messages |
| `send_rich_message` | Can send rich/embed messages |
| `edit_message` | Can edit sent messages |
| `delete_message` | Can delete messages |
| `typing` | Can show typing indicator |
| `file` | Can send/receive files |
| `keyboard` | Supports inline keyboards |
| `callback` | Supports button callbacks |
