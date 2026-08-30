---
description: Embed Scriptling in a Go application to evaluate business rules at runtime.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/tutorials/embedding-rules-engine/
sources:
    - resource: https://scriptling.dev/docs/tutorials/embedding-rules-engine/
status: stable
tags:
    - tutorials
    - embedding
    - go
title: Embedding a Rules Engine
type: Guide
---
# Embedding a Rules Engine

This tutorial walks through embedding Scriptling in a Go application to create a dynamic rules engine. You'll set up an interpreter, exchange variables, register custom functions, and evaluate user-defined rules.

## Prerequisites

- Go 1.26 or later
- Basic familiarity with Go modules

## Step 1: Project Setup

Create a new Go project:

```bash
mkdir rules-engine
cd rules-engine
go mod init example.com/rules-engine
go get github.com/paularlott/scriptling
```

Create `main.go`:

```go
package main

import (
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    result, err := p.Eval(`print("Rules engine ready")`)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    _ = result
}
```

Run it:

```bash
go run main.go
```

Output:

```
Rules engine ready
```

## Step 2: Pass Data to Scripts

Pass order data from Go into the script and evaluate a simple rule:

```go
package main

import (
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Pass order data from Go
    p.SetVar("order_amount", 1500.0)
    p.SetVar("customer_tier", "gold")
    p.SetVar("is_first_purchase", false)

    // Evaluate discount rule
    result, err := p.Eval(`
discount = 0

# Base discount by tier
if customer_tier == "gold":
    discount = 0.15
elif customer_tier == "silver":
    discount = 0.10
else:
    discount = 0.05

# First purchase bonus
if is_first_purchase:
    discount = discount + 0.05

# Bulk order bonus
if order_amount > 1000:
    discount = discount + 0.05

# Cap at 30%
if discount > 0.30:
    discount = 0.30

discount_amount = order_amount * discount
final_price = order_amount - discount_amount
`)

    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    _ = result

    // Read results back in Go
    discount, _ := p.GetVarAsFloat("discount")
    finalPrice, _ := p.GetVarAsFloat("final_price")

    fmt.Printf("Discount:    %.0f%%\n", discount*100)
    fmt.Printf("Final Price: $%.2f\n", finalPrice)
}
```

Output:

```
Discount:    20%
Final Price: $1200.00
```

## Step 3: Register Custom Go Functions

Expose Go functions to the script for data lookups:

```go
package main

import (
    "context"
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Mock customer database
    customers := map[string]map[string]interface{}{
        "alice": {"tier": "gold", "orders": 15, "total_spent": 12500.0},
        "bob":   {"tier": "silver", "orders": 3, "total_spent": 450.0},
        "carol": {"tier": "bronze", "orders": 1, "total_spent": 75.0},
    }

    // Register a lookup function
    p.RegisterFunc("lookup_customer", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        if len(args) < 1 {
            return &object.Error{Message: "lookup_customer requires a name"}
        }
        name, err := args[0].AsString()
        if err != nil {
            return err
        }
        customer, exists := customers[name]
        if !exists {
            return &object.Error{Message: fmt.Sprintf("customer not found: %s", name)}
        }
        return object.NewStringDict(map[string]object.Object{
            "tier":        object.NewString(customer["tier"].(string)),
            "orders":      object.NewInteger(int64(customer["orders"].(int))),
            "total_spent": object.NewFloat(customer["total_spent"].(float64)),
        })
    }, "lookup_customer(name) - Look up a customer by name")

    // Register a logging function
    p.RegisterFunc("log_action", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        message, _ := args[0].AsString()
        fmt.Printf("[LOG] %s\n", message)
        return &object.Null{}
    }, "log_action(message) - Log an action")

    // Evaluate rule that uses custom functions
    result, err := p.Eval(`
# Look up customer
customer = lookup_customer("alice")

tier = customer["tier"]
spent = customer["total_spent"]

# Determine loyalty bonus
if tier == "gold" and spent > 10000:
    bonus = "platinum_upgrade"
