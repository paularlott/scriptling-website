---
title: Host-Side Scripting
description: Register pure Scriptling functions and classes that run on the host with no RPC.
tags: [plugins, go]
weight: 20
---

A plugin can register Scriptling code that runs entirely on the host side. No RPC is involved: the code executes in the host's Scriptling environment. This is useful for utility functions, data transformations, or any logic that doesn't need the plugin process.

## RegisterScriptFunc

`RegisterScriptFunc()` registers a Scriptling function that runs on the host:

```go
package main

import "github.com/paularlott/scriptling/plugin"

func main() {
    server := plugin.NewServer("util", "1.0.0", "Utility plugin")

    server.RegisterScriptFunc("slug", `
def slug(text):
    return text.lower().replace(" ", "-")
`)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Host usage:

```python
import plugin.util
print(plugin.util.slug("Hello World"))
```

## RegisterScriptClass

`RegisterScriptClass()` registers a class implemented entirely in Scriptling:

```go
package main

import "github.com/paularlott/scriptling/plugin"

func main() {
    server := plugin.NewServer("util", "1.0.0", "Utility plugin")

    server.RegisterScriptClass("Pair", `
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def swap(self):
        return Pair(self.second, self.first)
`)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Host usage:

```python
import plugin.util

p = plugin.util.Pair(1, 2)
print(p.first)
s = p.swap()
print(s.first)
```

## When to Use Host-Side Scripting

| Need | Use |
| --- | --- |
| Pure data transformation | `RegisterScriptFunc` |
| Utility classes with no Go dependency | `RegisterScriptClass` |
| Augment a Go plugin with convenience helpers | Mix with `RegisterFunc`/`RegisterClass` |

Host-side scripts have no access to Go code or the plugin process. If you need to call back into the plugin, use a [custom wrapper](../client-wrappers/) instead.
