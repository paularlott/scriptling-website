---
title: Library Instantiation
description: Create library templates with instance-specific configuration.
weight: 4
---

When you need the same library with different configurations across multiple environments (e.g., different allowed paths, API keys, rate limits), use library instantiation.

## Overview

The pattern is:

1. Build a library template once using `LibraryBuilder`
2. Instantiate it multiple times with different configs
3. Functions access config via `object.InstanceDataFromContext(ctx)`

**Key benefit**: Thread-safe - each instance maintains its own config without shared state.

## Simple Libraries (Functions Only)

### Step 1: Define Config Type

```go
type MyConfig struct {
    AllowedPaths []string
    APIKey       string
}
```

### Step 2: Build Template with LibraryBuilder

```go
import (
    "context"
    "github.com/paularlott/scriptling/object"
)

builder := object.NewLibraryBuilder("mylib", "My library with instance config")

builder.Function("do_something", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Retrieve config from context
    config := object.InstanceDataFromContext(ctx).(MyConfig)

    // Use config
    if !isPathAllowed(config.AllowedPaths, path) {
        return &object.Error{Message: "access denied"}
    }

    return &object.String{Value: "success"}
})

template := builder.Build()
```

### Step 3: Instantiate and Register

```go
// Environment 1 - restricted
config1 := MyConfig{
    AllowedPaths: []string{"/tmp"},
    APIKey:       "key1",
}
lib1 := template.Instantiate(config1)

// Environment 2 - broader access
config2 := MyConfig{
    AllowedPaths: []string{"/tmp", "/home/user"},
    APIKey:       "key2",
}
lib2 := template.Instantiate(config2)

// Register to different interpreters
interpreter1.RegisterLibrary(lib1)
interpreter2.RegisterLibrary(lib2)
```

## Libraries with Classes (Native Pattern)

When your library provides classes using the Native API:

1. Build template with constructor function
2. Constructor retrieves config from context
3. Constructor stores config in instance fields
4. Class methods retrieve config from instance

### Step 1: Define Config and Class

```go
type FSConfig struct {
    AllowedPaths []string
}

// Define class with Native API
var PathClass = &object.Class{
    Name: "Path",
    Methods: map[string]object.Object{
        "exists": &object.Builtin{
            Fn:       pathExists,
            HelpText: "exists() - Check if path exists",
        },
        "joinpath": &object.Builtin{
            Fn:       pathJoinpath,
            HelpText: "joinpath(*other) - Combine path segments",
        },
    },
}
```

### Step 2: Build Library with Constructor

```go
builder := object.NewLibraryBuilder("pathlib", "Filesystem paths with security")

// Constructor function that creates Path instances
builder.Function("Path", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Retrieve config from context (injected by Instantiate)
    config := object.InstanceDataFromContext(ctx).(FSConfig)

    // Call helper to create instance
    return createPath(config, ctx, kwargs, args...)
})

template := builder.Build()
```

### Step 3: Implement Constructor Helper

```go
func createPath(config FSConfig, ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) < 1 {
        return &object.Error{Message: "Path() requires a path argument"}
    }

    pathStr, err := args[0].AsString()
    if err != nil {
        return err
    }

    // Validate against config
    if !config.IsPathAllowed(pathStr) {
        return &object.Error{Message: "access denied"}
    }

    // Create instance
    instance := &object.Instance{
        Class:  PathClass,
        Fields: make(map[string]object.Object),
    }

    // Store config in instance for methods to access
    instance.Fields["__config__"] = config
    instance.Fields["__path__"] = &object.String{Value: pathStr}

    return instance
}
```

### Step 4: Implement Class Methods

Methods retrieve config from `self.Fields["__config__"]`:

```go
func pathExists(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    self := args[0].(*object.Instance)

    // Retrieve config from instance
    config := self.Fields["__config__"].(FSConfig)
    pathStr := self.Fields["__path__"].(*object.String).Value

    // Validate access
    if !config.IsPathAllowed(pathStr) {
        return &object.Error{Message: "access denied"}
    }

    // Check if path exists
    _, err := os.Stat(pathStr)
    return &object.Boolean{Value: err == nil}
}

func pathJoinpath(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    self := args[0].(*object.Instance)
    config := self.Fields["__config__"].(FSConfig)
    basePath := self.Fields["__path__"].(*object.String).Value

    // Join path segments
    segments := []string{basePath}
    for _, arg := range args[1:] {
        seg, err := arg.AsString()
        if err != nil {
            return err
        }
        segments = append(segments, seg)
    }

    newPath := filepath.Join(segments...)

    // Create new Path instance with same config
    return createPath(config, ctx, kwargs, []object.Object{&object.String{Value: newPath}})
}
```

## Libraries with Classes (Builder Pattern)

Alternatively, use ClassBuilder for type-safe class creation:

```go
classBuilder := object.NewClassBuilder("Path")
classBuilder.Method("exists", func(self *object.Instance) bool {
    config := self.Fields["__config__"].(FSConfig)
    pathStr := self.Fields["__path__"].(*object.String).Value

    if !config.IsPathAllowed(pathStr) {
        panic("access denied")
    }

    _, err := os.Stat(pathStr)
    return err == nil
})

PathClass := classBuilder.Build()
```

The rest of the pattern (library builder, constructor, instantiation) remains the same.

## Data Flow Summary

### For Functions:

```
User calls function
    ↓
Wrapped function injects config into context
    ↓
Original function retrieves config via InstanceDataFromContext(ctx)
    ↓
Function uses config
```

### For Classes:

