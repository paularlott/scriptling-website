---
title: scriptling.websocket
linkTitle: websocket
weight: 5
---

WebSocket client library for connecting to WebSocket servers.

## Overview

The `scriptling.websocket` library provides a simple, synchronous WebSocket client API. It allows Scriptling scripts to connect to WebSocket servers, send and receive messages, and handle both text and binary data.

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(url, timeout=10, headers={})` | Connect to a WebSocket server |
| `is_text(message)` | Check if a received message is text (string) |
| `is_binary(message)` | Check if a received message is binary (list) |

## Connection Methods

When you call `connect()`, it returns a connection object with these methods:

| Method | Description |
|--------|-------------|
| `send(message)` | Send a text message (dict is auto-JSON encoded) |
| `send_binary(data)` | Send binary data as list of bytes |
| `receive(timeout=30)` | Receive a message (None on timeout/disconnect) |
| `connected()` | Check if connection is still open |
| `close()` | Close the connection |

## Setup

```go
import "github.com/paularlott/scriptling/extlibs"

// Register the WebSocket library
extlibs.RegisterWebSocketLibrary(p)
```

## Functions

### scriptling.websocket.connect(url, timeout=10, headers={})

Connect to a WebSocket server.

**Parameters:**

- `url` (string): WebSocket URL (ws:// or wss://)
- `timeout` (int, optional): Connection timeout in seconds (default: 10)
- `headers` (dict, optional): HTTP headers for the handshake

**Returns:** Connection object

**Example:**
```python
import scriptling.websocket as ws

conn = ws.connect("wss://echo.websocket.org", timeout=5)
```

## Connection Methods

### conn.send(message)

Send a text message. If the message is a dict, it's automatically JSON encoded.

**Parameters:**

- `message` (string or dict): Message to send

**Example:**
```python
conn.send("Hello, WebSocket!")
conn.send({"type": "ping", "data": "test"})  # Auto-JSON encoded
```

### conn.send_binary(data)

Send binary data.

**Parameters:**

- `data` (list): List of byte values (0-255)

**Example:**
```python
conn.send_binary([0x01, 0x02, 0x03, 0xFF])
```

### conn.receive(timeout=30)

Receive a message from the server.

**Parameters:**

- `timeout` (int, optional): Timeout in seconds (default: 30)

**Returns:**

- string for text messages
- list of bytes for binary messages
- None on timeout or disconnect

**Example:**
```python
msg = conn.receive(timeout=5)
if msg:
    print(f"Received: {msg}")
else:
    # Timeout or disconnected - check conn.connected()
    if not conn.connected():
        print("Disconnected!")
```

### conn.connected()

Check if the connection is still open.

**Returns:** True if connected, False otherwise

**Example:**
```python
while conn.connected():
    msg = conn.receive(timeout=60)
    if msg:
        conn.send(f"Echo: {msg}")
```

### conn.close()

Close the WebSocket connection.

**Example:**
```python
conn.close()
```

### scriptling.websocket.is_text(message)

Check if a received message is a text message.

**Parameters:**

- `message`: A message returned from `receive()`

**Returns:** True if the message is text (string), False otherwise

**Example:**
```python
msg = conn.receive()
if ws.is_text(msg):
    print(f"Text: {msg}")
```

### scriptling.websocket.is_binary(message)

Check if a received message is a binary message.

**Parameters:**

- `message`: A message returned from `receive()`

**Returns:** True if the message is binary (list of bytes), False otherwise

**Example:**
```python
msg = conn.receive()
if ws.is_binary(msg):
    print(f"Binary: {len(msg)} bytes")
```

### conn.remote_addr

The remote address of the connection (string).

## Examples

### Basic Echo Client

```python
import scriptling.websocket as ws

# Connect to echo server
conn = ws.connect("wss://echo.websocket.org", timeout=10)

# Send a message
conn.send("Hello, WebSocket!")

# Receive the echo
msg = conn.receive(timeout=5)
print(f"Received: {msg}")

# Clean up
conn.close()
```

### JSON Messaging

```python
import scriptling.websocket as ws

