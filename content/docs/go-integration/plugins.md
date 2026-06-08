---
title: Plugins
description: Enable executable plugins when embedding Scriptling in Go.
weight: 12
---

Applications that embed Scriptling can use the same executable plugin system as the CLI. Create one `plugin.Manager` for the application, load plugin directories during startup, and register plugin libraries with each Scriptling environment you create.

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

Each Scriptling environment belongs to one Go thread of execution and must not be evaluated concurrently. Create one environment per concurrent request or worker, then call `plugin.RegisterLibraries(env, manager)` for each environment.

The manager starts each plugin executable once. Multiple environments can share that manager, and plugin calls from those separate environments may overlap on the same plugin process.

## Startup and Failure Behavior

Plugins are loaded eagerly. Missing or invalid executables become manager warnings, which lets applications decide how visible those startup problems should be. A runtime RPC failure from a plugin call is returned as the script error for that call.

## More Detail

- [Plugin Manager](/docs/plugins/host-integration/) covers the same pattern from the plugin documentation section.
- [Go Plugins](/docs/plugins/go-plugins/) explains how to write a plugin executable in Go.
- [JSON-RPC Protocol](/docs/plugins/protocol/) documents the stdio protocol for non-Go plugins.
