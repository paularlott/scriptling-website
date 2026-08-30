---
description: Gossip protocol cluster membership and messaging with failure detection and routing.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/networking/gossip/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/networking/gossip/
status: stable
tags:
    - libraries
    - networking
title: scriptling.net.gossip
type: API Reference
---
# scriptling.net.gossip

Gossip protocol cluster membership and messaging, with automatic failure detection, metadata propagation, tag-based routing, node groups, leader election, encryption, and compression.

## Overview

The `scriptling.net.gossip` library implements a gossip protocol for decentralized cluster management. Nodes automatically discover each other, detect failures, and propagate metadata across the cluster. It supports both unreliable (UDP) and reliable (TCP) messaging, with optional AES encryption and Snappy compression. Advanced features include request/reply messaging, metadata-criteria-based node groups, and quorum-based leader election with optional metadata filtering.

### Handler concurrency

All registered callbacks: `handle()`, `handle_with_reply()`, `on_state_change()`, `on_metadata_change()`, `on_gossip_interval()`, node-group `on_node_added`/`on_node_removed`, and leader-election `on_event()`: fire automatically as messages and events arrive. They run on gossip's internal goroutines under the per-environment interpreter lock (GIL). There is no event pump and no `wait()` loop: handlers invoke themselves.

Because the GIL serializes script execution, a handler never runs concurrently with the rest of your script, so you do not need locks around shared state. Handlers interleave with your script only at its blocking points (or `yield_now()`), which is memory-safe.

A long-running node just stays alive: do work, or sleep: and handlers fire as traffic arrives:

```python
cluster.handle(gossip.MSG_USER, on_message)

while True:
    time.sleep(1)   # keep the process alive; handlers fire as messages arrive
```

Ordering: gossip messages carry Hybrid Logical Clock (HLC) timestamps, so application-level ordering is resolved at the data layer: handler delivery order is not significant and may differ from arrival order.

A single script can both call `send_request()` and serve its own `handle_with_reply()` responder: `send_request()` releases the GIL while it blocks, letting an incoming request's handler run and reply.

## Available Functions

| Function | Description |
|----------|-------------|
| `create(bind_addr="127.0.0.1:8000", ...)` | Create a gossip cluster node. |

## Constants

| Constant | Description |
|----------|-------------|
| `MSG_USER` | Minimum user-defined message type (`128`). Message types below this are reserved for the internal protocol. |

## Cluster Object

The `create()` function returns a cluster object with the following methods.

| Method | Description |
|--------|-------------|
| `start()` | Start the cluster node. |
| `join(peers)` | Join an existing cluster. |
| `leave()` | Gracefully leave the cluster. |
| `stop()` | Stop the cluster and clean up. |
| `send(message_type, data, reliable=False)` | Broadcast to all nodes. |
| `send_tagged(tag, message_type, data, reliable=False)` | Send to nodes with a matching tag. |
| `send_to(node_id, message_type, data, reliable=False)` | Send to a specific node. |
| `send_request(node_id, message_type, data)` | Send a request and wait for a reply. |
| `handle(message_type, handler)` | Register a message handler. |
| `handle_with_reply(message_type, handler)` | Register a request/reply handler. |
| `unhandle(message_type)` | Remove a registered handler. |
| `on_state_change(handler)` | Register a node state-change handler. |
| `on_metadata_change(handler)` | Register a remote metadata-change handler. |
| `on_gossip_interval(handler)` | Register a periodic gossip-interval handler. |
| `nodes()` | Get all known nodes. |
| `alive_nodes()` | Get all alive nodes. |
| `nodes_by_tag(tag)` | Get nodes with a specific tag. |
| `get_node(node_id)` | Get a specific node by ID. |
| `local_node()` | Get local node info. |
| `num_nodes()` | Get the total known node count. |
| `num_alive()` | Get the alive node count. |
| `num_suspect()` | Get the suspect node count. |
| `num_dead()` | Get the dead node count. |
| `node_id()` | Get the local node's UUID. |
| `is_local(node_id)` | Check if a node ID is the local node. |
| `candidates()` | Get a random subset of nodes for gossiping. |
| `set_metadata(key, value)` | Set a local metadata value. |
| `get_metadata(key)` | Get a local metadata value. |
| `all_metadata()` | Get all local metadata. |
| `delete_metadata(key)` | Delete a metadata key. |
| `create_node_group(criteria, on_node_added=None, on_node_removed=None)` | Create a metadata-criteria node group. |
| `create_leader_election(...)` | Create a leader-election manager. |

### Node group object

