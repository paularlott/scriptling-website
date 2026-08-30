---
description: UDP and TCP point-to-point messaging for direct host-to-host communication.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/networking/unicast/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/networking/unicast/
status: stable
tags:
    - libraries
    - networking
title: scriptling.net.unicast
type: API Reference
---
# scriptling.net.unicast

UDP and TCP point-to-point messaging for direct host-to-host communication.

## Overview

The `scriptling.net.unicast` library provides both client and server functionality for UDP and TCP connections. Use `connect()` to establish a connection to a remote host, or `listen()` to accept incoming connections.

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(host, port, protocol="udp", timeout=10)` | Connect to a remote host. |
| `listen(host, port=0, protocol="tcp")` | Listen for incoming connections. |

## Connection Object

The `connect()` function returns a connection object with the following methods and properties.

| Method | Description |
|--------|-------------|
| `send(message)` | Send a message to the remote peer. |
| `receive(timeout=30)` | Receive a message. |
| `close()` | Close the connection. |
| `connected()` | Check if the connection is still open. |

| Property | Type | Description |
|----------|------|-------------|
| `local_addr` | `str` | Local address of the connection. |
| `remote_addr` | `str` | Remote address of the connection. |

## TCP Listener Object

The `listen(protocol="tcp")` function returns a TCP listener object.

| Method/Property | Description |
|--------|-------------|
| `accept(timeout=30)` | Accept an incoming connection. |
| `close()` | Close the listener. |
| `addr` | `str` property: bound address. |

## UDP Listener Object

The `listen(protocol="udp")` function returns a UDP listener object.

| Method/Property | Description |
|--------|-------------|
| `receive(timeout=30)` | Receive from any sender. |
| `send_to(address, message)` | Send to a specific address. |
| `close()` | Close the listener. |
| `addr` | `str` property: bound address. |

## Functions

### `connect(host, port, protocol="udp", timeout=10)`

Connects to a remote host.

**Parameters:**
- `host` (`str`): Remote host address.
- `port` (`int`): Remote port number.
- `protocol` (`str`, optional): `"udp"` or `"tcp"`. Default: `"udp"`.
- `timeout` (`number`, optional): Connection timeout in seconds. Default: `10`.

**Returns:** `Connection`: connection object with `send()`, `receive()`, `close()`, `connected()` methods and `local_addr`, `remote_addr` properties.

```python
import scriptling.net.unicast as uc

conn = uc.connect("192.168.1.1", 8080, protocol="tcp")
```

### `listen(host, port=0, protocol="tcp")`

Listens for incoming connections.

**Parameters:**
- `host` (`str`): Bind address. Use `"0.0.0.0"` for all interfaces.
- `port` (`int`, optional): Port number. Default: `0` (auto-assign).
- `protocol` (`str`, optional): `"udp"` or `"tcp"`. Default: `"tcp"`.

**Returns:** a TCP listener with `accept()`, `close()`, `addr` if `protocol="tcp"`, or a UDP listener with `receive()`, `send_to()`, `close()`, `addr` if `protocol="udp"`.

```python
import scriptling.net.unicast as uc

server = uc.listen("0.0.0.0", 8080)
print(f"Listening on {server.addr}")
```

### `conn.send(message)`

Sends a message to the remote peer.

**Parameters:**
- `message` (`str` or `dict`): Message to send. Dicts are automatically JSON encoded.

**Returns:** `None`

```python
conn.send("Hello!")
conn.send({"action": "ping"})
```

### `conn.receive(timeout=30)`

Receives a message.

**Parameters:**
- `timeout` (`number`, optional): Timeout in seconds. Default: `30`.

**Returns:** `dict`: a dict with `"data"` ([`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) — call `.decode()` for text) and `"source"` (`str`) keys, or `None` on timeout.

```python
msg = conn.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
```

### `conn.close()`

Closes the connection.

**Parameters:** None

**Returns:** `None`

```python
conn.close()
```

### `conn.connected()`

Checks if the connection is still open.

**Parameters:** None

**Returns:** `bool`: `True` if connected, `False` otherwise.

```python
if conn.connected():
    conn.send("Still here!")
```

### `listener.accept(timeout=30)`

Accepts an incoming TCP connection.

**Parameters:**
- `timeout` (`number`, optional): Timeout in seconds. Default: `30`.

**Returns:** `Connection`: a connection object, or `None` on timeout.

```python
conn = server.accept(timeout=60)
if conn:
    print(f"Connection from {conn.remote_addr}")
```

### `listener.close()`

Closes the listener and stops accepting connections.

**Parameters:** None

**Returns:** `None`

```python
server.close()
```

### `listener.addr`

The local address the listener is bound to.

**Type:** `str` property.

### `listener.receive(timeout=30)` (UDP)

Receives a message from any sender.

**Parameters:**
- `timeout` (`number`, optional): Timeout in seconds. Default: `30`.

**Returns:** `dict`: a dict with `"data"` ([`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) — call `.decode()` for text) and `"source"` (`str`) keys, or `None` on timeout.

```python
msg = udp_server.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
```

### `listener.send_to(address, message)` (UDP)

Sends a message to a specific address.

**Parameters:**
- `address` (`str`): Target address, e.g. `"192.168.1.1:8080"`.
- `message` (`str` or `dict`): Message to send.

**Returns:** `None`

```python
udp_server.send_to("192.168.1.1:8080", "Reply!")
```

### `listener.close()` (UDP)

Closes the UDP listener.

**Parameters:** None

**Returns:** `None`

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.net.unicast` opens raw UDP and TCP sockets, letting scripts initiate outbound connections to any reachable host/port (`connect()`) or bind a listening socket to accept inbound connections (`listen()`). The library does not restrict which hosts, ports, or interfaces a script can use: that is the embedder's responsibility, typically enforced with OS-level firewalling or network namespacing around the process. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

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

- UDP is unreliable - messages may be lost, duplicated, or reordered.
- TCP provides reliable, ordered delivery.
- Maximum UDP message size is approximately 65KB.
- `receive()` returns `None` on timeout - use `connected()` to check for disconnect.
- Always call `close()` on connections and listeners to release resources.
- Use `"0.0.0.0"` as the host to listen on all network interfaces.

## See Also

- [scriptling.net.multicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/multicast.md): one-to-many UDP group messaging
- [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/gossip.md): gossip protocol cluster membership and messaging
- [scriptling.net.websocket](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/websocket.md): WebSocket client library
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md): full risk breakdown across all libraries
