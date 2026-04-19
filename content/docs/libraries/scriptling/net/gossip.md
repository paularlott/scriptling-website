---
title: scriptling.net.gossip
linkTitle: gossip
weight: 1
---

Gossip protocol cluster membership and messaging with automatic failure detection, metadata propagation, tag-based routing, encryption, and compression.

## Overview

The `scriptling.net.gossip` library implements a gossip protocol for decentralized cluster management. Nodes automatically discover each other, detect failures, and propagate metadata across the cluster. It supports both unreliable (UDP) and reliable (TCP) messaging with optional AES encryption and Snappy compression.

## Available Functions

| Function | Description |
|----------|-------------|
| `create(bind_addr, ...)` | Create a gossip cluster node |
| `decode_json(json_string)` | Decode a JSON string to a scriptling value |

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `MSG_USER` | 128 | Minimum user-defined message type |

## Cluster Methods

The `create()` function returns a cluster object with these methods:

| Method | Description |
|--------|-------------|
| `start()` | Start the cluster node |
| `join(peers)` | Join an existing cluster |
| `leave()` | Gracefully leave the cluster |
| `stop()` | Stop the cluster and clean up |
| `send(type, data, reliable=False)` | Broadcast to all nodes |
| `send_tagged(tag, type, data, reliable=False)` | Send to nodes with matching tag |
| `send_to(node_id, type, data, reliable=False)` | Send to a specific node |
| `handle(type, handler)` | Register a message handler |
| `on_state_change(handler)` | Register a state change handler |
| `nodes()` | Get all known nodes |
| `alive_nodes()` | Get all alive nodes |
| `local_node()` | Get local node info |
| `num_nodes()` | Get total node count |
| `num_alive()` | Get alive node count |
| `node_id()` | Get local node UUID |
| `set_metadata(key, value)` | Set local metadata |
| `get_metadata(key)` | Get local metadata value |
| `all_metadata()` | Get all local metadata |
| `delete_metadata(key)` | Delete a metadata key |

## Setup

```go
import scriptlinggossip "github.com/paularlott/scriptling/extlibs/net/gossip"

scriptlinggossip.Register(p, log)
```

## Functions

### scriptling.net.gossip.create(bind_addr="127.0.0.1:8000", ...)

Create a gossip cluster node.

**Parameters:**

- `bind_addr` (string): Address to bind to (default: `"127.0.0.1:8000"`)
- `node_id` (string): Unique node ID (auto-generated if empty)
- `advertise_addr` (string): Address to advertise to peers (default: same as bind_addr)
- `encryption_key` (string): Encryption key (16, 24, or 32 bytes for AES)
- `tags` (list): Tags for tag-based message routing
- `compression` (bool): Enable Snappy compression (default: False)
- `bearer_token` (string): Authentication bearer token
- `app_version` (string): Application version for compatibility checks

**Returns:** Cluster object

**Example:**
```python
import scriptling.net.gossip as gossip

cluster = gossip.create(
    bind_addr="127.0.0.1:8000",
    tags=["web"],
    encryption_key="0123456789abcdef"
)
```

## Cluster Methods

### cluster.start()

Start the cluster node. Begins transport, health monitoring, and gossip routines.

**Example:**
```python
cluster.start()
```

### cluster.join(peers)

Join an existing cluster by connecting to known peers.

**Parameters:**

- `peers` (string or list): One or more peer addresses to join

**Example:**
```python
cluster.join("127.0.0.1:8001")
cluster.join(["127.0.0.1:8001", "127.0.0.1:8002"])
```

### cluster.leave()

Gracefully leave the cluster. Other nodes will be notified.

**Example:**
```python
cluster.leave()
```

### cluster.stop()

Stop the cluster and clean up all resources.

**Example:**
```python
cluster.stop()
```

### cluster.send(message_type, data, reliable=False)

Broadcast a message to all cluster nodes.

**Parameters:**

- `message_type` (int): Message type (must be >= 128)
- `data`: Message payload (string, int, float, list, dict)
- `reliable` (bool): Use reliable TCP transport (default: False)

**Example:**
```python
cluster.send(128, "Hello cluster!")
cluster.send(128, {"key": "value"}, reliable=True)
```

### cluster.send_tagged(tag, message_type, data, reliable=False)

Send a tagged message. Only delivered to nodes that have the matching tag.

**Parameters:**

- `tag` (string): Tag for routing
- `message_type` (int): Message type (must be >= 128)
- `data`: Message payload
- `reliable` (bool): Use reliable transport (default: False)

**Example:**
```python
cluster.send_tagged("web", 128, "Hello web nodes!")
```

### cluster.send_to(node_id, message_type, data, reliable=False)

Send a direct message to a specific node.

**Parameters:**

