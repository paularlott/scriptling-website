---
title: Go Libraries
description: Creating Go libraries with functions and constants.
weight: 3
---

Create reusable Go libraries with functions, constants, and sub-libraries.

## Native Library API

### Basic Library

```go
import (
    "context"
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

// Register the library
func main() {
    p := scriptling.New()
    p.RegisterLibrary(MyLibrary)
}
```

Use from Scriptling:

```python
import mylib

connected = mylib.connect("localhost", 8080)
print(f"Max connections: {mylib.MAX_CONNECTIONS}")
print(f"Version: {mylib.VERSION}")
```

## Library with Sub-Libraries

```go
var DatabaseLibrary = object.NewLibrary("database",
    map[string]*object.Builtin{
        "connect": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                // Connection logic
                return &object.Boolean{Value: true}
            },
            HelpText: "connect(host, port) - Connect to database",
        },
    },
    map[string]object.Object{
        "DEFAULT_PORT": &object.Integer{Value: 5432},
    },
    "Database connectivity library",
)

// Add sub-libraries
var QueryLibrary = object.NewLibrary("query",
    map[string]*object.Builtin{
        "select": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                table, _ := args[0].AsString()
                // SELECT logic
                return &object.List{Elements: []object.Object{}}
            },
            HelpText: "select(table) - Select all rows from table",
        },
        "insert": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                table, _ := args[0].AsString()
                data, _ := args[1].AsDict()
                // INSERT logic
                return &object.Integer{Value: 1}
            },
            HelpText: "insert(table, data) - Insert row into table",
        },
    },
    nil,
    "Query operations",
)

func main() {
    p := scriptling.New()

    // Register main library
    p.RegisterLibrary(DatabaseLibrary)

    // Register as sub-library
    p.RegisterSubLibrary("database", "query", QueryLibrary)
}
```

Use from Scriptling:

```python
import database

db = database.connect("localhost", 5432)
rows = database.query.select("users")
database.query.insert("users", {"name": "Alice"})
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

## Factory Pattern for Stateful Libraries

Libraries that need to create objects with state:

```go
// Factory function that creates instances
var ConnectionLibrary = object.NewLibrary("connection",
    map[string]*object.Builtin{
        "create": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                host, _ := args[0].AsString()
                port, _ := kwargs.GetInt("port", 8080)

                // Create a new connection object (as dict with methods)
                conn := &object.Dict{Pairs: map[string]object.Object{
                    "host": &object.String{Value: host},
                    "port": object.NewInteger(int64(port)),
                    "connected": object.False,
                }}

                return conn
            },
            HelpText: "create(host, port=8080) - Create a new connection",
        },
    },
    nil,
    "Connection factory library",
)
```

## Complete Library Example

```go
package mylib

import (
    "context"
    "fmt"
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
            "PI":    object.NewFloat(3.14159265359),
            "E":     object.NewFloat(2.71828182846),
            "PHI":   object.NewFloat(1.61803398875),  // Golden ratio
            "VERSION": &object.String{Value: "1.0.0"},
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

## Registering Script Libraries

You can also register libraries written in Scriptling:

```go
p.RegisterScriptLibrary("helpers", `
def format_name(first, last):
    return first + " " + last

def capitalize(text):
    return text[0].upper() + text[1:]

DEFAULT_GREETING = "Hello"
`)

p.Eval(`
import helpers

name = helpers.format_name("john", "doe")
greeting = helpers.capitalize(helpers.DEFAULT_GREETING)
`)
```

## Best Practices

1. **Group related functions** - Put related functions in the same library
2. **Use sub-libraries** - Organize large libraries into sub-modules
3. **Provide help text** - Make functions discoverable
4. **Export constants** - Share configuration values
5. **Use lazy loading** - Load heavy libraries on demand
6. **Handle errors gracefully** - Return meaningful error messages

```go
// Good: Organized library with help text
var GoodLibrary = object.NewLibrary("goodlib",
    map[string]*object.Builtin{
        "process": {
            Fn: processFunc,
            HelpText: `process(data, options={}) - Process data

Parameters:
  data - Input data
  options - Configuration options

Returns:
  Processed result`,
        },
    },
    map[string]object.Object{
        "VERSION": &object.String{Value: "1.0.0"},
    },
    "A well-documented library",
)
```
