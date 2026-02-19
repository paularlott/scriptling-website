---
title: Data Types
description: Integers, floats, strings, booleans, lists, dictionaries, sets, and tuples in Scriptling.
weight: 2
---

Scriptling supports several built-in data types for representing different kinds of data.

## Integer

Whole numbers without a decimal point:

```python
x = 42
y = -10
z = 0

# Large integers
big = 9223372036854775807  # Max int64

# Arithmetic
result = 10 + 5   # 15
result = 10 - 3   # 7
result = 10 * 3   # 30
result = 10 // 3  # 3 (floor division)
result = 10 % 3   # 1 (modulo)
```

## Float

Numbers with a decimal point:

```python
pi = 3.14
temp = -273.15
scientific = 1.5e10  # Scientific notation

# Arithmetic
result = 3.14 + 2.86  # 6.0
result = 10.0 / 4.0   # 2.5
result = 10.0 // 3.0  # 3.0 (floor division)

# Division always returns float
result = 10 / 4  # 2.5 (not 2)
```

## String

Text sequences enclosed in single or double quotes:

```python
name = "Alice"
message = 'Hello'

# Triple-quoted strings for multi-line text
multi_line = """
Line 1
Line 2
Line 3
"""

# Raw strings (escapes not processed)
raw = r"\n\t"  # Literal backslash-n and backslash-t

# String operations
greeting = "Hello, " + name  # Concatenation
repeat = "ab" * 3           # "ababab" (repetition)
length = len("hello")       # 5
```

## Boolean

True or False values:

```python
flag = True
done = False

# Comparison results
is_greater = 5 > 3   # True
is_equal = "a" == "b"  # False

# Logical operations
result = True and False  # False
result = True or False   # True
result = not True        # False
```

## List

Ordered, mutable sequences:

```python
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True]
nested = [1, [2, 3], 4]
empty = []

# Access by index (0-based)
first = numbers[0]    # 1
last = numbers[4]     # 5

# Slicing
subset = numbers[1:4]  # [2, 3, 4]

# Modification
numbers[0] = 10       # [10, 2, 3, 4, 5]

# Common operations
len(numbers)          # 5
numbers.append(6)     # Add to end
numbers.extend([7, 8]) # Add multiple
```

## Dictionary

Key-value pairs with string keys:

```python
person = {"name": "Alice", "age": 30}
config = {"host": "localhost", "port": 8080}
empty = {}

# Access by key
name = person["name"]    # "Alice"
age = person["age"]      # 30

# With default value
email = person.get("email", "none@example.com")

# Modification
person["email"] = "alice@example.com"  # Add/update
person["age"] = 31                      # Update existing

# Common operations
keys(person)      # ["name", "age", "email"]
values(person)    # ["Alice", 31, "alice@example.com"]
items(person)     # [["name", "Alice"], ["age", 31], ...]
```

## Set

Unordered collections of unique elements:

```python
numbers = set([1, 2, 3])
unique = set([1, 2, 2, 3])  # {1, 2, 3}
empty = set()

# Set operations
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])

s1.union(s2)                # {1, 2, 3, 4}
s1.intersection(s2)         # {2, 3}
s1.difference(s2)           # {1}

# Modification
s1.add(5)
s1.remove(1)
s1.discard(99)  # No error if not found
```

## Tuple

Immutable ordered sequences:

```python
coords = (10, 20)
single = (42,)  # Single element tuple needs trailing comma
nested = ((1, 2), (3, 4))

# Access by index
x = coords[0]  # 10
y = coords[1]  # 20

# Cannot modify - tuples are immutable
# coords[0] = 5  # Error!

# Tuple unpacking
x, y = coords
a, b, c = (1, 2, 3)
```

## None

Represents the absence of a value:

```python
result = None

# Returned by functions with no explicit return
def do_nothing():
    pass

result = do_nothing()  # None

# Default value pattern
value = data.get("key")  # Returns None if key missing
if value is None:
    value = "default"
```

## Type Checking

```python
# type() function returns type name as string
type(42)        # "INTEGER"
type(3.14)      # "FLOAT"
type("hello")   # "STRING"
type([1, 2])    # "LIST"
type({"a": 1})  # "DICT"
type(True)      # "BOOLEAN"
type(None)      # "NONE"
type((1, 2))    # "TUPLE"

# isinstance() checks type
isinstance(42, "int")       # True
isinstance("hello", "str")  # True
isinstance([1, 2], "list")  # True

# .type() method on any object
x = 42
x.type()  # "INTEGER"
```

## Type Conversion

```python
# To string
str(42)      # "42"
str(3.14)    # "3.14"
str(True)    # "True"

# To integer
int("42")    # 42
int(3.14)    # 3 (truncates)
int(-3.9)    # -3 (truncates toward zero)

# To float
float("3.14")  # 3.14
float(42)      # 42.0

# To boolean
bool(0)        # False
bool(1)        # True
bool("")       # False
bool("hello")  # True
bool([])       # False
bool([1])      # True

# To list
list("abc")    # ["a", "b", "c"]
list((1, 2))   # [1, 2]

# To tuple
tuple([1, 2])  # (1, 2)

# To set
set([1, 2, 2, 3])  # {1, 2, 3}
```

## See Also

- [Operators](./operators/) - Operations on different types
- [Built-in Functions](./builtins/) - Type conversion and checking functions
- [Slicing](./slicing/) - Indexing and slicing operations
