---
title: Language Guide
description: Complete reference for the Scriptling programming language.
weight: 3
---

Scriptling is a dynamically-typed, interpreted language with Python-inspired syntax designed for embedding in Go applications.

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
    raise "Invalid value"

# Assert
assert x > 0, "x must be positive"
```

### Classes

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return "Hello, my name is " + self.name

# Inheritance with super()
class Dog(Animal):
    def __init__(self, name, breed):
        super(Dog, self).__init__(name)
        self.breed = breed
```

### HTTP and JSON

```python
import json
import requests

# HTTP GET
options = {"timeout": 10, "headers": {"Authorization": "Bearer token"}}
resp = requests.get("https://api.example.com/data", options)
if resp.status_code == 200:
    data = json.loads(resp.body)

# HTTP POST
payload = {"name": "Alice"}
body = json.dumps(payload)
response = requests.post("https://api.example.com/users", body)
```

## Detailed Topics

{{< cards >}}
{{< card link="syntax" title="Syntax Rules" description="Indentation, comments, case sensitivity, multiline syntax" >}}
{{< card link="types" title="Data Types" description="Integers, floats, strings, booleans, lists, dicts, sets" >}}
{{< card link="operators" title="Operators" description="Arithmetic, comparison, boolean, bitwise, precedence" >}}
{{< card link="control-flow" title="Control Flow" description="Conditionals, loops, match statements, break/continue" >}}
{{< card link="functions" title="Functions" description="Definition, parameters, *args, **kwargs, lambdas" >}}
{{< card link="error-handling" title="Error Handling" description="try/except/finally, raise, assert, exception types" >}}
{{< card link="classes" title="Classes" description="Class definition, inheritance, super()" >}}
{{< card link="builtins" title="Built-in Functions" description="Type conversions, math, string, list, dict functions" >}}
{{< card link="slicing" title="Indexing & Slicing" description="Single index, slice notation, slice() builtin" >}}
{{< card link="http" title="HTTP & JSON" description="HTTP requests, response objects, JSON handling" >}}
{{< card link="python-differences" title="Python Differences" description="What's NOT supported, key differences from Python" >}}
{{< card link="performance" title="Performance Guide" description="String concatenation, recursion vs iteration, benchmarking" >}}
{{< /cards >}}

## Key Differences from Python

- No nested classes
- No multiple inheritance
- HTTP response is a Response object with `status_code`, `body`, `headers`, `url` fields
- Default HTTP timeout: 5 seconds
- Use `import library` to load libraries dynamically

## See Also

- [CLI Reference](../cli/) - Command-line interface documentation
- [Libraries](../libraries/) - Standard and extended library reference
- [Security Guide](../security/) - Security best practices
