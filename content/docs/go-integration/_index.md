---
title: Go Integration
description: Embedding and using Scriptling from Go applications.
weight: 4
---

Complete guide for embedding Scriptling in Go applications.

## Installation

```bash
go get github.com/paularlott/scriptling
```

## Basic Usage

### Create Interpreter

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

### Execute Code

```go
// Simple execution
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

## Variable Exchange

### Set Variables from Go

```go
p.SetVar("api_base", "https://api.example.com")
p.SetVar("timeout", 30)
p.SetVar("config", map[string]interface{}{
    "host": "localhost",
    "port": 8080,
})
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

// Complex types
if config, err := p.GetVarAsDict("config"); err == nil {
    if host, ok := config["host"]; ok {
        fmt.Printf("Host: %s\n", host.Inspect())
    }
}
```

## Register Functions

### Register Go Functions

```go
p.RegisterFunc("custom", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    return &object.String{Value: "result"}
})
```

### Register Script Functions

```go
p.RegisterScriptFunc("my_func", `
def my_func(x):
    return x * 2
my_func
`)
```

### Register Script Libraries

```go
p.RegisterScriptLibrary("mylib", `
def add(a, b):
    return a + b

PI = 3.14159
`)
```

## Call Functions from Go

```go
// Register a function
p.RegisterFunc("multiply", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    a, _ := args[0].AsInt()
    b, _ := args[1].AsInt()
    return &object.Integer{Value: a * b}
})

// Call with Go arguments
result, err := p.CallFunction("multiply", 6, 7)
product, _ := result.AsInt()
fmt.Printf("Product: %d\n", product)  // 42
```

## Library Management

### Register Libraries

```go
import (
    "github.com/paularlott/scriptling/stdlib"
    "github.com/paularlott/scriptling/extlibs"
)

// Register all standard libraries
stdlib.RegisterAll(p)

// Register individual libraries
p.RegisterLibrary(stdlib.JSONLibrary)

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

## Output Capture

```go
p := scriptling.New()
p.EnableOutputCapture()

p.Eval(`
print("Line 1")
print("Line 2")
`)

output := p.GetOutput()  // "Line 1\nLine 2\n"
```

### Custom Output Writer

```go
var buf bytes.Buffer
p.SetOutputWriter(&buf)
p.Eval(`print("Hello")`)
fmt.Println(buf.String())  // "Hello\n"
```

## Error Handling

```go
result, err := p.Eval(script)
if err != nil {
    fmt.Printf("Script error: %v\n", err)
    return
}

// Check for exception objects
if ex, ok := object.AsException(result); ok {
    if ex.IsSystemExit() {
        os.Exit(ex.GetExitCode())
    }
}
```

## Performance Tips

1. **Reuse Interpreters** - Create once, use multiple times
2. **Load Only Needed Libraries** - Don't load JSON/HTTP if not needed
3. **Batch Operations** - Execute larger scripts rather than many small ones
4. **Pre-register Functions** - Register all Go functions before execution

```go
// Good: Reuse interpreter
p := scriptling.New()
for _, script := range scripts {
    p.Eval(script)
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

if response["status"] == 200:
    users = json.loads(response["body"])
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