- `node_id` (string): Target node UUID
- `message_type` (int): Message type (must be >= 128)
- `data`: Message payload
- `reliable` (bool): Use reliable transport (default: False)

**Example:**
```python
target = cluster.nodes()[0]
cluster.send_to(target["id"], 128, "Direct message!")
```

### cluster.handle(message_type, handler)

Register a handler for a specific message type.

**Parameters:**

- `message_type` (int): Message type to handle (must be >= 128)
- `handler` (function): Handler function called with a message dict

The handler receives a dict with:
- `type`: message type (int)
- `sender`: dict with `id`, `addr`, `state`, `metadata`
- `payload`: decoded message payload

**Example:**
```python
def on_message(msg):
    print(f"From {msg['sender']['id']}: {msg['payload']}")

cluster.handle(128, on_message)
```

### cluster.on_state_change(handler)

Register a handler called when any node changes state.

**Parameters:**

- `handler` (function): Handler function(node_id, new_state)

States: `"alive"`, `"suspect"`, `"dead"`, `"leaving"`

**Example:**
```python
def on_change(node_id, state):
    print(f"Node {node_id} is now {state}")

cluster.on_state_change(on_change)
```

### cluster.nodes()

Get all known nodes in the cluster.

**Returns:** List of node dicts with `id`, `addr`, `state`, `metadata`

**Example:**
```python
for node in cluster.nodes():
    print(f"{node['id']}: {node['state']} at {node['addr']}")
```

### cluster.alive_nodes()

Get all nodes currently in the alive state.

**Returns:** List of node dicts

### cluster.local_node()

Get the local node information.

**Returns:** Node dict with `id`, `addr`, `state`, `metadata`

### cluster.num_nodes()

Get the total number of known nodes.

**Returns:** int

### cluster.num_alive()

Get the number of alive nodes.

**Returns:** int

### cluster.node_id()

Get the local node's unique UUID.

**Returns:** string

### cluster.set_metadata(key, value)

Set a local node metadata value. Metadata is automatically gossiped to other nodes.

**Parameters:**

- `key` (string): Metadata key
- `value` (string, int, float, or bool): Metadata value

**Example:**
```python
cluster.set_metadata("role", "worker")
cluster.set_metadata("version", 2)
```

### cluster.get_metadata(key)

Get a local metadata value.

**Parameters:**

- `key` (string): Metadata key

**Returns:** string or None

### cluster.all_metadata()

Get all local metadata.

**Returns:** dict

### cluster.delete_metadata(key)

Delete a metadata key.

**Parameters:**

- `key` (string): Metadata key to delete

### scriptling.net.gossip.decode_json(json_string)

Decode a JSON string to a scriptling value.

**Parameters:**

- `json_string` (string): JSON string to decode

**Returns:** Decoded value (dict, list, string, int, float, bool, or None)

## Examples

### Basic Cluster

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="127.0.0.1:8000")
cluster.start()
cluster.join(["127.0.0.1:8001"])

cluster.handle(128, lambda msg: print(msg["payload"]))
cluster.send(128, "Hello!")

cluster.stop()
```

### Three-Node Cluster with Tags

```python
import scriptling.net.gossip as gossip

# Node 1 - web server
web = gossip.create(bind_addr="127.0.0.1:8000", tags=["web"])
web.start()

# Node 2 - worker
worker = gossip.create(bind_addr="127.0.0.1:8001", tags=["worker"])
worker.start()
worker.join(["127.0.0.1:8000"])

# Node 3 - both
hybrid = gossip.create(bind_addr="127.0.0.1:8002", tags=["web", "worker"])
hybrid.start()
hybrid.join(["127.0.0.1:8000"])

# Only web-tagged nodes receive this
web.send_tagged("web", 128, "Hello web nodes!")
```

### Metadata and State Monitoring

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="127.0.0.1:8000")
cluster.set_metadata("role", "leader")
cluster.set_metadata("version", 2)
cluster.start()

cluster.on_state_change(lambda node_id, state:
    print(f"Node {node_id} -> {state}")
)

cluster.join(["127.0.0.1:8001"])

# Check other nodes' metadata
for node in cluster.alive_nodes():
    print(f"{node['id']}: {node['metadata']}")
```

### Encrypted Cluster

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(
    bind_addr="0.0.0.0:8000",
    encryption_key="32-byte-key-here-1234567890ab",
    compression=True,
    bearer_token="secret-token"
)
cluster.start()
cluster.join(["10.0.0.1:8000"])
```

## Notes

- Message types 0-127 are reserved for internal protocol use
- User message types must be >= 128 (use `MSG_USER` constant)
- `reliable=True` uses TCP for guaranteed delivery
- Metadata is eventually consistent across the cluster
- Always call `stop()` to properly clean up resources
