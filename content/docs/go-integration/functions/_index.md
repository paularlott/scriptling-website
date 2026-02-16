---
title: Go Functions
description: Registering Go functions callable from Scriptling.
weight: 2
---

Register Go functions that can be called from Scriptling scripts.

## Native API

The native API gives you direct control with maximum performance.

### Basic Function

```go
import (
    "context"
    "github.com/paularlott/scriptling/object"
)

p.RegisterFunc("add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) != 2 {
        return &object.Error{Message: "add requires 2 arguments"}
    }

    a, err := args[0].AsInt()
    if err != nil {
        return &object.Error{Message: "first argument must be a number"}
    }

    b, err := args[1].AsInt()
    if err != nil {
        return &object.Error{Message: "second argument must be a number"}
    }

    return &object.Integer{Value: a + b}
})
```

### With Keyword Arguments

```go
p.RegisterFunc("format_greeting", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) < 1 {
        return &object.Error{Message: "format_greeting requires name argument"}
    }

    name, err := args[0].AsString()
    if err != nil {
        return &object.Error{Message: "name must be a string"}
    }

    // Extract keyword arguments with defaults
    prefix, _ := kwargs.GetString("prefix", "Hello")
    suffix, _ := kwargs.GetString("suffix", "!")
    uppercase, _ := kwargs.GetBool("uppercase", false)

    result := prefix + ", " + name + suffix
    if uppercase {
        result = strings.ToUpper(result)
    }

    return &object.String{Value: result}
})
```

Use from Scriptling:

```python
greeting = format_greeting("Alice")
# "Hello, Alice!"

greeting = format_greeting("Bob", prefix="Hi", suffix="!!!")
# "Hi, Bob!!!"

greeting = format_greeting("Charlie", uppercase=True)
# "HELLO, CHARLIE!"
```

### With Help Text

```go
p.RegisterFunc("calculate", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) < 2 {
        return &object.Error{Message: "calculate requires x and y arguments"}
    }

    x, _ := args[0].AsFloat()
    y, _ := args[1].AsFloat()
    op, _ := kwargs.GetString("operation", "add")

    var result float64
    switch op {
    case "add":
        result = x + y
    case "subtract":
        result = x - y
    case "multiply":
        result = x * y
    case "divide":
        if y == 0 {
            return &object.Error{Message: "division by zero"}
        }
        result = x / y
    default:
        return &object.Error{Message: "unknown operation: " + op}
    }

    return &object.Float{Value: result}
}, `calculate(x, y, operation="add") - Perform mathematical operation

Parameters:
  x - First number
  y - Second number
  operation - Operation to perform ("add", "subtract", "multiply", "divide")

Returns:
  The calculated result

Examples:
  calculate(10, 5)                    # 15
  calculate(10, 5, operation="subtract")  # 5
  calculate(10, 5, operation="multiply")  # 50`)
```

### Variadic Functions

```go
p.RegisterFunc("sum_all", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    total := int64(0)
    for _, arg := range args {
        val, err := arg.AsInt()
        if err != nil {
            return &object.Error{Message: "all arguments must be numbers"}
        }
        total += val
    }
    return &object.Integer{Value: total}
}, `sum_all(*args) - Sum all arguments

Example:
  sum_all(1, 2, 3, 4, 5)  # 15`)
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
return &object.Dict{Pairs: map[string]object.Object{
    "name":  &object.String{Value: "Alice"},
    "count": &object.Integer{Value: 42},
}}
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

## Registering Script Functions

### From Go Code

```go
// Register a function defined in Scriptling syntax
p.RegisterScriptFunc("my_func", `
def my_func(x):
    return x * 2
my_func
`)

// Now callable from scripts or Go
result, _ := p.CallFunction("my_func", 21)
// Returns: 42
```

### From File

```go
content, _ := os.ReadFile("helpers.py")
p.RegisterScriptFunc("helper", string(content))
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

## Complete Example

```go
package main

import (
    "context"
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Register custom functions
    p.RegisterFunc("greet", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        if len(args) < 1 {
            return &object.Error{Message: "greet requires a name"}
        }

        name, _ := args[0].AsString()
        formal, _ := kwargs.GetBool("formal", false)

        var greeting string
        if formal {
            greeting = "Good day, " + name
        } else {
            greeting = "Hi, " + name + "!"
        }

        return &object.String{Value: greeting}
    }, `greet(name, formal=False) - Generate a greeting

Parameters:
  name - Person's name
  formal - Use formal greeting (default: False)

Examples:
  greet("Alice")              # "Hi, Alice!"
  greet("Bob", formal=True)   # "Good day, Bob"`)

    // Use from script
    p.Eval(`
message1 = greet("Alice")
message2 = greet("Bob", formal=True)
print(message1)
print(message2)
`)
}
```
