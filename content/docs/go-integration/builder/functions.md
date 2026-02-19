---
title: Builder Functions
description: Type-safe function builder with automatic type conversion.
weight: 1
---

Create type-safe functions with automatic type conversion using the Function Builder.

## Basic Function

```go
import "github.com/paularlott/scriptling/object"

func registerAddFunction(p *scriptling.Scriptling) {
    fb := object.NewFunctionBuilder()

    // Define function with automatic type conversion
    fb.FunctionWithHelp(func(a, b int) int {
        return a + b
    }, "add(a, b) - Add two numbers together")

    p.RegisterFunc("add", fb.Build())
}
```

## Function Signatures

The Builder API supports flexible function signatures:

- `func(args...) result` - Positional arguments only
- `func(ctx context.Context, args...) result` - Context + positional arguments
- `func(kwargs object.Kwargs, args...) result` - Kwargs + positional arguments
- `func(ctx context.Context, kwargs object.Kwargs, args...) result` - All parameters
- `func(kwargs object.Kwargs) result` - Kwargs only
- `func(ctx context.Context, kwargs object.Kwargs) result` - Context + kwargs only

**Parameter Order Rules (ALWAYS in this order):**

1. Context (optional) - comes first if present
2. Kwargs (optional) - comes after context (or first if no context)
3. Positional arguments - ALWAYS LAST

## Examples

### Simple Positional Arguments

```go
fb := object.NewFunctionBuilder()
fb.Function(func(a, b int) int {
    return a + b
})
p.RegisterFunc("add", fb.Build())

// Usage: add(3, 4) → 7
```

### Multiple Parameter Types

```go
fb.FunctionWithHelp(func(name string, count int, ratio float64) string {
    return fmt.Sprintf("%s: %d items at %.2f ratio", name, count, ratio)
}, "format(name, count, ratio) - Format data")
```

### With Context

```go
fb.Function(func(ctx context.Context, timeout int) error {
    select {
    case <-time.After(time.Duration(timeout) * time.Second):
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
})
p.RegisterFunc("wait", fb.Build())
```

### With Kwargs

```go
fb.Function(func(kwargs object.Kwargs) (string, error) {
    host, err := kwargs.GetString("host", "localhost")
    if err != nil {
        return "", err
    }
    port, err := kwargs.GetInt("port", 8080)
    if err != nil {
        return "", err
    }
    return fmt.Sprintf("%s:%d", host, port), nil
})
p.RegisterFunc("connect", fb.Build())

// Usage: connect(host="example.com", port=443) → "example.com:443"
```

### Mixed Positional and Kwargs

```go
fb.Function(func(kwargs object.Kwargs, name string, count int) string {
    prefix, _ := kwargs.GetString("prefix", ">")
    return fmt.Sprintf("%s %s: %d", prefix, name, count)
})
p.RegisterFunc("log", fb.Build())

// Usage: log("task", 5, prefix=">>>") → ">>> task: 5"
```

### With Error Handling

```go
fb.Function(func(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
})
p.RegisterFunc("divide", fb.Build())
```

### With Complex Types

```go
fb.Function(func(items []any) float64 {
    sum := 0.0
    for _, item := range items {
        if v, ok := item.(float64); ok {
            sum += v
        }
    }
    return sum
})

fb.Function(func(config map[string]any) string {
    if host, ok := config["host"].(string); ok {
        return "Connected to " + host
    }
    return "No host"
})
```

## Adding Help Text

```go
fb.FunctionWithHelp(func(x float64) float64 {
    return math.Sqrt(x)
}, "sqrt(x) - Return the square root of x")

fb.FunctionWithHelp(func(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}, "divide(a, b) - Divide two numbers (returns error if b is zero)")
```

## Variadic Functions

Accept variable number of arguments:

```go
fb.FunctionFromVariadicWithHelp(func(args ...interface{}) []interface{} {
    // Process all arguments
    result := make([]interface{}, len(args))
    for i, arg := range args {
        result[i] = fmt.Sprintf("Item %d: %v", i, arg)
    }
    return result
}, "process_all(*args) - Process all arguments")

// Usage in script:
// result = process_all(1, "hello", True, [1, 2, 3])
```

## Builder Methods Reference

| Method | Description |
|--------|-------------|
| `Function(fn)` | Register a typed Go function |
| `FunctionWithHelp(fn, help)` | Register with help text |
| `Build()` | Return the BuiltinFunction |

## Choosing Between Native and Builder API

| Factor | Native API | Builder API |
|--------|------------|-------------|
| **Performance** | Faster (no reflection overhead) | Slight overhead |
| **Code Clarity** | More verbose | Cleaner |
| **Type Safety** | Manual checking | Automatic |
| **Flexibility** | Full control | Convention-based |
| **Best For** | Performance-critical, complex logic | Rapid development, simple functions |

## See Also

- [Builder Libraries](libraries/) - Type-safe library builder
- [Builder Classes](classes/) - Type-safe class builder
- [Native Functions](../native/functions/) - Direct control with maximum performance
