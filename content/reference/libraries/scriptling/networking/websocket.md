---
title: scriptling.net.websocket
linkTitle: websocket
weight: 5
---

WebSocket client library for connecting to WebSocket servers, with a simple synchronous API for sending and receiving text or binary messages.

## Overview

The `scriptling.net.websocket` library provides a simple, synchronous WebSocket client API. It allows Scriptling scripts to connect to WebSocket servers, send and receive messages, and handle both text and binary data.

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(url, timeout=10, headers={})` | Connect to a WebSocket server. |
| `is_text(message)` | Check if a received message is text. |
| `is_binary(message)` | Check if a received message is binary. |

## Connection Object

The `connect()` function returns a connection object with the following methods and properties.

| Method/Property | Description |
|--------|-------------|
| `send(message)` | Send a text message (dict is auto-JSON encoded). |
| `send_binary(data)` | Send binary data as a list of bytes. |
| `receive(timeout=30)` | Receive a message (`None` on timeout/disconnect). |
| `connected()` | Check if the connection is still open. |
| `close()` | Close the connection. |
| `remote_addr` | `str` property: remote address of the connection. |

## Functions

### `connect(url, timeout=10, headers={})`

Connects to a WebSocket server.

**Parameters:**
- `url` (`str`): WebSocket URL, `ws://` or `wss://`.
- `timeout` (`int`, optional): Connection timeout in seconds. Default: `10`.
- `headers` (`dict`, optional): HTTP headers to send during the handshake. Default: `{}`.

**Returns:** `Connection`: a connection object.

```python
import scriptling.net.websocket as ws

conn = ws.connect("wss://echo.websocket.org", timeout=5)
```

### `conn.send(message)`

Sends a text message. If `message` is a dict, it is automatically JSON encoded.

**Parameters:**
- `message` (`str` or `dict`): Message to send.

**Returns:** `None`

```python
conn.send("Hello, WebSocket!")
conn.send({"type": "ping", "data": "test"})  # Auto-JSON encoded
```

### `conn.send_binary(data)`

Sends binary data.

**Parameters:**
- `data` (`list`): List of byte values (`0`-`255`).

**Returns:** `None`

```python
conn.send_binary([0x01, 0x02, 0x03, 0xFF])
```

### `conn.receive(timeout=30)`

Receives a message from the server.

**Parameters:**
- `timeout` (`int`, optional): Timeout in seconds. Default: `30`.

**Returns:** `str` for text messages, `list` of bytes for binary messages, or `None` on timeout or disconnect.

```python
msg = conn.receive(timeout=5)
if msg:
    print(f"Received: {msg}")
else:
    # Timeout or disconnected - check conn.connected()
    if not conn.connected():
        print("Disconnected!")
```

### `conn.connected()`

Checks if the connection is still open.

**Parameters:** None

**Returns:** `bool`: `True` if connected, `False` otherwise.

```python
while conn.connected():
    msg = conn.receive(timeout=60)
    if msg:
        conn.send(f"Echo: {msg}")
```

### `conn.close()`

Closes the WebSocket connection.

**Parameters:** None

**Returns:** `None`

```python
conn.close()
```

### `is_text(message)`

Checks if a received message is a text message.

**Parameters:**
- `message`: A message returned from `receive()`.

**Returns:** `bool`: `True` if the message is text (`str`), `False` otherwise.

```python
msg = conn.receive()
if ws.is_text(msg):
    print(f"Text: {msg}")
```

### `is_binary(message)`

Checks if a received message is a binary message.

**Parameters:**
- `message`: A message returned from `receive()`.

**Returns:** `bool`: `True` if the message is binary (`list` of bytes), `False` otherwise.

```python
msg = conn.receive()
if ws.is_binary(msg):
    print(f"Binary: {len(msg)} bytes")
```

### `conn.remote_addr`

The remote address of the connection.

**Type:** `str` property.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.net.websocket` opens outbound WebSocket connections to any URL a script supplies, and can send and receive arbitrary data over that connection, including any headers (such as bearer tokens) the script passes in. The library does not restrict which hosts a script can connect to: that is the embedder's responsibility, typically enforced with OS-level firewalling or network namespacing around the process. See [Security Considerations](/docs/security/#network-security) for a full breakdown of network-enabled libraries.

## Examples

### Basic Echo Client

```python
import scriptling.net.websocket as ws

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
import scriptling.net.websocket as ws

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
import scriptling.net.websocket as ws

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
import scriptling.net.websocket as ws

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
import scriptling.net.websocket as ws

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

## Error Handling

```python
import scriptling.net.websocket as ws

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

- The library uses a synchronous API - `receive()` blocks until a message arrives or timeout.
- `receive()` returns `None` both on timeout and disconnect - use `connected()` to distinguish.
- Dicts passed to `send()` are automatically JSON encoded.
- Binary messages are represented as lists of byte values (`0`-`255`).
- Always call `close()` when done to properly clean up resources.

## Accepting WebSocket Connections (Server-Side)

This page documents the WebSocket *client*. To accept incoming WebSocket connections in a Scriptling-powered HTTP server, register a handler with `runtime.http.websocket(path, handler)`: see [scriptling.runtime.http](/reference/libraries/scriptling/runtime/http/) for details. The handler receives a `WebSocketClient` object exposing the same `connected()`, `receive()`, `send()`, `send_binary()`, `close()`, and `remote_addr` surface documented above, plus access to the module-level `is_text()` / `is_binary()` helpers for distinguishing message types:

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.websocket("/chat", "handlers.chat_handler")
```

```python
# handlers.py
import scriptling.net.websocket as ws

_clients = []

def chat_handler(client):
    """Handle a WebSocket connection - runs until connection closes."""
    _clients.append(client)
    client.send("Welcome to the chat!")

    try:
        while client.connected():
            msg = client.receive(timeout=60)
            if msg:
                for c in _clients:
                    if c.connected():
                        c.send(msg)
    finally:
        _clients.remove(client)
```

## See Also

- [scriptling.runtime.http](/reference/libraries/scriptling/runtime/http/): register server-side WebSocket endpoints with `runtime.http.websocket()`
- [scriptling.net.unicast](../unicast/): direct point-to-point UDP/TCP messaging
- [Security Guide](/docs/security/): full risk breakdown across all libraries
