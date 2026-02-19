---
title: Basics
description: Creating interpreters, variable exchange, and calling functions.
weight: 1
---

Core concepts for using Scriptling from Go applications.

## Creating an Interpreter

### Basic Setup

```go
package main

import (
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    // Create interpreter
    p := scriptling.New()

    // Register standard libraries
    stdlib.RegisterAll(p)

    // Execute Scriptling code
    result, err := p.Eval(`x = 5 + 3`)
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

### With Context and Timeout

```go
import (
    "context"
    "time"
)

// Create context with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// Evaluate with context
result, err := p.EvalWithContext(ctx, `
# Long-running operation
total = 0
for i in range(1000000):
    total += i
`)

// Call function with context
result, err := p.CallFunctionWithContext(ctx, "process_data", data)
```

## Executing Code

### Simple Execution

```go
// Single line
result, err := p.Eval("x = 42")

// Multi-line script
script := `
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

result = fibonacci(10)
`
result, err := p.Eval(script)
```

### Script Files

```go
import "os"

// Read and execute script file
content, err := os.ReadFile("script.py")
if err != nil {
    log.Fatal(err)
}

result, err := p.Eval(string(content))
```

## Variable Exchange

### Set Variables from Go

```go
// Simple types
p.SetVar("api_base", "https://api.example.com")
p.SetVar("timeout", 30)
p.SetVar("enabled", true)

// Complex types
p.SetVar("config", map[string]interface{}{
    "host": "localhost",
    "port": 8080,
    "debug": true,
})

// Lists
p.SetVar("items", []interface{}{1, 2, 3, 4, 5})
```

### Get Variables from Scriptling

```go
p.Eval(`result = 42`)

// Using convenience methods (recommended)
if value, err := p.GetVarAsInt("result"); err == nil {
    fmt.Printf("result = %d\n", value)
}

if name, err := p.GetVarAsString("name"); err == nil {
    fmt.Printf("name = %s\n", name)
}

if enabled, err := p.GetVarAsBool("enabled"); err == nil {
    fmt.Printf("enabled = %t\n", enabled)
}

// Complex types
if config, err := p.GetVarAsDict("config"); err == nil {
    if host, ok := config["host"]; ok {
        fmt.Printf("Host: %s\n", host.Inspect())
    }
}

// Lists
if items, err := p.GetVarAsList("items"); err == nil {
    for i, item := range items {
        fmt.Printf("items[%d] = %s\n", i, item.Inspect())
    }
}
```

### Raw Object Access

```go
// Get raw object for advanced operations
obj, exists := p.GetVar("result")
if exists {
    switch obj.(type) {
    case *object.Integer:
        val, _ := obj.AsInt()
        fmt.Printf("Integer: %d\n", val)
    case *object.String:
        val, _ := obj.AsString()
        fmt.Printf("String: %s\n", val)
    case *object.Dict:
        val, _ := obj.AsDict()
        fmt.Printf("Dict with %d keys\n", len(val))
    }
}
```

## Calling Functions

### Call Script Functions from Go

```go
// Define function in script
p.Eval(`
def greet(name, greeting="Hello"):
    return greeting + ", " + name + "!"
`)

// Call with positional arguments
result, err := p.CallFunction("greet", "Alice")
// Returns: "Hello, Alice!"

// Call with multiple arguments
result, err := p.CallFunction("greet", "Bob", "Hi")
// Returns: "Hi, Bob!"
```

### Get Return Values

```go
result, err := p.CallFunction("calculate", 10, 20)
if err != nil {
    log.Fatal(err)
}

// Convert result to Go type
if val, err := result.AsInt(); err == nil {
    fmt.Printf("Result: %d\n", val)
}

if val, err := result.AsString(); err == nil {
    fmt.Printf("Result: %s\n", val)
}

if val, err := result.AsBool(); err == nil {
    fmt.Printf("Result: %t\n", val)
}
```

## Output Capture

### Capture Print Output

```go
p := scriptling.New()
p.EnableOutputCapture()

p.Eval(`
print("Line 1")
print("Line 2")
`)

output := p.GetOutput()  // "Line 1\nLine 2\n" (also clears the buffer)
```

### Custom Output Writer

```go
import "bytes"

var buf bytes.Buffer
p.SetOutputWriter(&buf)
p.Eval(`print("Hello")`)
fmt.Println(buf.String())  // "Hello\n"
```

## Library Management

### Register Libraries

```go
import (
    "github.com/paularlott/scriptling/stdlib"
    "github.com/paularlott/scriptling/extlibs"
)

// Register all standard libraries at once
stdlib.RegisterAll(p)

// Register individual libraries
p.RegisterLibrary(stdlib.JSONLibrary)
p.RegisterLibrary(stdlib.MathLibrary)

// Register extended libraries
p.RegisterLibrary(extlibs.RequestsLibrary)

// Register os/pathlib with security restrictions
extlibs.RegisterOSLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterPathlibLibrary(p, []string{"/tmp", "/data"})
```

### Programmatic Import

```go
// Import libraries before executing scripts
p.Import("json")
p.Import("math")

// Now use libraries in scripts without import statements
p.Eval(`
data = json.dumps({"numbers": [1, 2, 3]})
result = math.sqrt(16)
`)
```

### On-Demand Library Loading

```go
// Set callback for lazy loading
p.SetOnDemandLibraryCallback(func(p *scriptling.Scriptling, name string) bool {
    switch name {
    case "heavylib":
        p.RegisterLibrary(createHeavyLibrary())
        return true
    case "speciallib":
        p.RegisterLibrary(createSpecialLibrary())
        return true
    }
    return false
})
```

## Error Handling

### Basic Error Handling

```go
result, err := p.Eval(script)
if err != nil {
    fmt.Printf("Script error: %v\n", err)
    return
}
```

### Exception Handling

```go
import "github.com/paularlott/scriptling/object"

result, err := p.Eval(script)
if err != nil {
    // Check for exception objects
    if ex, ok := object.AsException(result); ok {
        if ex.IsSystemExit() {
            os.Exit(ex.GetExitCode())
        }
        fmt.Printf("Exception: %s\n", ex.Message)
    }
    return
}
```

## Complete Example

```go
package main

import (
    "fmt"
    "log"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
    "github.com/paularlott/scriptling/extlibs"
)

func main() {
    // Create interpreter
    p := scriptling.New()

    // Register libraries
    stdlib.RegisterAll(p)
    p.RegisterLibrary(extlibs.RequestsLibrary)

    // Set configuration
    p.SetVar("api_base", "https://api.example.com")
    p.SetVar("timeout", 30)

    // Execute script
    script := `
import json
import requests

url = api_base + "/users"
options = {"timeout": timeout}
response = requests.get(url, options)

if response.status_code == 200:
    users = json.loads(response.body)
    result = {"count": len(users), "success": True}
else:
    result = {"count": 0, "success": False}
`

    result, err := p.Eval(script)
    if err != nil {
        log.Fatal(err)
    }

    // Access return value
    if dict, err := result.AsDict(); err == nil {
        if success, ok := dict["success"]; ok {
            if val, err := success.AsBool(); err == nil {
                fmt.Printf("Success: %t\n", val)
            }
        }
    }
}
```
