---
title: Builder API
description: Type-safe builder pattern for functions, classes, and libraries.
weight: 5
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

## Function Builder

### Basic Function

```go
import "github.com/paularlott/scriptling/object"

func registerAddFunction(p *scriptling.Scriptling) {
    fb := object.NewFunctionBuilder()

    // Define function with automatic type conversion
    fb.FunctionWithHelp(func(a, b int) int {
        return a + b
    }, "add(a, b) - Add two numbers together")

    p.RegisterFunc("add", fb.Build())
}
```

### Multiple Parameter Types

```go
// Function with different types
fb.FunctionWithHelp(func(name string, count int, ratio float64) string {
    return fmt.Sprintf("%s: %d items at %.2f ratio", name, count, ratio)
}, "format(name, count, ratio) - Format data")

// Types supported:
// - int, int64, float64
// - string, bool
// - []interface{} (lists)
// - map[string]interface{} (dicts)
```

### With Keyword Arguments

```go
fb.FunctionWithHelp(func(host string, port int, useTLS bool) string {
    protocol := "http"
    if useTLS {
        protocol = "https"
    }
    return fmt.Sprintf("%s://%s:%d", protocol, host, port)
}, `connect(host, port=8080, useTLS=False) - Build connection URL

Parameters:
  host - Server hostname
  port - Server port (default: 8080)
  useTLS - Use HTTPS (default: False)

Returns:
  Connection URL string`)
```

### Variadic Functions

```go
// Accept variable number of arguments
fb.FunctionFromVariadicWithHelp(func(args ...interface{}) []interface{} {
    // Process all arguments
    result := make([]interface{}, len(args))
    for i, arg := range args {
        result[i] = fmt.Sprintf("Item %d: %v", i, arg)
    }
    return result
}, "process_all(*args) - Process all arguments")

// Usage in script:
// result = process_all(1, "hello", True, [1, 2, 3])
```

## Class Builder

### Basic Class

```go
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

### With Inheritance

```go
func createStudentClass() *object.Class {
    cb := object.NewClassBuilder("Student")

    // Set base class
    personClass := createPersonClass()
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
        return fmt.Sprintf("%s is studying %s at %s",
            name, subject, self.Fields["school"].AsString())
    }, "study(subject) - Study a subject")

    return cb.Build()
}
```

## Library Builder

### Basic Library

```go
func createMathLibrary() *object.Library {
    lb := object.NewLibraryBuilder("mymath", "Extended math library")

    // Add functions
    lb.FunctionWithHelp("add", func(a, b float64) float64 {
        return a + b
    }, "add(a, b) - Add two numbers")

    lb.FunctionWithHelp("subtract", func(a, b float64) float64 {
        return a - b
    }, "subtract(a, b) - Subtract b from a")

    lb.FunctionWithHelp("multiply", func(a, b float64) float64 {
        return a * b
    }, "multiply(a, b) - Multiply two numbers")

    lb.FunctionWithHelp("divide", func(a, b float64) float64 {
        if b == 0 {
            panic("division by zero")
        }
        return a / b
    }, "divide(a, b) - Divide a by b")

    // Add constants
    lb.Constant("PI", 3.14159265359)
    lb.Constant("E", 2.71828182846)

    return lb.Build()
}
```

### Library with Sub-Libraries

```go
func createDatabaseLibrary() *object.Library {
    lb := object.NewLibraryBuilder("database", "Database connectivity")

    // Main library functions
    lb.FunctionWithHelp("connect", func(host string, port int, database string) bool {
        // Connection logic
        return true
    }, "connect(host, port, database) - Connect to database")

    lb.Constant("DEFAULT_PORT", 5432)

    // Create sub-library for queries
    queryLib := object.NewLibraryBuilder("query", "Query operations")

    queryLib.FunctionWithHelp("select", func(table string, columns []string) []map[string]interface{} {
        // SELECT logic
        return []map[string]interface{}{}
    }, "select(table, columns) - Select from table")

    queryLib.FunctionWithHelp("insert", func(table string, data map[string]interface{}) int64 {
        // INSERT logic
        return 1
    }, "insert(table, data) - Insert into table")

    queryLib.FunctionWithHelp("update", func(table string, data map[string]interface{}, where string) int64 {
        // UPDATE logic
        return 1
    }, "update(table, data, where) - Update table")

    // Add sub-library
    lb.SubLibrary("query", queryLib.Build())

    // Create another sub-library for transactions
    txLib := object.NewLibraryBuilder("transaction", "Transaction management")

    txLib.FunctionWithHelp("begin", func() string {
        return "tx_12345"
    }, "begin() - Start transaction")

    txLib.FunctionWithHelp("commit", func(txId string) bool {
        return true
    }, "commit(tx_id) - Commit transaction")

    txLib.FunctionWithHelp("rollback", func(txId string) bool {
        return true
    }, "rollback(tx_id) - Rollback transaction")

    lb.SubLibrary("transaction", txLib.Build())

    return lb.Build()
}
```

### Library with Multiple Classes

Use `lb.Class()` to attach one or more classes to a library:

```go
func createHTTPLibrary() *object.Library {
    lb := object.NewLibraryBuilder("http", "HTTP utilities")

    // Create first class
    httpClientClass := object.NewClassBuilder("Client")
    httpClientClass.MethodWithHelp("__init__", func(self *object.Instance, baseURL string) {
        self.Fields["base_url"] = object.NewString(baseURL)
        self.Fields["headers"] = &object.Dict{Pairs: map[string]object.Object{}}
    }, "__init__(base_url) - Create HTTP client")

    httpClientClass.MethodWithHelp("get", func(self *object.Instance, path string) map[string]interface{} {
        baseURL, _ := self.Fields["base_url"].AsString()
        // ... HTTP GET logic
        return map[string]interface{}{
            "status": 200,
            "body":   "response from " + baseURL + path,
        }
    }, "get(path) - Make GET request")

    // Create second class
    responseClass := object.NewClassBuilder("Response")
    responseClass.MethodWithHelp("__init__", func(self *object.Instance, status int, body string) {
        self.Fields["status"] = object.NewInteger(int64(status))
        self.Fields["body"] = object.NewString(body)
    }, "__init__(status, body) - Create response")

    responseClass.MethodWithHelp("ok", func(self *object.Instance) bool {
        status, _ := self.Fields["status"].AsInt()
        return status >= 200 && status < 300
    }, "ok() - Check if response was successful")

    responseClass.MethodWithHelp("json", func(self *object.Instance) map[string]interface{} {
        // ... JSON parsing logic
        return map[string]interface{}{}
    }, "json() - Parse body as JSON")

    // Attach both classes to library
    lb.Class("Client", httpClientClass.Build())
    lb.Class("Response", responseClass.Build())

    // Add helper functions
    lb.FunctionWithHelp("get", func(url string) map[string]interface{} {
        return map[string]interface{}{
            "status": 200,
            "body":   "quick GET response",
        }
    }, "get(url) - Quick GET request")

    return lb.Build()
}
```

Usage from Scriptling:

```python
import http

