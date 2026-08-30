---
description: Thread-safe key-value store for sharing state across requests and background tasks.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/kv/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/kv/
status: stable
tags:
    - libraries
    - runtime
title: scriptling.runtime.kv
type: API Reference
---
# scriptling.runtime.kv

## Overview

The `scriptling.runtime.kv` library exposes a **default** system store plus the ability to open additional named stores via `kv.open()`, for sharing state across HTTP handlers, JSON-RPC handlers, and background tasks. All stores share the same interface: a store object with methods for getting, setting, and managing keys.

## Available Functions

| Function | Description |
|----------|-------------|
| `open(name)` | Open or reuse a named KV store |

## Constants

| Constant | Description |
|----------|-------------|
| `kv.default` | The system-wide default KV store |

## Store Object Methods

| Method | Description |
|--------|-------------|
| `set(key, value, ttl=0)` | Store a value with optional TTL |
| `get(key, default=None)` | Retrieve a value by key |
| `incr(key, delta=1)` | Atomically increment an integer value, returns new value |
| `delete(key)` | Remove a key from the store |
| `exists(key)` | Check if a key exists |
| `ttl(key)` | Get remaining TTL for a key |
| `keys(pattern="*")` | Get keys matching a glob pattern |
| `clear()` | Remove all keys from the store |
| `close()` | Close the store immediately (no-op on `kv.default`) |

## Functions

### `open(name)`

Opens or reuses a named KV store. If a store with the given name is already open, the existing instance is returned; otherwise a new store is opened and registered.

**Parameters:**
- `name` (`str`): Store name. Use `":memory:name"` for an in-memory store shared by that name, or a filesystem path (e.g. `"/data/agent.db"`) for a persistent store. Empty string is not permitted.

**Returns:** Store object: with `set()`, `get()`, `incr()`, `delete()`, `exists()`, `ttl()`, `keys()`, `clear()`, and `close()` methods.

```python
import scriptling.runtime.kv as kv

# Open a named in-memory store: shared across all callers using the same name
scratch = kv.open(":memory:scratch")
scratch.set("temp", 42)
val = scratch.get("temp")
# No close() needed: store stays open for subsequent calls
```

```python
import scriptling.runtime.kv as kv

db = kv.open("/data/agent.db")
db.set("last_topic", "python async")
topic = db.get("last_topic", default="")
# Store remains open between interpreter invocations
```

## Store Methods

### `set(key, value, ttl=0)`

Stores a value with an optional TTL.

**Parameters:**
- `key` (`str`): Key to store under.
- `value` (any): Value to store (`str`, `int`, `float`, `bool`, `list`, or `dict`).
- `ttl` (`int`, optional): Time-to-live in seconds. `0` means no expiration. Default: `0`.

**Returns:** `None`

```python
import scriptling.runtime.kv as kv

kv.default.set("api_key", "secret123")
kv.default.set("session:abc", {"user": "bob"}, ttl=3600)
```

### `get(key, default=None)`

Retrieves a value by key.

**Parameters:**
- `key` (`str`): Key to retrieve.
- `default` (any, optional): Value to return if the key doesn't exist. Default: `None`.

**Returns:** any: the stored value (deep copy), or `default` if not found.

```python
import scriptling.runtime.kv as kv

api_key = kv.default.get("api_key")
session = kv.default.get("session:abc", default={})
```

### `incr(key, delta=1)`

Atomically increments an integer value stored at `key` by `delta`. The read and write happen under a single lock, so concurrent increments on the same key are safe and never lose updates. If the key does not exist, it is initialized to `0` before incrementing.

**Parameters:**
- `key` (`str`): Key to increment.
- `delta` (`int`, optional): Amount to add. Default: `1`.

**Returns:** `int`: the new value after increment.

```python
import scriptling.runtime.kv as kv

kv.default.set("hits", 0)
total = kv.default.incr("hits")        # 1
total = kv.default.incr("hits", delta=5)  # 6
```

### `delete(key)`

Removes a key from the store.

**Parameters:**
- `key` (`str`): Key to remove.

**Returns:** `None`

```python
import scriptling.runtime.kv as kv

kv.default.delete("session:abc")
```

### `exists(key)`

Checks if a key exists and is not expired.

**Parameters:**
- `key` (`str`): Key to check.

**Returns:** `bool`

```python
import scriptling.runtime.kv as kv

if kv.default.exists("session:abc"):
    print("Session exists")
```

### `ttl(key)`

Gets the remaining time-to-live for a key.

**Parameters:**
- `key` (`str`): Key to check.

**Returns:** `int`: seconds remaining, `-1` if no expiration, `-2` if the key doesn't exist.

```python
import scriptling.runtime.kv as kv

seconds_left = kv.default.ttl("session:abc")
```

### `keys(pattern="*")`

Gets all keys matching a glob pattern.

**Parameters:**
- `pattern` (`str`, optional): Glob pattern. Default: `"*"`.

**Returns:** `list`: matching keys.

```python
import scriptling.runtime.kv as kv

kv.default.set("user:1", {"name": "Alice"})
kv.default.set("user:2", {"name": "Bob"})

user_keys = kv.default.keys("user:*")  # ["user:1", "user:2"]
```

### `clear()`

Removes all keys from the store.

**Returns:** `None`

```python
import scriptling.runtime.kv as kv

kv.default.clear()
```

### `close()`

Closes the store immediately and removes it from the registry. The next call to `kv.open()` with the same name will reopen it. Calling `close()` on `kv.default` is a no-op.

**Returns:** `None`

```python
import scriptling.runtime.kv as kv

scratch = kv.open(":memory:scratch")
scratch.close()
```

## Examples

### Sharing state across requests

```python
import scriptling.runtime.kv as kv

# In HTTP handler
def handler(request):
    users = kv.default.get("users", default=[])
    users.append(request.json())
    kv.default.set("users", users)
    return runtime.http.json(200, {"count": len(users)})

# In background task
def worker():
    users = kv.default.get("users", default=[])
    print(f"Total users: {len(users)}")
```

### Shared named store across background tasks

```python
import scriptling.runtime.kv as kv
import scriptling.runtime as runtime

def task_a():
    store = kv.open(":memory:shared")
    store.set("result_a", "done")

def task_b():
    store = kv.open(":memory:shared")
    store.set("result_b", "done")

runtime.background("a", "task_a")
runtime.background("b", "task_b")
```

## Notes

- All operations are thread-safe.
- Values are deep-copied on retrieval.
- TTL expiration is automatic.
- Named stores persist in the registry until explicitly closed: `kv.open()` with the same name always returns the existing open store.
- In-memory stores use the `":memory:name"` prefix; persistent stores use a filesystem path.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.runtime.kv` has no network or filesystem access implications of its own (a persistent store's on-disk path is the only filesystem touchpoint, and that's an explicit, caller-chosen path). The practical risk is unbounded memory growth from named in-memory stores that are never cleared or closed: size keys and TTLs accordingly rather than treating this as an access-control concern.

## See Also

- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/./runtime.md): background tasks that often coordinate through `kv`
- [scriptling.runtime.sync](https://scriptling.dev/okf/scriptling-libraries/runtime/sync.md): concurrency primitives for coordinating tasks beyond simple key-value state
- [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md): HTTP handlers commonly read/write `kv.default`
