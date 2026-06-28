---
title: Builder Classes
description: Type-safe class builder with automatic method conversion.
weight: 9
aliases:
  - /docs/go-integration/builder/classes/
---

Create type-safe classes with automatic parameter conversion using the Class Builder.

## Basic Class

```go
import "github.com/paularlott/scriptling/object"

func createPersonClass() *object.Class {
    cb := object.NewClassBuilder("Person")

    // Constructor
    cb.MethodWithHelp("__init__", func(self *object.Instance, name string, age int) {
        self.SetField("name", object.NewString(name))
        self.SetField("age", object.NewInteger(int64(age)))
    }, "__init__(name, age) - Initialize Person")

    // Method returning value
    cb.MethodWithHelp("greet", func(self *object.Instance) string {
        name, _ := self.Field("name").AsString()
        return "Hello, " + name + "!"
    }, "greet() - Return greeting")

    // Method modifying state
    cb.MethodWithHelp("birthday", func(self *object.Instance) string {
        age, _ := self.Field("age").AsInt()
        newAge := age + 1
        self.SetField("age", object.NewInteger(newAge))
        return fmt.Sprintf("Happy birthday! You're now %d", newAge)
    }, "birthday() - Increment age")

    // Method with parameters
    cb.MethodWithHelp("set_email", func(self *object.Instance, email string) {
        self.SetField("email", object.NewString(email))
    }, "set_email(email) - Set email address")

    return cb.Build()
}
```

## Method Signatures

Class methods support flexible signatures. The first parameter is the receiver — either `*Instance` or a typed pointer:

### Instance Receiver (manual Fields)

- `func(self *Instance, args...) result` - Instance + positional arguments
- `func(self *Instance, ctx context.Context, args...) result` - Instance + context + positional
- `func(self *Instance, kwargs object.Kwargs, args...) result` - Instance + kwargs + positional
- `func(self *Instance, ctx context.Context, kwargs object.Kwargs, args...) result` - All parameters

### Typed Receiver (Go struct, automatic wrapping)

- `func(self *T, args...) result` - Struct + positional arguments
- `func(self *T, ctx context.Context, args...) result` - Struct + context + positional
- `func(self *T, kwargs object.Kwargs, args...) result` - Struct + kwargs + positional
- `func(self *T, ctx context.Context, kwargs object.Kwargs, args...) result` - All parameters

**Parameter Order Rules (ALWAYS in this order):**
1. Receiver (`self`) - ALWAYS FIRST (`*Instance` or typed pointer)
2. Context (optional) - comes second if present
3. Kwargs (optional) - comes after context (or second if no context)
4. Positional arguments - ALWAYS LAST

## Typed Receivers

When your class is backed by a Go struct, use `Constructor` to register a function that returns a pointer to your struct. The struct is automatically wrapped and stored on the instance. Methods whose first parameter matches the constructor's return type receive the unwrapped struct directly — no manual Field boxing/unboxing needed.

```go
type PlayerData struct {
    Name   string
    Health int
    MaxHP  int
}

cb := object.NewClassBuilder("Player")

cb.Constructor(func(name string, hp int) *PlayerData {
    return &PlayerData{Name: name, Health: hp, MaxHP: hp}
})

cb.Method("take_damage", func(self *PlayerData, amount int) string {
    self.Health -= amount
    if self.Health < 0 {
        self.Health = 0
    }
    return fmt.Sprintf("%s took %d damage, health: %d", self.Name, amount, self.Health)
})

cb.Method("heal", func(self *PlayerData, amount int) string {
    self.Health += amount
    if self.Health > self.MaxHP {
        self.Health = self.MaxHP
    }
    return fmt.Sprintf("%s healed %d, health: %d", self.Name, amount, self.Health)
})

cb.Method("name", func(self *PlayerData) string {
    return self.Name
})

cb.Method("__del__", func(self *PlayerData) {
    // Cleanup resources — runs when the instance is garbage collected
})
```

The constructor:
- Accepts typed parameters (with optional `context.Context` and `object.Kwargs`)
- Returns a pointer type (e.g., `*PlayerData`)
- Can optionally return an error as a second value: `func(...) (*T, error)`

