---
description: Enable executable plugins when embedding Scriptling in Go.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/plugins/
sources:
    - resource: https://scriptling.dev/docs/go-integration/plugins/
status: stable
tags:
    - go-integration
    - embedding
    - go
    - plugins
title: Plugins
type: Guide
---
# Plugins

Applications that embed Scriptling can use the same executable plugin system as the CLI. Create one `plugin.Manager` for the application, load plugin directories during startup, and register plugin libraries with each Scriptling environment you create.

```go
package main

import (
    "context"
    "log"

    logslog "github.com/paularlott/logger/slog"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    ctx := context.Background()

    appLogger := logslog.New(logslog.Config{
        Level:  "info",
        Format: "console",
    })

    manager := plugin.NewManager(appLogger, func(name string, err error) {
        log.Println("plugin crashed:", name, err)
        // Decide whether to terminate, restart, or mark this host unhealthy.
    })
    manager.AddDir("./plugins")
    if err := manager.Load(ctx); err != nil {
        log.Fatal(err)
    }
    defer manager.Close()

    for _, warning := range manager.Warnings() {
        log.Println("plugin warning:", warning)
    }

    env := scriptling.New()
    plugin.RegisterLibraries(env, manager)

    _, err := env.Eval(`
import plugin.hello
print(plugin.hello.greet("Ada"))
`)
    if err != nil {
        log.Fatal(err)
    }
}
```

## Environment Model

Each Scriptling environment is safe to evaluate from many goroutines: a per-environment interpreter lock (GIL) serializes script execution, so concurrent calls into one environment cannot corrupt its state. You can therefore share a single environment across goroutines for shared state, or create one environment per request/worker for isolation (independent environments also run fully in parallel, since each has its own lock). In either case, call `plugin.RegisterLibraries(env, manager)` per environment.

The manager starts each plugin executable once, or keeps one logical client per loaded HTTP(S) JSON-RPC endpoint. Multiple environments can share that manager, and plugin calls from those separate environments may overlap on the same plugin process or endpoint. The stdio JSON-RPC connection multiplexes overlapping calls by request id; HTTP endpoints receive one POST per call or batch. HTTP plugin transport is request/response only, so the server cannot initiate callbacks back to the client; use stdio plugins for host callbacks and `plugin.Logger(ctx)`. Connection pooling for executable plugins is intentionally not used because it would create multiple plugin process instances and violate the singleton plugin model.

## Manager Scoping

When each request needs its own isolated plugin namespace: for example a multi-tenant server where a script can load private endpoints at runtime: use `manager.NewScope()`. A scope is a lightweight child manager that shares the parent's pooled HTTP transports but keeps an independent plugin registry. Closing the scope unloads only its own plugins without touching the parent.

```go
// Server startup: one long-lived manager.
manager := plugin.NewManager(appLogger)
defer manager.Close()

// Per-request handler: isolated scope, closed when the request exits.
// HTTP/HTTPS only: scripts cannot load local executables.
scope := manager.NewScope(plugin.WithTransport(plugin.TransportHTTP))
defer scope.Close()

env := scriptling.New()
plugin.RegisterLibraries(env, scope)

// Scripts may call scriptling.plugin.load("name", "https://...") to register
// additional plugins that live only for this request's lifetime.
result, err := env.EvalWithContext(ctx, script)
```

Key properties:

- `scope.Get` and `scope.List` chain to the parent. A child scope may only add plugin names that do not already exist anywhere in the ancestor chain: loading a name the parent owns returns an error. Loading the exact same endpoint under the same name is idempotent and returns the ancestor's client.
- `scope.Unload(name)` only removes scope-local plugins. Attempting to unload a parent plugin from a scope returns an error.
- All scopes derived from the same root manager share the same pooled `*http.Transport` instances (TLS-verified and TLS-skip-verify). Connections established in one request are reused in subsequent requests even though each request uses its own scope.
- Scopes can be nested. `NewScope` on a scope creates a grandchild; lookup and transport inheritance propagate correctly through the full chain.

See [Plugin Manager](../plugins/host-integration.md) for the full scoping reference including `WithTransport` and nested scopes.


## Plugin Logs

Pass a logger to `plugin.NewManager(appLogger, crashHandler)` to install the manager-lifetime host logger used for records emitted by Go plugins through `plugin.Logger(ctx)`. Pass the same `github.com/paularlott/logger.Logger` your application already uses; the example above uses `github.com/paularlott/logger/slog` so plugin logs are visible during development. `manager.SetLogger()` is also available for late wiring. If no logger is configured, plugin log records are acknowledged and dropped.

A Go plugin writes to the host logger from an active plugin call:

```go
plugin.Logger(ctx).Info("plugin work started", "name", name)
```

## Crash Handling

Pass a crash handler to `plugin.NewManager(appLogger, crashHandler)` to handle plugin processes that exit unexpectedly after loading. `manager.SetCrashHandler()` is also available for late wiring. This is the normal long-running server hook for logging, terminating, restarting, or marking the host unhealthy.

```go
manager.SetCrashHandler(func(name string, err error) {
    log.Println("plugin crashed:", name, err)
})
```

`manager.Health()` reports plugin processes that have exited or whose stdio transport has closed. The returned map is empty when all loaded plugins are healthy.

## Startup and Failure Behavior

Plugins are loaded eagerly. Missing or invalid executables become manager warnings, which lets applications decide how visible those startup problems should be. A runtime RPC failure from a plugin call is returned as the script error for that call.

## More Detail

- [Plugin Manager](../plugins/host-integration.md) covers the same pattern from the plugin documentation section.
- [Go Plugins](../plugins/go-plugins.md) explains how to write a plugin executable in Go.
- [JSON-RPC Protocol](../plugins/protocol.md) documents the stdio protocol for non-Go plugins.