The `create_node_group()` method returns a node group object.

| Method | Description |
|--------|-------------|
| `nodes()` | Get all nodes in the group. |
| `contains(node_id)` | Check if a node is in the group. |
| `count()` | Get the number of nodes in the group. |
| `send_to_peers(message_type, data, reliable=False)` | Send to all group peers. |
| `close()` | Close the group and release resources. |

### Leader election object

The `create_leader_election()` method returns a leader election object.

| Method | Description |
|--------|-------------|
| `start()` | Start the election process. |
| `stop()` | Stop the election process. |
| `is_leader()` | Check if this node is the leader. |
| `has_leader()` | Check if a leader is elected. |
| `get_leader_id()` | Get the leader's node ID. |
| `send_to_peers(message_type, data, reliable=False)` | Send to eligible peers. |
| `on_event(event_type, handler)` | Register an election event handler. |

Event types passed to `on_event()`:

| Event | Description |
|-------|-------------|
| `"elected"` | A leader has been elected. |
| `"lost"` | The current leader has been lost. |
| `"became_leader"` | This node became the leader. |
| `"stepped_down"` | This node stepped down from leadership. |

## Functions

### `create(bind_addr="127.0.0.1:8000", ...)`

Creates a gossip cluster node.

**Parameters:**
- `bind_addr` (`str`, optional): Address to bind to. Default: `"127.0.0.1:8000"`.
- `node_id` (`str`, optional): Unique node ID. Default: `""` (auto-generated).
- `advertise_addr` (`str`, optional): Address to advertise to peers. Default: same as `bind_addr`.
- `encryption_key` (`str`, optional): AES encryption key, 16, 24, or 32 bytes. Default: `""` (no encryption).
- `tags` (`list`, optional): Tags for tag-based message routing. Default: `[]`.
- `compression` (`bool`, optional): Enable Snappy compression. Default: `False`.
- `bearer_token` (`str`, optional): Authentication bearer token. Default: `""`.
- `app_version` (`str`, optional): Application version for compatibility checks. Default: `""`.
- `transport` (`str`, optional): Transport type, `"socket"` or `"http"`. Default: `"socket"`.
- `compress_min_size` (`int`, optional): Minimum message size for compression. Default: `256`.
- `gossip_interval` (`str`, optional): Gossip interval duration. Default: `"5s"`.
- `gossip_max_interval` (`str`, optional): Maximum gossip interval. Default: `"20s"`.
- `metadata_gossip_interval` (`str`, optional): Metadata gossip interval. Default: `"500ms"`.
- `state_gossip_interval` (`str`, optional): State exchange interval. Default: `"45s"`.
- `fan_out_multiplier` (`float`, optional): Fan-out scaling factor. Default: `1.0`.
- `ttl_multiplier` (`float`, optional): TTL scaling factor. Default: `1.0`.
- `state_exchange_multiplier` (`float`, optional): State exchange scaling. Default: `0.8`.
- `force_reliable_transport` (`bool`, optional): Force TCP for all messages. Default: `False`.
- `prefer_ipv6` (`bool`, optional): Prefer IPv6 for DNS resolution. Default: `False`.
- `node_cleanup_interval` (`str`, optional): Dead node cleanup interval. Default: `"20s"`.
- `node_retention_time` (`str`, optional): How long to keep dead nodes. Default: `"1h"`.
- `leaving_node_timeout` (`str`, optional): Timeout before moving a leaving node to dead. Default: `"30s"`.
- `health_check_interval` (`str`, optional): Health check interval. Default: `"2s"`.
- `suspect_timeout` (`str`, optional): Time before marking a node suspect. Default: `"1.5s"`.
- `suspect_retry_interval` (`str`, optional): Suspect node retry interval. Default: `"1s"`.
- `dead_node_timeout` (`str`, optional): Time before marking a suspect node dead. Default: `"15s"`.
- `peer_recovery_interval` (`str`, optional): Peer recovery check interval. Default: `"30s"`.
- `insecure_skip_verify` (`bool`, optional): Skip TLS verification for the `"http"` transport. Default: `False`.

**Returns:** `Cluster`: a cluster node object.

```python
import scriptling.net.gossip as gossip

cluster = gossip.create(
    bind_addr="127.0.0.1:8000",
    tags=["web"],
    encryption_key="0123456789abcdef"
)
```

### `cluster.start()`

Starts the cluster node. Begins the transport, health monitoring, and gossip routines.

**Parameters:** None

**Returns:** `None`

```python
cluster.start()
```

### `cluster.join(peers)`

Joins an existing cluster by connecting to known peers.

