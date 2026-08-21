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

Get up and running with Scriptling as an embedded scripting language in your Go application.

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
    result, err := p.Eval(`
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

Pass data between Go and Scriptling:

```go
// Set variables from Go
p.SetVar("api_base", "https://api.example.com")
p.SetVar("timeout", 30)

// Execute script
p.Eval(`
response = requests.get(api_base + "/users", {"timeout": timeout})
data = json.loads(response.body)
result = len(data)
`)

// Get variables back
count, _ := p.GetVarAsInt("result")
fmt.Printf("Found %d users\n", count)
```

## Registering Libraries

Libraries are not available to scripts unless you register them. Register all standard libraries with a single call:

```go
import "github.com/paularlott/scriptling/stdlib"

// Register all standard libraries (json, math, re, time, etc.)
stdlib.RegisterAll(p)
```

Extended and `scriptling.*` libraries are registered individually. See [Library Registration](../go-integration/library-registration.md) for the complete list and signatures.

## Next Steps

- [Go Integration Basics](../go-integration/basics.md) - Complete guide to interpreters, variables, and functions
- [Native API](../go-integration/native.md) - Direct control with maximum performance
- [Builder API](../go-integration/builder.md) - Type-safe, cleaner syntax
- [Libraries](../../scriptling-libraries/scriptling-libraries.md) - Library usage and registration reference
- [Security Guide](../security.md) - Security best practices for embedding
