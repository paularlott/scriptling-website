---
title: Networking Libraries
linkTitle: Networking
description: Networking libraries for cluster membership, multicast, point-to-point messaging, WebSocket communication, and Mercure publish/subscribe.
tags: [libraries, networking]
weight: 14

aliases:
  - /reference/libraries/scriptling/networking/
---

Networking libraries for distributed communication patterns using the `scriptling.net` namespace, and `scriptling.mercure` for publishing and subscribing through Mercure hubs.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.net.gossip](gossip/) | Gossip protocol cluster membership and messaging |
| [scriptling.net.multicast](multicast/) | UDP multicast group messaging |
| [scriptling.net.resolve](resolve/) | DNS resolution for IP, SRV, and srv+http URLs |
| [scriptling.net.unicast](unicast/) | UDP and TCP point-to-point messaging |
| [scriptling.net.websocket](websocket/) | WebSocket client for connecting to WebSocket servers |
| [scriptling.mercure](mercure/) | Mercure hub client: publish updates and subscribe to topics over Server-Sent Events |

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

- [scriptling.mercure](mercure/) - Publish/subscribe through Mercure hubs
- [scriptling.runtime](../runtime/) - HTTP and JSON-RPC server libraries
- [scriptling.ai](../ai/) - AI agents that can drive networked tools
- [Libraries](../) - Full library reference index
- [Security Guide](/docs/security/#network-security) - Network-enabled libraries risk breakdown
