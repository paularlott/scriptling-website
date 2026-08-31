---
description: Embed Scriptling in a Go application.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/quick-start/embedding/
sources:
    - resource: https://scriptling.dev/docs/quick-start/embedding/
status: stable
tags:
    - quick-start
    - embedding
    - go
title: Embedding
type: Guide
---
# Embedding

Get up and running with Scriptling as an embedded scripting language in your Go application. Later fragments assume an initialized `p`; the complete examples show setup when registration or lifecycle is the topic.

## Installation

```bash
go get github.com/paularlott/scriptling
```

## Hello World

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
    _, err := p.Eval(`
print("Hello, World!")
`)
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

## Variables and Functions

```go
p := scriptling.New()
stdlib.RegisterAll(p)

result, err := p.Eval(`
# Variables
x = 42
name = "Alice"
numbers = [1, 2, 3]

# Functions
def greet(n):
    return "Hello " + n

# Output
print(greet(name))
print("Sum:", x + len(numbers))
`)
```

## Variable Exchange

Pass data between Go and Scriptling. This complete example registers the extended `requests` library separately from the standard libraries:

```go
package main

import (
    "fmt"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/extlibs"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)
    extlibs.RegisterRequestsLibrary(p)

    if err := p.SetVar("api_base", "https://jsonplaceholder.typicode.com"); err != nil {
        fmt.Println("Set variable:", err)
        return
    }
    if err := p.SetVar("timeout", 10); err != nil {
        fmt.Println("Set variable:", err)
        return
    }

    _, err := p.Eval(`
import json
import requests

response = requests.get(api_base + "/users", timeout=timeout)
response.raise_for_status()
data = json.loads(response.text)
result = len(data)
`)
    if err != nil {
        fmt.Println("Script error:", err)
        return
    }

    count, getErr := p.GetVarAsInt("result")
    if getErr != nil {
        fmt.Println("Result error:", getErr.Inspect())
        return
    }
    fmt.Printf("Found %d users\n", count)
}
```

This registers unrestricted outbound HTTP access. For untrusted scripts, pass a `netsecurity.Config` to `RegisterRequestsLibrary` and restrict the destinations scripts may contact; see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#network-policy).

## Registering Libraries

Libraries are not available to scripts unless you register them. Register all standard libraries with a single call:

```go
import "github.com/paularlott/scriptling/stdlib"

// Register all standard libraries (json, math, re, time, etc.)
stdlib.RegisterAll(p)
```

Extended and `scriptling.*` libraries are registered individually. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for the complete list and signatures.

## Next Steps

- [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md) - Complete guide to interpreters, variables, and functions
- [Native API](https://scriptling.dev/okf/scriptling-docs/go-integration/native.md) - Direct object-level control
- [Builder API](https://scriptling.dev/okf/scriptling-docs/go-integration/builder.md) - Type-safe, cleaner syntax
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Library usage and registration reference
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security best practices for embedding
