---
description: Register functions and classes in a Go plugin executable.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/plugins/go-plugins/
sources:
    - resource: https://scriptling.dev/docs/plugins/go-plugins/
status: stable
tags:
    - plugins
    - go
title: Go Plugins
type: Guide
---
# Go Plugins

A Go plugin registers functions, classes, and constants using the `plugin` and `object` packages. All registration goes through `RegisterFunc` and `RegisterClass`, which accept builder objects.

## Setup

Every Go plugin is a `package main` that creates a server and calls `Run`:

```go
package main

import "github.com/paularlott/scriptling/plugin"

func main() {
    server := plugin.NewServer("hello", "1.0.0", "Hello plugin")

    // register functions and classes here

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Build it and place the executable in a plugin directory:

```bash
go build -o ./plugins/hello .
scriptling --plugin-dir ./plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

## RegisterFunc with FunctionBuilder

`RegisterFunc` takes a name and a `*object.FunctionBuilder`. The builder wraps a typed Go function and `RegisterFunc` calls `.Build()` internally.

```go
package main

import (
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    server := plugin.NewServer("hello", "1.0.0", "Hello plugin")

    fb := object.NewFunctionBuilder()
    fb.Function(func(name string) string {
        return "Hello, " + name
    })
    server.RegisterFunc("greet", fb)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Host usage:

```python
import plugin.hello
print(plugin.hello.greet("Ada"))
```

## HTTP Transport

Go plugins can also serve the Scriptling plugin protocol over HTTP by mounting
the server as an `http.Handler`:

```go
package main

import (
    "log"
    "net/http"

    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    server := plugin.NewServer("hello_http", "1.0.0", "HTTP plugin")

    fb := object.NewFunctionBuilder()
    fb.Function(func(name string) string {
        return "Hello, " + name
    })
    server.RegisterFunc("greet", fb)

    http.Handle("/json-rpc", server)
    log.Fatal(http.ListenAndServe("127.0.0.1:8081", nil))
}
```

Load it from Scriptling as a full plugin peer:

```python
import scriptling.plugin

name = scriptling.plugin.load(
    "hello_http",
    "http://127.0.0.1:8081/json-rpc",
    scriptling=True,
    headers={"Authorization": "Bearer token"},
)
import plugin.hello_http
print(plugin.hello_http.greet("Ada"))
```

HTTP plugin transport is request/response only: it supports handshakes,
generated `plugin.*` proxies, function calls, object lifecycle, and batches,
but the server cannot initiate callbacks back to the client. Host callbacks and
`plugin.Logger(ctx)` require the bidirectional stdio transport. See the
`examples/plugins/http-go` example for a complete
server and client script.

### Advanced FunctionBuilder Callback

For full control over argument conversion, pass a raw `BuiltinFunction`-style callback to the same `FunctionBuilder`:

```go
package main

import (
    "context"

    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    server := plugin.NewServer("hello", "1.0.0", "Hello plugin")

    fb := object.NewFunctionBuilder()
    fb.Function(func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        name, err := args[0].AsString()
        if err != nil {
            return err
        }
        return object.NewString("native:" + name)
    })
    server.RegisterFunc("label", fb)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

## RegisterClass with ClassBuilder

`RegisterClass` takes a `*object.ClassBuilder`. Two styles are supported:

