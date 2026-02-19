---
title: Native Classes
description: Create custom classes with full control over methods and inheritance.
weight: 3
---

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

                instance.Fields["name"] = &object.String{Value: name}
                instance.Fields["age"] = object.NewInteger(age)

                return object.None
            },
            HelpText: "__init__(name, age) - Initialize Person",
        },
        "greet": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                name, _ := instance.Fields["name"].AsString()
                return &object.String{Value: "Hello, " + name + "!"}
            },
            HelpText: "greet() - Return greeting with person's name",
        },
        "birthday": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                age, _ := instance.Fields["age"].AsInt()
                instance.Fields["age"] = object.NewInteger(age + 1)

                return &object.String{Value: fmt.Sprintf("Happy birthday! You're now %d", age+1)}
            },
            HelpText: "birthday() - Increment age and return birthday message",
        },
        "get_info": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)

                name, _ := instance.Fields["name"].AsString()
                age, _ := instance.Fields["age"].AsInt()

                return object.NewStringDict(map[string]object.Object{
                    "name": &object.String{Value: name},
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

                instance.Fields["width"] = object.NewFloat(width)
                instance.Fields["height"] = object.NewFloat(height)
                return object.None
            },
            HelpText: "__init__(width, height) - Initialize Rectangle",
        },
        "area": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                width, _ := instance.Fields["width"].AsFloat()
                height, _ := instance.Fields["height"].AsFloat()
                return object.NewFloat(width * height)
            },
            HelpText: "area() - Calculate area",
        },
        "perimeter": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                width, _ := instance.Fields["width"].AsFloat()
                height, _ := instance.Fields["height"].AsFloat()
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
                instance.Fields["name"] = &object.String{Value: name}
                return object.None
            },
            HelpText: "__init__(name) - Initialize Animal",
        },
        "speak": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return &object.String{Value: "Generic animal sound"}
            },
            HelpText: "speak() - Make animal sound",
        },
        "info": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Fields["name"].AsString()
                return &object.String{Value: "Animal: " + name}
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
                animalInit.Fn(ctx, nil, instance, &object.String{Value: name})

                instance.Fields["breed"] = &object.String{Value: breed}
                return object.None
            },
            HelpText: "__init__(name, breed) - Initialize Dog",
        },
        "speak": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return &object.String{Value: "Woof!"}
            },
            HelpText: "speak() - Bark",
        },
        "fetch": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Fields["name"].AsString()
                return &object.String{Value: name + " fetches the ball!"}
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

### `__getitem__(key)` - Custom Indexing

```go
counterClass := &object.Class{
    Name: "Counter",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                instance.Fields["data"] = object.NewStringDict(map[string]object.Object{})
                return object.None
            },
        },
        "__getitem__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key := args[1].Inspect()
                data := instance.Fields["data"].(*object.Dict)
                if pair, ok := data.GetByString(key); ok {
                    return pair.Value
                }
                return &object.Integer{Value: 0}  // Default for missing keys
            },
            HelpText: "__getitem__(key) - Get count for key",
        },
        "set": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key := args[1].Inspect()
                value := args[2]
                data := instance.Fields["data"].(*object.Dict)
                data.SetByString(key, value)
                return object.None
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

**Note:** Use `object.NewStringDict()` to create dicts and `GetByString()`/`SetByString()` for access. Never manipulate the internal `Pairs` map keys directly — they use a type-prefixed canonical format.

### Other Special Methods

| Method | Purpose |
|--------|---------|
| `__init__` | Constructor called when creating instances |
| `__str__` | Custom string representation (for `str()` function) |
| `__len__` | Custom length (for `len()` function) |
| `__getitem__` | Custom indexing (for `obj[key]` syntax) |

## Classes in Libraries

Add classes to libraries via the constants map:

```go
myLib := object.NewLibrary("counters",
    map[string]*object.Builtin{
        "create_counter": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                // Factory function
                return &object.Instance{
                    Class: counterClass,
                    Fields: map[string]object.Object{
                        "data": object.NewStringDict(map[string]object.Object{}),
                    },
                }
            },
            HelpText: "create_counter() - Create a new Counter",
        },
    },
    map[string]object.Object{
        "Counter": counterClass,           // Expose for direct instantiation
        "VERSION": &object.String{Value: "1.0.0"},
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

                instance.Fields["base_url"] = &object.String{Value: baseURL}
                instance.Fields["timeout"] = object.NewInteger(int64(timeout))
                instance.Fields["headers"] = object.NewStringDict(map[string]object.Object{})

                return object.None
            },
            HelpText: "__init__(base_url='', timeout=30) - Create HTTP client",
        },
        "set_header": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                key, _ := args[1].AsString()
                value, _ := args[2].AsString()

                headers := instance.Fields["headers"].(*object.Dict)
                headers.SetByString(key, &object.String{Value: value})

                return object.None
            },
            HelpText: "set_header(key, value) - Set default header",
        },
        "get": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                path, _ := args[1].AsString()

                // Build URL
                baseURL, _ := instance.Fields["base_url"].AsString()
                url := baseURL + path

                // Get timeout
                timeoutSec, _ := instance.Fields["timeout"].AsInt()

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
                headers := instance.Fields["headers"].(*object.Dict)
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
                    "body":    &object.String{Value: string(body)},
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

### 2. Use `instance.Fields` for State

Store instance data in the Fields map:

```go
instance.Fields["name"] = &object.String{Value: name}
instance.Fields["count"] = object.NewInteger(count)
```

### 3. Return `object.None` for Void Methods

Methods without return values should return None:

```go
Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // ... implementation
    return object.None
}
```

### 4. Use Type Assertions Safely

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
    instance.Fields["data"] = &object.String{Value: value}
    return object.None
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
                    instance.Fields["count"] = &object.Integer{Value: 0}
                    return object.None
                },
            },
            "increment": &object.Builtin{
                Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                    instance := args[0].(*object.Instance)
                    count, _ := instance.Fields["count"].AsInt()
                    instance.Fields["count"] = object.NewInteger(count + 1)
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

- [Native Functions](functions/) - Register individual functions
- [Native Libraries](libraries/) - Create libraries with functions and constants
- [Builder Classes](../builder/classes/) - Type-safe class builder
