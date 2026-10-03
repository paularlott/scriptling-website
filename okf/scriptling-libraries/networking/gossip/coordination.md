---
description: Metadata-criteria node groups and quorum-based leader election on a scriptling.net.gossip cluster.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/networking/gossip/coordination/
sources:
    - resource: https://scriptling.dev/reference/libraries/networking/gossip/coordination/
status: stable
tags:
    - libraries
    - networking
title: Node Groups & Leader Election
type: API Reference
---
# Node Groups & Leader Election

Part of [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md). A cluster created with `gossip.create()` can track subsets of nodes by metadata (node groups) and elect a single leader by quorum. Callbacks registered here follow the same [handler concurrency](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md#handler-concurrency) rules as the rest of the library.

## Objects

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

## Examples

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

## Notes

- Node group criteria support the `"*"` wildcard and `"~value"` contains matching.
- Leader election heartbeat message types use the reserved (`< 128`) range.

## See Also

- [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md): cluster creation, messaging, membership, and metadata.
