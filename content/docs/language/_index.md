---
title: Language Guide
description: Complete reference for the Scriptling programming language.
weight: 2
---

Scriptling is a dynamically-typed, interpreted language with Python-inspired syntax.

## Syntax Rules

### Indentation

Scriptling uses **Python-style indentation** (4 spaces recommended) to define code blocks:

```python
if x > 5:
    print("yes")    # 4 spaces indent
    y = 10
```

### Comments

```python
# Single-line comments only
x = 5  # Inline comments supported
```

### Case Sensitivity

- Keywords: lowercase (`if`, `while`, `def`, `return`)
- Booleans: `True`, `False` (capitalized)
- Variables: case-sensitive (`myVar` ≠ `myvar`)

## Data Types

### Integer

```python
x = 42
y = -10
z = 0
```

### Float

```python
pi = 3.14
temp = -273.15
```

### String

```python
name = "Alice"
message = 'Hello'  # Single or double quotes
multi_line = """
This is a
multi-line string
"""
raw_string = r"\n\t"  # Raw string (escapes not processed)
```

### Boolean

```python
flag = True
done = False
```

### List

```python
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True]
nested = [1, [2, 3], 4]
empty = []
```

### Dictionary

```python
person = {"name": "Alice", "age": 30}
config = {"host": "localhost", "port": 8080}
empty = {}
```

### Set

```python
numbers = set([1, 2, 3])
unique = set([1, 2, 2, 3])  # {1, 2, 3}
empty = set()
```

## Operators

### Arithmetic

```python
x + y    # Addition
x - y    # Subtraction
x * y    # Multiplication
x ** y   # Exponentiation
x / y    # Division (always returns float)
x // y   # Floor division
x % y    # Modulo
```

### Comparison

```python
x == y   # Equal
x != y   # Not equal
x < y    # Less than
x > y    # Greater than
x <= y   # Less than or equal
x >= y   # Greater than or equal
```

### Boolean/Logical

```python
x and y  # Logical AND
x or y   # Logical OR
not x    # Logical NOT
```

### Bitwise

```python
~x       # Bitwise NOT
x & y    # Bitwise AND
x | y    # Bitwise OR
x ^ y    # Bitwise XOR
x << y   # Left shift
x >> y   # Right shift
```

### Chained Comparisons

```python
1 < x < 10        # Equivalent to: 1 < x and x < 10
18 <= age <= 65   # Working age check
```

## Control Flow

### If/Elif/Else

```python
if x > 10:
    print("large")
elif x > 5:
    print("medium")
else:
    print("small")
```

### While Loop

```python
counter = 0
while counter < 10:
    print(counter)
    counter += 1
```

### For Loop

```python
# Iterate over list
for item in [1, 2, 3]:
    print(item)

# Iterate over string
for char in "hello":
    print(char)

# Range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

### Loop Control

```python
# break - exit loop
for i in [1, 2, 3, 4, 5]:
    if i == 3:
        break
    print(i)  # Prints 1, 2

# continue - skip iteration
for i in [1, 2, 3, 4, 5]:
    if i == 3:
        continue
    print(i)  # Prints 1, 2, 4, 5
```

### Match Statement

```python
# Basic pattern matching
match status:
    case 200:
        print("Success")
    case 404:
        print("Not found")
    case _:
        print("Other")

# Type-based matching
match data:
    case int():
        print("Integer")
    case str():
        print("String")
    case list():
        print("List")

# Guard clauses
match value:
    case x if x > 100:
        print("Large")
    case x:
        print("Small")
```

## Functions

### Definition

```python
def add(a, b):
    return a + b

# Default parameters
def greet(name, greeting="Hello"):
    return greeting + ", " + name
```

### Keyword Arguments

```python
greet("World")  # Hello, World!
greet(name="Alice", greeting="Hi")  # Hi, Alice
```

### Variadic Arguments

```python
# *args collects positional arguments
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

sum_all(1, 2, 3)  # 6

# **kwargs collects keyword arguments
def test_kwargs(**kwargs):
    return kwargs

test_kwargs(a=1, b=2)  # {"a": 1, "b": 2}
```

### Lambda

```python
square = lambda x: x * 2
add = lambda a, b: a + b

# With sorted
sorted(["ccc", "a", "bb"], key=lambda s: len(s))
```

## Error Handling

### Try/Except/Finally

```python
try:
    result = risky_operation()
except:
    result = None
finally:
    cleanup()
```

### Raise

```python
if x < 0:
    raise "Value must be positive"
```

### Assert

```python
assert x > 0, "x must be positive"
```

## Classes

### Definition

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return "Hello, my name is " + self.name
```

### Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Generic sound"

class Dog(Animal):
    def __init__(self, name, breed):
        super(Dog, self).__init__(name)
        self.breed = breed

    def speak(self):
        return "Woof!"
```

## Built-in Functions

### Type Conversions

```python
str(42)       # "42"
int("42")     # 42
float("3.14") # 3.14
bool(0)       # False
list("abc")   # ["a", "b", "c"]
dict()        # {}
set([1,2,2])  # {1, 2}
```

### Math

```python
abs(-5)       # 5
min(3, 1, 2)  # 1
max(3, 1, 2)  # 3
round(3.7)    # 4
pow(2, 10)    # 1024
sum([1,2,3])  # 6
```

### String

```python
len("hello")              # 5
upper("hello")            # "HELLO"
lower("HELLO")            # "hello"
split("a,b,c", ",")       # ["a", "b", "c"]
join(["a", "b"], "-")     # "a-b"
replace("hello", "l", "L") # "heLLo"
strip("  hello  ")        # "hello"
```

### List

```python
len([1, 2, 3])    # 3
sorted([3, 1, 2]) # [1, 2, 3]
range(5)          # Iterator: 0, 1, 2, 3, 4
```

## Slicing

```python
nums = [0, 1, 2, 3, 4, 5]
nums[1:4]     # [1, 2, 3]
nums[:3]      # [0, 1, 2]
nums[3:]      # [3, 4, 5]
nums[::2]     # [0, 2, 4]
nums[::-1]    # [5, 4, 3, 2, 1, 0]
```

## Library Import

```python
import json
import requests

data = json.loads('{"key":"value"}')
response = requests.get("https://api.example.com")
```

## Differences from Python

- **Single Inheritance Only** - No multiple inheritance
- **No Nested Classes** - Classes must be at module level
- **Simplified Scope** - `nonlocal` and `global` work differently
- **Sandboxed** - No filesystem/network access unless enabled
- **HTTP Response** - Always `{"status": int, "body": string, "headers": dict}`
- **Default Timeout** - 5 seconds for HTTP requests
