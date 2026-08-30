---
title: scriptling.runtime.sync
linkTitle: runtime.sync
description: Named cross-environment concurrency primitives, atomics, shared variables, wait groups, and queues.
tags: [libraries, runtime]
weight: 1

aliases:
  - /reference/libraries/scriptling/runtime/sync/
---

## Overview

The `scriptling.runtime.sync` library provides named concurrency primitives shared across all environments (HTTP handlers, JSON-RPC handlers, background tasks). Use it to coordinate isolated environments that don't otherwise share in-memory state.

## Available Functions

| Function | Description |
|----------|-------------|
| `Atomic(name, initial=0)` | Get/create a named atomic counter |
| `Shared(name, initial)` | Get/create a named shared variable |
| `WaitGroup(name)` | Get/create a named wait group |
| `Queue(name, maxsize=0)` | Get/create a named thread-safe queue |

## Functions

### `Atomic(name, initial=0)`

Gets or creates a named atomic counter.

**Parameters:**
- `name` (`str`): Unique name for the counter.
- `initial` (`int`, optional): Initial value, only used if creating new. Default: `0`.

**Returns:** Atomic object: with `add(delta=1)`, `get()`, and `set(value)` methods, all lock-free and atomic.

```python
import scriptling.runtime as runtime

counter = runtime.sync.Atomic("requests", 0)
counter.add(1)      # Atomic increment
counter.add(-5)     # Atomic add
counter.set(100)    # Atomic set
value = counter.get()  # Atomic read
```

### `Shared(name, initial)`

Gets or creates a named shared variable.

**Parameters:**
- `name` (`str`): Unique name for the variable.
- `initial` (any): Initial value, only used if creating new.

**Returns:** Shared object: with `get()`, `set(value)`, and `update(fn)` methods, all thread-safe.

```python
import scriptling.runtime as runtime

shared = runtime.sync.Shared("config", {"debug": True})

# Read
config = shared.get()

# Write
config["debug"] = False
shared.set(config)

# Atomic read-modify-write: fn receives the current value and returns the new one
shared.update(lambda c: {**c, "reloads": c.get("reloads", 0) + 1})
```

#### `Shared.update(fn)`

Atomically updates the value: `fn` receives the current value and returns the new one. The read and write happen under the shared variable's lock, so the update is safe against concurrent callers.

**Parameters:**
- `fn` (`function`): Receives the current value and returns the new value.

**Returns:** the new value.

### `WaitGroup(name)`

Gets or creates a named wait group, following Go's `sync.WaitGroup` semantics.

**Parameters:**
- `name` (`str`): Unique name for the wait group.

**Returns:** WaitGroup object: with `add(delta=1)`, `done()`, and `wait()` methods.

```python
import scriptling.runtime as runtime

wg = runtime.sync.WaitGroup("tasks")

def worker(id):
    print(f"Worker {id}")
    wg.done()

for i in range(10):
    wg.add(1)
    runtime.background(worker, i)

wg.wait()  # Wait for all workers
```

### `Queue(name, maxsize=0)`

Gets or creates a named thread-safe queue.

**Parameters:**
- `name` (`str`): Unique name for the queue.
- `maxsize` (`int`, optional): Maximum queue size. `0` means unbounded. Default: `0`.

**Returns:** Queue object: with `put(item)`, `get()`, `size()`, and `close()` methods.

```python
import scriptling.runtime as runtime

queue = runtime.sync.Queue("jobs", maxsize=100)

# Producer
def producer():
    for i in range(10):
        queue.put(i)

# Consumer
def consumer():
    while True:
        item = queue.get()
        if item is None:
            break
        process(item)

runtime.background(producer)
runtime.background(consumer)
```

## Examples

### Cross-environment coordination

```python
import scriptling.runtime as runtime

# In HTTP handler
def handler(request):
    queue = runtime.sync.Queue("jobs")
    queue.put({"task": "process", "data": request.json()})
    return runtime.http.json(200, {"status": "queued"})

# In background task
def worker():
    queue = runtime.sync.Queue("jobs")
    while True:
        job = queue.get()
        process_job(job)
```

## Notes

- All primitives are named and shared across environments: look them up by name from any handler or task rather than relying on closures.
- Names must be unique within each primitive type.
- Atomic operations are lock-free.
- Queue supports bounded and unbounded modes.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.runtime.sync` has no network or filesystem access: it's purely in-process concurrency primitives (locks, counters, queues). The risk here is misuse rather than access control: deadlocks from an unmatched `WaitGroup.add()`/`done()`, or a goroutine blocked forever on a full/empty `Queue`. Design coordination carefully rather than treating this as a security boundary.

## See Also

- [scriptling.runtime](../../runtime/): `background()` tasks that typically use these primitives to coordinate
- [scriptling.runtime.kv](../kv/): simpler key-value sharing for cases that don't need locks or queues
- [scriptling.runtime.sandbox](../sandbox/): isolated environments that do *not* share state, unlike `sync` primitives
