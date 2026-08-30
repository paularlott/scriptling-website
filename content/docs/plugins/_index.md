---
title: Plugins
description: Extend Scriptling with executable plugins over JSON-RPC.
tags: [plugins]
weight: 8
---

Plugins are standalone executables that Scriptling loads eagerly at startup.
They communicate over line-delimited JSON-RPC on stdio and expose libraries
under the host-owned `plugin.` namespace. Runtime-loaded peers can also be
connected over HTTP(S) with `scriptling.plugin.load(..., scriptling=True)` when
they expose the Scriptling plugin protocol at a JSON-RPC endpoint.

HTTP plugin transport is request/response only. It supports handshakes,
function calls, object lifecycle, generated `plugin.*` proxies, and batches,
but the server cannot initiate callbacks back to the client. That limit is
not negotiated at load: a plugin registering callback-bearing functions loads
without warning and the call fails at call time (the host may not even be
able to reach the network the plugin server sits on, so refusing at load
would be guessing). Host callbacks and `plugin.Logger(ctx)` require the
bidirectional stdio transport.

A plugin declares a name. A bare name such as `hello` registers in the plugin namespace: scripts import `plugin.hello`. A name containing a dot is the author's namespace and is used verbatim: `myplugin.hello` imports as `myplugin.hello`, and the first-party database plugins declare `scriptling.sqlite` and friends so their imports match compiled-in builds. Verbatim names that collide with a library the host already has are refused with a warning at load, so a plugin can never shadow a built-in.

## First-Party Plugins

The database plugins ship with Scriptling in every release form: compiled into `scriptling-full`, selectable individually with build tags, or as external plugin binaries from the release page (one `plugins-<os>-<arch>.zip` per platform, containing all four binaries named plainly; unzip it and point `--plugin-dir` at the folder). See the [database libraries reference](../../reference/libraries/databases/) for the full APIs.

| Plugin | Import | Description |
|--------|--------|-------------|
| SQLite | `scriptling.sqlite` | Embedded relational database (pure Go, no server) |
| SQL | `scriptling.sql` | MySQL, MariaDB and PostgreSQL client with one API and `?` placeholders everywhere |
| Valkey | `scriptling.valkey` | Valkey and Redis key/value client (strings, counters, TTLs, patterns) |
| BadgerDB | `scriptling.badgerdb` | Embedded key/value store mirroring the valkey API |

All four enforce the host security policy (allowed paths for the file-backed pair, the network policy for the network pair), and the [examples directory](https://github.com/paularlott/scriptling/tree/main/examples/databases) has runnable scripts with container commands for local test servers.

## Start Here

- [Using Plugins](using/) - Load plugin directories and call plugin libraries.
- [Plugin Manager](host-integration/) - Enable plugins in applications embedding Scriptling.
- [Go Plugins](go-plugins/) - Register functions, classes, and constants in a Go plugin.
  - [Client Wrappers](go-plugins/client-wrappers/) - Auto-generated proxies and custom Scriptling wrappers.
  - [Host-Side Scripting](go-plugins/host-side-scripting/) - Pure Scriptling functions and classes on the host.
- [C Plugins](c-plugins/) - Build plugins in C using the single-header SDK.
- [Bash Plugins](bash/) - Implement the JSON-RPC protocol directly.
- [PHP Plugins](php-plugins/) - Serve the protocol from plain PHP over HTTP.
- [JSON-RPC Protocol](protocol/) - Wire format reference for all methods and value encoding.

## Scriptling Scripts as Plugins

A Scriptling script can itself act as a plugin server using `runtime.plugin`,
no compiled binary required. See [Plugin Server Mode](../cli/plugin-server/) in
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
