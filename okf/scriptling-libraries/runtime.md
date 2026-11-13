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

## Registration

The runtime libraries are registered one at a time. `scriptling.runtime.kv` (package `extlibs/runtime/kv`) and `scriptling.runtime.http` (package `extlibs/runtime/http`) have packages of their own; the rest are in `extlibs/runtime`. Each sub-library registered on the same interpreter is also an attribute of `scriptling.runtime`, so `import scriptling.runtime as rt; rt.kv` works when `scriptling.runtime.kv` is registered. The CLI registers all of them; disable one with `--disable-lib scriptling.runtime.kv` (and so on), or the parent and all of its sub-libraries except `scriptling.runtime.plugin` (disabled by its own name) with `--disable-lib scriptling.runtime`. See [Runtime Libraries](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries).

## See Also

- [scriptling.runtime.kv](https://scriptling.dev/okf/scriptling-libraries/runtime/kv.md) - Thread-safe key-value store
- [scriptling.runtime.sandbox](https://scriptling.dev/okf/scriptling-libraries/runtime/sandbox.md) - Isolated script execution environments
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for runtime libraries
