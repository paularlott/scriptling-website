---
title: Native API
description: Direct control with maximum performance for extending Scriptling.
weight: 2
---

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

## Topics

- [Functions](functions/) - Register individual Go functions
- [Libraries](libraries/) - Create libraries with functions and constants
- [Classes](classes/) - Define custom classes

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
        return &object.Integer{Value: a + b}
    })

    p.Eval(`result = add(10, 20)`)  // result = 30
}
```

## See Also

- [Builder API](../builder/) - Type-safe, cleaner syntax
- [Script Extensions](../scripts/) - Extend using Scriptling code
