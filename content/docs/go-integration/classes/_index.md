---
title: Go Classes
description: Creating Go classes for object-oriented integration.
weight: 4
---

Create Go classes that can be instantiated and used from Scriptling.

## Basic Class

### Define a Class

```go
import (
    "context"
    "fmt"
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

                return &object.Dict{Pairs: map[string]object.Object{
                    "name": &object.String{Value: name},
                    "age":  object.NewInteger(age),
                }}
            },
            HelpText: "get_info() - Return person info as dict",
        },
    },
}
```

### Register and Use

```go
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

                instance.Fields["name"] = &object.String{Value: name}
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
`)
}
```

## Class with Static Methods

```go
var UtilityClass = &object.Class{
    Name: "Utility",
    Methods: map[string]object.Object{
        "format_currency": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                // Static method - self is still passed but ignored
                amount, _ := args[1].AsFloat()
                return &object.String{Value: fmt.Sprintf("$%.2f", amount)}
            },
            HelpText: "format_currency(amount) - Format as currency",
        },
        "now": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return &object.String{Value: time.Now().Format(time.RFC3339)}
            },
            HelpText: "now() - Get current timestamp",
        },
    },
}
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
                instance.Fields["headers"] = &object.Dict{Pairs: map[string]object.Object{}}

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
                headers.Pairs[key] = &object.String{Value: value}

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
                for key, val := range headers.Pairs {
                    valStr, _ := val.AsString()
                    req.Header.Set(key, valStr)
                }

                // Execute
                resp, err := client.Do(req)
                if err != nil {
                    return &object.Error{Message: err.Error()}
                }
                defer resp.Body.Close()

                body, _ := io.ReadAll(resp.Body)

                return &object.Dict{Pairs: map[string]object.Object{
                    "status":  object.NewInteger(int64(resp.StatusCode)),
                    "body":    &object.String{Value: string(body)},
                    "headers": &object.Dict{Pairs: map[string]object.Object{}},
                }}
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

1. **Always handle `self`** - First argument is always the instance
2. **Use `instance.Fields` for state** - Store instance data in the Fields map
3. **Return `object.None` for void methods** - Methods without return values
4. **Provide help text** - Document all methods
5. **Use type assertions safely** - Check types before casting

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
