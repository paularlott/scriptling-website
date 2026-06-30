---
title: Writing a Go Plugin
description: Build an executable plugin that exposes functions and classes under plugin.*.
weight: 25
---

This tutorial builds a Go executable plugin and loads it with `--plugin-dir`.

## Create the Plugin

Create `hello-plugin/main.go`:

```go
package main

import (
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

type configData struct {
    name string
}

func main() {
    server := plugin.NewServer("hello", "1.0.0", "Hello plugin")

    fb := object.NewFunctionBuilder()
    fb.Function(func(name string) string {
        return "Hello, " + name
    })
    server.RegisterFunc("greet", fb)

    cb := object.NewClassBuilder("Config").
        Constructor(func(name string) *configData {
            return &configData{name: name}
        }).
        Method("get", func(self *configData) string {
            return self.name
        }).
        Method("set", func(self *configData, name string) {
            self.name = name
        })
    server.RegisterClass(cb)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

The plugin declares the short name `hello`. Scriptling owns the `plugin.` namespace and imports it as `plugin.hello`.

## Build It

```bash
mkdir -p ./plugins
go build -o ./plugins/hello ./hello-plugin
```

Every executable directly inside `./plugins` is attempted as a plugin.

## Use It

```bash
scriptling --plugin-dir ./plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

Output:

```text
Hello, Ada
```

Classes are proxied too:

```python
import plugin.hello

cfg = plugin.hello.Config("Ada")
print(cfg.get())
cfg.set("Bob")
print(cfg.get())
```

Use `scriptling.plugin.release(cfg)` for deterministic cleanup. A GC finalizer is installed as a fallback, but finalizers are not prompt.

## Class Styles

The example above uses a **typed receiver**: the constructor returns a Go struct pointer and methods receive it directly. You can also use `*object.Instance` for manual field management:

### Typed Receiver (recommended)

```go
type counter struct {
    value int64
}

cb := object.NewClassBuilder("Counter").
    Constructor(func(start int) *counter {
        return &counter{value: int64(start)}
    }).
    Method("inc", func(self *counter, n int) int {
        self.value += int64(n)
        return int(self.value)
    }).
    Method("get", func(self *counter) int {
        return int(self.value)
    })
```

The constructor returns a pointer type. All methods whose first parameter matches that type receive the unwrapped struct directly: no manual field boxing.

### Instance Fields

```go
cb := object.NewClassBuilder("Counter").
    Method("__init__", func(self *object.Instance, start int) {
        self.SetField("value", object.NewInteger(int64(start)))
    }).
    Method("inc", func(self *object.Instance, n int) int {
        current := self.Field("value").(*object.Integer).IntValue()
        next := current + int64(n)
        self.SetField("value", object.NewInteger(next))
        return int(next)
    }).
    Method("get", func(self *object.Instance) int {
        return int(self.Field("value").(*object.Integer).IntValue())
    })
```

Methods receive the raw `*object.Instance` and manage fields manually. Use this for simple cases or when you need direct control over instance state.

## Custom Wrappers

A plugin can supply Scriptling source that replaces the auto-generated proxy for a registered function or class. The wrapper name must match the registered name:

```go
fb := object.NewFunctionBuilder()
fb.Function(func(name string) string {
    return "Hello, " + name
})
server.RegisterFunc("greet", fb)

server.Wrapper("greet", `
import scriptling.plugin

def greet(name):
    return scriptling.plugin.call_function("plugin.hello", "greet", name) + "!"
`)
```

The host uses the supplied source instead of the auto-generated proxy. See [Client Wrappers](/docs/plugins/go-plugins/client-wrappers/) for details.

## Pure Host-Side Code

A plugin can also register Scriptling code that runs entirely on the host with no RPC:

```go
server.RegisterScriptFunc("slug", `
def slug(text):
    return text.lower().replace(" ", "-")
`)
```

See [Host-Side Scripting](/docs/plugins/go-plugins/host-side-scripting/) for `RegisterScriptFunc` and `RegisterScriptClass`.
