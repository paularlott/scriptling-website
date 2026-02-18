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

## Quick Start

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

## Topics

- [Basics](basics/) - Creating interpreters, variable exchange, calling functions
- [Go Functions](functions/) - Registering Go functions callable from Scriptling
- [Go Libraries](libraries/) - Creating Go libraries with functions and constants
- [Go Classes](classes/) - Creating Go classes for object-oriented integration
- [Builder API](builder/) - Type-safe builder pattern for performance
- [Linting](lint/) - Code analysis for detecting syntax errors without execution

## Two Integration Approaches

### Native API

Direct control with maximum performance:

```go
p.RegisterFunc("add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    a, _ := args[0].AsInt()
    b, _ := args[1].AsInt()
    return &object.Integer{Value: a + b}
})
```

### Builder API

Type-safe, cleaner syntax with automatic conversion:

```go
fb := object.NewFunctionBuilder()
fb.FunctionWithHelp(func(a, b int) int {
    return a + b
}, "add(a, b) - Add two numbers")
p.RegisterFunc("add", fb.Build())
```

## Performance Tips

1. **Reuse Interpreters** - Create once, use multiple times
2. **Load Only Needed Libraries** - Don't load JSON/HTTP if not needed
3. **Batch Operations** - Execute larger scripts rather than many small ones
4. **Pre-register Functions** - Register all Go functions before execution
5. **Use Native API for Hot Paths** - Avoid reflection overhead in tight loops

```go
// Good: Reuse interpreter
p := scriptling.New()
for _, script := range scripts {
    p.Eval(script)
}
```
