---
title: Client Wrappers
description: How the host wraps plugin functions and classes, auto-generated proxies and custom Scriptling wrappers.
weight: 10
---

When a plugin registers a function or class, the host needs Scriptling code to call it. By default the host auto-generates a proxy. You can replace this with custom Scriptling source using `Wrapper()`.

## Auto-Generated Proxies

Functions and classes registered with `RegisterFunc` or `RegisterClass` get an auto-generated proxy on the host. The proxy forwards calls to the plugin over JSON-RPC:

```go
fb := object.NewFunctionBuilder()
fb.Function(func(name string) string {
    return "Hello, " + name
})
server.RegisterFunc("greet", fb)
```

The host generates something equivalent to:

```python
import scriptling.plugin

def greet(*args, **kwargs):
    return scriptling.plugin.call_function("plugin.hello", "greet", *args, **kwargs)
```

For classes, the auto-generated proxy handles `__init__`, method calls, and cleanup:

```python
class Counter:
    def __init__(self, *args, **kwargs):
        self._plugin_remote = scriptling.plugin._new_object("plugin.counter", "Counter", *args, **kwargs)

    def inc(self, *args, **kwargs):
        return scriptling.plugin.call_method(self._plugin_remote, "inc", *args, **kwargs)

    def __del__(self):
        scriptling.plugin.release(self._plugin_remote)
```

The `__del__` method sends `object.destroy` to the plugin, which calls the plugin-side `__del__` to free resources (file handles, connections, etc.). The evaluator also installs a GC finalizer on the proxy instance, so cleanup happens automatically when the object becomes unreachable: even if `__del__` is never called explicitly.

## Custom Wrappers

`Wrapper()` replaces the auto-generated proxy with custom Scriptling source. The name must match the registered function or class name. The underlying RPC function or class is still callable via `scriptling.plugin.call_function`, `scriptling.plugin._new_object`, and `scriptling.plugin.call_method`.

### Wrapping a Function

```go
fb := object.NewFunctionBuilder()
fb.Function(func(name string) string {
    return "wrapped:" + name
})
server.RegisterFunc("decorate", fb)

server.Wrapper("decorate", `
import scriptling.plugin

def decorate(name):
    return scriptling.plugin.call_function("plugin.mixed", "decorate", name) + "!"
`)
```

### Wrapping a Class

```go
cb := object.NewClassBuilder("Config").
    Constructor(func(name string) *configData {
        return &configData{name: name}
    }).
    Method("get", func(self *configData, key string) string {
        return self.values[key]
    })
server.RegisterClass(cb)

server.Wrapper("Config", `
import scriptling.plugin

class Config:
    def __init__(self, name):
        self._plugin_remote = scriptling.plugin._new_object("plugin.mixed", "Config", name)

    def get(self, key):
        return scriptling.plugin.call_method(self._plugin_remote, "get", key)

    def __del__(self):
        scriptling.plugin.release(self._plugin_remote)
`)
```

The host uses the supplied source instead of auto-generating a proxy. The underlying RPC function or class remains callable.

**Custom class wrappers must include `__del__`** that calls `scriptling.plugin.release(self._plugin_remote)`: without it, the plugin-side object is never destroyed and resources leak.

### When to Use Custom Wrappers

| Need | Example |
| --- | --- |
| Default parameter values | `def search(query, limit=10)` |
| Argument transformation | Convert a dict to positional args |
| Convenience methods | Combine multiple RPC calls into one function |
| Rename or hide internals | Expose a cleaner API than the raw RPC |

## Mixed Example

A single plugin can use both auto-generated proxies and custom wrappers:

```go
package main

import (
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

type configData struct {
    name   string
    values map[string]string
}

func main() {
    server := plugin.NewServer("mixed", "1.0.0", "Mixed demo")

    // Auto-generated proxy: no Wrapper() call
    fb := object.NewFunctionBuilder()
    fb.Function(func(name string) string {
        return "generated:" + name
    })
    server.RegisterFunc("generated", fb)

    // Custom wrapper: Wrapper() replaces the auto-proxy
    fbWrap := object.NewFunctionBuilder()
    fbWrap.Function(func(name string) string {
        return "wrapped:" + name
    })
    server.RegisterFunc("decorate", fbWrap)
    server.Wrapper("decorate", `
import scriptling.plugin

def decorate(name):
    return scriptling.plugin.call_function("plugin.mixed", "decorate", name) + "!"
`)

    // Custom class wrapper
    cb := object.NewClassBuilder("Config").
        Constructor(func(name string) *configData {
            return &configData{name: name, values: map[string]string{}}
        }).
        Method("get", func(self *configData, key string) string {
            return self.values[key]
        }).
        Method("set", func(self *configData, key, val string) {
            self.values[key] = val
        })
    server.RegisterClass(cb)
    server.Wrapper("Config", `
import scriptling.plugin

class Config:
    def __init__(self, name):
        self._plugin_remote = scriptling.plugin._new_object("plugin.mixed", "Config", name)

    def get(self, key):
        return scriptling.plugin.call_method(self._plugin_remote, "get", key)

    def set(self, key, val):
        scriptling.plugin.call_method(self._plugin_remote, "set", key, val)

    def __del__(self):
        scriptling.plugin.release(self._plugin_remote)
`)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Host usage:

```python
import plugin.mixed

print(plugin.mixed.generated("Ada"))   # auto-generated proxy
print(plugin.mixed.decorate("Ada"))    # custom wrapper

cfg = plugin.mixed.Config("Ada")       # custom class wrapper
cfg.set("host", "localhost")
print(cfg.get("host"))
```
