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

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    ctx := context.Background()

    manager := plugin.NewManager()
    manager.SetCrashHandler(func(name string, err error) {
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

## Crash Handling

`manager.SetCrashHandler()` installs a callback for plugin processes that exit unexpectedly after loading. Long-running applications can log the failure, terminate, restart the process, or mark themselves unhealthy.

```go
manager.SetCrashHandler(func(name string, err error) {
    log.Println("plugin crashed:", name, err)
})
```

`manager.Health()` is still available for polling or health endpoints. It returns a map of unhealthy plugin library names to errors and is empty when all loaded plugins are healthy.

## Server Applications

For long-running servers, create the manager during application startup and close it during shutdown. Register plugin libraries in every request environment.

Scriptling's CLI server mode does this for `--plugin-dir` automatically.
