---
description: Networking libraries for cluster membership, multicast, point-to-point messaging, and WebSocket communication.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/networking/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/networking/
status: stable
tags:
    - libraries
    - networking
title: Networking Libraries
type: API Reference
---
# Networking Libraries

Networking libraries for distributed communication patterns using the `scriptling.net` namespace.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.net.gossip](networking/gossip.md) | Gossip protocol cluster membership and messaging |
| [scriptling.net.multicast](networking/multicast.md) | UDP multicast group messaging |
| [scriptling.net.resolve](networking/resolve.md) | DNS resolution for IP, SRV, and srv+http URLs |
| [scriptling.net.unicast](networking/unicast.md) | UDP and TCP point-to-point messaging |
| [scriptling.net.websocket](networking/websocket.md) | WebSocket client for connecting to WebSocket servers |

## Quick Start

```python
import scriptling.net.websocket as ws

# Connect to a WebSocket server
conn = ws.connect("wss://echo.websocket.org", timeout=5)

# Send and receive a message
conn.send("hello")
message = conn.receive()
print(message)

conn.close()
```

## See Also

- [scriptling.runtime](runtime.md) - HTTP and JSON-RPC server libraries
- [scriptling.ai](ai.md) - AI agents that can drive networked tools
- [Libraries](../scriptling-libraries.md) - Full library reference index
- [Security Guide](../../scriptling-docs/security.md#network-security) - Network-enabled libraries risk breakdown
