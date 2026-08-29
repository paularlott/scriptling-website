---
title: scriptling.valkey
linkTitle: valkey
description: Valkey and Redis key/value client with strings, counters, TTLs, sets, queues and key patterns.
tags: [libraries, databases, valkey, redis]
weight: 4
---

## Overview

`scriptling.valkey` connects to Valkey or Redis servers: one server, a cluster, or a master behind sentinels. The string-KV core is mirrored exactly by [scriptling.badgerdb](../badgerdb/), so those scripts move between a shared cache and local storage by changing the connect line and nothing else: strings, hashes, batch operations, counters and TTLs. Sets, queues, database selection, flushes and the cluster/sentinel modes are valkey-only: they use native redis features an embedded store has no counterpart for.

```python
import scriptling.valkey as valkey

client = valkey.connect("valkey://localhost:6379")
client.set("greeting", "hello", ttl_seconds=60)
print(client.get("greeting"))            # hello
print(client.ttl("greeting"))            # remaining seconds
client.incr("hits")
print(client.keys("gr*"))                # ["greeting"]
client.close()
```

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(url="valkey://localhost:6379", mode="single", master_set="mymaster")` | Connect to a server, cluster or sentinel and return a `Client` |

## Functions

### `connect(url="valkey://localhost:6379", mode="single", master_set="mymaster")`

Connects and returns a [`Client`](#client). Accepted schemes:

- `valkey://`, `redis://`, `tcp://`: plaintext
- `valkeys://`, `rediss://`: TLS
- optional `user:pass@` credentials and a `/db` number (`valkey://localhost:6379/1`)

A bare `host:port` also works, and the url takes one address or a comma-separated seed list (`valkey://node-a:7000,node-b:7000,node-c:7000`); credentials and the db are shared by every address. Every address, including the nodes a cluster's topology discovery returns, must pass the host's network policy.

`mode` picks the client shape:

| Mode | Behaviour |
|------|-----------|
| `single` (default) | talk straight to the one server named in the url |
| `cluster` | treat the addresses as cluster seeds and follow the topology |
| `sentinel` | treat the addresses as sentinels and follow the master named by `master_set` (default `mymaster`) |
| `auto` | ask the server: build a cluster client when it answers like one, a single connection otherwise |

`mode()` on the client reports what the connection is: `"standalone"`, `"cluster"` or `"sentinel"`.

## Client

| Method | Description |
|--------|-------------|
| `get(key)` | Value stored at key, or `None` when missing |
| `set(key, value, ttl_seconds=0)` | Store a string; `ttl_seconds` of 0 means no expiry |
| `set_if_absent(key, value, ttl_seconds=0)` | Store only when the key does not exist, returning whether it was stored; the take-once primitive behind locks |
| `mget(*keys)` | Values for the keys in one round trip, in order; `None` where a key is missing |
| `mset(mapping, ttl_seconds=0)` | Store every entry of a dict in one round trip |
| `delete(*keys)` | Delete keys, returning how many existed |
| `exists(*keys)` | Return how many of the keys exist |
| `expire(key, ttl_seconds)` | Set a key's time to live; `False` when the key is missing |
| `persist(key)` | Remove a key's expiry so it lives forever; `False` when missing |
| `ttl(key)` | Remaining seconds, `None` when missing, `-1` when the key has no expiry |
| `incr(key, amount=1)` | Add to the integer stored at key, returning the new value |
| `decr(key, amount=1)` | Subtract from the integer stored at key |
| `hash_set(key, field, value)` | Set one hash field, returning `1` when the field was new, `0` when it overwrote |
| `hash_get(key, field)` | The field's value, or `None` when the key or field is missing |
| `hash_delete(key, *fields)` | Delete fields, returning how many existed; the key disappears with its last field |
| `hash_all(key)` | Every field and value as a dict; empty when the key is missing |
| `hash_size(key)` | How many fields the hash holds |
| `select(index)` | Switch the database every later command addresses; each database is dialed once and its pool kept, so switching back is instant |
| `db()` | The database index this client currently addresses |
| `mode()` | How the client talks to the server: `"standalone"`, `"cluster"` or `"sentinel"` |
| `flushdb()` | Delete every key in the current database |
| `flushall()` | Delete every key in every database on the server |
| `keys(pattern)` | Keys matching a glob pattern (`*` and `?`) |
| `ping()` | Check the server is reachable, raising on failure |
| `close()` | Close the client and release its connections (all databases it touched) |
| `set_add(key, *members)` | Add members to a set; returns how many were new |
| `set_remove(key, *members)` | Remove members from a set; returns how many existed |
| `set_members(key)` | Every member of the set, unordered |
| `set_contains(key, member)` | Whether member is in the set |
| `set_size(key)` | Number of members in the set |
| `queue_push(key, *values)` | Push values onto the queue's tail; returns the queue length |
| `queue_pop(key)` | Pop the value at the queue's head, or `None` when empty |
| `queue_wait(key, timeout)` | Pop the head value, blocking server-side up to `timeout` seconds (fractional allowed; `0` behaves like `queue_pop`); `None` on timeout |
| `queue_peek(key)` | The value at the queue's head without removing it |
| `queue_size(key)` | Number of values in the queue |
| `queue_range(key, start=0, stop=-1)` | Values from the queue in order, head first, without removing them |

