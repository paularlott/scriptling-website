---
description: UDP multicast group messaging for one-to-many communication on local networks.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/networking/multicast/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/networking/multicast/
status: stable
tags:
    - libraries
    - networking
title: scriptling.net.multicast
type: API Reference
---
# scriptling.net.multicast

UDP multicast group messaging for one-to-many communication on local networks.

## Overview

The `scriptling.net.multicast` library provides UDP multicast support for sending messages to a group of hosts simultaneously. It uses IP multicast addresses (`224.0.0.0` - `239.255.255.255`) to deliver messages to all members of a multicast group.

## Available Functions

| Function | Description |
|----------|-------------|
| `join(group_addr, port, interface="", ttl=1)` | Join a multicast group. |

## Group Object

The `join()` function returns a group object with the following methods and properties.

| Method | Description |
|--------|-------------|
| `send(message)` | Send a message to the group. |
| `receive(timeout=30)` | Receive a message from the group. |
| `close()` | Leave the group and close the connection. |

| Property | Type | Description |
|----------|------|-------------|
| `group_addr` | `str` | Multicast group address. |
| `port` | `int` | Multicast port number. |
| `local_addr` | `str` | Local bound address. |

## Functions

### `join(group_addr, port, interface="", ttl=1)`

Joins a multicast group.

**Parameters:**
- `group_addr` (`str`): Multicast group address, e.g. `"239.1.1.1"`.
- `port` (`int`): Port number for the multicast group.
- `interface` (`str`, optional): Network interface to bind to. Default: `""` (auto-select).
- `ttl` (`int`, optional): Multicast TTL / hop limit. Default: `1` (local network only; increase to route across subnets).

**Returns:** `Group`: a group object with `send()`, `receive()`, `close()` methods and `group_addr`, `port`, `local_addr` properties.

```python
import scriptling.net.multicast as mc

group = mc.join("239.1.1.1", 9999)
```

To route across subnets, increase the TTL:

```python
group = mc.join("239.1.1.1", 9999, ttl=4)
```

### `group.send(message)`

Sends a message to the multicast group.

**Parameters:**
- `message` (`str` or `dict`): Message to send. Dicts are automatically JSON encoded.

**Returns:** `None`

```python
group.send("Hello group!")
group.send({"type": "ping", "ts": 1234})
```

### `group.receive(timeout=30)`

Receives a message from the multicast group.

**Parameters:**
- `timeout` (`number`, optional): Timeout in seconds. Default: `30`.

**Returns:** `dict`: a dict with `"data"` ([`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) — call `.decode()` for text) and `"source"` (`str`) keys, or `None` on timeout.

```python
msg = group.receive(timeout=5)
if msg:
    print(f"From {msg['source']}: {msg['data']}")
else:
    print("No message received (timeout)")
```

### `group.close()`

Leaves the multicast group and closes the connection.

**Parameters:** None

**Returns:** `None`

```python
group.close()
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.net.multicast` opens a raw UDP socket and joins a multicast group, allowing scripts to send and receive data with any other host on the local network segment (or further, if `ttl` is increased) that joins the same group address and port. The library does not restrict which group addresses or ports a script can join: that is the embedder's responsibility, typically enforced with OS-level firewalling or network namespacing. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

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

- Only IP multicast addresses (`224.x.x.x` - `239.x.x.x`) are valid.
- UDP multicast is inherently unreliable - messages may be lost.
- Maximum message size is limited by UDP (approximately 65KB).
- Use the `interface` parameter on multi-homed hosts to select the correct NIC.
- Default TTL is `1` (local network only); set `ttl` higher to cross router hops.
- Always call `close()` when done to release the socket.

## See Also

- [scriptling.net.unicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/unicast.md): direct point-to-point UDP/TCP messaging
- [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/gossip.md): gossip protocol cluster membership and messaging
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md): full risk breakdown across all libraries
