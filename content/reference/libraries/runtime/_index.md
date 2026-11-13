---
title: Runtime
description: Runtime utilities for background tasks, HTTP servers, key-value storage, concurrency, and plugin server support.
tags: [libraries, runtime]
weight: 16

aliases:
  - /reference/libraries/scriptling/runtime/
---

Libraries for runtime functionality including background task execution, HTTP server integration, key-value storage, concurrency primitives, and exposing a script as a first-class plugin server.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.runtime](runtime/) | Background tasks and async execution |
| [scriptling.runtime.http](http/) | HTTP route registration and response helpers |
| [scriptling.runtime.jsonrpc](jsonrpc/) | Concurrent JSON-RPC 2.0 server over stdio or HTTP |
| [scriptling.runtime.kv](kv/) | Thread-safe key-value store |
| [scriptling.runtime.plugin](plugin/) | Expose a script as a first-class plugin server |
| [scriptling.runtime.sync](sync/) | Named cross-environment concurrency primitives |
| [scriptling.runtime.sandbox](sandbox/) | Isolated script execution environments |
| [scriptling.runtime.mcp](mcp/) | Register MCP tools via decorators |

## Quick Start

```python
import scriptling.runtime as runtime
import scriptling.runtime.kv as kv

# Background task (handler is passed by name)
def my_task():
    print("Running in background")

runtime.background("my_task", "my_task")

# Key-value storage
store = kv.open("./mydata.db")
store.set("key", "value")
print(store.get("key"))
```

## Registration

The runtime libraries are registered one at a time. `scriptling.runtime.kv` (package `extlibs/runtime/kv`) and `scriptling.runtime.http` (package `extlibs/runtime/http`) have packages of their own; the rest are in `extlibs/runtime`. Each sub-library registered on the same interpreter is also an attribute of `scriptling.runtime`, so `import scriptling.runtime as rt; rt.kv` works when `scriptling.runtime.kv` is registered. The CLI registers all of them; disable one with `--disable-lib scriptling.runtime.kv` (and so on), or the parent and all of its sub-libraries except `scriptling.runtime.plugin` (disabled by its own name) with `--disable-lib scriptling.runtime`. See [Runtime Libraries](/docs/go-integration/library-registration/#runtime-libraries).

## See Also

- [scriptling.runtime.kv](kv/) - Thread-safe key-value store
- [scriptling.runtime.sandbox](sandbox/) - Isolated script execution environments
- [Libraries](../) - Full library reference index
- [Security Guide](/docs/security/) - Security guidance for runtime libraries
