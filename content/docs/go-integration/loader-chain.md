---
title: Library Loader Chain
description: Flexible library loading from multiple sources.
weight: 5
---

The `libloader` package provides a flexible, chainable library loading system. Load libraries from the filesystem, APIs, or custom sources with Python-style folder organization.

## Overview

The loader chain pattern allows you to:
- Load libraries from multiple sources (filesystem, API, memory)
- Try sources in priority order
- Support Python-style folder structure for nested modules

## Basic Usage

### Filesystem Loader

Load libraries from a directory with Python-style folder support:

```go
import (
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/libloader"
)

func main() {
    p := scriptling.New()

    // Load from filesystem
    loader := libloader.NewFilesystem("/app/libs")
    p.SetLibraryLoader(loader)

    // Now scripts can import
    p.Eval(`
import utils           # Loads from /app/libs/utils.py
import knot.groups     # Loads from /app/libs/knot/groups.py
`)
}
```

### Folder Structure

The filesystem loader follows Python's module organization:

```
libs/
  json.py              # import json
  utils.py             # import utils
  knot/
    __init__.py        # (optional) package initialization
    groups.py          # import knot.groups
    roles.py           # import knot.roles
    users.py           # import knot.users
    api/
      v1.py            # import knot.api.v1
      v2.py            # import knot.api.v2
```

**Loading Priority:**

For `import knot.groups`, the loader checks:
1. `libs/knot/groups.py` (folder structure - preferred)
2. `libs/knot.groups.py` (flat file - legacy fallback)

## Loader Chain

Chain multiple loaders to try different sources in order:

```go
// Try filesystem first, then API
chain := libloader.NewChain(
    libloader.NewFilesystem("/app/libs"),
    libloader.NewAPI("https://api.example.com/libs"),
)
p.SetLibraryLoader(chain)
```

When a script imports a library:
1. First loader tries to find it
2. If not found, next loader tries
3. Continues until a loader finds it or all loaders are exhausted

### Multiple Filesystem Directories

Search multiple directories with priority:

```go
// User libs override system libs
loader := libloader.NewMultiFilesystem(
    "/home/user/libs",   // Highest priority
    "/app/system/libs",  // Fallback
)
p.SetLibraryLoader(loader)
```

## Built-in Loaders

### FilesystemLoader

Loads libraries from the filesystem with folder support.

```go
loader := libloader.NewFilesystem("/app/libs")

// With options
loader := libloader.NewFilesystem("/app/libs",
    libloader.WithExtension(".scriptling"),  // Custom extension
    libloader.WithFollowLinks(false),         // Don't follow symlinks
    libloader.WithDescription("user libs"),   // Custom description
)
```

### MemoryLoader

Load libraries from an in-memory map (useful for testing):

```go
loader := libloader.NewMemoryLoader(map[string]string{
    "testlib": `def hello(): return "Hello"`,
    "math.extra": `PI = 3.14159`,
})
p.SetLibraryLoader(loader)
```

### FuncLoader

Create a loader from a simple function:

```go
loader := libloader.NewFuncLoader(func(name string) (string, bool, error) {
    // Custom loading logic
    if name == "special" {
        return `def func(): pass`, true, nil
    }
    return "", false, nil
}, "custom loader")
```

## Custom Loaders

Implement the `LibraryLoader` interface for custom sources:

```go
type LibraryLoader interface {
    Load(name string) (source string, found bool, err error)
    Description() string
}
```

### Example: API Loader

```go
type APILoader struct {
    baseURL string
}

func (l *APILoader) Load(name string) (string, bool, error) {
    resp, err := http.Get(l.baseURL + "/" + name + ".py")
    if err != nil {
        return "", false, err
    }
    defer resp.Body.Close()

    if resp.StatusCode == 404 {
        return "", false, nil
    }

    content, err := io.ReadAll(resp.Body)
    if err != nil {
        return "", false, err
    }

    return string(content), true, nil
}

func (l *APILoader) Description() string {
    return "api:" + l.baseURL
}
```

### Using Custom Loader

```go
apiLoader := &APILoader{baseURL: "https://api.example.com/libs"}

chain := libloader.NewChain(
    libloader.NewFilesystem("/app/libs"),  // Local first
    apiLoader,                             // Remote fallback
)
p.SetLibraryLoader(chain)
```

## Combining with Go Libraries

The loader chain works alongside registered Go libraries:

```go
p := scriptling.New()

// Register Go libraries (checked first)
p.RegisterLibrary(object.NewLibrary("json", jsonFunctions, nil, "JSON library"))

// Set up loader for script libraries
loader := libloader.NewFilesystem("/app/libs")
p.SetLibraryLoader(loader)

// Import order:
// 1. Check registered Go libraries
// 2. Check registered script libraries
// 3. Try library loader chain
p.Eval(`
import json          # Uses Go library
import knot.groups   # Uses loader chain
`)
```

## Best Practices

1. **Order matters**: Put faster/local loaders before slower/remote ones
2. **Use folder structure**: Organize related modules in folders like Python
3. **Handle errors**: Log loader errors for debugging
4. **Test with MemoryLoader**: Use in-memory loader for unit tests

## See Also

- [Script Libraries](scripts/) - Write libraries in Scriptling
- [Native Libraries](native/libraries/) - Create Go libraries
- [CLI Library Loading](../cli/) - Using --libdir flag
