---
title: Builder Libraries
description: Type-safe library builder with functions, constants, and sub-libraries.
weight: 2
---

Create type-safe libraries with functions, constants, and sub-libraries using the Library Builder.

## Basic Library

```go
import "github.com/paularlott/scriptling/object"

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

// Register
p.RegisterLibrary(createMathLibrary())

// Use from script:
// import mymath
// result = mymath.add(10, 20)
// pi = mymath.PI
```

## Adding Constants

```go
lb.Constant("VERSION", "1.0.0")
lb.Constant("MAX_CONNECTIONS", 100)
lb.Constant("DEBUG_MODE", true)
lb.Constant("DEFAULT_TIMEOUT", 30.5)
```

## Sub-Libraries

Organize functionality into sub-libraries:

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

## Library with Classes

Use `lb.Class()` to attach classes to a library:

```go
func createHTTPLibrary() *object.Library {
    lb := object.NewLibraryBuilder("http", "HTTP utilities")

    // Create first class
    httpClientClass := object.NewClassBuilder("Client")
    httpClientClass.MethodWithHelp("__init__", func(self *object.Instance, baseURL string) {
        self.Fields["base_url"] = object.NewString(baseURL)
        self.Fields["headers"] = object.NewStringDict(map[string]object.Object{})
    }, "__init__(base_url) - Create HTTP client")

    httpClientClass.MethodWithHelp("get", func(self *object.Instance, path string) map[string]interface{} {
        baseURL, _ := self.Fields["base_url"].AsString()
        // ... HTTP GET logic
        return map[string]interface{}{
            "status": 200,
            "body":   "response from " + baseURL + path,
        }
    }, "get(path) - Make GET request")

    // Attach class to library
    lb.Class("Client", httpClientClass.Build())

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

Usage:

```python
import http

# Use class
client = http.Client("https://api.example.com")
response = client.get("/users")
print(response["status"])

# Use helper function
quick = http.get("https://example.com/api")
```

## Builder Methods Reference

| Method | Description |
|--------|-------------|
| `Function(name, fn)` | Register a typed Go function |
| `FunctionWithHelp(name, fn, help)` | Register with help text |
| `Constant(name, value)` | Register a constant value |
| `SubLibrary(name, lib)` | Add a sub-library |
| `FunctionFromVariadic(name, fn)` | Register a variadic function |
| `Alias(alias, original)` | Create an alias for an existing function |
| `Class(name, class)` | Attach a class to the library |
| `Build()` | Create and return the Library |
| `Clear()` | Remove all registered functions and constants |
| `Merge(other)` | Merge another builder's functions and constants |

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

## See Also

- [Builder Functions](functions/) - Type-safe function builder
- [Builder Classes](classes/) - Type-safe class builder
- [Native Libraries](../native/libraries/) - Direct control with maximum performance