Methods:
- First parameter must match the constructor's return type
- Read and write struct fields directly — no `self.Field()` calls or type assertions needed
- `__del__` is called when the instance is garbage collected, or explicitly via `instance.__del__()`
- `__del__` can also be called multiple times explicitly — it runs every time it is called
- GC finalizers are not prompt: prefer explicit cleanup for critical resources

### Exposing Struct Fields with Properties

Go struct fields are **private** to Scriptling — they're wrapped in an internal `_receiver` field. To make them accessible as `player.name`, register properties:

```go
type PlayerData struct {
    Name   string
    Health int
}

cb := object.NewClassBuilder("Player")

cb.Constructor(func(name string, hp int) *PlayerData {
    return &PlayerData{Name: name, Health: hp}
})

cb.Property("name", func(self *PlayerData) string {
    return self.Name
})

cb.PropertyWithSetter("health",
    func(self *PlayerData) int {
        return self.Health
    },
    func(self *PlayerData, hp int) {
        self.Health = hp
    },
)
```

```python
p = Player("Ada", 100)
print(p.name)     # "Ada" — calls property getter
p.health = 50     # calls property setter
```

This gives you full control over what's exposed. You can derive computed values, validate inputs, or keep internal state truly private.

### When to Use Typed Receivers

| Factor | `*Instance` (manual) | Typed Receiver |
|--------|---------------------|----------------|
| **Best for** | Simple state, mixed types | Go struct-backed classes |
| **State access** | `self.SetField("key", v)` / `self.Field("key")` | Direct struct field access |
| **Exposed to Scriptling** | Yes — Fields are readable/writable | No — use `Property()` to expose |
| **Cleanup (`__del__`)** | Receives `*object.Instance` | Receives Go struct directly |
| **GC trigger** | Yes — finalizer installed on instance | Yes — finalizer installed on instance |
| **Boilerplate** | More (boxing/unboxing) | Less |

## Examples

### Simple Instance Method

```go
cb.Method("get_name", func(self *object.Instance) string {
    name, _ := self.Field("name").AsString()
    return name
})
```

### Method with Parameters

```go
cb.Method("add_friend", func(self *object.Instance, friendName string) {
    friends, _ := self.Field("friends").(*object.List)
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

    self.SetField("timeout", object.NewInteger(int64(timeout)))
    self.SetField("debug", object.NewBoolean(debug))
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

Registers a read-only getter as a `@property`. The getter receives `self` only, returns the attribute value, and is called when Scriptling reads `obj.name`. Do **not** include extra parameters:

```go
cb.Property("area", func(self *object.Instance) float64 {
    r, _ := self.Field("radius").AsFloat()
    return math.Pi * r * r
})

// c = Circle(5)
// print(c.area)  # no parens needed
// c.area = 10    # error: property is read-only
```

### `PropertyWithSetter(name, getter, setter)`

Registers a getter and setter. The getter receives `self` only. The setter receives `self` and the new value, and may validate or normalize before storing it. Setter return values are ignored by normal assignment:

```go
cb.PropertyWithSetter("radius",
    func(self *object.Instance) float64 {
        r, _ := self.Field("_r").AsFloat()
        return r
    },
    func(self *object.Instance, v float64) {
        self.SetField("_r", object.NewFloat(v))
    },
)

// c.radius = 10   # calls setter
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
        self.SetField("name", object.NewString(name))
        self.SetField("age", object.NewInteger(int64(age)))
        // Add student-specific field
        self.SetField("school", object.NewString(school))
    }, "__init__(name, age, school) - Initialize Student")

    // Student-specific method
    cb.MethodWithHelp("study", func(self *object.Instance, subject string) string {
        name, _ := self.Field("name").AsString()
        school, _ := self.Field("school").AsString()
        return fmt.Sprintf("%s is studying %s at %s", name, subject, school)
    }, "study(subject) - Study a subject")

    return cb.Build()
}
```

## Scriptling Inheritance from Go Classes

Scriptling classes can inherit from Go-registered classes. The child class must call `super().__init__()` to trigger the Go constructor — `__init__` is not automatically chained:

```python
class BetterCounter(Counter):
    def __init__(self, start, label):
        super().__init__(start)
        self.label = label

    def labeled_get(self):
        return self.label + ": " + str(self.get())
