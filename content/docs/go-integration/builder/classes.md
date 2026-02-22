---
title: Builder Classes
description: Type-safe class builder with automatic method conversion.
weight: 3
---

Create type-safe classes with automatic parameter conversion using the Class Builder.

## Basic Class

```go
import "github.com/paularlott/scriptling/object"

func createPersonClass() *object.Class {
    cb := object.NewClassBuilder("Person")

    // Constructor
    cb.MethodWithHelp("__init__", func(self *object.Instance, name string, age int) {
        self.Fields["name"] = object.NewString(name)
        self.Fields["age"] = object.NewInteger(int64(age))
    }, "__init__(name, age) - Initialize Person")

    // Method returning value
    cb.MethodWithHelp("greet", func(self *object.Instance) string {
        name, _ := self.Fields["name"].AsString()
        return "Hello, " + name + "!"
    }, "greet() - Return greeting")

    // Method modifying state
    cb.MethodWithHelp("birthday", func(self *object.Instance) string {
        age, _ := self.Fields["age"].AsInt()
        newAge := age + 1
        self.Fields["age"] = object.NewInteger(newAge)
        return fmt.Sprintf("Happy birthday! You're now %d", newAge)
    }, "birthday() - Increment age")

    // Method with parameters
    cb.MethodWithHelp("set_email", func(self *object.Instance, email string) {
        self.Fields["email"] = object.NewString(email)
    }, "set_email(email) - Set email address")

    return cb.Build()
}
```

## Method Signatures

Class methods support flexible signatures. The first parameter is ALWAYS the instance (`self`):

- `func(self *Instance, args...) result` - Instance + positional arguments
- `func(self *Instance, ctx context.Context, args...) result` - Instance + context + positional
- `func(self *Instance, kwargs object.Kwargs, args...) result` - Instance + kwargs + positional
- `func(self *Instance, ctx context.Context, kwargs object.Kwargs, args...) result` - All parameters

**Parameter Order Rules (ALWAYS in this order):**
1. Instance (`self`) - ALWAYS FIRST
2. Context (optional) - comes second if present
3. Kwargs (optional) - comes after context (or second if no context)
4. Positional arguments - ALWAYS LAST

## Examples

### Simple Instance Method

```go
cb.Method("get_name", func(self *object.Instance) string {
    name, _ := self.Fields["name"].AsString()
    return name
})
```

### Method with Parameters

```go
cb.Method("add_friend", func(self *object.Instance, friendName string) {
    friends, _ := self.Fields["friends"].(*object.List)
    friends.Elements = append(friends.Elements, object.NewString(friendName))
})
```

### Method with Context and Error Handling

```go
cb.Method("save", func(self *object.Instance, ctx context.Context) error {
    // Simulate async save operation
    select {
    case <-time.After(100 * time.Millisecond):
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
})
```

### Method with Kwargs

```go
cb.Method("configure", func(self *object.Instance, kwargs object.Kwargs) error {
    timeout, _ := kwargs.GetInt("timeout", 30)
    debug, _ := kwargs.GetBool("debug", false)

    self.Fields["timeout"] = object.NewInteger(int64(timeout))
    self.Fields["debug"] = object.NewBoolean(debug)
    return nil
})
```

### Method with Context and Kwargs

```go
cb.Method("fetch", func(self *object.Instance, ctx context.Context, kwargs object.Kwargs) (string, error) {
    url, _ := kwargs.GetString("url", "")
    timeout, _ := kwargs.GetInt("timeout", 30)

    // Use context for timeout
    ctx, cancel := context.WithTimeout(ctx, time.Duration(timeout)*time.Second)
    defer cancel()

    // Fetch data...
    return "data", nil
})
```

## Properties and Static Methods

### `Property(name, fn)`

Registers a read-only getter as a `@property`. The getter receives `self` only — do **not** include extra parameters:

```go
cb.Property("area", func(self *object.Instance) float64 {
    r, _ := self.Fields["radius"].AsFloat()
    return math.Pi * r * r
})

// c = Circle(5)
// print(c.area)  # no parens needed
// c.area = 10    # error: property is read-only
```

### `PropertyWithSetter(name, getter, setter)`

Registers a getter and setter. The setter receives `self` and the new value:

```go
cb.PropertyWithSetter("radius",
    func(self *object.Instance) float64 {
        r, _ := self.Fields["_r"].AsFloat()
        return r
    },
    func(self *object.Instance, v float64) {
        self.Fields["_r"] = &object.Float{Value: v}
    },
)

// c.radius = 10  # calls setter
// print(c.radius) # calls getter
```

### `StaticMethod(name, fn)`

Registers a `@staticmethod`. The function does **not** receive `self` — do not include `*object.Instance` as the first parameter:

```go
cb.StaticMethod("from_degrees", func(deg float64) float64 {
    return deg * math.Pi / 180
})

// MyClass.from_degrees(180)  # called on class
// obj.from_degrees(90)       # also callable on instance
```

## Inheritance

Set a base class for inheritance:

```go
func createStudentClass(personClass *object.Class) *object.Class {
    cb := object.NewClassBuilder("Student")

    // Set base class
    cb.BaseClass(personClass)

    // Extended constructor (calls parent __init__)
    cb.MethodWithHelp("__init__", func(self *object.Instance, name string, age int, school string) {
        // Initialize base class fields
        self.Fields["name"] = object.NewString(name)
        self.Fields["age"] = object.NewInteger(int64(age))
        // Add student-specific field
        self.Fields["school"] = object.NewString(school)
    }, "__init__(name, age, school) - Initialize Student")

    // Student-specific method
    cb.MethodWithHelp("study", func(self *object.Instance, subject string) string {
        name, _ := self.Fields["name"].AsString()
        school, _ := self.Fields["school"].AsString()
        return fmt.Sprintf("%s is studying %s at %s", name, subject, school)
    }, "study(subject) - Study a subject")

    return cb.Build()
}
```

