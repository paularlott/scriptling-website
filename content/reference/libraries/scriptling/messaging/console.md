---
title: scriptling.messaging.console
linkTitle: console
weight: 4
---

Console-based messaging client for building interactive terminal bots. This library wraps a Console instance to provide the same messaging API as other platforms, allowing you to test and run bots in the terminal.

## Available Functions

| Function | Description |
|----------|-------------|
| `client(console)` | Wrap a Console instance as a messaging bot client |
| `keyboard(rows)` | Build a button keyboard (text-based) |
| `command(bot, name, handler)` | Register a command handler |
| `on_callback(bot, handler)` | Register callback handler |
| `on_message(bot, handler)` | Register message handler |
| `on_file(bot, handler)` | Register file handler |
| `auth(bot, handler)` | Register auth handler |
| `run(bot)` | Start the bot event loop |
| `send_message(bot, dest, text, ...)` | Send a message |
| `send_rich_message(bot, dest, msg)` | Send a rich message |
| `edit_message(bot, dest, msg_id, text)` | Edit a message |
| `delete_message(bot, dest, msg_id)` | Delete a message |
| `send_file(bot, dest, source, ...)` | Send a file |
| `typing(bot, dest)` | Send typing indicator |
| `answer_callback(bot, id, text="")` | Acknowledge a callback |
| `download(bot, ref)` | Download a file |
| `capabilities(bot)` | Get platform capabilities |

## Creating a Client

### console.client(console_instance)

Wraps a Console instance as a messaging bot client.

**Parameters:**
- `console_instance` (Console): A Console instance from `scriptling.console`

**Returns:** ConsoleClient instance

**Example:**

```python
import scriptling.console as con
import scriptling.messaging.console as console

# Create a Console instance
cons = con.create()

# Wrap it as a messaging client
bot = console.client(cons)
```

## Event Handlers

### console.command(bot, name, help_text, handler)

Registers a command handler for `/command` style messages.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `name` (str): Command name (without /)
- `help_text` (str): Help text for the command
- `handler` (callable): Function receiving context dict

**Example:**

```python
import scriptling.console as con
import scriptling.messaging.console as console

cons = con.create()
bot = console.client(cons)

def handle_start(ctx):
    ctx.reply("Welcome to the bot!")

console.command(bot, "start", "Start the bot", handle_start)
console.command(bot, "help", "Show help", lambda ctx: ctx.reply("Help text..."))

console.run(bot)
```

### console.on_callback(bot, handler)

Registers a handler for button callback events. In the console, callbacks are handled via text input.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_button(ctx):
    data = ctx.callback_data
    ctx.answer()
    ctx.reply(f"You selected: {data}")

console.on_callback(bot, handle_button)
```

### console.on_message(bot, handler)

Registers a handler for all non-command messages.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_message(ctx):
    ctx.reply(f"Echo: {ctx.text}")

console.on_message(bot, handle_message)
```

### console.on_file(bot, handler)

Registers a handler for file input.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `handler` (callable): Function receiving context dict

**Example:**

```python
def handle_file(ctx):
    file = ctx.file
    ctx.reply(f"Received file: {file.name} ({file.size} bytes)")

console.on_file(bot, handle_file)
```

### console.auth(bot, handler)

Registers an authentication handler for custom access control.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `handler` (callable): Function returning True to allow, False to deny

**Example:**

```python
def check_auth(ctx):
    # Console always allows access by default
    return True

console.auth(bot, check_auth)
```

## Sending Messages

### console.send_message(bot, dest, text, parse_mode="", keyboard=None)

Sends a text message to the console.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored in console, always outputs to terminal)
- `text` (str or dict): Message text or rich message dict
- `parse_mode` (str, optional): Not used for console
- `keyboard` (list, optional): Button keyboard (displayed as numbered options)

**Example:**

```python
# Simple text message
console.send_message(bot, "", "Hello!")

# With keyboard (displayed as numbered options)
kb = console.keyboard([
    [{"text": "Yes", "data": "yes"}, {"text": "No", "data": "no"}]
])
console.send_message(bot, "", "Choose:", keyboard=kb)
```

### console.send_rich_message(bot, dest, msg)

Sends a rich message to the console.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored)
- `msg` (dict): Rich message dict with title, body, color, image, url

**Example:**

```python
console.send_rich_message(bot, "", {
    "title": "Alert",
    "body": "Something happened!",
    "color": "#FF0000"
})
```

### console.edit_message(bot, dest, msg_id, text)

Updates a message (in console, this reprints the message with an edit indicator).

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored)
- `msg_id` (str): Message ID
- `text` (str): New message text