- **`*Instance` methods**: manually manage instance fields via `SetField`/`Field` for in-process state (shown below). Plugin-side fields live inside the plugin process; the host only sees the methods and properties you register on the builder.
- **Typed receivers**: use `Constructor` to auto-wrap a Go struct (see [Storing Go Structs](#storing-go-structs)). Go struct fields are private; only registered methods and properties are exposed to Scriptling.

`RegisterClass` calls `.Build()` internally.

```go
package main

import (
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    server := plugin.NewServer("counter", "1.0.0", "Counter demo")

    cb := object.NewClassBuilder("Counter").
        Method("__init__", func(self *object.Instance, start int) {
            self.SetField("value", object.NewInteger(int64(start)))
        }).
        Method("inc", func(self *object.Instance, amount int) int {
            current := self.Field("value").(*object.Integer).IntValue()
            next := current + int64(amount)
            self.SetField("value", object.NewInteger(next))
            return int(next)
        }).
        Method("get", func(self *object.Instance) int {
            return int(self.Field("value").(*object.Integer).IntValue())
        })

    server.RegisterClass(cb)

    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

Host usage:

```python
import plugin.counter

c = plugin.counter.Counter(4)
print(c.inc(3))
print(c.get())
```

## Storing Go Structs

### Typed Receivers (recommended)

For classes backed by Go structs, use `Constructor` to register a function that returns a pointer to your struct. The struct is automatically wrapped and stored on the instance. Methods whose first parameter matches the constructor's return type receive the unwrapped struct directly: no manual Field boxing/unboxing needed.

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
    server := plugin.NewServer("cfg", "1.0.0", "Config demo")

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

The constructor function can accept typed parameters (with optional `context.Context` and `object.Kwargs`) and must return a pointer type. The return type becomes the **receiver type**: all methods whose first parameter matches it receive the unwrapped struct directly.

Methods registered with `Method()` are exposed to Scriptling. Go struct fields are **not**: they are private to the Go side. Use `Property()` or `PropertyWithSetter()` on the builder to expose them (see [Builder Classes: Properties](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-classes.md#exposing-struct-fields-with-properties)).

Constructors can also return an error as a second value:

```go
Constructor(func(path string) (*Handle, error) {
    h, err := openResource(path)
    if err != nil {
        return nil, err
    }
    return h, nil
})
```

### \_\_del\_\_ for Cleanup

Plugin classes hold real resources inside the plugin process: file handles, database connections, network sockets, etc. Define a `__del__` method to clean up when the host releases the object:

```go
type fileHandle struct {
    file *os.File
}

cb := object.NewClassBuilder("Handle").
    Constructor(func(path string) (*fileHandle, error) {
        f, err := os.Open(path)
        if err != nil {
            return nil, err
        }
        return &fileHandle{file: f}, nil
    }).
    Method("read", func(self *fileHandle) string {
        data, _ := io.ReadAll(self.file)
        return string(data)
    }).
    Method("__del__", func(self *fileHandle) {
        self.file.Close()
    })
```

The lifecycle works like this:

1. Host calls `plugin.mylib.Handle("data.txt")` → host sends `object.new` to plugin
2. Plugin creates the real instance, runs `__init__`, stores it in memory
3. Host-side proxy becomes unreachable → Go GC fires finalizer → sends `object.destroy` to plugin
4. Plugin receives `object.destroy` → calls `__del__` on the real instance → `self.file.Close()`

You can also trigger cleanup explicitly:

- From Scriptling: `scriptling.plugin.release(handle)` or `handle.__del__()`
- From Go: `plugin.ReleaseWithContext(ctx, obj)` for request-scoped cleanup; `plugin.Release(obj)` uses `plugin.DefaultReleaseTimeout`
- `__del__` can be called multiple times explicitly: each call runs the function
- When triggered by GC (via `object.destroy`), the server calls `__del__` at most once per object

With typed receivers, `__del__` receives the Go struct directly. With `*object.Instance`, it receives the instance and can clean up fields manually.


## Plugin Class Properties

Use `Property()` for getter-only properties and `PropertyWithSetter()` for read/write properties. Properties are exposed to the host as native Scriptling properties, so users write `obj.name` and `obj.name = value` rather than calling RPC helper functions directly.

```go
type counter struct {
    value int
}

cb := object.NewClassBuilder("Counter").
    Constructor(func(start int) *counter {
        return &counter{value: start}
    }).
    PropertyWithSetter("value",
        func(self *counter) int {
            return self.value
        },
        func(self *counter, value int) {
            self.value = value
        },
    ).
    Property("label", func(self *counter) string {
        return fmt.Sprintf("counter:%d", self.value)
    })

server.RegisterClass(cb)
```

Host usage:

```python
import plugin.properties

c = plugin.properties.Counter(10)
c.value = c.value + 5
print(c.value)   # 15
print(c.label)   # counter:15
```

`Property()` creates a read-only property. Assigning to it raises a Scriptling attribute error. `PropertyWithSetter()` creates a getter and setter pair; the setter receives the same receiver as methods and the new value as its next argument.

See `examples/plugins/properties` for a runnable plugin.

## Plugin Logging

Go plugins can ask for a call-scoped proxy to the host logger with `plugin.Logger(ctx)`. The proxy implements the standard `github.com/paularlott/logger.Logger` interface and sends records back to the manager-lifetime host logger over JSON-RPC.

```go
fb := object.NewFunctionBuilder()
fb.Function(func(ctx context.Context, name string, tags []any) string {
    plugin.Logger(ctx).With("plugin", "logger").Info("plugin work started",
        "name", name,
        "tags", tags,
    )
    return "logged:" + name
})
server.RegisterFunc("work", fb)
```

Host usage:

```python
import plugin.logger

print(plugin.logger.work("Ada", ["demo", 1]))
```

The logger proxy is call-scoped because it uses the active `context.Context` to reach the JSON-RPC runtime for that plugin call. Do not store it globally; call `plugin.Logger(ctx)` from functions, constructors, methods, or property accessors that receive the active `context.Context`. Values in log key/value pairs use the same transport conversion as function arguments: structs and maps become dictionaries, and slices or arrays become lists.

See `examples/plugins/logger` for a runnable plugin.

## Function Callbacks

A Scriptling function can be passed into a plugin call. The host sends it as a scoped callback reference, and the Go plugin receives it as `plugin.Callback`. The callback can be invoked until the outer plugin function returns.

```go
type tokenEvent struct {
    Token string `json:"token"`
    Index int    `json:"index"`
}

fb := object.NewFunctionBuilder()
fb.Function(func(ctx context.Context, onEvent plugin.Callback) (string, error) {
    if _, err := onEvent.Call(ctx, tokenEvent{Token: "Hello", Index: 0}); err != nil {
        return "", err
    }
    if _, err := onEvent.Call(ctx, []any{"done", 1}); err != nil {
        return "", err
    }
    return "Hello", nil
})
server.RegisterFunc("stream", fb)
```

Host usage:

```python
import plugin.callback

events = []

def on_event(event):
    events.append(event)
    return "ack"

text = plugin.callback.stream(on_event)
```

Callback payloads use the normal plugin transport values. Go maps and exported struct fields arrive as Scriptling dictionaries; slices and arrays arrive as Scriptling lists. If the Scriptling callback raises an error, `Callback.Call` returns that error and the plugin should return it from the outer function.

## Constants

```go
server.Constant("version", "1.0.0")
server.Constant("max_retries", 3)
```

## Further Reading

- [Client Wrappers](https://scriptling.dev/okf/scriptling-docs/plugins/go-plugins/client-wrappers.md): How the host wraps plugin functions and classes, and how to customise the wrapper source.
- [Host-Side Scripting](https://scriptling.dev/okf/scriptling-docs/plugins/go-plugins/host-side-scripting.md): Register pure Scriptling functions and classes that run on the host with no RPC.
