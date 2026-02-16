---
title: Quick Start
description: Get up and running with Scriptling quickly.
weight: 1
---

Get up and running with Scriptling in minutes.

## Installation

### Homebrew (macOS & Linux)

```bash
brew install paularlott/tap/scriptling
```

### GitHub Releases

Download pre-built binaries from [GitHub Releases](https://github.com/paularlott/scriptling/releases):

- Linux (AMD64, ARM64)
- macOS (AMD64, ARM64)
- Windows (AMD64, ARM64)

### Go Module

For embedding in Go applications:

```bash
go get github.com/paularlott/scriptling
```

### Build from Source

```bash
# Clone the repository
git clone https://github.com/paularlott/scriptling.git
cd scriptling

# Install Task (build tool)
brew install go-task/tap/go-task

# Build CLI for current platform
task build

# Run scripts
./bin/scriptling script.py
```

## Basic Usage

### Hello World

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

### Variables and Functions

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

### Variable Exchange

```go
// Set variables from Go
p.SetVar("api_base", "https://api.example.com")
p.SetVar("timeout", 30)

// Execute script
p.Eval(`
response = requests.get(api_base + "/users", {"timeout": timeout})
data = json.loads(response["body"])
result = len(data)
`)

// Get variables back
count, _ := p.GetVarAsInt("result")
fmt.Printf("Found %d users\n", count)
```

## CLI Usage

### Run a Script

```bash
scriptling script.py
```

### Interactive Mode

```bash
scriptling --interactive
```

### Pipe Script

```bash
echo 'print("Hello")' | scriptling
```

### HTTP Server

```bash
scriptling --server :8000 script.py
```

### MCP Server

```bash
scriptling --server :8000 --mcp-tools ./tools script.py
```

## Next Steps

- [Language Guide](../language/) - Learn the complete language syntax
- [Libraries](../libraries/) - Explore available libraries
- [Go Integration](../go-integration/) - Deep dive into Go embedding
- [CLI Reference](../cli/) - CLI tool documentation
