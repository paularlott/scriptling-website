---
title: Go Integration
description: Embed Scriptling in your Go application.
tags: [go-integration, embedding]
weight: 3
stream: embedding
---

Complete guide for embedding Scriptling in Go applications.

## Choose by integration goal

- **Evaluate scripts and exchange values:** Start with [Basics](basics/).
- **Expose Go functions or classes quickly:** Use the type-safe [Builder API](builder/).
- **Control conversion and performance directly:** Use the [Native API](native/).
- **Control which modules scripts can import:** Read [Library Registration](library-registration/) and the [Library Loader Chain](loader-chain/).
- **Extend the host out of process:** See [Embedding Plugins](plugins/). If you want to run Scriptling itself as a server, use the [CLI server guides](/docs/cli/) instead.

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
    _, err := p.Eval(`x = 5 + 3`)
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

Focused examples on the pages below generally assume `p` has been initialized as shown here. Setup is repeated only when a registration or interpreter-lifecycle choice is part of the example.

## Topics

- [Basics](basics/) - Creating interpreters, variable exchange, calling functions
- [Native API](native/) - Direct object-level control
- [Native Functions](native-functions/) - Register individual Go functions
- [Native Classes](native-classes/) - Create custom classes with full control
- [Native Libraries](native-libraries/) - Create libraries with functions and constants
- [Builder API](builder/) - Type-safe, cleaner syntax
- [Builder Functions](builder-functions/) - Type-safe function builder
- [Builder Libraries](builder-libraries/) - Type-safe library builder
- [Builder Classes](builder-classes/) - Type-safe class builder
- [Builder Instantiation](builder-instantiation/) - Library templates with per-instance config
- [Script Extensions](scripts/) - Extend using Scriptling code
- [Embedding Plugins](plugins/) - Enable executable plugins in embedded applications
- [Library Loader Chain](loader-chain/) - Flexible library loading from multiple sources
- [Documenting Extensions](documentation/) - Add help text to functions and libraries
- [Library Registration](library-registration/) - Register built-in libraries when embedding
- [Linting](lint/) - Code analysis for detecting syntax errors without execution
- [GC Release Hooks](gc-release-hooks/) - Best-effort cleanup hooks for Go-owned objects

## Two Integration Approaches

### Native API

Direct object-level control with predictable overhead:

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

1. **Choose a lifecycle deliberately** - Reuse as-is only for one persistent script session; call `Reset()` between unrelated jobs or `Clone()` for isolated interpreters
2. **Load Only Needed Libraries** - Don't load JSON/HTTP if not needed
3. **Batch Operations** - Execute larger scripts rather than many small ones
4. **Pre-register Functions** - Register all Go functions before execution
5. **Measure Hot Paths** - Builder signatures are cached and common shapes use fast wrappers; compare Native and Builder APIs with your workload

```go
// Reuse registrations while clearing script globals between unrelated jobs.
p := scriptling.New()
stdlib.RegisterAll(p)
for _, source := range scripts {
    _, err := p.Eval(source)
    p.Reset()
    if err != nil {
        return err
    }
}
```

For a stateful session, omit `Reset()` so globals and imports persist. See [Interpreter lifecycle](basics/#interpreter-lifecycle) for `ResetEnv` and `Clone` choices.

## Choosing Your Approach

| Use Case | Recommended Approach |
|----------|---------------------|
| Simple functions | Builder API |
| Rapid development | Builder API |
| Performance-critical code | Native API |
| Complex type handling | Native API |
| Reusing Scriptling code | Script Extensions |
| Building on Go libraries | Script Extensions |
