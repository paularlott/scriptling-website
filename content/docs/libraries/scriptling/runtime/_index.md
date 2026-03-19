---
title: Runtime
description: Runtime utilities for background tasks, HTTP servers, key-value storage, and concurrency.
weight: 2
---

Libraries for runtime functionality including background task execution, HTTP server integration, key-value storage, and concurrency primitives.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.runtime](runtime/) | Background tasks and async execution |
| [scriptling.runtime.http](http/) | HTTP route registration and response helpers |
| [scriptling.runtime.kv](kv/) | Thread-safe key-value store |
| [scriptling.runtime.sync](sync/) | Named cross-environment concurrency primitives |
| [scriptling.runtime.sandbox](sandbox/) | Isolated script execution environments |

## Quick Start

```python
import scriptling.runtime as runtime
import scriptling.runtime.kv as kv

# Background task
def my_task():
    print("Running in background")

runtime.spawn(my_task)

# Key-value storage
store = kv.open("./mydata.db")
store.set("key", "value")
print(store.get("key"))
```