elif tier == "silver" and spent > 500:
    bonus = "gold_upgrade"
else:
    bonus = "maintain"

log_action("Customer tier: " + tier + ", bonus: " + bonus)
`)

    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    bonus, _ := p.GetVarAsString("bonus")
    fmt.Println("Result:", bonus)
    _ = result
}
```

Output:

```
[LOG] Customer tier: gold, bonus: platinum_upgrade
Result: platinum_upgrade
```

## Step 4: Load Rules from Files

Load rule definitions from external files so rules can be updated without recompiling:

Create `rules/discount.py`:

```python
# Discount rule: calculates the discount for an order
# Inputs: order_amount (float), customer_tier (string), is_first_purchase (bool)

discount = 0

if customer_tier == "gold":
    discount = 0.15
elif customer_tier == "silver":
    discount = 0.10
else:
    discount = 0.05

if is_first_purchase:
    discount = discount + 0.05

if order_amount > 1000:
    discount = discount + 0.05

if discount > 0.30:
    discount = 0.30

discount_amount = order_amount * discount
final_price = order_amount - discount_amount
```

Update `main.go` to load rules from files:

```go
package main

import (
    "fmt"
    "os"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
)

func evalRule(p *scriptling.Scriptling, ruleFile string) error {
    script, err := os.ReadFile(ruleFile)
    if err != nil {
        return fmt.Errorf("loading rule: %w", err)
    }

    _, err = p.Eval(string(script))
    return err
}

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Set input variables
    p.SetVar("order_amount", 750.0)
    p.SetVar("customer_tier", "silver")
    p.SetVar("is_first_purchase", true)

    // Load and evaluate the rule file
    err := evalRule(p, "rules/discount.py")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }

    // Read results
    discount, _ := p.GetVarAsFloat("discount")
    finalPrice, _ := p.GetVarAsFloat("final_price")

    fmt.Printf("Discount:    %.0f%%\n", discount*100)
    fmt.Printf("Final Price: $%.2f\n", finalPrice)
}
```

## Step 5: Use the Builder API for Type Safety

For production code, use the Builder API for type-safe function registration:

```go
package main

import (
    "context"
    "fmt"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // Build a library with native functions
    lib := object.NewLibraryBuilder("inventory", "Inventory functions")

    lib.FunctionWithHelp("check_stock", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        sku, err := args[0].AsString()
        if err != nil {
            return err
        }
        // Simulate stock check
        stock := map[string]int64{
            "widget-001": 42,
            "widget-002": 0,
            "widget-003": 7,
        }
        return object.NewInteger(stock[sku])
    }, "check_stock(sku) - Check stock level for a product SKU")

    lib.FunctionWithHelp("calculate_shipping", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
        weight, _ := args[0].(*object.Float).FloatValue()
        zone, _ := args[1].AsString()
        rates := map[string]float64{
            "domestic":     5.99,
            "international": 24.99,
        }
        base := rates[zone]
        return object.NewFloat(base + (weight * 0.50))
    }, "calculate_shipping(weight, zone) - Calculate shipping cost based on weight and zone")

    // Register the library
    p.RegisterLibrary(lib.Build())

    // Use it in a script
    _, err := p.Eval(`
import inventory

sku = "widget-001"
stock = inventory.check_stock(sku)
shipping = inventory.calculate_shipping(2.5, "domestic")

print(f"Stock for {sku}: {stock}")
print(f"Shipping: ${shipping:.2f}")
`)

    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

## What You Learned

- Creating a Scriptling interpreter in Go
- Exchanging variables between Go and Scriptling
- Registering custom Go functions for scripts to call
- Loading rules from external files
- Using the Builder API for type-safe function registration

## See Also

- [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md) - Complete interpreter setup guide
- [Native Functions](https://scriptling.dev/okf/scriptling-docs/go-integration/native-functions.md) - Direct function registration
- [Builder Functions](https://scriptling.dev/okf/scriptling-docs/go-integration/builder-functions.md) - Type-safe builder API
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - Registering libraries
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Sandboxing and security best practices
