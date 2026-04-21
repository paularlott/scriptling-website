---
title: scriptling.net.gossip
linkTitle: gossip
weight: 1
---

Gossip protocol cluster membership and messaging with automatic failure detection, metadata propagation, tag-based routing, node groups, leader election, encryption, and compression.

## Overview

The `scriptling.net.gossip` library implements a gossip protocol for decentralized cluster management. Nodes automatically discover each other, detect failures, and propagate metadata across the cluster. It supports both unreliable (UDP) and reliable (TCP) messaging with optional AES encryption and Snappy compression.

Advanced features include request/reply messaging, metadata-criteria-based node groups, and quorum-based leader election with optional metadata filtering.

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
| `send_request(node_id, type, data)` | Send request and wait for reply |
| `handle(type, handler)` | Register a message handler |
| `handle_with_reply(type, handler)` | Register a request/reply handler |
| `unhandle(type)` | Remove a registered handler |
| `on_state_change(handler)` | Register a state change handler |
| `on_metadata_change(handler)` | Register a metadata change handler |
| `on_gossip_interval(handler)` | Register a periodic gossip handler |
| `nodes()` | Get all known nodes |
| `alive_nodes()` | Get all alive nodes |
| `nodes_by_tag(tag)` | Get nodes with a specific tag |
| `get_node(node_id)` | Get a specific node by ID |
| `local_node()` | Get local node info |
| `num_nodes()` | Get total node count |
| `num_alive()` | Get alive node count |
| `num_suspect()` | Get suspect node count |
| `num_dead()` | Get dead node count |
| `node_id()` | Get local node UUID |
| `is_local(node_id)` | Check if node ID is local |
| `candidates()` | Get random subset of nodes for gossiping |
| `set_metadata(key, value)` | Set local metadata |
| `get_metadata(key)` | Get local metadata value |
| `all_metadata()` | Get all local metadata |
| `delete_metadata(key)` | Delete a metadata key |
| `create_node_group(criteria, ...)` | Create a metadata-criteria node group |
| `create_leader_election(...)` | Create a leader election manager |

## Node Group Methods

The `create_node_group()` method returns a node group object:

| Method | Description |
|--------|-------------|
| `nodes()` | Get all nodes in the group |
| `contains(node_id)` | Check if a node is in the group |
| `count()` | Get number of nodes in the group |
| `send_to_peers(type, data, reliable=False)` | Send to all group peers |
| `close()` | Close the group and release resources |

## Leader Election Methods

The `create_leader_election()` method returns a leader election object:

| Method | Description |
|--------|-------------|
| `start()` | Start the election process |
| `stop()` | Stop the election process |
| `is_leader()` | Check if this node is the leader |
| `has_leader()` | Check if a leader is elected |
| `get_leader_id()` | Get the leader's node ID |
| `send_to_peers(type, data, reliable=False)` | Send to eligible peers |
| `on_event(event_type, handler)` | Register an election event handler |

### Leader Election Events

| Event | Description |
|-------|-------------|
| `"elected"` | A leader has been elected |
| `"lost"` | The current leader has been lost |
| `"became_leader"` | This node became the leader |
| `"stepped_down"` | This node stepped down from leadership |

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
- `transport` (string): Transport type: `"socket"` or `"http"` (default: `"socket"`)

**Advanced Configuration:**

- `compress_min_size` (int): Min message size for compression (default: 256)
- `gossip_interval` (string): Gossip interval duration (default: `"5s"`)
- `gossip_max_interval` (string): Max gossip interval (default: `"20s"`)
- `metadata_gossip_interval` (string): Metadata gossip interval (default: `"500ms"`)
- `state_gossip_interval` (string): State exchange interval (default: `"45s"`)
- `fan_out_multiplier` (float): Fan-out scaling factor (default: 1.0)
- `ttl_multiplier` (float): TTL scaling factor (default: 1.0)
- `state_exchange_multiplier` (float): State exchange scaling (default: 0.8)
- `force_reliable_transport` (bool): Force TCP for all messages (default: False)
- `prefer_ipv6` (bool): Prefer IPv6 for DNS resolution (default: False)
- `node_cleanup_interval` (string): Dead node cleanup interval (default: `"20s"`)
- `node_retention_time` (string): How long to keep dead nodes (default: `"1h"`)
- `leaving_node_timeout` (string): Timeout before moving leaving to dead (default: `"30s"`)
- `health_check_interval` (string): Health check interval (default: `"2s"`)
- `suspect_timeout` (string): Time before marking node suspect (default: `"1.5s"`)
- `suspect_retry_interval` (string): Suspect node retry interval (default: `"1s"`)
- `dead_node_timeout` (string): Time before marking suspect to dead (default: `"15s"`)
- `peer_recovery_interval` (string): Peer recovery check interval (default: `"30s"`)
- `insecure_skip_verify` (bool): Skip TLS verification for HTTP (default: False)

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

