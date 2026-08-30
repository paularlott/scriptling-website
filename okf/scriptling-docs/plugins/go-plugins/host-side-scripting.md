---
description: Register Scriptling functions and classes that run on the host, and wrap plugin objects with host-side code.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/plugins/go-plugins/host-side-scripting/
sources:
    - resource: https://scriptling.dev/docs/plugins/go-plugins/host-side-scripting/
status: stable
tags:
    - plugins
    - go
title: Host-Side Scripting
type: Guide
---
# Host-Side Scripting

A plugin can register Scriptling code that runs entirely on the host side. The source travels in the handshake schema, the host compiles and runs it in its own interpreter, and no RPC happens unless the code itself chooses to call back into the plugin. This is the mechanism behind the database plugins' ORM: the query builder chains, criteria objects and model gateways are Scriptling source shipped inside the plugin, running host-side, crossing the wire only when a query executes.

Three registration calls cover the cases:

| Call | What it does |
| --- | --- |
| `RegisterScriptFunc(name, source)` | A function defined in Scriptling source, running host-side |
| `RegisterScriptClass(name, source)` | A class defined in Scriptling source, instances and methods host-side |
| `Wrapper(name, source)` | Attaches source to an entry that is also registered the Go way: the Go class or function stays in the plugin process, and the host runs your source instead of the auto-generated RPC shim |

## RegisterScriptFunc

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

Zero RPC: the function executes in the host's environment.

## RegisterScriptClass

```go
server.RegisterScriptClass("Pair", `
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def swap(self):
        return Pair(self.second, self.first)
`)
```

Host usage:

```python
import plugin.util

p = plugin.util.Pair(1, 2)
s = p.swap()
```

Instances are ordinary host-side objects; nothing lives in the plugin process.

## Wrapper: host-side code around a plugin object

`Wrapper` is the important one for wrapping real plugin objects. The Go class
stays server-side (constructible, holding your handles), while the host gets
your source instead of the auto-generated proxy. The database plugins use
exactly this shape:

```go
// Server side: the Go class with the real handle.
server.RegisterClass(connectionClass)

// Host side: a wrapper whose methods RPC on demand, plus anything else
// you want to define there.
server.Wrapper("Connection", `
class Connection:
    def __init__(self, path):
        self._remote = scriptling.plugin._new_object("myplugin", "Connection", path)

    def query(self, sql, *params):
        return scriptling.plugin.call_method(self._remote, "query", sql, *params)

    def close(self):
        return scriptling.plugin.call_method(self._remote, "close")
`)
```

The generated module imports `scriptling.plugin` for you, so `_new_object`,
`call_method` and `call_function` are the bridge back into the plugin. A
wrapper method that only formats or validates arguments costs no round trip;
one that calls `call_method` costs exactly one.

## Rules to know

- **Every helper must be registered individually.** The schema carries one
  source per entry. A class whose source references a helper class or
  function fails at call time unless that helper is registered too, under the
  name the source uses.
- **One source flips the whole module.** If any entry carries a source, the
  host registers the entire library as script: entries without sources get
  their auto-generated RPC shims emitted alongside yours. You cannot mix the
  two behaviours per entry; you choose per entry only whether you supply the
  source.
- **The host's interpreter defines the semantics.** Your source runs under
  the host's language version. First-party plugins ship in lockstep with the
  host, so this is invisible; third parties should target the oldest host
  they intend to support.
- **Naming rules still apply.** Script-source entries land inside the
  plugin's module (`scriptling.sqlite._orm_Kit`, for example); the declared
  plugin name decides the module name, and verbatim dotted names that
  collide with a registered library are refused at load.
- **Trust is unchanged.** Host-side source runs with host privileges, but so
  does the plugin process itself, so this adds no new boundary; it only
  moves where the code executes.

## When to use what

| Need | Use |
| --- | --- |
| Pure data transformation | `RegisterScriptFunc` |
| Utility classes with no Go dependency | `RegisterScriptClass` |
| A host-side API over a plugin-side object | `Wrapper` around a registered Go class |
| Chained APIs that must not pay per-call RPC | `Wrapper` plus helper classes, calling back only at the boundary |

For a complete, production example of all three, see the sqlite plugin's
`cmd/main.go` and the shared ORM kit in `plugins/internal/relational` in the
Scriptling repository.