## Cross-Approach Inheritance

The Builder API and Native API work seamlessly together for inheritance.

### Builder Class Inheriting from Native Base

```go
// Native base class (Person)
personClass := &object.Class{
    Name: "Person",
    Methods: map[string]object.Object{
        "__init__": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := args[1].AsString()
                age, _ := args[2].AsInt()
                instance.Fields["name"] = &object.String{Value: name}
                instance.Fields["age"] = &object.Integer{Value: age}
                return object.NULL
            },
        },
        "greet": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Fields["name"].AsString()
                return &object.String{Value: "Hello, I'm " + name}
            },
        },
    },
}

// Builder API derived class (Employee)
cb := object.NewClassBuilder("Employee")
cb.BaseClass(personClass)  // Inherit from native class

cb.Method("__init__", func(self *object.Instance, name string, age int, department string) {
    // Call parent __init__ using native API
    parentInit := personClass.Methods["__init__"].(*object.Builtin)
    parentInit.Fn(nil, nil, self, &object.String{Value: name}, &object.Integer{Value: int64(age)})

    // Add employee-specific field
    self.Fields["department"] = &object.String{Value: department}
})

employeeClass := cb.Build()
```

## Complete Example: Game Library

```go
package main

import (
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/stdlib"
)

// Player class using builder
func createPlayerClass() *object.Class {
    cb := object.NewClassBuilder("Player")

    cb.MethodWithHelp("__init__", func(self *object.Instance, name string, health int) {
        self.Fields["name"] = object.NewString(name)
        self.Fields["health"] = object.NewInteger(int64(health))
        self.Fields["max_health"] = object.NewInteger(int64(health))
        self.Fields["inventory"] = &object.List{Elements: []object.Object{}}
    }, "__init__(name, health) - Create player")

    cb.MethodWithHelp("take_damage", func(self *object.Instance, amount int) string {
        health, _ := self.Fields["health"].AsInt()
        newHealth := health - amount
        if newHealth < 0 {
            newHealth = 0
        }
        self.Fields["health"] = object.NewInteger(newHealth)

        name, _ := self.Fields["name"].AsString()
        if newHealth == 0 {
            return name + " has been defeated!"
        }
        return fmt.Sprintf("%s took %d damage, health: %d", name, amount, newHealth)
    }, "take_damage(amount) - Take damage")

    cb.MethodWithHelp("heal", func(self *object.Instance, amount int) string {
        health, _ := self.Fields["health"].AsInt()
        maxHealth, _ := self.Fields["max_health"].AsInt()
        newHealth := health + amount
        if newHealth > maxHealth {
            newHealth = maxHealth
        }
        self.Fields["health"] = object.NewInteger(newHealth)

        name, _ := self.Fields["name"].AsString()
        return fmt.Sprintf("%s healed %d, health: %d", name, amount, newHealth)
    }, "heal(amount) - Heal player")

    cb.MethodWithHelp("add_item", func(self *object.Instance, item string) {
        inventory := self.Fields["inventory"].(*object.List)
        inventory.Elements = append(inventory.Elements, object.NewString(item))
    }, "add_item(item) - Add item to inventory")

    cb.MethodWithHelp("get_status", func(self *object.Instance) map[string]interface{} {
        name, _ := self.Fields["name"].AsString()
        health, _ := self.Fields["health"].AsInt()
        maxHealth, _ := self.Fields["max_health"].AsInt()
        inventory := self.Fields["inventory"].(*object.List)

        items := make([]string, len(inventory.Elements))
        for i, item := range inventory.Elements {
            items[i], _ = item.AsString()
        }

        return map[string]interface{}{
            "name":       name,
            "health":     health,
            "max_health": maxHealth,
            "alive":      health > 0,
            "inventory":  items,
        }
    }, "get_status() - Get player status")

    return cb.Build()
}

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Create and register
    playerClass := createPlayerClass()
    p.SetVar("Player", playerClass)

    // Use from script
    p.Eval(`
# Create player
hero = Player("Hero", 100)

# Add items
hero.add_item("Sword")
hero.add_item("Shield")
hero.add_item("Health Potion")

# Combat
print(hero.take_damage(15))

# Heal
print(hero.heal(20))

# Check status
status = hero.get_status()
print("Player:", status["name"], "Health:", status["health"])
print("Inventory:", status["inventory"])
`)
}
```

## Builder Methods Reference

| Method | Description |
|--------|-------------|
| `Method(name, fn)` | Register a typed Go method |
| `MethodWithHelp(name, fn, help)` | Register method with help text |
| `Property(name, fn)` | Register a read-only getter as `@property` |
| `PropertyWithSetter(name, getter, setter)` | Register a getter+setter `@property` |
| `StaticMethod(name, fn)` | Register a `@staticmethod` (no `self` parameter) |
| `BaseClass(base)` | Set base class for inheritance |
| `Environment(env)` | Set environment (usually not needed) |
| `Build()` | Create and return the Class |

## Choosing Between Native and Builder API

| Factor | Native API | Builder API |
|--------|------------|-------------|
| **Performance** | Faster (no reflection overhead) | Slight overhead |
| **Type Safety** | Manual checking | Automatic conversion |
| **Control** | Full control over method logic | Convention-based |
| **Help Text** | Manual `HelpText` field | Chainable `MethodWithHelp()` |
| **Best For** | Complex inheritance, performance | Type-safe methods, rapid development |

## See Also

- [Builder Functions](functions/) - Type-safe function builder
- [Builder Libraries](libraries/) - Type-safe library builder
- [Native Classes](../native/classes/) - Direct control with maximum performance