### cluster.send_request(node_id, message_type, data)

Send a request to a specific node and wait for a reply.

**Parameters:**

- `node_id` (string): Target node UUID
- `message_type` (int): Message type (must be >= 128)
- `data`: Message payload

**Returns:** The reply payload from the target node

**Example:**
```python
reply = cluster.send_request(target_id, 128, {"cmd": "ping"})
print(reply)
```

### cluster.handle(message_type, handler)

Register a handler for a specific message type.

**Parameters:**

- `message_type` (int): Message type to handle (must be >= 128)
- `handler` (function): Handler function called with a message dict

The handler receives a dict with:
- `type`: message type (int)
- `sender`: dict with `id`, `addr`, `state`, `metadata`, `tags`
- `payload`: decoded message payload

**Example:**
```python
def on_message(msg):
    print(f"From {msg['sender']['id']}: {msg['payload']}")

cluster.handle(128, on_message)
```

### cluster.handle_with_reply(message_type, handler)

Register a request/reply handler. The handler must return the reply data.

**Parameters:**

- `message_type` (int): Message type to handle (must be >= 128)
- `handler` (function): Handler function called with a message dict, must return reply data

The handler receives the same dict as `handle()`.

**Example:**
```python
def on_request(msg):
    return {"status": "ok", "echo": msg["payload"]}

cluster.handle_with_reply(128, on_request)
```

### cluster.unhandle(message_type)

Remove a previously registered message handler.

**Parameters:**

- `message_type` (int): Message type to unregister (must be >= 128)

**Returns:** bool - True if a handler was removed

**Example:**
```python
cluster.unhandle(128)
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

### cluster.on_metadata_change(handler)

Register a handler called when any remote node's metadata changes.

**Parameters:**

- `handler` (function): Handler function(node_dict)

**Example:**
```python
def on_meta(node):
    print(f"Node {node['id']} metadata: {node['metadata']}")

cluster.on_metadata_change(on_meta)
```

### cluster.on_gossip_interval(handler)

Register a handler called every gossip interval.

**Parameters:**

- `handler` (function): Handler function() called at each interval

**Example:**
```python
def on_tick():
    print(f"Alive: {cluster.num_alive()}")

cluster.on_gossip_interval(on_tick)
```

### cluster.nodes()

Get all known nodes in the cluster.

**Returns:** List of node dicts with `id`, `addr`, `state`, `metadata`, `tags`

**Example:**
```python
for node in cluster.nodes():
    print(f"{node['id']}: {node['state']} at {node['addr']}")
```

### cluster.alive_nodes()

Get all nodes currently in the alive state.

**Returns:** List of node dicts

### cluster.nodes_by_tag(tag)

Get all nodes that have a specific tag.

**Parameters:**

- `tag` (string): Tag to filter by

**Returns:** List of node dicts with the matching tag

**Example:**
```python
web_nodes = cluster.nodes_by_tag("web")
```

### cluster.get_node(node_id)

Get a specific node by ID.

**Parameters:**

- `node_id` (string): Node UUID

**Returns:** Node dict or None if not found

**Example:**
```python
node = cluster.get_node("some-uuid")
if node:
    print(node["state"])
```

### cluster.local_node()

Get the local node information.

**Returns:** Node dict with `id`, `addr`, `state`, `metadata`, `tags`

### cluster.num_nodes()

Get the total number of known nodes.

**Returns:** int

### cluster.num_alive()

Get the number of alive nodes.

**Returns:** int

### cluster.num_suspect()

Get the number of suspect nodes.

**Returns:** int

### cluster.num_dead()

Get the number of dead nodes.

**Returns:** int

### cluster.node_id()

Get the local node's unique UUID.

**Returns:** string

### cluster.is_local(node_id)

Check if a node ID refers to the local node.

**Parameters:**

- `node_id` (string): Node UUID to check

**Returns:** bool

**Example:**
```python
if cluster.is_local(node["id"]):
    print("That's me!")
