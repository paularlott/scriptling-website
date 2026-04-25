---
title: scriptling.net.multicast
linkTitle: multicast
weight: 2
---

UDP multicast group messaging for one-to-many communication on local networks.

## Overview

The `scriptling.net.multicast` library provides UDP multicast support for sending messages to a group of hosts simultaneously. It uses IP multicast addresses (224.0.0.0 - 239.255.255.255) to deliver messages to all members of a multicast group.

## Available Functions

| Function | Description |
|----------|-------------|
| `join(group_addr, port, interface="", ttl=1)` | Join a multicast group |

## Group Object Methods

The `join()` function returns a group object with these methods:

| Method | Description |
|--------|-------------|
| `send(message)` | Send a message to the group |
| `receive(timeout=30)` | Receive a message from the group |
| `close()` | Leave the group and close the connection |

## Group Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `group_addr` | string | Multicast group address |
| `port` | int | Multicast port number |
| `local_addr` | string | Local bound address |

## Setup

```go
import scriptlingmulticast "github.com/paularlott/scriptling/extlibs/net/multicast"

scriptlingmulticast.Register(p)
```

## Functions

### scriptling.net.multicast.join(group_addr, port, interface="", ttl=1)

Join a multicast group.

**Parameters:**

- `group_addr` (string): Multicast group address (e.g., `"239.1.1.1"`)
- `port` (int): Port number for the multicast group
- `interface` (string, optional): Network interface to bind to (default: auto-select)
- `ttl` (int, optional): Multicast TTL / hop limit (default: `1`, local network only; increase to route across subnets)

**Returns:** Group object with `send()`, `receive()`, `close()` methods and `group_addr`, `port`, `local_addr` properties

**Example:**
```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)
```

To route across subnets, increase the TTL:

```python
group = mc.join("239.1.1.1", 9999, ttl=4)
```

## Group Methods

### group.send(message)

Send a message to the multicast group.

**Parameters:**

- `message` (string or dict): Message to send. Dicts are automatically JSON encoded.

**Example:**
```python
group.send("Hello group!")
group.send({"type": "ping", "ts": 1234})
```

### group.receive(timeout=30)

Receive a message from the multicast group.

**Parameters:**

- `timeout` (number, optional): Timeout in seconds (default: 30)

**Returns:**

- Dict with `"data"` and `"source"` keys
- None on timeout

**Example:**
```python
msg = group.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
else:
    print("No message received (timeout)")
```

### group.close()

Leave the multicast group and close the connection.

**Example:**
```python
group.close()
```

## Examples

### Basic Multicast

```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)
group.send("Hello group!")

msg = group.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")

group.close()
```

### Service Discovery

```python
import scriptling.net.multicast as mc
import json

group = mc.join("239.1.1.1", 9999)

# Announce this service
group.send(json.dumps({"service": "api", "port": 8080, "host": "10.0.0.5"}))

# Listen for other services
msg = group.receive(timeout=10)
if msg:
    info = json.loads(msg["data"])
    print(f"Found {info['service']} at {info['host']}:{info['port']}")

group.close()
```

### Continuous Listener

```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)

while True:
    msg = group.receive(timeout=60)
    if msg:
        print(f"[{msg['source']}] {msg['data']}")

group.close()
```

### Using Dict Messages

```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)

# Dicts are automatically JSON encoded
group.send({"action": "heartbeat", "node": "worker-1"})

msg = group.receive(timeout=5)
if msg:
    # msg["data"] is a JSON string
    import json
    data = json.loads(msg["data"])
    print(data["action"])

group.close()
```

## Error Handling

```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)

try:
    group.send("Hello!")
    msg = group.receive(timeout=5)
    if msg:
        print(f"Received: {msg['data']}")
finally:
    group.close()
```

## Notes

- Only IP multicast addresses (224.x.x.x - 239.x.x.x) are valid
- UDP multicast is inherently unreliable - messages may be lost
- Maximum message size is limited by UDP (approximately 65KB)
- Use `interface` parameter on multi-homed hosts to select the correct NIC
- Default TTL is `1` (local network only); set `ttl` higher to cross router hops
- Always call `close()` when done to release the socket
