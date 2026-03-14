---
title: scriptling.runtime.kv
linkTitle: runtime.kv
weight: 1
---

Thread-safe key-value store for sharing state across requests and background tasks.

The `kv` sub-library exposes a **default** system store and the ability to open additional named stores via `kv.open()`. All stores share the same interface — a store object with methods for getting, setting, and managing keys.

## Store Object Methods

| Method                   | Description                        |
| ------------------------ | ---------------------------------- |
| `set(key, value, ttl=0)` | Store value with optional TTL      |
| `get(key, default=None)` | Retrieve value by key              |
| `delete(key)`            | Remove a key from the store        |
| `exists(key)`            | Check if key exists                |
| `ttl(key)`               | Get remaining TTL for a key        |
| `keys(pattern="*")`      | Get keys matching glob pattern     |
| `clear()`                | Remove all keys from store         |
| `close()`                | Release the store (no-op on default) |

## Library Functions

| Function      | Description                        |
| ------------- | ---------------------------------- |
| `open(name)`  | Open or reuse a named KV store     |

## Library Constants

| Constant  | Description                        |
| --------- | ---------------------------------- |
| `default` | The system-wide default KV store   |

## Setup

```go
import "github.com/paularlott/scriptling/extlibs"

// Register the KV sub-library (call after InitKVStore)
extlibs.RegisterRuntimeKVLibrary(p)

// Or register all runtime sub-libraries at once
extlibs.RegisterRuntimeLibraryAll(p, nil)
```

## Store Methods

### set(key, value, ttl=0)

Store a value with optional TTL.

**Parameters:**

- `key` (string): Key to store under
- `value`: Value to store (string, int, float, bool, list, dict)
- `ttl` (int, optional): Time-to-live in seconds (0 = no expiration)

### get(key, default=None)

Retrieve a value by key.

**Parameters:**

- `key` (string): Key to retrieve
- `default`: Value to return if key doesn't exist

**Returns:** Stored value (deep copy) or default

### delete(key)

Remove a key from the store.

### exists(key)

Check if a key exists and is not expired.

**Returns:** Boolean

### ttl(key)

Get remaining time-to-live for a key.

**Returns:** Seconds remaining, -1 if no expiration, -2 if key doesn't exist

### keys(pattern="*")

Get all keys matching a glob pattern.

**Parameters:**

- `pattern` (string, optional): Glob pattern (default: `"*"`)

**Returns:** List of matching keys

### clear()

Remove all keys from the store.

### close()

Release the store and decrement its reference count. When all references to a named store are closed, the underlying database is closed. Calling `close()` on `kv.default` is a no-op.

## Library Functions

### kv.open(name)

Open or reuse a named KV store. Stores are shared by name — multiple calls with the same name return separate wrapper objects backed by the same database.

**Parameters:**

- `name` (string): Store name.
  - Use `":memory:name"` for an in-memory store shared by that name.
  - Use a filesystem path (e.g. `"/data/agent.db"`) for a persistent store.
  - Empty string is not permitted.

**Returns:** Store object

## Examples

### Default Store

```python
import scriptling.runtime.kv as kv

# Store values in the system default store
kv.default.set("api_key", "secret123")
kv.default.set("session:abc", {"user": "bob"}, ttl=3600)

# Retrieve values
api_key = kv.default.get("api_key")
session = kv.default.get("session:abc", default={})

# Check existence
if kv.default.exists("session:abc"):
    print("Session exists")
```

### Named In-Memory Store

```python
import scriptling.runtime.kv as kv

# Open a named in-memory store — shared across all callers using the same name
scratch = kv.open(":memory:scratch")
scratch.set("temp", 42)
val = scratch.get("temp")
scratch.close()
```

### Persistent Store

```python
import scriptling.runtime.kv as kv

db = kv.open("/data/agent.db")
db.set("last_topic", "python async")
topic = db.get("last_topic", default="")
db.close()
```

### Pattern Matching

```python
import scriptling.runtime.kv as kv

kv.default.set("user:1", {"name": "Alice"})
kv.default.set("user:2", {"name": "Bob"})
kv.default.set("session:abc", {"user_id": 1})

# Get all user keys
user_keys = kv.default.keys("user:*")  # ["user:1", "user:2"]
```

### Sharing State Across Requests

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

### Shared Named Store Across Background Tasks

```python
import scriptling.runtime.kv as kv
import scriptling.runtime as runtime

def task_a():
    store = kv.open(":memory:shared")
    store.set("result_a", "done")
    store.close()

def task_b():
    store = kv.open(":memory:shared")
    store.set("result_b", "done")
    store.close()

runtime.background("a", "task_a")
runtime.background("b", "task_b")
```

## Notes

- All operations are thread-safe
- Values are deep-copied on retrieval
- TTL expiration is automatic
- Supports glob patterns for key matching
- `kv.default` is always available and its `close()` is a no-op
- Named stores are reference-counted — the database closes only when all wrappers are closed
- In-memory stores use the `":memory:name"` prefix; persistent stores use a filesystem path
