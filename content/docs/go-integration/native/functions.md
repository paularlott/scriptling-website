---
title: Native Functions
description: Register individual Go functions with direct control.
weight: 1
---

Register Go functions that can be called from Scriptling scripts using the Native API.

## Basic Function

For functions that only use positional arguments:

```go
import (
    "context"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

func main() {
    p := scriptling.New()

    p.RegisterFunc("double", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        if len(args) != 1 {
            return &object.Error{Message: "double requires 1 argument"}
        }

        if intObj, ok := args[0].(*object.Integer); ok {
            return &object.Integer{Value: intObj.Value * 2}
        }

        return &object.Error{Message: "argument must be integer"}
    })

    p.Eval(`
result = double(21)
print(result)  # 42
`)
}
```

## Function with Keyword Arguments

Functions can accept keyword arguments using the `kwargs` wrapper:

```go
p.RegisterFunc("make_duration", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Reject positional arguments
    if len(args) > 0 {
        return &object.Error{Message: "make_duration takes no positional arguments"}
    }

    // Use kwargs helper methods with defaults
    hours, err := kwargs.GetFloat("hours", 0.0)
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    minutes, err := kwargs.GetFloat("minutes", 0.0)
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    seconds, err := kwargs.GetFloat("seconds", 0.0)
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    totalSeconds := hours*3600 + minutes*60 + seconds
    return &object.Float{Value: totalSeconds}
})

p.Eval(`
duration = make_duration(hours=2, minutes=30)
print(duration)  # 9000.0
`)
```

## Mixed Positional and Keyword Arguments

```go
p.RegisterFunc("format_greeting", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) != 1 {
        return &object.Error{Message: "format_greeting requires name argument"}
    }

    name, err := args[0].AsString()
    if err != nil {
        return &object.Error{Message: "name must be string"}
    }

    // Use kwargs helper methods with defaults
    prefix, err := kwargs.GetString("prefix", "Hello")
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    suffix, err := kwargs.GetString("suffix", "!")
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    return &object.String{Value: prefix + ", " + name + suffix}
})

p.Eval(`
print(format_greeting("World"))                    # Hello, World!
print(format_greeting("World", prefix="Hi"))       # Hi, World!
print(format_greeting("World", suffix="..."))      # Hello, World...
print(format_greeting("World", prefix="Hey", suffix="?"))  # Hey, World?
`)
```

## Kwargs Helper Methods

The `object.Kwargs` type provides convenient helper methods:

| Method | Description |
|--------|-------------|
| `GetString(name, default) (string, Object)` | Extract string, return default if missing |
| `GetInt(name, default) (int64, Object)` | Extract int (accepts Integer/Float) |
| `GetFloat(name, default) (float64, Object)` | Extract float (accepts Integer/Float) |
| `GetBool(name, default) (bool, Object)` | Extract bool |
| `GetList(name, default) ([]Object, Object)` | Extract list elements |
| `Has(name) bool` | Check if key exists |
| `Keys() []string` | Get all keys |
| `Len() int` | Get number of kwargs |
| `Get(name) Object` | Get raw Object value |

### Must* Variants

For simple cases where you want to use defaults on any error:

| Method | Description |
|--------|-------------|
| `MustGetString(name, default) string` | Extract string, ignore errors |
| `MustGetInt(name, default) int64` | Extract int, ignore errors |
| `MustGetFloat(name, default) float64` | Extract float, ignore errors |
| `MustGetBool(name, default) bool` | Extract bool, ignore errors |
| `MustGetList(name, default) []Object` | Extract list, ignore errors |

## Type-Safe Accessor Methods

All Scriptling objects implement type-safe accessor methods:

```go
// Using type-safe accessors (clean!)
p.RegisterFunc("add_tax", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) != 2 {
        return &object.Error{Message: "add_tax requires 2 arguments"}
    }

    // AsFloat() automatically handles both Integer and Float
    price, err := args[0].AsFloat()
    if err != nil {
        return &object.Error{Message: "price: " + err.Error()}
    }

    rate, err := args[1].AsFloat()
    if err != nil {
        return &object.Error{Message: "rate: " + err.Error()}
    }

    result := price * (1 + rate)
    return &object.Float{Value: result}
})
```

### Available Accessor Methods

| Method | Description |
|--------|-------------|
| `AsString() (string, Object)` | Extract string value |
| `AsInt() (int64, Object)` | Extract integer (floats truncate) |
| `AsFloat() (float64, Object)` | Extract float (ints convert automatically) |
| `AsBool() (bool, Object)` | Extract boolean |
| `AsList() ([]Object, Object)` | Extract list/tuple elements (returns a copy) |
| `AsDict() (map[string]Object, Object)` | Extract dict as map (keys are human-readable strings) |

> **Note:** The second return value is `nil` on success, or an `*Error` object on failure. You can check for errors like `if err != nil { ... }`.

### Coercion Methods