**Parameters:**
- `peers` (`str` or `list`): One or more peer addresses to join.

**Returns:** `None`

```python
cluster.join("127.0.0.1:8001")
cluster.join(["127.0.0.1:8001", "127.0.0.1:8002"])
```

### `cluster.leave()`

Gracefully leaves the cluster. Other nodes are notified.

**Parameters:** None

**Returns:** `None`

```python
cluster.leave()
```

### `cluster.stop()`

Stops the cluster and cleans up all resources.

**Parameters:** None

**Returns:** `None`

```python
cluster.stop()
```

### `cluster.send(message_type, data, reliable=False)`

Broadcasts a message to all cluster nodes.

**Parameters:**
- `message_type` (`int`): Message type. Must be `>= 128` (see `MSG_USER`).
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.
- `reliable` (`bool`, optional): Use reliable TCP transport instead of UDP. Default: `False`.

**Returns:** `None`

```python
cluster.send(128, "Hello cluster!")
cluster.send(128, {"key": "value"}, reliable=True)
```

### `cluster.send_tagged(tag, message_type, data, reliable=False)`

Sends a tagged message. Only delivered to nodes that have the matching tag.

**Parameters:**
- `tag` (`str`): Tag for routing.
- `message_type` (`int`): Message type. Must be `>= 128`.
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.
- `reliable` (`bool`, optional): Use reliable transport. Default: `False`.

**Returns:** `None`

```python
cluster.send_tagged("web", 128, "Hello web nodes!")
```

### `cluster.send_to(node_id, message_type, data, reliable=False)`

Sends a direct message to a specific node.

**Parameters:**
- `node_id` (`str`): Target node UUID.
- `message_type` (`int`): Message type. Must be `>= 128`.
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.
- `reliable` (`bool`, optional): Use reliable transport. Default: `False`.

**Returns:** `None`

```python
target = cluster.nodes()[0]
cluster.send_to(target["id"], 128, "Direct message!")
```

### `cluster.send_request(node_id, message_type, data)`

Sends a request to a specific node and waits for a reply. Releases the interpreter lock while waiting, so the calling script's own `handle_with_reply()` responders can still run.

**Parameters:**
- `node_id` (`str`): Target node UUID.
- `message_type` (`int`): Message type. Must be `>= 128`.
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.

**Returns:** the reply payload from the target node (type depends on what the remote handler returned).

```python
reply = cluster.send_request(target_id, 128, {"cmd": "ping"})
print(reply)
```

### `cluster.handle(message_type, handler)`

Registers a handler for a specific message type.

**Parameters:**
- `message_type` (`int`): Message type to handle. Must be `>= 128`.
- `handler` (`callable`): Function called with a message dict containing `type` (`int`), `sender` (`dict` with `id`, `addr`, `state`, `metadata`, `tags`), and `payload` (the decoded message payload).

**Returns:** `None`

```python
def on_message(msg):
    print(f"From {msg['sender']['id']}: {msg['payload']}")

cluster.handle(128, on_message)
```

### `cluster.handle_with_reply(message_type, handler)`

Registers a request/reply handler. The handler's return value is sent back as the reply.

**Parameters:**
- `message_type` (`int`): Message type to handle. Must be `>= 128`.
- `handler` (`callable`): Function called with the same message dict as `handle()`; its return value becomes the reply payload.

**Returns:** `None`

```python
def on_request(msg):
    return {"status": "ok", "echo": msg["payload"]}

cluster.handle_with_reply(128, on_request)
```

### `cluster.unhandle(message_type)`

Removes a previously registered message handler.

**Parameters:**
- `message_type` (`int`): Message type to unregister.

**Returns:** `bool`: `True` if a handler was removed.

```python
cluster.unhandle(128)
```

### `cluster.on_state_change(handler)`

Registers a handler called when any node changes state.

**Parameters:**
- `handler` (`callable`): Function called as `handler(node_id, new_state)`. `new_state` is one of `"alive"`, `"suspect"`, `"dead"`, `"leaving"`.

**Returns:** `None`

```python
def on_change(node_id, state):
    print(f"Node {node_id} is now {state}")

cluster.on_state_change(on_change)
```

### `cluster.on_metadata_change(handler)`

Registers a handler called when any remote node's metadata changes.

**Parameters:**
- `handler` (`callable`): Function called as `handler(node_dict)`.

**Returns:** `None`

```python
def on_meta(node):
    print(f"Node {node['id']} metadata: {node['metadata']}")

cluster.on_metadata_change(on_meta)
```

