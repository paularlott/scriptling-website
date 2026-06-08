---
title: Go Plugins
description: Register functions and classes in a Go plugin executable.
weight: 3
---

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

- **`*Instance` methods** — manually manage `self.Fields` (shown below). Fields stored in `self.Fields` are readable and writable from Scriptling.
- **Typed receivers** — use `Constructor` to auto-wrap a Go struct (see [Storing Go Structs](#storing-go-structs)). Go struct fields are private; only registered methods and properties are exposed to Scriptling.

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
            self.Fields["value"] = object.NewInteger(int64(start))
        }).
        Method("inc", func(self *object.Instance, amount int) int {
            current := self.Fields["value"].(*object.Integer).IntValue()
            next := current + int64(amount)
            self.Fields["value"] = object.NewInteger(next)
            return int(next)
        }).
        Method("get", func(self *object.Instance) int {
            return int(self.Fields["value"].(*object.Integer).IntValue())
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

For classes backed by Go structs, use `Constructor` to register a function that returns a pointer to your struct. The struct is automatically wrapped and stored on the instance. Methods whose first parameter matches the constructor's return type receive the unwrapped struct directly — no manual Field boxing/unboxing needed.

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

The constructor function can accept typed parameters (with optional `context.Context` and `object.Kwargs`) and must return a pointer type. The return type becomes the **receiver type** — all methods whose first parameter matches it receive the unwrapped struct directly.

Methods registered with `Method()` are exposed to Scriptling. Go struct fields are **not** — they are private to the Go side. Use `Property()` or `PropertyWithSetter()` on the builder to expose them (see [Builder Classes: Properties](../../go-integration/builder-classes/#exposing-struct-fields-with-properties)).

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

Plugin classes hold real resources inside the plugin process — file handles, database connections, network sockets, etc. Define a `__del__` method to clean up when the host releases the object:

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
- `__del__` can be called multiple times explicitly — each call runs the function
- When triggered by GC (via `object.destroy`), the server calls `__del__` at most once per object

With typed receivers, `__del__` receives the Go struct directly. With `*object.Instance`, it receives the instance and can clean up fields manually.

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

- [Client Wrappers](client-wrappers/) — How the host wraps plugin functions and classes, and how to customise the wrapper source.
- [Host-Side Scripting](host-side-scripting/) — Register pure Scriptling functions and classes that run on the host with no RPC.
