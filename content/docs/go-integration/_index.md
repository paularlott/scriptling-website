---
title: Go Integration
description: Embed Scriptling in your Go application.
tags: [go-integration, embedding]
weight: 3
stream: embedding
---

Embed Scriptling in a Go application: create interpreters, choose which libraries scripts can import, and expose your own Go functions, classes, and libraries.

```bash
go get github.com/paularlott/scriptling
```

New to embedding? The [Go embedding quick start](/docs/quick-start/embedding/) runs a first script in a few lines; [Basics](basics/) then covers the full interpreter API. Focused examples on the pages below assume an initialized `p` as shown there.

## Reading Order

1. [Basics](basics/): create interpreters, exchange variables, call script functions, capture output, set resource limits.
2. [Library Registration](library-registration/): register standard and extended libraries, and set filesystem and [network policy](library-registration/#network-policy) before untrusted scripts run.
3. [Script Extensions](scripts/): extend the host with libraries written in Scriptling itself.
4. Extending in Go: pick an API (see below), then follow its pages.
   - **Native API**: [overview](native/), [functions](native-functions/), [classes](native-classes/), [libraries](native-libraries/).
   - **Builder API**: [overview](builder/), [functions](builder-functions/), [libraries](builder-libraries/), [classes](builder-classes/), [instantiation](builder-instantiation/) (one library template, per-environment config).
5. Further topics: [Library Loader Chain](loader-chain/), [Plugin Manager](/docs/plugins/host-integration/) (executable plugins in an embedded host), [Documenting Extensions](documentation/), [Checking Script Requirements](script-metadata/), [Linting](lint/), [GC Release Hooks](gc-release-hooks/).

To run Scriptling itself as a server instead of embedding it, use the [CLI server guides](/docs/cli/).

## Native vs Builder: Which to Use

The two APIs interoperate: `FunctionBuilder.Build()` returns an ordinary native function, and `LibraryBuilder`/`ClassBuilder` produce the same `*object.Library` and `*object.Class` values the Native API uses. Mix them freely, for example a builder library that exposes a native class, or a builder class inheriting from a native one.

| | Native API | Builder API |
|--|------------|-------------|
| You write | `func(ctx, kwargs, args ...object.Object) object.Object` | Ordinary Go funcs, e.g. `func(a, b int) int` |
| Argument checks and conversion | Manual (`AsInt`, `kwargs.GetString`, ...) | Automatic from the Go signature |
| Overhead | Direct object handling | Signature cached at build time; common shapes use fast wrappers, others fall back to `reflect.Call` |
| Best for | Measured hot paths; variable, optional, or mixed-type arguments | Most typed integrations |

Start with the Builder API for typical functions and libraries. Switch a function to the Native API when a benchmark of your real workload shows conversion cost matters, or when you need full control over arguments and return objects. Scriptling's own libraries use both.

```go
// Native
p.RegisterFunc("add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    a, _ := args[0].AsInt()
    b, _ := args[1].AsInt()
    return object.NewInteger(a + b)
})

// Builder
fb := object.NewFunctionBuilder()
fb.FunctionWithHelp(func(a, b int) int { return a + b }, "add(a, b) - Add two numbers")
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