### `cluster.on_gossip_interval(handler)`

Registers a handler called at every gossip interval.

**Parameters:**
- `handler` (`callable`): Function called with no arguments at each interval.

**Returns:** `None`

```python
def on_tick():
    print(f"Alive: {cluster.num_alive()}")

cluster.on_gossip_interval(on_tick)
```

### `cluster.nodes()`

Gets all known nodes in the cluster.

**Parameters:** None

**Returns:** `list`: list of node dicts, each with `id`, `addr`, `state`, `metadata`, `tags`.

```python
for node in cluster.nodes():
    print(f"{node['id']}: {node['state']} at {node['addr']}")
```

### `cluster.alive_nodes()`

Gets all nodes currently in the alive state.

**Parameters:** None

**Returns:** `list`: list of node dicts.

### `cluster.nodes_by_tag(tag)`

Gets all nodes that have a specific tag.

**Parameters:**
- `tag` (`str`): Tag to filter by.

**Returns:** `list`: list of node dicts with the matching tag.

```python
web_nodes = cluster.nodes_by_tag("web")
```

### `cluster.get_node(node_id)`

Gets a specific node by ID.

**Parameters:**
- `node_id` (`str`): Node UUID.

**Returns:** `dict`: node dict, or `None` if not found.

```python
node = cluster.get_node("some-uuid")
if node:
    print(node["state"])
```

### `cluster.local_node()`

Gets the local node's information.

**Parameters:** None

**Returns:** `dict`: node dict with `id`, `addr`, `state`, `metadata`, `tags`.

### `cluster.num_nodes()`

Gets the total number of known nodes.

**Parameters:** None

**Returns:** `int`

### `cluster.num_alive()`

Gets the number of alive nodes.

**Parameters:** None

**Returns:** `int`

### `cluster.num_suspect()`

Gets the number of suspect nodes.

**Parameters:** None

**Returns:** `int`

### `cluster.num_dead()`

Gets the number of dead nodes.

**Parameters:** None

**Returns:** `int`

### `cluster.node_id()`

Gets the local node's unique UUID.

**Parameters:** None

**Returns:** `str`

### `cluster.is_local(node_id)`

Checks if a node ID refers to the local node.

**Parameters:**
- `node_id` (`str`): Node UUID to check.

**Returns:** `bool`

```python
if cluster.is_local(node["id"]):
    print("That's me!")
```

### `cluster.candidates()`

Gets a random subset of nodes for gossiping.

**Parameters:** None

**Returns:** `list`: list of node dicts.

### `cluster.set_metadata(key, value)`

Sets a local node metadata value. Metadata is automatically gossiped to other nodes.

**Parameters:**
- `key` (`str`): Metadata key.
- `value` (`str`, `int`, `float`, or `bool`): Metadata value.

**Returns:** `None`

```python
cluster.set_metadata("role", "worker")
cluster.set_metadata("version", 2)
```

### `cluster.get_metadata(key)`

Gets a local metadata value.

**Parameters:**
- `key` (`str`): Metadata key.

**Returns:** `str`: the value, or `None` if not set.

### `cluster.all_metadata()`

Gets all local metadata.

**Parameters:** None

**Returns:** `dict`

### `cluster.delete_metadata(key)`

Deletes a metadata key.

**Parameters:**
- `key` (`str`): Metadata key to delete.

**Returns:** `None`

### `cluster.create_node_group(criteria, on_node_added=None, on_node_removed=None)`

Creates a metadata-criteria-based node group. The group automatically tracks nodes whose metadata matches the criteria.

**Parameters:**
- `criteria` (`dict`): Metadata key-value pairs to match. Use `"*"` to match any value, or `"~value"` to match values containing `value`.
- `on_node_added` (`callable`, optional): Function called as `on_node_added(node_dict)` when a node joins the group. Default: `None`.
- `on_node_removed` (`callable`, optional): Function called as `on_node_removed(node_dict)` when a node leaves the group. Default: `None`.

**Returns:** `NodeGroup`: a node group object.

```python
workers = cluster.create_node_group(
    criteria={"role": "worker"},
    on_node_added=lambda n: print(f"Worker joined: {n['id']}")
)
print(f"Workers: {workers.count()}")
workers.send_to_peers(128, {"task": "process"})
workers.close()
```

### `cluster.create_leader_election(check_interval="1s", leader_timeout="3s", heartbeat_msg_type=65, quorum_percentage=60, metadata_criteria=None)`

Creates a leader election manager with quorum-based election.

