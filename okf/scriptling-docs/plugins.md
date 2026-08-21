---
description: Extend Scriptling with executable plugins over JSON-RPC.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/plugins/
sources:
    - resource: https://scriptling.dev/docs/plugins/
status: stable
tags:
    - plugins
title: Plugins
type: Guide
---
# Plugins

Plugins are standalone executables that Scriptling loads eagerly at startup.
They communicate over line-delimited JSON-RPC on stdio and expose libraries
under the host-owned `plugin.` namespace. Runtime-loaded peers can also be
connected over HTTP(S) with `scriptling.plugin.load(..., scriptling=True)` when
they expose the Scriptling plugin protocol at a JSON-RPC endpoint.

HTTP plugin transport is request/response only. It supports handshakes,
function calls, object lifecycle, generated `plugin.*` proxies, and batches,
but the server cannot initiate callbacks back to the client. Host callbacks and
`plugin.Logger(ctx)` require the bidirectional stdio transport.

A plugin declares a short name such as `hello`. Scriptling imports it as `plugin.hello`.

## Start Here

- [Using Plugins](plugins/using.md) - Load plugin directories and call plugin libraries.
- [Plugin Manager](plugins/host-integration.md) - Enable plugins in applications embedding Scriptling.
- [Go Plugins](plugins/go-plugins.md) - Register functions, classes, and constants in a Go plugin.
  - [Client Wrappers](plugins/go-plugins/client-wrappers.md) - Auto-generated proxies and custom Scriptling wrappers.
  - [Host-Side Scripting](plugins/go-plugins/host-side-scripting.md) - Pure Scriptling functions and classes on the host.
- [C Plugins](plugins/c-plugins.md) - Build plugins in C using the single-header SDK.
- [Bash Plugins](plugins/bash.md) - Implement the JSON-RPC protocol directly.
- [JSON-RPC Protocol](plugins/protocol.md) - Wire format reference for all methods and value encoding.

## Scriptling Scripts as Plugins

A Scriptling script can itself act as a plugin server using `runtime.plugin`,
no compiled binary required. See [Plugin Server Mode](cli/plugin-server.md) in
the CLI reference.

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

The default plugin transport is JSON-RPC over stdio. Go plugins can also expose
the same protocol over HTTP with `plugin.Server.ServeHTTP`; HTTP plugin
transport supports handshakes, function calls, object lifecycle, and batches.
Host callbacks and `plugin.Logger(ctx)` require the bidirectional stdio
transport.