**Example:**

```python
console.edit_message(bot, "", message_id, "Updated text")
```

### console.delete_message(bot, dest, msg_id)

Deletes a message (in console, this shows a deletion notice).

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored)
- `msg_id` (str): Message ID

**Example:**

```python
console.delete_message(bot, "", message_id)
```

## Sending Files

### console.send_file(bot, dest, source, filename="", caption="", base64=False)

Sends a file (displays file info in console).

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored)
- `source` (str): File path or base64 data
- `filename` (str, optional): Filename to display
- `caption` (str, optional): File caption
- `base64` (bool, optional): True if source is base64 data

**Example:**

```python
# Send from file path
console.send_file(bot, "", "/path/to/file.pdf", filename="document.pdf")
```

## Utilities

### console.typing(bot, dest)

Shows a typing indicator in the console.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `dest` (str): Destination (ignored)

**Example:**

```python
console.typing(bot, "")
# Do some work...
console.send_message(bot, "", "Done!")
```

### console.answer_callback(bot, id, text="")

Acknowledges a callback.

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `id` (str): Callback ID
- `text` (str, optional): Text to display

**Example:**

```python
def handle_callback(ctx):
    console.answer_callback(bot, ctx.callback_id, "Processing...")
```

### console.download(bot, ref)

Downloads a file (returns file data if available).

**Parameters:**
- `bot` (ConsoleClient): Bot instance
- `ref` (str): File reference

**Returns:** str - Base64 encoded file data

**Example:**

```python
def handle_file(ctx):
    data = console.download(bot, ctx.file.id)
    # Process base64 data...
```

### console.capabilities(bot)

Returns list of platform capabilities.

**Parameters:**
- `bot` (ConsoleClient): Bot instance

**Returns:** list - List of capability strings

**Example:**

```python
caps = console.capabilities(bot)
# ["send_message", "typing", ...]
```

### console.keyboard(rows)

Builds a button keyboard grid (displayed as numbered options in console).

**Parameters:**
- `rows` (list): List of button rows, each row is a list of button dicts

**Button Dict:**
- `text` (str): Button label
- `data` (str): Callback data

**Example:**

```python
kb = console.keyboard([
    [{"text": "Option 1", "data": "opt1"}, {"text": "Option 2", "data": "opt2"}]
])
```

## Running the Bot

### console.run(bot)

Starts the bot event loop. This blocks until the bot is stopped.

**Parameters:**
- `bot` (ConsoleClient): Bot instance

**Example:**

```python
import scriptling.console as con
import scriptling.messaging.console as console

cons = con.create()
bot = console.client(cons)
console.command(bot, "start", "Start", lambda ctx: ctx.reply("Hello!"))
console.run(bot)  # Blocks here, reads from terminal
```

## Complete Example

```python
import scriptling.console as con
import scriptling.messaging.console as console

# Create console and bot
cons = con.create()
bot = console.client(cons)

# Register commands
console.command(bot, "start", "Start the bot", lambda ctx: (
    ctx.reply("Welcome! Type /help for commands.")
))

console.command(bot, "help", "Show help", lambda ctx: (
    ctx.reply("Commands: /start, /help, /echo, /quit")
))

console.command(bot, "echo", "Echo your message", lambda ctx: (
    ctx.reply(" ".join(ctx.args) if ctx.args else "Usage: /echo <message>")
))

console.command(bot, "quit", "Exit the bot", lambda ctx: (
    ctx.reply("Goodbye!") or exit(0)
))

# Handle button callbacks
console.on_callback(bot, lambda ctx: (
    ctx.answer() or ctx.reply(f"You selected: {ctx.callback_data}")
))

# Handle regular messages
console.on_message(bot, lambda ctx: ctx.reply(f"You said: {ctx.text}"))

# Start the bot
print("Bot started. Type /help for commands.")
console.run(bot)
```

## Console-Specific Notes

### Terminal Interface

The console messaging client provides a terminal-based interface for testing bots without deploying to a real chat platform.

### Button Input

Keyboards are displayed as numbered options. Users can select an option by typing its number or the callback data.

### Limited Features

Some features are limited or simulated in the console:
- **Rich messages**: Displayed as formatted text
- **Typing indicator**: Shows "..." in the terminal
- **File handling**: Limited to displaying file info
- **Message editing/deletion**: Shows notices rather than actual edits

### Testing and Development

Use the console messaging client for:
- Testing bot logic before deploying
- Developing commands and handlers
- Debugging bot behavior
- Local interaction testing

### No Authentication

The console doesn't require authentication. The `user.id` and `user.name` fields are set to default values like "console_user".
