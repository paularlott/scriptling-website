---
description: Give native Go classes special (dunder) methods such as __getitem__, and expose properties and static methods with object.Property and object.StaticMethod.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/native-classes/special-methods/
sources:
    - resource: https://scriptling.dev/docs/go-integration/native-classes/special-methods/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: Dunder Methods & Properties
type: Guide
---
# Dunder Methods & Properties

Part of [Native Classes](https://scriptling.dev/okf/scriptling-docs/go-integration/native-classes.md). The examples assume the class basics covered there.

## Special Methods

### Full Dunder Method Reference

| Method | Purpose |
|--------|---------|
| `__init__` | Constructor called when creating instances |
| `__str__` | String representation: used by `str()` and f-strings |
| `__repr__` | Debug representation: used by `repr()` |
| `__len__` | Length: used by `len()` |
| `__bool__` | Truthiness: falls back to `__len__` if absent |
| `__iter__` | Return an iterator object |
| `__next__` | Return next value; raise `StopIteration` when done |
| `__contains__` | Membership test: used by `in` operator |
| `__eq__` | Equality (`==`) |
| `__ne__` | Inequality (`!=`) |
| `__lt__` | Less-than (`<`): also used by `sorted()` |
| `__gt__` | Greater-than (`>`) |
| `__le__` | Less-than-or-equal (`<=`) |
| `__ge__` | Greater-than-or-equal (`>=`) |
| `__enter__` | Context manager entry: called by `with` |
| `__exit__` | Context manager exit: always called; return truthy to suppress exceptions |
| `__getitem__` | Custom indexing: used by `obj[key]` |

All dunder methods are inherited through the class hierarchy.

### `__getitem__(key)` - Custom Indexing

```go
counterClass := &object.Class{
    Name: "Counter",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                instance.SetField("data", object.NewStringDict(map[string]object.Object{}))
                return &object.Null{}
            },
        },
        "__getitem__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key := args[1].Inspect()
                data := instance.Field("data").(*object.Dict)
                if pair, ok := data.GetByString(key); ok {
                    return pair.Value
                }
                return object.NewInteger(0)  // Default for missing keys
            },
            HelpText: "__getitem__(key) - Get count for key",
        },
        "set": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key := args[1].Inspect()
                value := args[2]
                data := instance.Field("data").(*object.Dict)
                data.SetByString(key, value)
                return &object.Null{}
            },
            HelpText: "set(key, value) - Set a count",
        },
    },
}

// Enables: c[key] syntax
p.Eval(`
c = Counter()
c.set("apples", 5)
print(c["apples"])   # 5
print(c["oranges"])  # 0 (default)
`)
```

**Note:** Use `object.NewStringDict()` to create dicts and `GetByString()`/`SetByString()` for access. Never manipulate the internal `Pairs` map keys directly: they use a type-prefixed canonical format.

## Properties and Static Methods

Wrap methods in `object.Property` or `object.StaticMethod` to get the same behaviour as `@property` and `@staticmethod` in Scriptling scripts.

### `object.Property`

The `Getter` is called with `self` as the only argument when the attribute is accessed (no call parens needed from the script). Add a `Setter` to allow assignment:

```go
var CircleClass = &object.Class{
    Name: "Circle",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                r, _ := args[1].AsFloat()
                instance.SetField("radius", object.NewFloat(r))
                return &object.Null{}
            },
        },
        "radius": &object.Property{
            Getter: &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    return instance.Field("radius")
                },
            },
            Setter: &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    instance.SetField("radius", args[1])
                    return &object.Null{}
                },
            },
        },
        "area": &object.Property{  // read-only: no Setter
            Getter: &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    r, _ := instance.Field("radius").AsFloat()
                    return object.NewFloat(3.14159 * r * r)
                },
            },
        },
    },
}

// c = Circle(5.0)
// print(c.radius)  # 5 : no parens
// c.radius = 10    # calls setter
// print(c.area)    # read-only, assignment raises error
```

### `object.StaticMethod`

The `Fn` is called without `self`. Callable on both the class and instances:

```go
var MathClass = &object.Class{
    Name: "Math",
    Methods: map[string]object.Object{
        "square": &object.StaticMethod{
            Fn: &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    v, _ := args[0].AsFloat()
                    return object.NewFloat(v * v)
                },
            },
        },
    },
}

// Math.square(4)  # 16
// m = Math()
// m.square(4)     # 16
```

## See Also

- [Native Classes](https://scriptling.dev/okf/scriptling-docs/go-integration/native-classes.md) - Defining classes, `__init__`, and inheritance in Go
- [Dunder Methods](https://scriptling.dev/okf/scriptling-reference/classes/dunder-methods.md) - The same methods in Scriptling-defined classes
