---
title: Native Libraries
description: Create libraries with functions, constants, and sub-libraries.
weight: 2
---

Create reusable Go libraries with functions, constants, and sub-libraries using the Native API.

## Basic Library

```go
import (
    "context"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

var MyLibrary = object.NewLibrary("mylib",
    // Functions
    map[string]*object.Builtin{
        "connect": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                host, _ := args[0].AsString()
                port, _ := args[1].AsInt()

                fmt.Printf("Connecting to %s:%d\n", host, port)
                return &object.Boolean{Value: true}
            },
            HelpText: "connect(host, port) - Connect to a host and port",
        },
        "disconnect": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                fmt.Println("Disconnecting...")
                return &object.Boolean{Value: false}
            },
            HelpText: "disconnect() - Disconnect from current connection",
        },
    },
    // Constants
    map[string]object.Object{
        "MAX_CONNECTIONS": &object.Integer{Value: 100},
        "VERSION":         &object.String{Value: "1.0.0"},
        "DEBUG":           &object.Boolean{Value: true},
    },
    // Description
    "My custom library with connection utilities",
)

func main() {
    p := scriptling.New()
    p.RegisterLibrary(MyLibrary)
}
```

Use from Scriptling:

```python
import mylib

connected = mylib.connect("localhost", 8080)
print("Max connections:", mylib.MAX_CONNECTIONS)
print("Version:", mylib.VERSION)
```

## Library with State

Libraries can maintain state using Go closures:

```go
// Logger library that maintains state
type Logger struct {
    level    string
    messages []string
}

func NewLogger() *Logger {
    return &Logger{
        level:    "INFO",
        messages: make([]string, 0),
    }
}

func (l *Logger) CreateLibrary() map[string]*object.Builtin {
    return map[string]*object.Builtin{
        "set_level": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                if len(args) != 1 {
                    return &object.Error{Message: "set_level requires 1 argument"}
                }
                level, err := args[0].AsString()
                if err != nil {
                    return &object.Error{Message: "level must be string"}
                }
                l.level = level
                return &object.String{Value: "Level set to " + l.level}
            },
            HelpText: "set_level(level) - Set the logging level",
        },
        "log": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                if len(args) != 1 {
                    return &object.Error{Message: "log requires 1 argument"}
                }
                msg, err := args[0].AsString()
                if err != nil {
                    return &object.Error{Message: "message must be string"}
                }

                // Get environment for output
                env := evaluator.GetEnvFromContext(ctx)
                writer := env.GetWriter()

                logMsg := fmt.Sprintf("[%s] %s", l.level, msg)
                l.messages = append(l.messages, logMsg)
                fmt.Fprintln(writer, logMsg)

                return &object.String{Value: "logged"}
            },
            HelpText: "log(message) - Log a message",
        },
        "get_messages": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                elements := make([]object.Object, len(l.messages))
                for i, msg := range l.messages {
                    elements[i] = &object.String{Value: msg}
                }
                return &object.List{Elements: elements}
            },
            HelpText: "get_messages() - Get all logged messages",
        },
    }
}

// Usage
func main() {
    p := scriptling.New()
    logger := NewLogger()
    p.RegisterLibrary(object.NewLibrary("logger", logger.CreateLibrary(), nil, "Logger library"))

    p.Eval(`
import logger
logger.set_level("DEBUG")
logger.log("Application started")
logger.log("Processing data")
`)
}
```

## Sub-Libraries

Organize related functionality into sub-libraries:

```go
// Create URL parsing sub-library
parseLib := object.NewLibrary("parse",
    map[string]*object.Builtin{
        "quote": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                s, _ := args[0].AsString()
                return &object.String{Value: url.QueryEscape(s)}
            },
            HelpText: "quote(s) - URL encode a string",
        },
        "unquote": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                s, _ := args[0].AsString()
                val, _ := url.QueryUnescape(s)
                return &object.String{Value: val}
            },
            HelpText: "unquote(s) - URL decode a string",
        },
    },
    nil,
    "URL parsing utilities",
)

// Create main URL library and add sub-library
urlLib := object.NewLibrary("url",
    map[string]*object.Builtin{
        "join": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                base, _ := args[0].AsString()
                path, _ := args[1].AsString()
                return &object.String{Value: strings.TrimSuffix(base, "/") + "/" + strings.TrimPrefix(path, "/")}
            },
            HelpText: "join(base, path) - Join URL path segments",
        },
    },
    map[string]object.Object{
        "parse": parseLib,  // Sub-library as a constant
    },
    "URL utilities",
)

p.RegisterLibrary(urlLib)

// Use in script
p.Eval(`
import url
print(url.join("https://example.com", "/api/users"))  # https://example.com/api/users
print(url.parse.quote("hello world"))                   # hello+world
`)
```

## On-Demand Library Loading

Load libraries only when they're first imported:

```go
func main() {
    p := scriptling.New()

    // Set callback for lazy loading
    p.SetOnDemandLibraryCallback(func(p *scriptling.Scriptling, name string) bool {
        switch name {
        case "heavylib":
            // Only load when first imported
            p.RegisterLibrary(createHeavyLibrary())
            return true
        case "ai":
            p.RegisterLibrary(createAILibrary())
            return true
        case "mcp":
            p.RegisterLibrary(createMCPLibrary())
            return true
        }
        return false  // Library not found
    })

    // Library will be loaded when first referenced
    p.Eval(`
