---
description: Reference for the Scriptling language - syntax, data types, operators, control flow, functions, classes, and built-in functions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/
sources:
    - resource: https://scriptling.dev/reference/
status: stable
tags:
    - reference
title: Language Guide
type: Reference
---
# Language Guide

Scriptling is a dynamically-typed, interpreted language with Python-inspired syntax designed for embedding in Go applications.

## Choose a reference path

- **Learning Scriptling:** Read the quick reference below, then follow the detailed language topics in order as needed.
- **Looking up an API:** Go directly to [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md) or the [Library Reference](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md).
- **Adding database access:** Browse the [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/databases.md) for drivers and the ORM.
- **Using a runtime or host feature:** See the [CLI Guide](https://scriptling.dev/okf/scriptling-docs/cli.md), [Go Integration](https://scriptling.dev/okf/scriptling-docs/go-integration.md), or [Plugins](https://scriptling.dev/okf/scriptling-docs/plugins.md) rather than treating it as language syntax.

## Quick Reference

### Variables and Types

```python
# Variables
x = 10
name = "Alice"
price = 3.14

# Booleans and None
flag = True
done = False
result = None

# Lists and Dictionaries
nums = [1, 2, 3]
data = {"key": "value"}
first = nums[0]
val = data["key"]

# Sets
numbers = set([1, 2, 3])
unique = set([1, 2, 2, 3])  # {1, 2, 3}
```

### Operators

```python
# Arithmetic
+, -, *, /, //, %, **

# Comparison
==, !=, <, >, <=, >=

# Boolean/Logical
and, or, not

# Bitwise
&, |, ^, ~, <<, >>

# Augmented Assignment
+=, -=, *=, /=, //=, %=, &=, |=, ^=, <<=, >>=

# Chained comparisons
1 < x < 10        # Equivalent to: 1 < x and x < 10
```

### Control Flow

```python
# If/Elif/Else
if x > 10:
    print("large")
elif x > 5:
    print("medium")
else:
    print("small")

# While Loop
while x > 0:
    x -= 1

# For Loop
for item in [1, 2, 3]:
    if item == 2:
        continue  # Skip 2
    print(item)

# Match statement (pattern matching)
match status:
    case 200:
        print("Success")
    case 404:
        print("Not found")
    case _:
        print("Other")
```

### Functions

```python
# Definition
def add(a, b):
    return a + b

# Default parameters
def greet(name, greeting="Hello"):
    return greeting + ", " + name

# Variadic arguments (*args)
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

# Keyword arguments collection (**kwargs)
def test_kwargs(**kwargs):
    return kwargs

result = test_kwargs(a=1, b=2)  # {"a": 1, "b": 2}

# Keyword-only parameters
def resize(image, *, width, height=100):
    return image + ": " + str(width) + "x" + str(height)

# Lambda
square = lambda x: x * 2
sorted(["ccc", "a", "bb"], key=lambda s: len(s))
```

### Error Handling

```python
# Try/Except/Finally
try:
    result = risky_operation()
except:
    result = None
finally:
    cleanup()

# Raise errors
if x < 0:
    raise ValueError("Invalid value")

# Assert
assert x > 0, "x must be positive"
```

### Modules and `__name__`

```python
# __name__ is "__main__" when run directly, module name when imported
if __name__ == "__main__":
    print("Running as main script")
```

## Detailed Topics

- [Syntax Rules](https://scriptling.dev/okf/scriptling-reference/syntax.md) - Indentation, comments, case sensitivity, multiline syntax

- [Data Types](https://scriptling.dev/okf/scriptling-reference/types.md) - Integers, floats, strings, booleans, lists, dicts, sets

- [Operators](https://scriptling.dev/okf/scriptling-reference/operators.md) - Arithmetic, comparison, boolean, bitwise, precedence

- [Control Flow](https://scriptling.dev/okf/scriptling-reference/control-flow.md) - Conditionals, loops, match statements, break/continue

- [Functions](https://scriptling.dev/okf/scriptling-reference/functions.md) - Definition, parameters, *args, **kwargs, lambdas

- [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md) - try/except/finally, raise, assert, exception types

- [Decorators](https://scriptling.dev/okf/scriptling-reference/decorators.md) - Wrapping functions and classes, factories with arguments, stacking

- [Classes](https://scriptling.dev/okf/scriptling-reference/classes.md) - Class definition, inheritance, super()

- [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md) - Type conversions, math, string, list, dict functions

- [Indexing & Slicing](https://scriptling.dev/okf/scriptling-reference/slicing.md) - Single index, slice notation, slice() builtin

- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Standard, Scriptling, and extended library reference

- [Python Differences](https://scriptling.dev/okf/scriptling-reference/python-differences.md) - What's NOT supported, key differences from Python

- [Performance Guide](https://scriptling.dev/okf/scriptling-reference/performance.md) - String concatenation, recursion vs iteration, benchmarking


## Key Differences from Python

- No nested classes
- No multiple inheritance
- Use `import library` to load libraries dynamically

## See Also

- [Quick Start](https://scriptling.dev/okf/scriptling-docs/quick-start.md) - Get started with CLI or embedding
- [Go Integration](https://scriptling.dev/okf/scriptling-docs/go-integration.md) - Embedding Scriptling in Go
- [CLI Guide](https://scriptling.dev/okf/scriptling-docs/cli.md) - Command-line interface documentation
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security best practices
