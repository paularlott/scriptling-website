---
description: Networking libraries for cluster membership, multicast, point-to-point messaging, and WebSocket communication.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/networking/
sources:
    - resource: https://scriptling.dev/reference/libraries/networking/
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
| [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md) | Gossip protocol cluster membership and messaging |
| [scriptling.net.multicast](https://scriptling.dev/okf/scriptling-libraries/networking/multicast.md) | UDP multicast group messaging |
| [scriptling.net.resolve](https://scriptling.dev/okf/scriptling-libraries/networking/resolve.md) | DNS resolution for IP, SRV, and srv+http URLs |
| [scriptling.net.unicast](https://scriptling.dev/okf/scriptling-libraries/networking/unicast.md) | UDP and TCP point-to-point messaging |
| [scriptling.net.websocket](https://scriptling.dev/okf/scriptling-libraries/networking/websocket.md) | WebSocket client for connecting to WebSocket servers |

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

- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/./runtime.md) - HTTP and JSON-RPC server libraries
- [scriptling.ai](https://scriptling.dev/okf/scriptling-libraries/./ai.md) - AI agents that can drive networked tools
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) - Network-enabled libraries risk breakdown
