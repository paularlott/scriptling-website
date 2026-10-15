---
title: Basics
description: Creating interpreters, variable exchange, and calling functions.
tags: [go-integration, embedding, go]
weight: 1
---

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

A host that runs scripts written by other people needs limits that a timeout
alone does not give it: how far a script can fan out, how much memory it can
hold and how large a single value can grow. Bound running time with the
context passed to `EvalWithContext` and the other `*WithContext` calls (see
[With Context and Timeout](#with-context-and-timeout)).

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

### Per-Interpreter Limits

Every interpreter has two limits. Each follows a process-wide default
unless the interpreter sets its own. Nothing is limited until a limit is set:
every default is off.

| Limit | Default | What happens when it is reached |
| --- | --- | --- |
| Memory: estimated memory the interpreter holds | none | Garbage is collected; if still over, the interpreter's running calls are cancelled with `memory limit exceeded` |
| Value: largest single string, bytes value, list, tuple, dict or set | none | The operation raises `MemoryError`, which the script can catch |

Set the defaults once at startup. They apply to each interpreter separately,
never to the process as a whole:

```go
scriptling.SetMemoryLimit(64 << 20)   // 64 MiB per interpreter
scriptling.SetMaxValueBytes(8 << 20)  // 8 MiB per value
```

An interpreter can set its own limits when it is created, or later. `0` means
no limit for that interpreter whatever the default, and
`scriptling.InheritLimit` returns it to the default:

```go
p := scriptling.New(
    scriptling.WithMemoryLimit(256 << 20),
    scriptling.WithMaxValueBytes(0), // no value limit for this one
)

p.SetMemoryLimit(scriptling.InheritLimit) // back to the default
```

An interpreter without its own limit follows the default as it changes, so
raising the default later raises it for every interpreter that inherits it.
Change limits between calls: a change is enforced from the next call. When a
memory limit is lowered below what the interpreter already holds, the next
call collects garbage and, if it is still over, stops before it runs.
`p.Clone()` keeps the parent's limit settings, with its own memory accounting.

### Memory Limit

Go cannot attribute heap memory to an interpreter, so memory is estimated.
The points where a script can make memory grow (strings, bytes, list storage,
dicts, sets and object attributes) report their sizes. One allocation in
roughly every 64 KiB is sampled at random, as Go's heap profiler does, and
charged to the interpreter running on that goroutine; the charge is credited
back when the object is collected. Allocations of 64 KiB or more are charged
exactly. The estimate is unbiased, but it is an estimate: integers and floats
are not counted on their own, only through the lists and dicts that hold them.

When the estimate goes over the limit, the interpreter forces a garbage
collection, because much of what was charged may already be garbage. Only if
it is still over are its running calls cancelled. A script that allocates far
more than its limit in total, but holds little at once, is not stopped.

Large values are checked before they are made: a string repetition, padding,
join, read body and so on that would not fit in the room left raises
`MemoryError` instead of allocating.

A cancelled call returns an error containing `memory limit exceeded`. Go
builtins and libraries running inside the call see
`context.Cause(ctx) == scriptling.ErrMemoryLimitExceeded` on the context
they are given; the context the host passed in is not cancelled. The
interpreter can be used again afterwards.

`p.ResourceUsage()` reports the interpreter's estimated memory in use, its
peak, the total allocated and how many calls the limit has cancelled:

```go
usage := p.ResourceUsage()
fmt.Println(usage.MemoryBytes, usage.PeakMemoryBytes, usage.AllocatedBytes, usage.MemoryLimitCancellations)
```

Memory is only measured while accounting is on, which it is once any memory
limit has been set in the process. From then on each string and bytes value
created costs a few nanoseconds more; with no memory limit set anywhere the
cost is one atomic load. A value limit is similar: once one has been set
anywhere, values larger than the smallest limit ever set take the checking
path for the rest of the process, in every interpreter.

Sandboxes (`scriptling.runtime.sandbox`) and background tasks
(`runtime.background`) share the guard of the script that started them: the
same memory and value limits, and their memory counts against the same
budget. A script cannot get round its limits by running code in them. If the
shared budget is exceeded, every call running under it is cancelled. A
background task is not part of the call that started it, though: it keeps
running after that call returns, still charged to the same budget.

A host can do the same for its own nested interpreters, such as a builtin that
runs a second `Scriptling`:

```go
child := scriptling.New()
child.ShareResourceGuard(parent.ResourceGuard())
```

Without that, a nested interpreter has its own limits and budget, and memory
it allocates is charged to it rather than to the interpreter that called it.

### Value Limit

The value limit stops a single operation asking for a huge allocation:
`"x" * n`, `"x".center(n)`, `f"{x:>{n}}"`, `bytes(n)`, `str.join`,
`str.replace`, `str.split`, `list(range(n))`, list, dict and set growth,
literals (checked before their elements are evaluated), `*args`,
`secrets.token_bytes(n)`, HTTP response bodies, file and archive reads,
`sys.stdin.read()`, `io.StringIO` buffers, rendered templates and captured
`print` output. The results of library functions and string and bytes methods
(`base64.b64encode`, `json.dumps` and so on) are also checked as they are
returned, and script data handed to `json.dumps`, templates and request
bodies is converted under the limit, since a value shared by many containers
converts once per reference. Lists, tuples, dicts and sets count 16 bytes per element. Going over
raises `MemoryError`:

```python
try:
    data = "x" * n
except MemoryError as e:
    print("too big:", e)
```

With only a memory limit set, reads, captured output, `StringIO` buffers and
rendered templates are still refused once they no longer fit in the memory
left. Libraries whose results come from files or directories rather than
script values, such as `scriptling.grep`, `scriptling.sed`, `scriptling.find`,
`os.listdir` and `csv.loads`, build their results under the limits as they
go: a call whose result would not fit stops with `MemoryError` rather than
gathering everything first.

Constant expressions folded when the script is parsed, such as `"ab" * 3`,
are checked against the value limit when they are evaluated, like the same
expression with a variable. Whatever the value limit, a
string or bytes repetition (`"x" * n`), padding width (`"x".ljust(n)`) or
format width (`"%*d"`) is still capped at 1 GiB and a list or tuple
repetition at about 134 million elements, as before limits existed. Libraries that read data of
unknown size can use `object.ReadAllLimited` and `object.ReadFileLimited`,
and check a size up front with `object.CheckAlloc`.

## Library Management

### Register Libraries

Libraries are not available to scripts unless you register them. Register all standard libraries with a single call:

```go
import "github.com/paularlott/scriptling/stdlib"

stdlib.RegisterAll(p)
```

Extended and `scriptling.*` libraries are registered individually, and filesystem libraries take an `allowedPaths` argument for access control. See [Library Registration](../library-registration/) for the complete list of libraries and their registration functions.

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

See [Library Loader Chain](../loader-chain/) for full documentation.

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

- [Library Registration](../library-registration/) - How to register built-in libraries
- [Native API](../native/) - Direct object-level control
- [Builder API](../builder/) - Type-safe, cleaner syntax
- [Security Guide](../../security/) - Security best practices for embedding
- [Libraries](../../../reference/libraries/) - Usage reference for all libraries