# Use classes
client = http.Client("https://api.example.com")
response = client.get("/users")
print(response["status"])

resp = http.Response(200, '{"data": "test"}')
if resp.ok():
    data = resp.json()

# Use helper function
quick = http.get("https://example.com/api")
```

Usage:

```python
import database

# Connect
connected = database.connect("localhost", database.DEFAULT_PORT, "mydb")

# Query
users = database.query.select("users", ["id", "name"])
database.query.insert("users", {"name": "Alice"})

# Transaction
tx = database.transaction.begin()
database.query.insert("users", {"name": "Bob"})
database.transaction.commit(tx)
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

// Game library using builder
func createGameLibrary(playerClass *object.Class) *object.Library {
    lb := object.NewLibraryBuilder("game", "Game utilities")

    lb.FunctionWithHelp("create_enemy", func(name string, power int) map[string]interface{} {
        return map[string]interface{}{
            "name":  name,
            "power": power,
            "type":  "enemy",
        }
    }, "create_enemy(name, power) - Create an enemy")

    lb.FunctionWithHelp("calculate_damage", func(attackerPower int, defenderArmor int) int {
        damage := attackerPower - defenderArmor
        if damage < 1 {
            damage = 1
        }
        return damage
    }, "calculate_damage(attacker_power, defender_armor) - Calculate damage")

    lb.FunctionWithHelp("roll_dice", func(sides int) int {
        // Simplified - in real code use rand
        return sides / 2 + 1
    }, "roll_dice(sides) - Roll a dice")

    // Add class to library
    lb.Class("Player", playerClass)

    // Constants
    lb.Constant("MAX_LEVEL", 100)
    lb.Constant("BASE_HEALTH", 100)

    return lb.Build()
}

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Create and register
    playerClass := createPlayerClass()
    gameLib := createGameLibrary(playerClass)
    p.RegisterLibrary(gameLib)

    // Use from script
    p.Eval(`
import game

# Create player
hero = game.Player("Hero", game.BASE_HEALTH)

# Add items
hero.add_item("Sword")
hero.add_item("Shield")
hero.add_item("Health Potion")

# Combat
enemy = game.create_enemy("Goblin", 15)
damage = game.calculate_damage(enemy["power"], 5)
print(hero.take_damage(damage))

# Heal
print(hero.heal(20))

# Check status
status = hero.get_status()
print(f"Player: {status['name']}, Health: {status['health']}/{status['max_health']}")
print(f"Inventory: {status['inventory']}")
`)
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

## Best Practices

1. **Use builders for clarity** - Code is more readable and maintainable
2. **Always add help text** - Makes APIs discoverable
3. **Group related functions** - Use sub-libraries for organization
4. **Return meaningful types** - Use maps for complex returns
5. **Handle errors with panic** - Builder will convert to error objects

```go
// Good: Clear, documented function
lb.FunctionWithHelp("fetch", func(url string, timeout int) map[string]interface{} {
    if timeout <= 0 {
        panic("timeout must be positive")
    }
    // ... implementation
    return map[string]interface{}{
        "status": 200,
        "body":   "response",
    }
}, `fetch(url, timeout=30) - Fetch URL

Parameters:
  url - URL to fetch
  timeout - Timeout in seconds

Returns:
  {"status": int, "body": string}`)
```