```

### cluster.candidates()

Get a random subset of nodes for gossiping.

**Returns:** List of node dicts

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

### cluster.create_node_group(criteria, on_node_added=None, on_node_removed=None)

Create a metadata-criteria-based node group. The group automatically tracks nodes whose metadata matches the criteria.

**Parameters:**

- `criteria` (dict): Metadata key-value pairs to match. Use `"*"` for any value, `"~value"` for contains
- `on_node_added` (function, optional): Callback function(node_dict) when a node joins the group
- `on_node_removed` (function, optional): Callback function(node_dict) when a node leaves the group

**Returns:** NodeGroup object

**Example:**
```python
workers = cluster.create_node_group(
    criteria={"role": "worker"},
    on_node_added=lambda n: print(f"Worker joined: {n['id']}")
)
print(f"Workers: {workers.count()}")
workers.send_to_peers(128, {"task": "process"})
workers.close()
```

### cluster.create_leader_election(check_interval="1s", leader_timeout="3s", heartbeat_msg_type=65, quorum_percentage=60, metadata_criteria=None)

Create a leader election manager with quorum-based election.

**Parameters:**

- `check_interval` (string): Duration between leader checks (default: `"1s"`)
- `leader_timeout` (string): Duration without heartbeat before leader lost (default: `"3s"`)
- `heartbeat_msg_type` (int): Message type for heartbeats (default: 65, reserved range)
- `quorum_percentage` (int): Percentage of nodes required for quorum 1-100 (default: 60)
- `metadata_criteria` (dict, optional): Metadata criteria to limit eligible nodes

**Returns:** LeaderElection object

**Example:**
```python
election = cluster.create_leader_election(
    quorum_percentage=51,
    metadata_criteria={"role": "leader-eligible"}
)

election.on_event("became_leader", lambda e, n: print("I'm leader!"))
election.on_event("stepped_down", lambda e, n: print("Stepped down"))
election.start()
```

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

cluster.on_metadata_change(lambda node:
    print(f"Node {node['id']} metadata changed")
)

cluster.join(["127.0.0.1:8001"])

# Check other nodes' metadata
for node in cluster.alive_nodes():
    print(f"{node['id']}: {node['metadata']}")
```

### Request/Reply Messaging

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="127.0.0.1:8000")
cluster.start()

# Register a handler that returns a reply
cluster.handle_with_reply(128, lambda msg: {"echo": msg["payload"]})

# Send a request and wait for the reply
for node in cluster.alive_nodes():
    reply = cluster.send_request(node["id"], 128, "ping")
    print(f"Reply from {node['id']}: {reply}")
```

### Node Groups

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="127.0.0.1:8000")
cluster.set_metadata("role", "coordinator")
cluster.start()
cluster.join(["127.0.0.1:8001"])

# Create a group that tracks worker nodes
workers = cluster.create_node_group(
    criteria={"role": "worker"},
    on_node_added=lambda n: print(f"Worker online: {n['id']}"),
    on_node_removed=lambda n: print(f"Worker offline: {n['id']}")
)

# Send tasks to all workers
workers.send_to_peers(128, {"task": "process_data"})

print(f"Active workers: {workers.count()}")
workers.close()
```

### Leader Election

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(bind_addr="127.0.0.1:8000")
cluster.start()
cluster.join(["127.0.0.1:8001", "127.0.0.1:8002"])

election = cluster.create_leader_election(quorum_percentage=51)

election.on_event("became_leader", lambda e, n: print("I became the leader!"))
election.on_event("stepped_down", lambda e, n: print("I stepped down"))
election.on_event("elected", lambda e, n: print(f"Leader elected: {n}"))
election.on_event("lost", lambda e, n: print("Leader lost"))

election.start()

if election.is_leader():
    print("Performing leader-only tasks")
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
- Node group criteria support `"*"` wildcard and `"~value"` contains matching
- Leader election heartbeat message types use the reserved range (< 128)