```

How inheritance behaves depends on which pattern the Go class uses:

### Instance Fields — fully accessible

When the Go class uses `*object.Instance` and stores values via `SetField`, those fields are accessible from Scriptling as normal attributes:

```go
// Go side
cb := object.NewClassBuilder("Config").
    Method("__init__", func(self *object.Instance, name string) {
        self.SetField("name", object.NewString(name))
    }).
    Method("get", func(self *object.Instance) string {
        return self.Field("name").(*object.String).StringValue()
    })
```

```python
# Scriptling side — child can read parent fields directly
class ChildConfig(Config):
    def __init__(self, name):
        super().__init__(name)

    def upper_name(self):
        return self.name.upper()  # reads parent's Fields["name"]
```

### Typed Receivers — private by default

When the Go class uses a typed receiver, the Go struct's fields are **not accessible** from Scriptling — they're opaque inside the internal `_receiver` wrapper. Child classes can call parent methods (which unwrap the receiver internally) but cannot read or write the Go struct's fields directly:

```python
# Scriptling side
class BetterPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def bonus(self, n):
        return self.add_score(n * 2)  # works — calls Go method

    def get_name(self):
        return self.Name  # None — Go struct fields are not exposed
```

To expose Go struct fields to Scriptling children, register properties on the Go class:

```go
cb.Property("name", func(self *playerData) string {
    return self.Name
})
```

```python
class BetterPlayer(Player):
    def get_name(self):
        return self.name  # works — calls property getter
```

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
                instance.SetField("name", object.NewString(name))
                instance.SetField("age", object.NewInteger(age))
                return object.NULL
            },
        },
        "greet": &object.Builtin{
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                instance := args[0].(*object.Instance)
                name, _ := instance.Field("name").AsString()
                return object.NewString("Hello, I'm " + name)
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
    parentInit.Fn(nil, nil, self, object.NewString(name), object.NewInteger(int64(age)))

    // Add employee-specific field
    self.SetField("department", object.NewString(department))
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
        self.SetField("name", object.NewString(name))
        self.SetField("health", object.NewInteger(int64(health)))
        self.SetField("max_health", object.NewInteger(int64(health)))
        self.SetField("inventory", &object.List{Elements: []object.Object{}})
    }, "__init__(name, health) - Create player")

    cb.MethodWithHelp("take_damage", func(self *object.Instance, amount int) string {
        health, _ := self.Field("health").AsInt()
        newHealth := health - amount
        if newHealth < 0 {
            newHealth = 0
        }
        self.SetField("health", object.NewInteger(newHealth))

        name, _ := self.Field("name").AsString()
        if newHealth == 0 {
            return name + " has been defeated!"
        }
        return fmt.Sprintf("%s took %d damage, health: %d", name, amount, newHealth)
    }, "take_damage(amount) - Take damage")

    cb.MethodWithHelp("heal", func(self *object.Instance, amount int) string {
        health, _ := self.Field("health").AsInt()
        maxHealth, _ := self.Field("max_health").AsInt()
        newHealth := health + amount
        if newHealth > maxHealth {
            newHealth = maxHealth
        }
        self.SetField("health", object.NewInteger(newHealth))

        name, _ := self.Field("name").AsString()
        return fmt.Sprintf("%s healed %d, health: %d", name, amount, newHealth)
    }, "heal(amount) - Heal player")

    cb.MethodWithHelp("add_item", func(self *object.Instance, item string) {
        inventory := self.Field("inventory").(*object.List)
        inventory.Elements = append(inventory.Elements, object.NewString(item))
    }, "add_item(item) - Add item to inventory")

    cb.MethodWithHelp("get_status", func(self *object.Instance) map[string]interface{} {
        name, _ := self.Field("name").AsString()
        health, _ := self.Field("health").AsInt()
        maxHealth, _ := self.Field("max_health").AsInt()
        inventory := self.Field("inventory").(*object.List)

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
| `Constructor(fn)` | Register a typed constructor (returns `*T`, sets receiver type) |
| `Method(name, fn)` | Register a typed Go method (receiver is `*Instance` or `*T`) |
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
- [Native Classes](native-classes/) - Direct control with maximum performance
