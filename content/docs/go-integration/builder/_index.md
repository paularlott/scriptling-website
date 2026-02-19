---
title: Builder API
description: Type-safe builder pattern for functions, classes, and libraries.
weight: 3
---

The Builder API provides a type-safe, clean way to create functions, classes, and libraries with automatic type conversion.

## Why Use Builders?

| Feature | Native API | Builder API |
|---------|------------|-------------|
| Type safety | Manual checking | Automatic |
| Code clarity | Verbose | Clean |
| Error handling | Manual | Automatic |
| Performance | Maximum | Slight overhead at registration |

Use the **Builder API** for cleaner code and type safety. Use the **Native API** only for performance-critical code.

## Topics

- [Functions](functions/) - Type-safe function builder
- [Libraries](libraries/) - Type-safe library builder
- [Classes](classes/) - Type-safe class builder
- [Instantiation](instantiation/) - Library templates with per-instance configuration

## Supported Types

The Builder API automatically converts between Go types and Scriptling objects:

| Go Type | Scriptling Type | Notes |
|---------|-----------------|-------|
| `string` | `STRING` | Direct conversion |
| `int`, `int32`, `int64` | `INTEGER` | Accepts both Integer and Float |
| `float32`, `float64` | `FLOAT` | Accepts both Integer and Float |
| `bool` | `BOOLEAN` | Direct conversion |
| `[]any` | `LIST` | Converts to/from Scriptling lists |
| `map[string]any` | `DICT` | Converts to/from Scriptling dicts |
| `nil` | `None` | Null value |

## Quick Example

```go
import "github.com/paularlott/scriptling/object"

func main() {
    p := scriptling.New()

    // Builder API: Clean, type-safe
    fb := object.NewFunctionBuilder()
    fb.FunctionWithHelp(func(a, b int) int {
        return a + b
    }, "add(a, b) - Add two numbers together")
    p.RegisterFunc("add", fb.Build())

    p.Eval(`result = add(10, 20)`)  // result = 30
}
```

## Performance Considerations

### When to Use Each API

```go
// Use Builder API for:
// - Most functions and libraries
// - Cleaner, maintainable code
// - Automatic type conversion

fb := object.NewFunctionBuilder()
fb.Function(func(a, b int) int { return a + b })
p.RegisterFunc("add", fb.Build())

// Use Native API for:
// - Performance-critical code
// - Tight loops called thousands of times
// - Complex type handling

p.RegisterFunc("fast_add", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    a, _ := args[0].AsInt()  // Direct, no reflection
    b, _ := args[1].AsInt()
    return object.NewInteger(a + b)
})
```

### Optimization Tips

1. **Register once** - Builders have overhead at registration, not execution
2. **Pre-build classes** - Create class instances before scripts run
3. **Cache built objects** - Reuse built libraries across interpreters

```go
// Pre-build library once
var cachedLibrary *object.Library

func init() {
    cachedLibrary = createMyLibrary()
}

func main() {
    p := scriptling.New()
    p.RegisterLibrary(cachedLibrary)  // Fast, already built
}
```

## See Also

- [Native API](../native/) - Direct control with maximum performance
- [Script Extensions](../scripts/) - Extend using Scriptling code