import heavylib  # Triggers callback, loads library
result = heavylib.process(data)
`)
}
```

## Complete Library Example

```go
package mylib

import (
    "context"
    "fmt"
    "math"
    "github.com/paularlott/scriptling/object"
)

// Create a comprehensive library
func CreateMathLibrary() *object.Library {
    return object.NewLibrary("mymath",
        map[string]*object.Builtin{
            // Basic operations
            "add": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    a, _ := args[0].AsFloat()
                    b, _ := args[1].AsFloat()
                    return object.NewFloat(a + b)
                },
                HelpText: "add(a, b) - Add two numbers",
            },
            "subtract": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    a, _ := args[0].AsFloat()
                    b, _ := args[1].AsFloat()
                    return object.NewFloat(a - b)
                },
                HelpText: "subtract(a, b) - Subtract b from a",
            },
            "multiply": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    a, _ := args[0].AsFloat()
                    b, _ := args[1].AsFloat()
                    return object.NewFloat(a * b)
                },
                HelpText: "multiply(a, b) - Multiply two numbers",
            },
            "divide": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    a, _ := args[0].AsFloat()
                    b, _ := args[1].AsFloat()
                    if b == 0 {
                        return &object.Error{Message: "division by zero"}
                    }
                    return object.NewFloat(a / b)
                },
                HelpText: "divide(a, b) - Divide a by b",
            },

            // Advanced operations
            "power": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    base, _ := args[0].AsFloat()
                    exp, _ := args[1].AsFloat()
                    return object.NewFloat(math.Pow(base, exp))
                },
                HelpText: "power(base, exp) - Raise base to power",
            },
            "sqrt": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    x, _ := args[0].AsFloat()
                    return object.NewFloat(math.Sqrt(x))
                },
                HelpText: "sqrt(x) - Square root of x",
            },

            // Statistical functions
            "mean": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    list, _ := args[0].AsList()
                    if len(list) == 0 {
                        return object.NewFloat(0)
                    }

                    sum := 0.0
                    for _, item := range list {
                        val, _ := item.AsFloat()
                        sum += val
                    }
                    return object.NewFloat(sum / float64(len(list)))
                },
                HelpText: "mean(numbers) - Calculate arithmetic mean",
            },
            "sum": {
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    list, _ := args[0].AsList()
                    sum := 0.0
                    for _, item := range list {
                        val, _ := item.AsFloat()
                        sum += val
                    }
                    return object.NewFloat(sum)
                },
                HelpText: "sum(numbers) - Sum all numbers in list",
            },
        },
        map[string]object.Object{
            "PI":       object.NewFloat(3.14159265359),
            "E":        object.NewFloat(2.71828182846),
            "PHI":      object.NewFloat(1.61803398875),  // Golden ratio
            "VERSION":  &object.String{Value: "1.0.0"},
        },
        "Extended math library with statistical functions",
    )
}

// Usage
func main() {
    p := scriptling.New()
    p.RegisterLibrary(CreateMathLibrary())

    p.Eval(`
import mymath

result = mymath.add(10, 20)
pi = mymath.PI
average = mymath.mean([1, 2, 3, 4, 5])
`)
}
```

## Best Practices

### 1. Group Related Functions

```go
// Good: Organized by functionality
mathLib := object.NewLibrary("math", map[string]*object.Builtin{
    "add": {...},
    "subtract": {...},
    "multiply": {...},
}, nil, "Math operations")

stringLib := object.NewLibrary("string", map[string]*object.Builtin{
    "upper": {...},
    "lower": {...},
    "trim": {...},
}, nil, "String operations")
```

### 2. Provide Descriptive Help Text

```go
"add": {
    Fn: func(...) { ... },
    HelpText: `add(a, b) - Add two numbers

  Parameters:
    a - First number
    b - Second number

  Returns:
    The sum of a and b

  Examples:
    add(2, 3)  # Returns 5`,
}
```

### 3. Use Constants for Configuration

```go
configLib := object.NewLibrary(
    "config",
    map[string]*object.Builtin{
        "get_config": {...},
    },
    map[string]object.Object{
        "API_VERSION": &object.String{Value: "v1"},
        "TIMEOUT":     &object.Integer{Value: 30},
        "DEBUG":       &object.Boolean{Value: false},
    },
    "Configuration library",
)
```

### 4. Add Library Description

```go
myLib := object.NewLibrary("mylib",
    functions,
    constants,
    "My custom data processing library",  // Description shown by help()
)
```

## Testing Libraries

```go
func TestLibrary(t *testing.T) {
    p := scriptling.New()

    // Create and register library
    lib := object.NewLibrary("testlib", map[string]*object.Builtin{
        "add": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                a, _ := args[0].(*object.Integer)
                b, _ := args[1].(*object.Integer)
                return &object.Integer{Value: a.Value + b.Value}
            },
        },
    }, nil, "Test library")
    p.RegisterLibrary(lib)

    // Test the library
    result, err := p.Eval(`
import testlib
result = testlib.add(10, 20)
`)
    if err != nil {
        t.Fatalf("Eval error: %v", err)
    }

    if value, objErr := p.GetVarAsInt("result"); objErr == nil {
        if value != 30 {
            t.Errorf("Expected 30, got %d", value)
        }
    }
}
```

## See Also

- [Native Functions](functions/) - Register individual functions
- [Native Classes](classes/) - Define custom classes
- [Builder Libraries](../builder/libraries/) - Type-safe library builder
