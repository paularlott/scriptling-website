---
title: Embedding
description: Embed Scriptling in a Go application.
weight: 2
stream: embedding
---

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

Extended and `scriptling.*` libraries are registered individually. See [Library Registration](../go-integration/library-registration/) for the complete list and signatures.

## Next Steps

- [Go Integration Basics](../basics/) - Complete guide to interpreters, variables, and functions
- [Native API](../native/) - Direct control with maximum performance
- [Builder API](../builder/) - Type-safe, cleaner syntax
- [Libraries](../../../reference/libraries/) - Library usage and registration reference
- [Security Guide](../../security/) - Security best practices for embedding
