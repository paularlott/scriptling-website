---
description: Create custom classes with full control over methods and inheritance.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/native-classes/
sources:
    - resource: https://scriptling.dev/docs/go-integration/native-classes/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: Native Classes
type: Guide
---
# Native Classes

Create Go classes that can be instantiated and used from Scriptling using the Native API.

## Basic Class

A class is an `*object.Class` structure containing methods:

```go
import (
    "context"
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

var PersonClass = &object.Class{
    Name: "Person",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                // args[0] is always 'self' (the instance)
                instance := args[0].(*object.Instance)

                name, _ := args[1].AsString()
                age, _ := args[2].AsInt()

                instance.SetField("name", object.NewString(name))
                instance.SetField("age", object.NewInteger(age))

                return &object.Null{}
            },
            HelpText: "__init__(name, age) - Initialize Person",
        },
        "greet": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                name, _ := instance.Field("name").AsString()
                return object.NewString("Hello, " + name + "!")
            },
            HelpText: "greet() - Return greeting with person's name",
        },
        "birthday": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                age, _ := instance.Field("age").AsInt()
                instance.SetField("age", object.NewInteger(age + 1))

                return object.NewString(fmt.Sprintf("Happy birthday! You're now %d", age+1))
            },
            HelpText: "birthday() - Increment age and return birthday message",
        },
        "get_info": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                name, _ := instance.Field("name").AsString()
                age, _ := instance.Field("age").AsInt()

                return object.NewStringDict(map[string]object.Object{
                    "name": object.NewString(name),
                    "age":  object.NewInteger(age),
                })
            },
            HelpText: "get_info() - Return person info as dict",
        },
    },
}

func main() {
    p := scriptling.New()

    // Register class
    p.SetVar("Person", PersonClass)

    // Use from Scriptling
    p.Eval(`
person = Person("Alice", 30)
print(person.greet())      # "Hello, Alice!"
print(person.birthday())   # "Happy birthday! You're now 31"
info = person.get_info()
`)
}
```

## Creating Instances from Go

```go
func main() {
    p := scriptling.New()
    p.SetVar("Person", PersonClass)

    // Create instance from Go
    instance, err := p.CreateInstance("Person", "Bob", 25)
    if err != nil {
        log.Fatal(err)
    }

    // Store instance in variable
    p.SetObjectVar("bob", instance)

    // Call methods
    greeting, _ := p.CallMethod(instance, "greet")
    fmt.Println(greeting.Inspect())  // "Hello, Bob!"

    // Use from script
    p.Eval(`
print(bob.greet())
bob.birthday()
`)
}
```

## The __init__ Method

The `__init__` method is the constructor, called when creating a new instance:

```go
var RectangleClass = &object.Class{
    Name: "Rectangle",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                if len(args) < 3 {
                    return &object.Error{Message: "__init__ requires instance, width, and height"}
                }
                instance := args[0].(*object.Instance)
                width, _ := args[1].AsFloat()
                height, _ := args[2].AsFloat()

                instance.SetField("width", object.NewFloat(width))
                instance.SetField("height", object.NewFloat(height))
                return &object.Null{}
            },
            HelpText: "__init__(width, height) - Initialize Rectangle",
        },
        "area": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                width, _ := instance.Field("width").AsFloat()
                height, _ := instance.Field("height").AsFloat()
                return object.NewFloat(width * height)
            },
            HelpText: "area() - Calculate area",
        },
        "perimeter": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                width, _ := instance.Field("width").AsFloat()
                height, _ := instance.Field("height").AsFloat()
                return object.NewFloat(2 * (width + height))
            },
            HelpText: "perimeter() - Calculate perimeter",
        },
    },
}
```

## Inheritance

### Base Class

```go
var AnimalClass = &object.Class{
    Name: "Animal",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := args[1].AsString()
                instance.SetField("name", object.NewString(name))
                return &object.Null{}
            },
            HelpText: "__init__(name) - Initialize Animal",
        },
        "speak": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return object.NewString("Generic animal sound")
            },
            HelpText: "speak() - Make animal sound",
        },
        "info": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Field("name").AsString()
                return object.NewString("Animal: " + name)
            },
            HelpText: "info() - Return animal info",
        },
    },
}
```