| Method | Type Safety | Description |
|--------|-------------|-------------|
| `AsString()` | Strict | Returns string only if object is a STRING |
| `AsInt()` | Strict | Returns int64 only if object is INTEGER/FLOAT |
| `AsFloat()` | Strict | Returns float64 only if object is INTEGER/FLOAT |
| `CoerceString()` | Loose | **Auto-converts** any type to string |
| `CoerceInt()` | Loose | **Auto-converts** strings/floats to int |
| `CoerceFloat()` | Loose | **Auto-converts** strings/ints to float |

## Function with Output Capture

Functions can write to the output capture system:

```go
import (
    "fmt"
    "github.com/paularlott/scriptling/evaluator"
)

p.RegisterFunc("debug_print", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Get environment from context
    env := evaluator.GetEnvFromContext(ctx)
    writer := env.GetWriter()

    // Print debug information
    fmt.Fprintf(writer, "[DEBUG] Function called with %d arguments\n", len(args))
    for i, arg := range args {
        fmt.Fprintf(writer, "[DEBUG] Arg %d: %s\n", i, arg.Inspect())
    }

    return &object.String{Value: "logged"}
})
```

## Adding Help Text

```go
p.RegisterFunc("calculate", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Implementation
    return &object.Integer{Value: 42}
}, `calculate(x, y) - Perform calculation

  Parameters:
    x - First number
    y - Second number

  Returns:
    The calculated result

  Examples:
    calculate(10, 5)  # Returns 15
`)

// Users can then access help:
// help("calculate")  # Shows the documentation
```

If you omit the help text, basic help will be auto-generated:

```go
p.RegisterFunc("my_func", func(...) object.Object {
    // Auto-generates: "my_func(...) - User-defined function"
    return object.NULL
})
```

## Return Types

### Integers

```go
return &object.Integer{Value: 42}
return object.NewInteger(42)
```

### Floats

```go
return &object.Float{Value: 3.14}
return object.NewFloat(3.14)
```

### Strings

```go
return &object.String{Value: "hello"}
```

### Booleans

```go
return &object.Boolean{Value: true}
return object.True
return object.False
```

### Lists

```go
return &object.List{Elements: []object.Object{
    &object.Integer{Value: 1},
    &object.String{Value: "two"},
}}
```

### Dictionaries

```go
return object.NewStringDict(map[string]object.Object{
    "name":  &object.String{Value: "Alice"},
    "count": &object.Integer{Value: 42},
})
```

### None/Null

```go
return object.None
```

### Errors

```go
return &object.Error{Message: "something went wrong"}
```

## Context Usage

### Cancellation

```go
p.RegisterFunc("long_operation", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    for i := 0; i < 1000000; i++ {
        // Check for cancellation
        select {
        case <-ctx.Done():
            return &object.Error{Message: "operation cancelled"}
        default:
            // Continue processing
        }
    }
    return &object.Integer{Value: 1}
})
```

### Timeout Handling

```go
p.RegisterFunc("fetch_with_timeout", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    url, _ := args[0].AsString()
    timeoutSec, _ := kwargs.GetInt("timeout", 30)

    // Create child context with timeout
    childCtx, cancel := context.WithTimeout(ctx, time.Duration(timeoutSec)*time.Second)
    defer cancel()

    // Use childCtx for operations
    result := fetchData(childCtx, url)

    return result
})
```

## Best Practices

### 1. Always Validate Arguments

```go
p.RegisterFunc("divide", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) != 2 {
        return &object.Error{Message: "divide requires 2 arguments: (a, b)"}
    }

    a, err := args[0].AsFloat()
    if err != nil {
        return &object.Error{Message: "first argument must be a number"}
    }

    b, err := args[1].AsFloat()
    if err != nil {
        return &object.Error{Message: "second argument must be a number"}
    }

    if b == 0 {
        return &object.Error{Message: "division by zero"}
    }

    return &object.Float{Value: a / b}
})
```

### 2. Provide Help Text

```go
p.RegisterFunc("process", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // implementation
}, `process(data, options={}) - Process data with options

Parameters:
  data - Input data to process
  options - Optional configuration dictionary
    - format: Output format ("json", "xml")
    - validate: Validate input (default: True)

Returns:
  Processed result as dictionary`)
```

### 3. Handle Context

```go
p.RegisterFunc("fetch", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    url, _ := args[0].AsString()

    // Create HTTP request with context
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return &object.Error{Message: err.Error()}
    }

    // ... rest of implementation
})
```

### 4. Use Kwargs for Optional Parameters

```go
p.RegisterFunc("connect", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    host, _ := args[0].AsString()

    // Optional parameters with defaults
    port, _ := kwargs.GetInt("port", 8080)
    timeout, _ := kwargs.GetInt("timeout", 30)
    useTLS, _ := kwargs.GetBool("tls", false)

    // implementation
})
```

## See Also

- [Native Libraries](libraries/) - Create libraries with functions and constants
- [Native Classes](classes/) - Define custom classes
- [Builder Functions](../builder/functions/) - Type-safe function builder