```
User calls constructor (e.g., pathlib.Path("/tmp"))
    ↓
Wrapped constructor injects config into context
    ↓
Constructor retrieves config via InstanceDataFromContext(ctx)
    ↓
Constructor stores config in instance.Fields["__config__"]
    ↓
User calls method (e.g., p.exists())
    ↓
Method retrieves config from self.Fields["__config__"]
    ↓
Method uses config
```

## Complete Example

```go
package main

import (
    "context"
    "os"
    "path/filepath"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

type FSConfig struct {
    AllowedPaths []string
}

func (c FSConfig) IsPathAllowed(path string) bool {
    for _, allowed := range c.AllowedPaths {
        if filepath.IsAbs(path) && len(path) >= len(allowed) && path[:len(allowed)] == allowed {
            return true
        }
    }
    return false
}

var PathClass = &object.Class{
    Name: "Path",
    Methods: map[string]object.Object{
        "exists": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                self := args[0].(*object.Instance)
                config := self.Fields["__config__"].(FSConfig)
                pathStr := self.Fields["__path__"].(*object.String).Value

                if !config.IsPathAllowed(pathStr) {
                    return &object.Error{Message: "access denied"}
                }

                _, err := os.Stat(pathStr)
                return &object.Boolean{Value: err == nil}
            },
            HelpText: "exists() - Check if path exists",
        },
    },
}

func createPath(config FSConfig, ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) < 1 {
        return &object.Error{Message: "Path() requires a path argument"}
    }

    pathStr, err := args[0].AsString()
    if err != nil {
        return err
    }

    if !config.IsPathAllowed(pathStr) {
        return &object.Error{Message: "access denied"}
    }

    instance := &object.Instance{
        Class:  PathClass,
        Fields: make(map[string]object.Object),
    }
    instance.Fields["__config__"] = config
    instance.Fields["__path__"] = &object.String{Value: pathStr}

    return instance
}

func createPathlibLibrary() *object.Library {
    builder := object.NewLibraryBuilder("pathlib", "Filesystem paths with security")

    builder.Function("Path", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        config := object.InstanceDataFromContext(ctx).(FSConfig)
        return createPath(config, ctx, kwargs, args...)
    })

    return builder.Build()
}

func main() {
    // Create template
    template := createPathlibLibrary()

    // Instantiate with different configs
    config1 := FSConfig{AllowedPaths: []string{"/tmp"}}
    config2 := FSConfig{AllowedPaths: []string{"/tmp", "/home/user"}}

    lib1 := template.Instantiate(config1)
    lib2 := template.Instantiate(config2)

    // Register to different interpreters
    p1 := scriptling.New()
    p1.RegisterLibrary(lib1)

    p2 := scriptling.New()
    p2.RegisterLibrary(lib2)

    // Use in scripts
    p1.Eval(`
import pathlib
p = pathlib.Path("/tmp/file.txt")
if p.exists():
    print("File exists")
`)
}
```

## Thread Safety

The implementation is thread-safe:

- Instance data is injected into context per-call
- No shared mutable state between instances
- Each interpreter can run in its own goroutine
- Functions can be called concurrently without data crossover

```go
// Safe to run concurrently
go func() {
    interpreter1.Eval("mylib.do_something()")
}()

go func() {
    interpreter2.Eval("mylib.do_something()")
}()
```

## Best Practices

### Type-Safe Config Retrieval

```go
func getConfig(ctx context.Context) (MyConfig, error) {
    data := object.InstanceDataFromContext(ctx)
    if data == nil {
        return MyConfig{}, fmt.Errorf("no instance data")
    }
    config, ok := data.(MyConfig)
    if !ok {
        return MyConfig{}, fmt.Errorf("invalid config type")
    }
    return config, nil
}
```

### Consistent Field Names

- `__config__` - for instance configuration
- `__data__` - for instance data
- Regular names for user-visible fields

### Validate in Constructor

```go
func createPath(config FSConfig, ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Validate config
    if len(config.AllowedPaths) == 0 {
        return &object.Error{Message: "no allowed paths configured"}
    }

    // Validate arguments
    if len(args) < 1 {
        return &object.Error{Message: "Path() requires a path argument"}
    }

    // Validate path against config
    pathStr, err := args[0].AsString()
    if err != nil {
        return err
    }

    if !config.IsPathAllowed(pathStr) {
        return &object.Error{Message: "access denied"}
    }

    // Create instance...
}
```

### Methods Creating New Instances

When a method needs to create a new instance of the same class, retrieve config from `self` and pass to constructor:

```go
func pathJoinpath(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    self := args[0].(*object.Instance)
    config := self.Fields["__config__"].(FSConfig)

    // ... compute newPath ...

    // Create new instance with same config
    return createPath(config, ctx, kwargs, []object.Object{&object.String{Value: newPath}})
}
```

## Quick Reference

```go
// 1. Build template
builder := object.NewLibraryBuilder("mylib", "Description")
builder.Function("func", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    config := object.InstanceDataFromContext(ctx).(MyConfig)
    // Use config...
})
template := builder.Build()

// 2. Instantiate
lib := template.Instantiate(MyConfig{...})

// 3. Register
interpreter.RegisterLibrary(lib)

// 4. Use
interpreter.Import("mylib")
interpreter.Eval("mylib.func()")
```

For classes, add constructor that stores config in instance fields, and methods retrieve from `self.Fields["__config__"]`.

## See Also

- [Builder Libraries](libraries/) - Basic library building
- [Native Classes](../native/classes/) - Native class creation
- [Builder Classes](classes/) - Builder class creation
