---
title: Plugins
description: Extend Scriptling with executable plugins over JSON-RPC.
weight: 8
---

Plugins are standalone executables that Scriptling loads eagerly at startup. They communicate over line-delimited JSON-RPC on stdio and expose libraries under the host-owned `plugin.` namespace.

A plugin declares a short name such as `hello`. Scriptling imports it as `plugin.hello`.

## Start Here

- [Using Plugins](using/) - Load plugin directories and call plugin libraries.
- [Plugin Manager](host-integration/) - Enable plugins in applications embedding Scriptling.
- [Go Plugins](go-plugins/) - Register functions, classes, and constants in a Go plugin.
  - [Client Wrappers](go-plugins/client-wrappers/) - Auto-generated proxies and custom Scriptling wrappers.
  - [Host-Side Scripting](go-plugins/host-side-scripting/) - Pure Scriptling functions and classes on the host.
- [C Plugins](c-plugins/) - Build plugins in C using the single-header SDK.
- [Bash Plugins](bash/) - Implement the JSON-RPC protocol directly.
- [JSON-RPC Protocol](protocol/) - Wire format reference for all methods and value encoding.

## Naming Model

Plugins live under `plugin.<name>` in Scriptling code, but the executable declares only `<name>` in the handshake or Go server constructor:

```go
server := plugin.NewServer("hello", "1.0.0", "Hello plugin")
```

```python
import plugin.hello
print(plugin.hello.greet("Ada"))
```

The `plugin.` prefix is host-owned. A plugin should declare a short name such as `hello`; if an executable declares `plugin.hello`, the host normalizes it to the same library name, `plugin.hello`. If two executables normalize to the same library name, only the first one is loaded and the duplicate is reported as a manager warning.

`scriptling.plugin` is different: it is the built-in control library used for listing plugins, inspecting metadata, direct function calls, and explicit release of remote objects.

## Transports

The transport is JSON-RPC over stdio.
