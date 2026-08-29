---
title: scriptling.badgerdb
linkTitle: badgerdb
description: BadgerDB embedded key/value store with the valkey API on local storage.
tags: [libraries, databases, badger]
weight: 5
---

## Overview

`scriptling.badgerdb` embeds BadgerDB as a local key/value store, no server needed. The string-KV core is mirrored exactly by [scriptling.valkey](../valkey/), so those scripts move between local storage and a shared cache by changing the open line and nothing else: strings, hashes, batch operations, counters and TTLs. Valkey's sets, queues and database selection have no counterpart here; badgerdb implements what the store does natively.

```python
import scriptling.badgerdb as badger

client = badger.open("/var/data/state")
client.set("greeting", "hello", ttl_seconds=60)
print(client.get("greeting"))            # hello
print(client.ttl("greeting"))            # remaining seconds
client.incr("hits")
print(client.keys("gr*"))                # ["greeting"]
client.close()
```

Badger allows one process to hold a database open at a time (a second open fails on the lock file). The directory must fall inside the host's `--allowed-paths` when one is configured.

## Available Functions

| Function | Description |
|----------|-------------|
| `open(path)` | Open (creating if needed) a database directory and return a `Client` |

## Client

Identical surface to the [valkey Client](../valkey/#client):

| Method | Description |
|--------|-------------|
| `get(key)` | Value stored at key, or `None` when missing |
| `set(key, value, ttl_seconds=0)` | Store a string; `ttl_seconds` of 0 means no expiry |
| `set_if_absent(key, value, ttl_seconds=0)` | Store only when the key does not exist, returning whether it was stored |
| `mget(*keys)` | Values for the keys in one call, in order; `None` where a key is missing |
| `mset(mapping, ttl_seconds=0)` | Store every entry of a dict in one call |
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
| `keys(pattern)` | Keys matching a glob pattern (`*` and `?`) |
| `ping()` | Check the store is reachable, raising on failure |
| `close()` | Close the database and release its lock |

Transactions, iterators and value-log plumbing stay implementation details inside the plugin: scripts see flat operations. `incr` preserves a key's TTL, matching redis semantics.

## Hashes

Hashes are implemented the way a key/value store does them natively: a hash
occupies one key, so `keys()`, `exists`, `delete`, `expire`, `ttl` and
`persist` see the whole hash as one key with one expiry covering every field.
The expiry survives field writes and the key disappears with its last field,
the same semantics as on valkey:

```python
client.hash_set("session:1", "user", "ada")
client.hash_set("session:1", "role", "admin")
client.hash_get("session:1", "user")            # -> "ada"
client.hash_all("session:1")                    # -> {"user": "ada", "role": "admin"}
client.expire("session:1", 300)                 # expiry covers the whole hash
client.hash_size("session:1")                   # -> 2
```

## See Also

- [Valkey](../valkey/): the same string-KV core against a server, plus sets and queues
- [Database Libraries](./): all four backends, two API shapes
