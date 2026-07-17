---
title: Networking Libraries
linkTitle: Networking
description: Networking libraries for cluster membership, multicast, point-to-point messaging, and WebSocket communication.
tags: [libraries, networking]
weight: 4
---

Networking libraries for distributed communication patterns using the `scriptling.net` namespace.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.net.gossip](gossip/) | Gossip protocol cluster membership and messaging |
| [scriptling.net.multicast](multicast/) | UDP multicast group messaging |
| [scriptling.net.resolve](resolve/) | DNS resolution for IP, SRV, and srv+http URLs |
| [scriptling.net.unicast](unicast/) | UDP and TCP point-to-point messaging |
| [scriptling.net.websocket](websocket/) | WebSocket client for connecting to WebSocket servers |

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

- [scriptling.runtime](../runtime/) - HTTP and JSON-RPC server libraries
- [scriptling.ai](../ai/) - AI agents that can drive networked tools
- [Libraries](../../) - Full library reference index
- [Security Guide](/docs/security/#network-security) - Network-enabled libraries risk breakdown
