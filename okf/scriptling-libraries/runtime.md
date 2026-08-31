---
description: Runtime utilities for background tasks, HTTP servers, key-value storage, concurrency, and plugin server support.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/
status: stable
tags:
    - libraries
    - runtime
title: Runtime
type: API Reference
---
# Runtime

Libraries for runtime functionality including background task execution, HTTP server integration, key-value storage, concurrency primitives, and exposing a script as a first-class plugin server.

## Available Libraries

| Library | Description |
|---------|-------------|
| [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/runtime/runtime.md) | Background tasks and async execution |
| [scriptling.runtime.http](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md) | HTTP route registration and response helpers |
| [scriptling.runtime.jsonrpc](https://scriptling.dev/okf/scriptling-libraries/runtime/jsonrpc.md) | Concurrent JSON-RPC 2.0 server over stdio or HTTP |
| [scriptling.runtime.kv](https://scriptling.dev/okf/scriptling-libraries/runtime/kv.md) | Thread-safe key-value store |
| [scriptling.runtime.plugin](https://scriptling.dev/okf/scriptling-libraries/runtime/plugin.md) | Expose a script as a first-class plugin server |
| [scriptling.runtime.sync](https://scriptling.dev/okf/scriptling-libraries/runtime/sync.md) | Named cross-environment concurrency primitives |
| [scriptling.runtime.sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md) | Isolated script execution environments |
| [scriptling.runtime.mcp](https://scriptling.dev/okf/scriptling-libraries/runtime/mcp.md) | Register MCP tools via decorators |

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

## See Also

- [scriptling.runtime.kv](https://scriptling.dev/okf/scriptling-libraries/runtime/kv.md) - Thread-safe key-value store
- [scriptling.runtime.sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md) - Isolated script execution environments
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for runtime libraries