**Parameters:**
- `check_interval` (`str`, optional): Duration between leader checks. Default: `"1s"`.
- `leader_timeout` (`str`, optional): Duration without a heartbeat before the leader is considered lost. Default: `"3s"`.
- `heartbeat_msg_type` (`int`, optional): Message type for heartbeats, from the reserved (`< 128`) range. Default: `65`.
- `quorum_percentage` (`int`, optional): Percentage of nodes required for quorum, `1`-`100`. Default: `60`.
- `metadata_criteria` (`dict`, optional): Metadata criteria to limit eligible nodes. Default: `None` (all nodes eligible).

**Returns:** `LeaderElection`: a leader election object.

```python
election = cluster.create_leader_election(
    quorum_percentage=51,
    metadata_criteria={"role": "leader-eligible"}
)

election.on_event("became_leader", lambda e, n: print("I'm leader!"))
election.on_event("stepped_down", lambda e, n: print("Stepped down"))
election.start()
```

### `node_group.nodes()`

Gets all nodes currently in the group.

**Parameters:** None

**Returns:** `list`: list of node dicts.

### `node_group.contains(node_id)`

Checks if a node is in the group.

**Parameters:**
- `node_id` (`str`): Node UUID to check.

**Returns:** `bool`

### `node_group.count()`

Gets the number of nodes in the group.

**Parameters:** None

**Returns:** `int`

### `node_group.send_to_peers(message_type, data, reliable=False)`

Sends a message to all peers in the group.

**Parameters:**
- `message_type` (`int`): Message type. Must be `>= 128`.
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.
- `reliable` (`bool`, optional): Use reliable transport. Default: `False`.

**Returns:** `None`

### `node_group.close()`

Closes the group and releases resources.

**Parameters:** None

**Returns:** `None`

### `leader_election.start()`

Starts the election process.

**Parameters:** None

**Returns:** `None`

### `leader_election.stop()`

Stops the election process.

**Parameters:** None

**Returns:** `None`

### `leader_election.is_leader()`

Checks if this node is the current leader.

**Parameters:** None

**Returns:** `bool`

```python
if election.is_leader():
    print("Performing leader-only tasks")
```

### `leader_election.has_leader()`

Checks if a leader is currently elected.

**Parameters:** None

**Returns:** `bool`

### `leader_election.get_leader_id()`

Gets the current leader's node ID.

**Parameters:** None

**Returns:** `str`

### `leader_election.send_to_peers(message_type, data, reliable=False)`

Sends a message to all eligible peers (those matching `metadata_criteria`, if set).

**Parameters:**
- `message_type` (`int`): Message type. Must be `>= 128`.
- `data` (`str`, `int`, `float`, `list`, or `dict`): Message payload.
- `reliable` (`bool`, optional): Use reliable transport. Default: `False`.

**Returns:** `None`

### `leader_election.on_event(event_type, handler)`

Registers a handler for a leader election event.

**Parameters:**
- `event_type` (`str`): One of `"elected"`, `"lost"`, `"became_leader"`, `"stepped_down"`.
- `handler` (`callable`): Function called when the event fires.

**Returns:** `None`

```python
election.on_event("became_leader", lambda e, n: print("I became the leader!"))
election.on_event("stepped_down", lambda e, n: print("I stepped down"))
election.on_event("elected", lambda e, n: print(f"Leader elected: {n}"))
election.on_event("lost", lambda e, n: print("Leader lost"))
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.net.gossip` opens raw UDP/TCP sockets to bind, join, and exchange traffic with other cluster nodes, and can both send and receive arbitrary script-supplied payloads over the network. The library itself does not restrict which hosts or ports a script can bind to or contact: that is the embedder's responsibility, typically enforced with OS-level firewalling, network namespacing, or by controlling which addresses are reachable from the process. Use `encryption_key` and `bearer_token` to protect traffic and authenticate peers when running across untrusted networks. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

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

- Message types 0-127 are reserved for internal protocol use; user message types must be `>= 128` (use the `MSG_USER` constant).
- `reliable=True` uses TCP for guaranteed delivery.
- Metadata is eventually consistent across the cluster.
- Always call `stop()` to properly clean up resources.
- Node group criteria support the `"*"` wildcard and `"~value"` contains matching.
- Leader election heartbeat message types use the reserved (`< 128`) range.

## See Also

- [scriptling.net.unicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/unicast.md): direct point-to-point UDP/TCP messaging
- [scriptling.net.multicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/multicast.md): one-to-many UDP group messaging
- [scriptling.net.resolve](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/resolve.md): DNS and SRV record resolution
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md): full risk breakdown across all libraries
