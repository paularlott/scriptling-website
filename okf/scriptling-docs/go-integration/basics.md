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

## Program Cache

Every script the interpreter runs is parsed and compiled once and kept in a
process-wide cache, so evaluating the same source again skips both steps. The
cache is shared by all interpreter instances in the process and is bounded by a
memory budget of 64 MiB by default; when it fills, the least recently used
programs are dropped and simply parsed again on their next use. An undersized
budget costs time, never correctness.

### Set the Budget

```go
// Allow 256 MiB of parsed scripts; useful for hosts that run many distinct scripts.
scriptling.SetProgramCacheMaxBytes(256 << 20)

// Remove the limit entirely.
scriptling.SetProgramCacheMaxBytes(0)

// Back to the default.
scriptling.SetProgramCacheMaxBytes(scriptling.DefaultProgramCacheMaxBytes)
```

Lowering the budget evicts programs immediately. Set it once at startup, before
scripts run.

### Check Whether It Fits

Hit and miss counts tell you whether the budget suits your set of scripts. A
miss rate that stays high on a long-running host, together with evictions,
means scripts are being re-parsed because they no longer fit.

```go
stats := scriptling.GetProgramCacheStats()
fmt.Printf("%d programs, %d of %d bytes, hits=%d misses=%d evictions=%d\n",
    stats.Entries, stats.UsedBytes, stats.MaxBytes,
    stats.Hits, stats.Misses, stats.Evictions)
```

`MaxBytes` is 0 when the byte limit is off.


## Script Resource Limits

A host that runs scripts written by other people needs two ceilings that a
per-script timeout does not give it: how far one script can fan out, and how
much memory the scripts can hold between them. Both are process-wide settings,
set once at startup, and neither adds any cost to the evaluator's hot path.

### Cap Fan-Out

`max_parallel` is a request from the script. The host decides the ceiling:

```go
import (
    "github.com/paularlott/scriptling/extlibs"
    scriptlingai "github.com/paularlott/scriptling/extlibs/ai"
)

// client.Pipeline, completion_parallel and ask_parallel
scriptlingai.SetMaxParallelLimit(10)

// requests.parallel
extlibs.SetRequestsMaxParallelLimit(10)
```

A script that asks for `max_parallel=50` under a ceiling of 10 gets 10; nothing
is raised, because the ceiling is the host's resource policy rather than a
script error. A ceiling of 0 removes it. The check is one atomic load when a
pipeline or batch is created.

### Limit Memory

Go cannot attribute heap memory to one interpreter without accounting on
every allocation, which would slow every script. The memory guard therefore
works at process level: a single goroutine samples the heap on a timer, and
while the heap stays above the ceiling after a garbage collection it cancels
the most recently started script. Shedding newest-first protects work that was
already within budget from a newcomer that is not.

```go
// Cancel the newest running script while heap objects exceed 384 MiB.
scriptling.SetMemoryLimit(384 << 20)

// Disable.
scriptling.SetMemoryLimit(0)
```

A cancelled script's evaluation returns an error containing
`memory limit exceeded`, and `context.Cause` on its context is
`scriptling.ErrMemoryLimitExceeded`. The ceiling applies to the whole
process, so set it well above the host's own baseline heap, typically around
three quarters of the container's memory allocation; a ceiling below the
baseline cancels every script as soon as it starts.

`scriptling.GetMemoryLimitStats()` reports the configured limit, the heap at
the last sample, how many scripts are running and how many the guard has
cancelled since the process started. A cancellation count that keeps rising on
a host with a sensible ceiling means some script holds far more than it should,
and the limit is doing its job.

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
