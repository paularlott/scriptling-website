---
title: Plugin Manager
description: Enable plugins in Go applications embedding Scriptling.
weight: 2
---

Applications that embed Scriptling own a plugin manager. Load plugins once, then register plugin libraries with every Scriptling environment you create.

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

    p := scriptling.New()
    plugin.RegisterLibraries(p, manager)

    _, err := p.Eval(`
import plugin.hello
print(plugin.hello.greet("Ada"))
`)
    if err != nil {
        log.Fatal(err)
    }
}
```

## Multiple Environments

The manager starts each plugin executable once. Multiple Scriptling environments can share the same manager. Each environment must still be evaluated by only one Go thread at a time. The stdio JSON-RPC connection multiplexes overlapping calls by request id; connection pooling is intentionally not used because it would create multiple plugin process instances and violate the singleton plugin model:

```go
p1 := scriptling.New()
plugin.RegisterLibraries(p1, manager)

p2 := scriptling.New()
plugin.RegisterLibraries(p2, manager)
```


## Plugin Logs

Pass a logger to `plugin.NewManager(appLogger, crashHandler)` to install the manager-lifetime host logger used for records emitted by Go plugins through `plugin.Logger(ctx)`. Pass the same logger your application already uses; the example above uses `github.com/paularlott/logger/slog` so plugin logs are visible during development. `manager.SetLogger()` is also available for late wiring. If no logger is configured, plugin log records are acknowledged and dropped.

## Crash Handling

Pass a crash handler to `plugin.NewManager(appLogger, crashHandler)` to handle plugin processes that exit unexpectedly after loading. `manager.SetCrashHandler()` is also available for late wiring. Long-running applications can log the failure, terminate, restart the process, or mark themselves unhealthy.

```go
manager.SetCrashHandler(func(name string, err error) {
    log.Println("plugin crashed:", name, err)
})
```

`manager.Health()` is still available for polling or health endpoints. It returns a map of unhealthy plugin library names to errors and is empty when all loaded plugins are healthy.

## Server Applications

For long-running servers, create the manager during application startup and close it during shutdown. Register plugin libraries in every request environment.

Scriptling's CLI server mode does this for `--plugin-dir` automatically.

## Loading JSON-RPC Peers on Demand

`Manager.LoadPath` spawns a single executable at runtime without scanning a
directory. `Manager.LoadURL` connects to an HTTP(S) JSON-RPC endpoint.
`Manager.Unload` closes one and removes it. These are safe to call while the
manager is also serving `--plugin-dir` plugins.

```go
// Plugin protocol peer (scriptling.handshake + function.call etc.)
client, err := manager.LoadPath(ctx, "widgets", "/opt/widgets/widget", true, nil)
if err != nil { log.Fatal(err) }
defer manager.Unload("widgets")

// Typed plugin call — ints stay ints, etc.
result, err := client.CallFunction(ctx, "build",
    []plugin.Value{{Type: "string", Value: "chair"}}, nil)

// Pass command-line arguments, e.g. loading scriptling itself in raw JSON-RPC mode.
client, err = manager.LoadPath(ctx, "rpc", "scriptling", false,
    []string{"--json-rpc", "./setup.py"})
if err != nil { log.Fatal(err) }
defer manager.Unload("rpc")

// HTTP JSON-RPC endpoint. The last argument skips TLS verification for
// local/self-signed HTTPS servers.
client, err = manager.LoadURL(ctx, "remote", "https://127.0.0.1:8443/json-rpc", false, true)
if err != nil { log.Fatal(err) }
defer manager.Unload("remote")
```

HTTP plugin transport is request/response only. It supports calls, objects, and
batches, but the server cannot initiate callbacks back to the client. Use stdio
plugins when host callbacks or `plugin.Logger(ctx)` are required.

`LoadPath` is idempotent on absolute path + name; `LoadURL` is idempotent on
URL + name. A second call with the same peer and name returns the existing
client. Loading an already-loaded peer under a different name, or loading a new
peer under a name already in use, returns an error.

The CLI always constructs a manager (even without `--plugin-dir`) so that
`scriptling.plugin.load` / `unload` / `call` are available to scripts in run,
server, and `--json-rpc` modes. Embedded applications get the same behaviour
as long as they construct a manager and call `plugin.RegisterLibraries` on
each environment.