conn = ws.connect("wss://api.example.com/ws", timeout=10)

# Send JSON by passing a dict
conn.send({
    "action": "subscribe",
    "channel": "updates"
})

# Receive messages
while conn.connected():
    msg = conn.receive(timeout=30)
    if msg:
        print(f"Update: {msg}")
    else:
        # Check if still connected after None
        if not conn.connected():
            break

conn.close()
```

### Binary Data

```python
import scriptling.websocket as ws

conn = ws.connect("wss://binary.example.com/ws", timeout=10)

# Send binary data
conn.send_binary([0x01, 0x02, 0x03, 0x04])

# Receive binary response
msg = conn.receive(timeout=5)
if msg:
    # Binary messages come back as list of bytes
    print(f"Received {len(msg)} bytes")
    first_byte = msg[0]

conn.close()
```

### Handling Mixed Text and Binary

```python
import scriptling.websocket as ws

conn = ws.connect("wss://mixed.example.com/ws", timeout=10)

while conn.connected():
    msg = conn.receive(timeout=30)
    if not msg:
        continue

    if ws.is_text(msg):
        print(f"Text message: {msg}")
    elif ws.is_binary(msg):
        print(f"Binary message: {len(msg)} bytes")

conn.close()
```

### With Custom Headers

```python
import scriptling.websocket as ws

conn = ws.connect(
    "wss://api.example.com/ws",
    timeout=10,
    headers={
        "Authorization": "Bearer my-token",
        "X-Custom-Header": "value"
    }
)

conn.send("Hello with auth!")
msg = conn.receive(timeout=5)
print(msg)

conn.close()
```

## WebSocket Server (runtime.http.websocket)

To accept WebSocket connections in your server, use `runtime.http.websocket()`:

### runtime.http.websocket(path, handler)

Register a WebSocket endpoint.

**Parameters:**

- `path` (string): URL path for the WebSocket endpoint
- `handler` (string): Handler function as "library.function"

The handler receives a WebSocketClient object and runs for the connection lifetime.

### Server Example

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.websocket("/chat", "handlers.chat_handler")
```

```python
# handlers.py
_clients = []

def chat_handler(client):
    """Handle a WebSocket connection - runs until connection closes."""
    _clients.append(client)
    client.send("Welcome to the chat!")

    try:
        while client.connected():
            msg = client.receive(timeout=60)
            if msg:
                # Broadcast to all clients
                for c in _clients:
                    if c.connected():
                        c.send(msg)
    finally:
        _clients.remove(client)
```

### WebSocketClient Object (Server-side)

The client object passed to server handlers has:

| Method/Field | Description |
|--------------|-------------|
| `client.connected()` | Check if client is still connected |
| `client.receive(timeout=30)` | Receive message (None on timeout) |
| `client.send(message)` | Send text message (dict auto-JSON) |
| `client.send_binary(data)` | Send binary data |
| `client.close()` | Close the connection |
| `client.remote_addr` | Client's remote address |

To check message type in server handlers, use the module-level functions:

```python
import scriptling.websocket as ws

def handler(client):
    while client.connected():
        msg = client.receive(timeout=60)
        if msg:
            if ws.is_text(msg):
                client.send(f"Echo text: {msg}")
            elif ws.is_binary(msg):
                client.send_binary(msg)  # Echo binary back
```

## Error Handling

```python
import scriptling.websocket as ws

conn = ws.connect("wss://example.com/ws", timeout=10)

try:
    conn.send("Hello")
    msg = conn.receive(timeout=5)
    if msg is None and not conn.connected():
        print("Connection lost")
    elif msg is None:
        print("Timeout - no message received")
    else:
        print(f"Received: {msg}")
finally:
    conn.close()
```

## Notes

- The library uses a synchronous API - `receive()` blocks until a message arrives or timeout
- `receive()` returns None both on timeout and disconnect - use `connected()` to distinguish
- Dicts passed to `send()` are automatically JSON encoded
- Binary messages are represented as lists of byte values (0-255)
- Always call `close()` when done to properly clean up resources
