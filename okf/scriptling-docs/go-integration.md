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

## Choose by integration goal

- **Evaluate scripts and exchange values:** Start with [Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md).
- **Expose Go functions or classes quickly:** Use the type-safe [Builder API](https://scriptling.dev/okf/scriptling-docs/go-integration/builder.md).
- **Control conversion and performance directly:** Use the [Native API](https://scriptling.dev/okf/scriptling-docs/go-integration/native.md).
- **Control which modules scripts can import:** Read [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) and the [Library Loader Chain](https://scriptling.dev/okf/scriptling-docs/go-integration/loader-chain.md).
- **Run scripts that declare their requirements:** Check their [Script Metadata](https://scriptling.dev/okf/scriptling-docs/go-integration/script-metadata.md) blocks before executing them.
- **Extend the host out of process:** See [Embedding Plugins](https://scriptling.dev/okf/scriptling-docs/go-integration/plugins.md). If you want to run Scriptling itself as a server, use the [CLI server guides](https://scriptling.dev/okf/scriptling-docs/cli.md) instead.

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

- [Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md) - Creating interpreters, variable exchange, calling functions
- [Native API](https://scriptling.dev/okf/scriptling-docs/go-integration/native.md) - Direct object-level control
- [Native Functions](https://scriptling.dev/okf/scriptling-docs/go-integration/native-functions.md) - Register individual Go functions
- [Native Classes](https://scriptling.dev/okf/scriptling-docs/go-integration/native-classes.md) - Create custom classes with full control
- [Native Libraries](https://scriptling.dev/okf/scriptling-docs/go-integration/native-libraries.md) - Create libraries with functions and constants
- [Builder API](https://scriptling.dev/okf/scriptling-docs/go-integration/builder.md) - Type-safe, cleaner syntax
- [Builder Functions](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-functions.md) - Type-safe function builder
- [Builder Libraries](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-libraries.md) - Type-safe library builder
- [Builder Classes](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-classes.md) - Type-safe class builder
- [Builder Instantiation](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-instantiation.md) - Library templates with per-instance config
- [Script Extensions](https://scriptling.dev/okf/scriptling-docs/go-integration/scripts.md) - Extend using Scriptling code
- [Embedding Plugins](https://scriptling.dev/okf/scriptling-docs/go-integration/plugins.md) - Enable executable plugins in embedded applications
- [Library Loader Chain](https://scriptling.dev/okf/scriptling-docs/go-integration/loader-chain.md) - Flexible library loading from multiple sources
- [Checking Script Requirements](https://scriptling.dev/okf/scriptling-docs/go-integration/script-metadata.md) - Verify scripts' inline metadata blocks before running them
- [Documenting Extensions](https://scriptling.dev/okf/scriptling-docs/go-integration/documentation.md) - Add help text to functions and libraries
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - Register built-in libraries when embedding
- [Linting](https://scriptling.dev/okf/scriptling-docs/go-integration/lint.md) - Code analysis for detecting syntax errors without execution
- [GC Release Hooks](https://scriptling.dev/okf/scriptling-docs/go-integration/gc-release-hooks.md) - Best-effort cleanup hooks for Go-owned objects

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

For a stateful session, omit `Reset()` so globals and imports persist. See [Interpreter lifecycle](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#interpreter-lifecycle) for `ResetEnv` and `Clone` choices.

## Choosing Your Approach

| Use Case | Recommended Approach |
|----------|---------------------|
| Simple functions | Builder API |
| Rapid development | Builder API |
| Performance-critical code | Native API |
| Complex type handling | Native API |
| Reusing Scriptling code | Script Extensions |
| Building on Go libraries | Script Extensions |