### Derived Class

```go
var DogClass = &object.Class{
    Name: "Dog",
    BaseClass: AnimalClass,  // Inherit from Animal
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := args[1].AsString()
                breed, _ := args[2].AsString()

                // Call parent __init__
                animalInit := AnimalClass.Methods["__init__"].(*object.Builtin)
                animalInit.Fn(ctx, nil, instance, object.NewString(name))

                instance.SetField("breed", object.NewString(breed))
                return &object.Null{}
            },
            HelpText: "__init__(name, breed) - Initialize Dog",
        },
        "speak": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return object.NewString("Woof!")
            },
            HelpText: "speak() - Bark",
        },
        "fetch": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Field("name").AsString()
                return object.NewString(name + " fetches the ball!")
            },
            HelpText: "fetch() - Fetch something",
        },
    },
}
```

### Using Inheritance

```go
func main() {
    p := scriptling.New()
    p.SetVar("Animal", AnimalClass)
    p.SetVar("Dog", DogClass)

    p.Eval(`
dog = Dog("Rex", "German Shepherd")
print(dog.speak())   # "Woof!" (overridden method)
print(dog.fetch())   # "Rex fetches the ball!"
print(dog.info())    # "Animal: Rex" (inherited method)
`)
}
```

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

## Classes in Libraries

Add classes to libraries via the constants map:

```go
myLib := object.NewLibrary("counters",
    map[string]*object.Builtin{
        "create_counter": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                // Factory function
                return object.NewInstanceWithFields(counterClass, map[string]object.Object{
                    "data": object.NewStringDict(map[string]object.Object{}),
                })
            },
            HelpText: "create_counter() - Create a new Counter",
        },
    },
    map[string]object.Object{
        "Counter": counterClass,           // Expose for direct instantiation
        "VERSION": object.NewString("1.0.0"),
    },
    "Counter utilities library",
)

p.RegisterLibrary(myLib)

// Use in Scriptling
p.Eval(`
import counters

# Use factory
c = counters.create_counter()

# Or use class directly
c2 = counters.Counter()
`)
```

## Complete Example: HTTP Client Class

```go
package main

import (
    "context"
    "fmt"
    "io"
    "net/http"
    "time"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
)

var HTTPClientClass = &object.Class{
    Name: "HTTPClient",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                // Get optional parameters
                baseURL, _ := kwargs.GetString("base_url", "")
                timeout, _ := kwargs.GetInt("timeout", 30)

                instance.SetField("base_url", object.NewString(baseURL))
                instance.SetField("timeout", object.NewInteger(int64(timeout)))
                instance.SetField("headers", object.NewStringDict(map[string]object.Object{}))

                return &object.Null{}
            },
            HelpText: "__init__(base_url='', timeout=30) - Create HTTP client",
        },
        "set_header": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key, _ := args[1].AsString()
                value, _ := args[2].AsString()

                headers := instance.Field("headers").(*object.Dict)
                headers.SetByString(key, object.NewString(value))

                return &object.Null{}
            },
            HelpText: "set_header(key, value) - Set default header",
        },
        "get": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                path, _ := args[1].AsString()

                // Build URL
                baseURL, _ := instance.Field("base_url").AsString()
                url := baseURL + path

                // Get timeout
                timeoutSec, _ := instance.Field("timeout").AsInt()

                // Create client with timeout
                client := &http.Client{
                    Timeout: time.Duration(timeoutSec) * time.Second,
                }

                // Create request
                req, err := http.NewRequest("GET", url, nil)
                if err != nil {
                    return &object.Error{Message: err.Error()}
                }

                // Add headers
                headers := instance.Field("headers").(*object.Dict)
                for _, pair := range headers.Pairs {
                    key := pair.Key.Inspect()
                    valStr, _ := pair.Value.AsString()
                    req.Header.Set(key, valStr)
                }

                // Execute
                resp, err := client.Do(req)
                if err != nil {
                    return &object.Error{Message: err.Error()}
                }
                defer resp.Body.Close()

                body, _ := io.ReadAll(resp.Body)

                return object.NewStringDict(map[string]object.Object{
                    "status":  object.NewInteger(int64(resp.StatusCode)),
                    "body":    object.NewString(string(body)),
                    "headers": object.NewStringDict(map[string]object.Object{}),
                })
            },
            HelpText: "get(path) - Make GET request",
        },
    },
}

func main() {
    p := scriptling.New()
    p.SetVar("HTTPClient", HTTPClientClass)

    p.Eval(`
