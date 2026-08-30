---
description: Direct control with maximum performance for extending Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/native/
sources:
    - resource: https://scriptling.dev/docs/go-integration/native/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: Native API
type: Guide
---
# Native API

The Native API provides direct access to Scriptling's internal object system with maximum performance and full control.

## When to Use Native API

| Factor | Native API | Builder API |
|--------|------------|-------------|
| **Performance** | Maximum | Slight overhead at registration |
| **Control** | Full control | Convention-based |
| **Type Safety** | Manual checking | Automatic |
| **Code Clarity** | More verbose | Cleaner |
| **Best For** | Performance-critical, complex logic | Rapid development, simple functions |

## Function Signature

All Native API functions use this signature:

```go
func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object
```

- `ctx`: Context for cancellation and environment access
- `kwargs`: Keyword arguments wrapper with helper methods
- `args`: Positional arguments as Scriptling objects
- Returns: A Scriptling object result

`args` is **borrowed for the call only**: the interpreter reuses its backing array across calls, so do not retain `args` (or a sub-slice like `args[1:]`) past the return — don't store it in a field/map/global, capture it in a goroutine or a returned closure, or hand it to a `*object.List{Elements: args}`. Read elements, iterate, or spread `args...` into a synchronous call freely; if you need to keep it, copy first (`make([]object.Object, len(args)); copy(...)`). This matches CPython's `tp_call` convention.

## Blocking operations and the interpreter lock

Each environment has an interpreter lock (GIL) that serializes script execution. Your native function runs **holding this lock**: that's what makes shared-state threads (`runtime.background(shared=True)`) and concurrent handlers safe. If your function does blocking work (HTTP, file or database I/O, network reads, subprocess), release the lock for the duration of the blocking call with `object.RunBlocking` so other goroutines can run script while yours is blocked:

```go
import "net/http"

p.RegisterFunc("fetch", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    url, _ := args[0].CoerceString()

    var resp *http.Response
    var err error
    object.RunBlocking(ctx, func() {
        resp, err = http.Get(url) // blocking call: GIL released here
    })
    if err != nil {
        return &object.Error{Message: err.Error()}
    }
    defer resp.Body.Close()
    // ...read/decode resp.Body (wrap any further blocking reads too)...
    return object.NewString("ok")
})
```

`RunBlocking` is a no-op when there is no lock on the context (e.g. a raw worker goroutine), so it is always safe to call. Forgetting it won't corrupt state: the lock stays held: but it will **starve** other shared-environment threads while your call blocks, so any I/O-bound native function should wrap its blocking calls.

## Topics

- [Functions](https://scriptling.dev/okf/scriptling-docs/go-integration/native-functions.md) - Register individual Go functions
- [Libraries](https://scriptling.dev/okf/scriptling-docs/go-integration/native-libraries.md) - Create libraries with functions and constants
- [Classes](https://scriptling.dev/okf/scriptling-docs/go-integration/native-classes.md) - Define custom classes

## Quick Example

```go
import (
    "context"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

func main() {
    p := scriptling.New()

    // Native API: Direct control
    p.RegisterFunc("add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        if len(args) != 2 {
            return &object.Error{Message: "add requires 2 arguments"}
        }
        a, _ := args[0].AsInt()
        b, _ := args[1].AsInt()
        return object.NewInteger(a + b)
    })

    p.Eval(`result = add(10, 20)`)  // result = 30
}
```

## See Also

- [Builder API](https://scriptling.dev/okf/scriptling-docs/go-integration/builder.md) - Type-safe, cleaner syntax
- [Script Extensions](https://scriptling.dev/okf/scriptling-docs/go-integration/scripts.md) - Extend using Scriptling code
