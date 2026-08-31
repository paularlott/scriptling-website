---
description: Creating interpreters, variable exchange, and calling functions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/basics/
sources:
    - resource: https://scriptling.dev/docs/go-integration/basics/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: Basics
type: Guide
---
# Basics

Core concepts for using Scriptling from Go applications. After the basic setup, focused fragments assume the same initialized `p`; standalone examples repeat setup only when registration or lifecycle is relevant.

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
    _, err := p.Eval(`x = 5 + 3`)
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
// Read and execute a script file
result, err := p.EvalFile("script.py")
```

Error messages from `EvalFile` include the filename automatically.

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

// Sets
if s, err := p.GetVarAsSet("my_set"); err == nil {
    fmt.Printf("set has %d elements\n", len(s.Elements))
}

// Tuples
if elems, err := p.GetVarAsTuple("my_tuple"); err == nil {
    for i, el := range elems {
        fmt.Printf("tuple[%d] = %s\n", i, el.Inspect())
    }
}
```

### Inspect and Modify the Environment

```go
// List names in lexical order. Only the injected "import" key is omitted;
// other globals, including imported bindings and dunder names, may appear.
names := p.ListVars()
fmt.Println("Variables:", names)

// Remove a variable
p.UnsetVar("temp_result")
```

### Converted and Raw Object Access

`GetVar` converts a Scriptling value to its Go representation and reports lookup failures as an `object.Object` error:

```go
value, objErr := p.GetVar("result")
if objErr != nil {
    fmt.Println("Lookup failed:", objErr.Inspect())
} else {
    fmt.Printf("Go value: %T(%v)\n", value, value)
}
```

Use `GetVarAsObject` when you need the original Scriptling object. Unlike `GetVar` and the typed convenience methods, its second return value is a Go `error`:

```go
obj, err := p.GetVarAsObject("result")
if err != nil {
    fmt.Println("Lookup failed:", err)
} else {
    switch value := obj.(type) {
    case *object.Integer:
        fmt.Printf("Integer: %d\n", value.IntValue())
    case *object.String:
        fmt.Printf("String: %s\n", value.StringValue())
    case *object.Dict:
        fmt.Printf("Dict with %d keys\n", len(value.Pairs))
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

Libraries are not available to scripts unless you register them. Register all standard libraries with a single call:

```go
import "github.com/paularlott/scriptling/stdlib"

stdlib.RegisterAll(p)
```

Extended and `scriptling.*` libraries are registered individually, and filesystem libraries take an `allowedPaths` argument for access control. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for the complete list of libraries and their registration functions.

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

### Interpreter Lifecycle

An interpreter is stateful: globals, functions, classes, and imported bindings persist across `Eval` calls. Reuse it unchanged only when those calls belong to the same logical script session.

For independent sequential jobs, preserve registrations but clear script state before the next job:

```go
if _, err := p.Eval(firstJob); err != nil {
    return err
}
p.Reset() // also clears captured output; imports load again on demand
if _, err := p.Eval(nextJob); err != nil {
    return err
}
```

Use `ResetEnv("name", "config")` when selected bindings should survive; the injected `import` builtin is always retained. Use `Clone()` when each request, tenant, or concurrent job needs a fresh environment based on the same registrations.

### Cloning Interpreters

Create an isolated interpreter that shares library registrations but has a fresh environment. Useful for per-request or multi-tenant isolation:

```go
// Set up a template interpreter once
template := scriptling.New()
stdlib.RegisterAll(template)
template.RegisterScriptLibrary("mylib", myLibScript)

// Per-request: clone gives a fresh env with the same libraries available
handler := func(w http.ResponseWriter, r *http.Request) {
    p := template.Clone()
    p.SetVar("request_id", r.Header.Get("X-Request-ID"))
    result, err := p.EvalFile("handler.py")
    // ...
}
```

Each clone re-evaluates script libraries on first import, so no mutable state (counters, caches) is shared between clones.

### Library Loading

Use the `libloader` package for flexible library loading:

```go
import "github.com/paularlott/scriptling/libloader"

// Load libraries from filesystem (Python-style folder structure)
loader := libloader.NewFilesystem("/app/libs")
p.SetLibraryLoader(loader)

// Chain multiple loaders
chain := libloader.NewChain(
    libloader.NewFilesystem("/app/libs"),
    libloader.NewMemoryLoader(map[string]string{}),
)
p.SetLibraryLoader(chain)
```

See [Library Loader Chain](https://scriptling.dev/okf/scriptling-docs/go-integration/loader-chain.md) for full documentation.

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

// Inspect the result before err: SystemExit(0) is a clean exit and may have
// a nil Go error, while non-zero exits return both the exception and an error.
if ex, ok := object.AsException(result); ok && ex.IsSystemExit() {
    os.Exit(ex.GetExitCode())
}
if err != nil {
    fmt.Printf("Script error: %v\n", err)
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
    extlibs.RegisterRequestsLibrary(p)

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
    users = response.json()
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

## See Also

- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - How to register built-in libraries
- [Native API](https://scriptling.dev/okf/scriptling-docs/go-integration/native.md) - Direct object-level control
- [Builder API](https://scriptling.dev/okf/scriptling-docs/go-integration/builder.md) - Type-safe, cleaner syntax
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security best practices for embedding
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Usage reference for all libraries