client = HTTPClient(base_url="https://api.example.com", timeout=10)
client.set_header("Authorization", "Bearer token123")
client.set_header("Content-Type", "application/json")

response = client.get("/users")
if response["status"] == 200:
    print("Success!")
    print(response["body"])
else:
    print("Error:", response["status"])
`)
}
```

## Best Practices

### 1. Always Handle `self`

First argument is always the instance:

```go
Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    instance := args[0].(*object.Instance)  // self
    // ... rest of implementation
}
```

### 2. Use Instance Fields for User-Visible State

Store data that scripts can read as fields:

```go
instance.SetField("name", object.NewString(name))
instance.SetField("count", object.NewInteger(count))
```

### 3. Use `instance.NativeData` for Go-Only State

When your class wraps a Go value (a connection, file handle, parsed template, etc.) that scripts should never access directly, store it in `NativeData` instead of `Fields`. This avoids polluting the field namespace and removes the need for a wrapper type that implements `object.Object`:

```go
type myConn struct {
    conn net.Conn
    id   string
}

var MyClass = &object.Class{
    Name: "MyClient",
    Methods: map[string]object.Object{
        "send": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                c, ok := instance.NativeData.(*myConn)
                if !ok {
                    return errors.NewError("invalid client")
                }
                msg, _ := args[1].AsString()
                c.conn.Write([]byte(msg))
                return &object.Null{}
            },
        },
    },
}

// Create instance with NativeData
func newClientInstance(conn net.Conn) *object.Instance {
    return object.NewInstanceWithData(MyClass, nil, &myConn{conn: conn})
}
```

Use field accessors (`SetField`/`Field`) for data scripts can read; use `NativeData` for internal Go state. Shallow and deep copies of an instance do not copy `NativeData`, so native-backed objects should be treated as handles rather than copyable data containers.

### 4. Return `&object.Null{}` for Void Methods

Methods without return values should return `&object.Null{}`:

```go
Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // ... implementation
    return &object.Null{}
}
```

### 5. Use Type Assertions Safely

Check types before casting:

```go
// Safe type handling
func safeMethod(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    if len(args) < 2 {
        return &object.Error{Message: "method requires at least 1 argument"}
    }

    instance, ok := args[0].(*object.Instance)
    if !ok {
        return &object.Error{Message: "invalid instance"}
    }

    value, err := args[1].AsString()
    if err != nil {
        return &object.Error{Message: "argument must be a string"}
    }

    // Safe to use instance and value
    instance.SetField("data", object.NewString(value))
    return &object.Null{}
}
```

## Testing Classes

```go
func TestClass(t *testing.T) {
    p := scriptling.New()

    // Create class
    counterClass := &object.Class{
        Name: "Counter",
        Methods: map[string]object.Object{
            "__init__": &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    instance.SetField("count", object.NewInteger(0))
                    return &object.Null{}
                },
            },
            "increment": &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    count, _ := instance.Field("count").AsInt()
                    instance.SetField("count", object.NewInteger(count + 1))
                    return object.NewInteger(count + 1)
                },
            },
        },
    }

    // Register class
    p.SetVar("Counter", counterClass)

    // Test the class
    result, err := p.Eval(`
c = Counter()
c.increment()
c.increment()
result = c.increment()
`)
    if err != nil {
        t.Fatalf("Eval error: %v", err)
    }

    if value, objErr := result.AsInt(); objErr == nil {
        if value != 3 {
            t.Errorf("Expected 3, got %d", value)
        }
    }
}
```

## See Also

- [Native Functions](native-functions.md) - Register individual functions
- [Native Libraries](native-libraries.md) - Create libraries with functions and constants
- [Builder Classes](builder-classes.md) - Type-safe class builder
