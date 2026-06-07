---
title: scriptling.net.unicast
linkTitle: unicast
weight: 3
---

UDP and TCP point-to-point messaging for direct host-to-host communication.

## Overview

The `scriptling.net.unicast` library provides both client and server functionality for UDP and TCP connections. Use `connect()` to establish a connection to a remote host, or `listen()` to accept incoming connections.

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(host, port, protocol="udp", timeout=10)` | Connect to a remote host |
| `listen(host, port, protocol="tcp")` | Listen for incoming connections |

## Connection Object Methods

The `connect()` function returns a connection object with these methods:

| Method | Description |
|--------|-------------|
| `send(message)` | Send a message to the remote peer |
| `receive(timeout=30)` | Receive a message |
| `close()` | Close the connection |
| `connected()` | Check if connection is still open |

## Connection Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `local_addr` | string | Local address of the connection |
| `remote_addr` | string | Remote address of the connection |

## TCP Listener Methods

The `listen(protocol="tcp")` function returns a TCP listener:

| Method | Description |
|--------|-------------|
| `accept(timeout=30)` | Accept an incoming connection |
| `close()` | Close the listener |
| `addr` | string property - bound address |

## UDP Listener Methods

The `listen(protocol="udp")` function returns a UDP listener:

| Method | Description |
|--------|-------------|
| `receive(timeout=30)` | Receive from any sender |
| `send_to(address, message)` | Send to a specific address |
| `close()` | Close the listener |
| `addr` | string property - bound address |

## Functions

### scriptling.net.unicast.connect(host, port, protocol="udp", timeout=10)

Connect to a remote host.

**Parameters:**

- `host` (string): Remote host address
- `port` (int): Remote port number
- `protocol` (string): `"udp"` or `"tcp"` (default: `"udp"`)
- `timeout` (number): Connection timeout in seconds (default: 10)

**Returns:** Connection object with `send()`, `receive()`, `close()`, `connected()` methods and `local_addr`, `remote_addr` properties

**Example:**
```python
import scriptling.net.unicast as uc

conn = uc.connect("192.168.1.1", 8080, protocol="tcp")
```

### scriptling.net.unicast.listen(host, port=0, protocol="tcp")

Listen for incoming connections.

**Parameters:**

- `host` (string): Bind address (use `"0.0.0.0"` for all interfaces)
- `port` (int): Port number (default: 0 = auto-assign)
- `protocol` (string): `"udp"` or `"tcp"` (default: `"tcp"`)

**Returns:**

- TCP: Listener with `accept()`, `close()`, `addr`
- UDP: Listener with `receive()`, `send_to()`, `close()`, `addr`

**Example:**
```python
import scriptling.net.unicast as uc

server = uc.listen("0.0.0.0", 8080)
print(f"Listening on {server.addr}")
```

## Connection Methods

### conn.send(message)

Send a message to the remote peer.

**Parameters:**

- `message` (string or dict): Message to send. Dicts are automatically JSON encoded.

**Example:**
```python
conn.send("Hello!")
conn.send({"action": "ping"})
```

### conn.receive(timeout=30)

Receive a message.

**Parameters:**

- `timeout` (number, optional): Timeout in seconds (default: 30)

**Returns:**

- Dict with `"data"` and `"source"` keys
- None on timeout

**Example:**
```python
msg = conn.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
```

### conn.close()

Close the connection.

**Example:**
```python
conn.close()
```

### conn.connected()

Check if the connection is still open.

**Returns:** True if connected, False otherwise

**Example:**
```python
if conn.connected():
    conn.send("Still here!")
```

## TCP Listener Methods

### listener.accept(timeout=30)

Accept an incoming TCP connection.

**Parameters:**

- `timeout` (number, optional): Timeout in seconds (default: 30)

**Returns:** Connection object or None on timeout

**Example:**
```python
conn = server.accept(timeout=60)
if conn:
    print(f"Connection from {conn.remote_addr}")
```

### listener.close()

Close the listener and stop accepting connections.

**Example:**
```python
server.close()
```

### listener.addr

The local address the listener is bound to (string).

## UDP Listener Methods

### listener.receive(timeout=30)

Receive a message from any sender.

**Parameters:**

- `timeout` (number, optional): Timeout in seconds (default: 30)

**Returns:** Dict with `"data"` and `"source"` keys, or None on timeout

**Example:**
```python
msg = udp_server.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
```

### listener.send_to(address, message)

Send a message to a specific address.

**Parameters:**

- `address` (string): Target address (e.g., `"192.168.1.1:8080"`)
- `message` (string or dict): Message to send

**Example:**
```python
udp_server.send_to("192.168.1.1:8080", "Reply!")
```

### listener.close()

Close the UDP listener.

## Examples

### TCP Echo Server

```python
import scriptling.net.unicast as uc

server = uc.listen("0.0.0.0", 8080)
print(f"Listening on {server.addr}")

conn = server.accept(timeout=60)
if conn:
    print(f"Connection from {conn.remote_addr}")
    msg = conn.receive(timeout=30)
    if msg:
        conn.send("Echo: " + msg["data"])
    conn.close()

server.close()
```

### TCP Client

```python
import scriptling.net.unicast as uc

conn = uc.connect("127.0.0.1", 8080, protocol="tcp")
conn.send("Hello, server!")

msg = conn.receive(timeout=5)
if msg:
    print(f"Server said: {msg['data']}")

conn.close()
```

### UDP Client/Server

```python
import scriptling.net.unicast as uc

# Server
server = uc.listen("0.0.0.0", 9090, protocol="udp")
msg = server.receive(timeout=10)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
    server.send_to(msg["source"], "Got it!")
server.close()

# Client
conn = uc.connect("127.0.0.1", 9090, protocol="udp")
conn.send("Hello UDP!")
msg = conn.receive(timeout=5)
if msg:
    print(f"Reply: {msg['data']}")
conn.close()
```

### Multi-Connection Server

```python
import scriptling.net.unicast as uc

server = uc.listen("0.0.0.0", 8080)

connections = []
while True:
    conn = server.accept(timeout=60)
    if conn is None:
        continue

    msg = conn.receive(timeout=30)
    if msg:
        for c in connections:
            if c.connected():
                c.send(msg["data"])
        connections.append(conn)
    else:
        conn.close()

server.close()
```

### Using Dict Messages

```python
import scriptling.net.unicast as uc

conn = uc.connect("127.0.0.1", 8080, protocol="tcp")

# Dicts are automatically JSON encoded
conn.send({"action": "register", "name": "worker-1"})

msg = conn.receive(timeout=5)
if msg:
    import json
    data = json.loads(msg["data"])
    print(data)

conn.close()
```

## Error Handling

```python
import scriptling.net.unicast as uc

server = uc.listen("0.0.0.0", 8080)

try:
    conn = server.accept(timeout=60)
    if conn:
        try:
            msg = conn.receive(timeout=30)
            if msg:
                conn.send("Echo: " + msg["data"])
        finally:
            conn.close()
finally:
    server.close()
```

## Notes

- UDP is unreliable - messages may be lost, duplicated, or reordered
- TCP provides reliable, ordered delivery
- Maximum UDP message size is approximately 65KB
- `receive()` returns None on timeout - use `connected()` to check for disconnect
- Always call `close()` on connections and listeners to release resources
- Use `"0.0.0.0"` as the host to listen on all network interfaces
