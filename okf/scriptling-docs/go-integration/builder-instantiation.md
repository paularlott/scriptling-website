---
description: Create library templates with instance-specific configuration.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/builder-instantiation/
sources:
    - resource: https://scriptling.dev/docs/go-integration/builder-instantiation/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: Builder Instantiation
type: Guide
---
# Builder Instantiation

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

    return object.NewString("success")
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
type pathData struct {
    config FSConfig
    path   string
}

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

    // Create instance. Script-visible properties use SetField;
    // internal Go-only state goes in NativeData.
    return object.NewInstanceWithData(PathClass, nil, &pathData{
        config: config,
        path:   pathStr,
    })
}
```

### Step 4: Implement Class Methods

Methods retrieve internal state from `self.NativeData`:

```go
func pathExists(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    self := args[0].(*object.Instance)

    // Retrieve Go-only state from instance
    data, ok := self.NativeData.(*pathData)
    if !ok {
        return errors.NewError("invalid Path instance")
    }
    config := data.config
    pathStr := data.path

    // Validate access
    if !config.IsPathAllowed(pathStr) {
        return &object.Error{Message: "access denied"}
    }

    // Check if path exists
    _, err := os.Stat(pathStr)
    return object.NewBoolean(err == nil)
}

func pathJoinpath(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    self := args[0].(*object.Instance)
    data, ok := self.NativeData.(*pathData)
    if !ok {
        return errors.NewError("invalid Path instance")
    }
    config := data.config
    basePath := data.path

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
    return createPath(config, ctx, kwargs, []object.Object{object.NewString(newPath)})
}
```

## Libraries with Classes (Builder Pattern)

Alternatively, use ClassBuilder for type-safe class creation. For Go struct-backed classes, use `Constructor` with a typed receiver:

```go
classBuilder := object.NewClassBuilder("Path")
classBuilder.Constructor(func(config FSConfig, pathStr string) (*pathData, error) {
    if !config.IsPathAllowed(pathStr) {
        return nil, fmt.Errorf("access denied")
    }
    return &pathData{config: config, path: pathStr}, nil
})
classBuilder.Method("exists", func(self *pathData) bool {
    _, err := os.Stat(self.path)
    return err == nil
})

PathClass := classBuilder.Build()
```

For simpler cases without instantiation, use the manual pattern:

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
Constructor stores config in instance.NativeData
    ↓
User calls method (e.g., p.exists())
    ↓
Method retrieves config from self.NativeData
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
                data, ok := self.NativeData.(*pathData)
                if !ok {
                    return &object.Error{Message: "invalid Path instance"}
                }

                if !data.config.IsPathAllowed(data.path) {
                    return &object.Error{Message: "access denied"}
                }

                _, err := os.Stat(data.path)
                return object.NewBoolean(err == nil)
            },
            HelpText: "exists() - Check if path exists",
        },
    },
}

type pathData struct {
    config FSConfig
    path   string
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

    return object.NewInstanceWithData(PathClass, nil, &pathData{
        config: config,
        path:   pathStr,
    })
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

Each environment carries a per-environment interpreter lock (GIL) that serializes script execution, so a single environment is safe to call from many goroutines. Independent environments have independent locks and run fully in parallel. Use one environment per goroutine for isolation, or share one environment across goroutines for shared state.

- Instance data is injected into context per-call
- No shared mutable state between instances
- Functions can be called concurrently without data crossover

```go
// Safe to run concurrently: separate environments (parallel, isolated)...
go func() {
    interpreter1.Eval("mylib.do_something()")
}()

go func() {
    interpreter2.Eval("mylib.do_something()")
}()

// ...or a single shared environment (serialized by the GIL).
go func() { shared.Eval("mylib.do_something())" }()
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

### Store Go-Only State in NativeData

Keep Go-only state (config, parsed paths, handles) on `instance.NativeData` rather than as script-visible fields. Regular names are for fields the script can read and write.

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
    data, ok := self.NativeData.(*pathData)
    if !ok {
        return &object.Error{Message: "invalid Path instance"}
    }
    config := data.config

    // ... compute newPath ...

    // Create new instance with same config
    return createPath(config, ctx, kwargs, []object.Object{object.NewString(newPath)})
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

For classes, add a constructor that stores config on `instance.NativeData`, and methods retrieve it via `self.NativeData.(*yourType)`.

## See Also

- [Builder Libraries](builder-libraries.md) - Basic library building
- [Native Classes](native-classes.md) - Native class creation
- [Builder Classes](builder-classes.md) - Builder class creation