## Databases

A valkey server numbers its databases; the URL picks the starting one (`valkey://host:6379/1`), and `select` switches while running:

```python
client = valkey.connect("valkey://localhost:6379")
client.select(2)          # every later command addresses database 2
print(client.db())        # 2
```

Switching never dials twice: each database is connected once and its pool
kept, so `select(2)`, `select(0)`, `select(2)` costs two connections total
and the third switch is instant. Nothing closes on a switch, so commands
already running on another database finish undisturbed, and `close()`
releases every pool the client opened. (A protocol-level SELECT cannot be
used: the client multiplexes its connections and would not replay the
selection after a reconnect.)

## Hashes

Field-value pairs under one key. The expiry covers the whole hash, survives
field writes, and the key disappears with its last field:

```python
client.hash_set("session:1", "user", "ada")     # -> 1 (new field)
client.hash_set("session:1", "role", "admin")   # -> 1
client.hash_get("session:1", "user")            # -> "ada"
client.hash_all("session:1")                    # -> {"user": "ada", "role": "admin"}
client.hash_size("session:1")                   # -> 2
client.hash_delete("session:1", "role")         # -> 1 (how many existed)
```

Hashes are part of the mirrored core: [badgerdb](../badgerdb/) implements the
same five operations on its native storage.

## Sets

Unordered collections of unique strings:

```python
client.set_add("crew", "ada", "grace")     # -> 2 (how many were new)
client.set_contains("crew", "ada")         # -> True
client.set_size("crew")                    # -> 2
print(client.set_members("crew"))          # unordered
client.set_remove("crew", "ada")           # -> 1 (how many existed)
```

## Queues

FIFO queues backed by redis lists: producers push at the tail, consumers pop at the head:

```python
client.queue_push("jobs", "resize", "email")   # -> 2 (length)
client.queue_peek("jobs")                      # -> "resize", not removed
client.queue_pop("jobs")                       # -> "resize"
client.queue_wait("jobs", 5)                   # block up to 5s for the next value
client.queue_size("jobs")                      # -> 1
client.queue_range("jobs")                     # remaining values, head first
```

`queue_pop` returns `None` when the queue is empty. `queue_wait(key, timeout)` blocks server-side for up to the timeout (fractional seconds allowed; `0` behaves like `queue_pop`) and returns the head value or `None`, so a worker loop can wait instead of polling:

```python
while True:
    job = client.queue_wait("jobs", 5)
    if job is None:
        continue          # timeout, loop keeps the script responsive
    handle(job)
```

There is deliberately no infinite wait: a re-issued `queue_wait` keeps the script cancellable rather than pinned forever on one call.

## Clusters and Sentinels

`connect(url, mode=...)` picks the client shape; the default `single` talks to the one server in the url. For a cluster, list seed addresses and let the client follow the topology:

```python
client = valkey.connect("valkey://node-a:7000,node-b:7000,node-c:7000", mode="cluster")
print(client.mode())      # cluster
```

On a cluster the whole API works unchanged with one redis-rule exception: **multi-key methods** (`delete`, `exists`, `mget`, `mset`) accept keys that hash to the same slot only, because that is what the server itself enforces. Give the keys a shared hash tag when you need them together: `mset({"job:1{a}": "x", "job:2{a}": "y"})`.

`select()` has nothing to switch: a cluster has a single database (0), and a sentinel client tracks the master's database 0 (a select cannot be replayed across a failover), so both refuse it.

For a master behind sentinels, list the sentinel addresses and name the master set:

```python
client = valkey.connect("valkey://s1:26379,s2:26379,s3:26379", mode="sentinel",
                        master_set="mymaster")
```

Sentinels are usually reached on port 26379, so spell it out. `mode="auto"` asks the server instead of you: it builds a cluster client when the server answers like one and falls back to a single connection otherwise.

## Flushing

`flushdb()` deletes every key in the current database; `flushall()` deletes every key in every database. Both are destructive and immediate. On a cluster the command reaches every node that accepts writes (replicas need no flush; they mirror their master), so one call clears the whole cluster:

```python
client.select(1)
client.flushdb()          # database 1 only
client.flushall()         # every database, everywhere
```

## See Also

- [BadgerDB](../badgerdb/): the same string-KV core, embedded
- [Database Libraries](./): all four backends, two API shapes
