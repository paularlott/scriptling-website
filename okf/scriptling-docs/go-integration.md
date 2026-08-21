---
description: Embed Scriptling in your Go application.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/
sources:
    - resource: https://scriptling.dev/docs/go-integration/
status: stable
tags:
    - go-integration
    - embedding
title: Go Integration
type: Guide
---
# Go Integration

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

- [Basics](go-integration/basics.md) - Creating interpreters, variable exchange, calling functions
- [Native API](go-integration/native.md) - Direct control with maximum performance
- [Native Functions](go-integration/native-functions.md) - Register individual Go functions
- [Native Classes](go-integration/native-classes.md) - Create custom classes with full control
- [Native Libraries](go-integration/native-libraries.md) - Create libraries with functions and constants
- [Builder API](go-integration/builder.md) - Type-safe, cleaner syntax
- [Builder Functions](go-integration/builder-functions.md) - Type-safe function builder
- [Builder Libraries](go-integration/builder-libraries.md) - Type-safe library builder
- [Builder Classes](go-integration/builder-classes.md) - Type-safe class builder
- [Builder Instantiation](go-integration/builder-instantiation.md) - Library templates with per-instance config
- [Script Extensions](go-integration/scripts.md) - Extend using Scriptling code
- [Plugins](go-integration/plugins.md) - Enable executable plugins in embedded applications
- [Library Loader Chain](go-integration/loader-chain.md) - Flexible library loading from multiple sources
- [Documenting Extensions](go-integration/documentation.md) - Add help text to functions and libraries
- [Linting](go-integration/lint.md) - Code analysis for detecting syntax errors without execution

## Two Integration Approaches

### Native API

Direct control with maximum performance:

```go
p.RegisterFunc("add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    a, _ := args[0].AsInt()
    b, _ := args[1].AsInt()
    return object.NewInteger(a + b)
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

## Choosing Your Approach

| Use Case | Recommended Approach |
|----------|---------------------|
| Simple functions | Builder API |
| Rapid development | Builder API |
| Performance-critical code | Native API |
| Complex type handling | Native API |
| Reusing Scriptling code | Script Extensions |
| Building on Go libraries | Script Extensions |
