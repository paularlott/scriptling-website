---
title: Built-in Functions
description: Type conversions, math, string, list, and dictionary built-in functions in Scriptling.
weight: 8
---

Scriptling provides many built-in functions that are always available without importing.

## Type Conversions

### str()

Convert any value to a string:

```python
str(42)       # "42"
str(3.14)     # "3.14"
str(True)     # "True"
str([1, 2])   # "[1, 2]"
str({"a": 1}) # '{"a": 1}'
```

### int()

Convert to integer:

```python
int("42")     # 42
int(3.14)     # 3 (truncates toward zero)
int(-3.9)     # -3 (truncates toward zero)
int(42)       # 42 (no change)
```

### float()

Convert to float:

```python
float("3.14") # 3.14
float(42)     # 42.0
float("42")   # 42.0
```

### bool()

Convert to boolean:

```python
bool(0)        # False
bool(1)        # True
bool("")       # False
bool("hello")  # True
bool([])       # False
bool([1])      # True
bool({})       # False
bool(None)     # False
```

### list()

Convert to list:

```python
list("abc")       # ["a", "b", "c"]
list((1, 2, 3))   # [1, 2, 3]
list({1, 2, 3})   # [1, 2, 3] (order not guaranteed)
list(range(3))    # [0, 1, 2]
```

### tuple()

Convert to tuple:

```python
tuple([1, 2, 3])  # (1, 2, 3)
tuple("ab")       # ('a', 'b')
tuple(range(3))   # (0, 1, 2)
```

### set()

Create a set from an iterable:

```python
set([1, 2, 2, 3])  # {1, 2, 3}
set("hello")       # {'h', 'e', 'l', 'o'}
set()              # Empty set
```

### dict()

Create a dictionary:

```python
dict()  # {}
```

## Type Checking

### type()

Get the type name as a string:

```python
type(42)        # "INTEGER"
type(3.14)      # "FLOAT"
type("hello")   # "STRING"
type([1, 2])    # "LIST"
type({"a": 1})  # "DICT"
type(True)      # "BOOLEAN"
type(None)      # "NONE"
type((1, 2))    # "TUPLE"
```

### .type() Method

All objects support the `.type()` method:

```python
x = 42
x.type()  # "INTEGER"

y = "hello"
y.type()  # "STRING"
```

### isinstance()

Check if a value is of a specific type:

```python
isinstance(42, "int")         # True
isinstance(3.14, "float")     # True
isinstance("hello", "str")    # True
isinstance([1, 2], "list")    # True
isinstance({"a": 1}, "dict")  # True
isinstance(True, "bool")      # True
isinstance(None, "NoneType")  # True
isinstance((1, 2), "tuple")   # True
```

### callable()

Check if a value can be called as a function:

```python
callable(len)             # True
callable(lambda x: x)     # True
callable(42)              # False
callable("hello")         # False
```

## Math Functions

```python
abs(-5)                   # 5
min(3, 1, 2)              # 1
max(3, 1, 2)              # 3
round(3.7)                # 4
round(3.14159, 2)         # 3.14
pow(2, 10)                # 1024
pow(2, 10, 1000)          # 24 (modular: 2^10 % 1000)
divmod(17, 5)             # (3, 2) - returns (quotient, remainder)
sum([1, 2, 3, 4, 5])      # 15
sum([1.5, 2.5, 3.0])      # 7.0
```

## Number Formatting

```python
hex(255)                  # "0xff"
hex(-255)                 # "-0xff"
bin(10)                   # "0b1010"
bin(-10)                  # "-0b1010"
oct(8)                    # "0o10"
oct(-8)                   # "-0o10"
```

## Character Conversion

```python
chr(65)                   # "A"
chr(97)                   # "a"
ord("A")                  # 65
ord("a")                  # 97
```

## String Functions

```python
len("hello")                        # 5
upper("hello")                      # "HELLO"
lower("HELLO")                      # "hello"
capitalize("hello world")           # "Hello world"
title("hello world")                # "Hello World"
split("a,b,c", ",")                 # ["a", "b", "c"]
join(["a", "b", "c"], "-")          # "a-b-c"
replace("hello world", "world", "python")  # "hello python"
strip("  hello  ")                  # "hello"
strip("??hello??", "?")             # "hello"
lstrip("  hello  ")                 # "hello  "
lstrip("??hello", "?")              # "hello"
rstrip("  hello  ")                 # "  hello"
rstrip("hello??", "?")              # "hello"
startswith("hello", "he")           # True
endswith("hello", "lo")             # True
```

## String Methods

```python
s = "hello world"
s.find("world")                    # 6 (index of substring, -1 if not found)
s.index("world")                   # 6 (like find, raises error if not found)
s.count("o")                       # 2 (count occurrences)

# String formatting
"Hello, {}!".format("World")       # "Hello, World!"
"{} + {} = {}".format(1, 2, 3)     # "1 + 2 = 3"

# Character type checks
"123".isdigit()                    # True
"abc".isalpha()                    # True
"abc123".isalnum()                 # True
"   ".isspace()                    # True
"HELLO".isupper()                  # True
"hello".islower()                  # True

# Case conversion
"Hello World".swapcase()           # "hELLO wORLD"

# Splitting and partitioning
"hello\nworld".splitlines()        # ["hello", "world"]
"hello-world".partition("-")       # ("hello", "-", "world")
"a-b-c".rpartition("-")            # ("a-b", "-", "c")

# Prefix/suffix removal
"TestCase".removeprefix("Test")    # "Case"
"file.py".removesuffix(".py")      # "file"

# Encoding
"ABC".encode()                     # [65, 66, 67] (byte values)

# Padding and alignment
"42".zfill(5)                      # "00042"
"-42".zfill(5)                     # "-0042"
"hi".center(6)                     # "  hi  "
"hi".center(7, "*")                # "**hi***"
"hi".ljust(5)                      # "hi   "
"hi".rjust(5)                      # "   hi"
```

## List Functions

```python
len([1, 2, 3])                     # 3

# append modifies list in-place
my_list = [1, 2]
my_list.append(3)                  # my_list is now [1, 2, 3]

# extend modifies list in-place
list_a = [1, 2]
list_b = [3, 4]
list_a.extend(list_b)              # list_a is now [1, 2, 3, 4]

# sorted returns a new sorted list
sorted([3, 1, 4, 1, 5])            # [1, 1, 3, 4, 5]
sorted(["banana", "apple"])        # ["apple", "banana"]
sorted([3, 1, 2], reverse=True)    # [3, 2, 1]

# sorted with key function
sorted(["ccc", "a", "bb"], key=lambda s: len(s))  # ["a", "bb", "ccc"]
sorted([1, 2, 3], key=lambda x: -x)               # [3, 2, 1]
```

## List Methods

```python
lst = [10, 20, 30, 20, 40]
lst.index(20)                      # 1 (first index of value)
lst.count(20)                      # 2 (count occurrences)

lst = [1, 2, 3, 4, 5]
lst.pop()                          # 5 (removes and returns last element)
lst.pop(0)                         # 1 (removes and returns element at index)

lst = [1, 2, 4, 5]
lst.insert(2, 3)                   # lst is now [1, 2, 3, 4, 5]

lst = [1, 2, 3, 2, 4]
lst.remove(2)                      # lst is now [1, 3, 2, 4] (removes first occurrence)

lst = [1, 2, 3]
lst.clear()                        # lst is now []

original = [1, 2, 3]
copied = original.copy()           # shallow copy

lst = [1, 2, 3, 4, 5]
lst.reverse()                      # lst is now [5, 4, 3, 2, 1]
```

## Set Methods

```python
s = set([1, 2])
s.add(3)            # s is now {1, 2, 3}
s.remove(2)         # s is now {1, 3}
s.discard(99)       # No error if element not found
s.pop()             # Removes and returns arbitrary element
s.clear()           # Removes all elements
s.copy()            # Returns a shallow copy

# Set operations
s1 = set([1, 2])
s2 = set([2, 3])
s1.union(s2)                # {1, 2, 3}
s1.intersection(s2)         # {2}
s1.difference(s2)           # {1}
s1.symmetric_difference(s2) # {1, 3}
s1.issubset(s2)             # False
s1.issuperset(s2)           # False
```

## Dictionary Functions

```python
person = {"name": "Alice", "age": 30}

len(person)                        # 2
keys(person)                       # ["name", "age"]
values(person)                     # ["Alice", 30]
items(person)                      # [["name", "Alice"], ["age", 30]]

# Iterate over dictionary
for item in items(person):
    key = item[0]
    value = item[1]
    print(key, value)
```

## Dict Methods

```python
d = {"a": 1, "b": 2, "c": 3}
d.get("a")                         # 1
d.get("x")                         # None
d.get("x", "default")              # "default"

d = {"a": 1, "b": 2, "c": 3}
d.pop("b")                         # 2 (removes and returns value)
d.pop("x", "not found")            # "not found" (with default)

d1 = {"a": 1, "b": 2}
d2 = {"b": 20, "c": 3}
d1.update(d2)                      # d1 is now {"a": 1, "b": 20, "c": 3}

d = {"a": 1, "b": 2}
d.clear()                          # d is now {}

original = {"a": 1, "b": 2}
copied = original.copy()           # shallow copy

d = {"a": 1}
d.setdefault("a", 100)             # 1 (returns existing value)
d.setdefault("b", 200)             # 200 (sets and returns new value)
```

## Iteration Utilities

```python
# These return iterators (lazy evaluation)
enumerate(["a", "b"])              # Iterator: (0, "a"), (1, "b")
zip([1, 2], ["a", "b"])            # Iterator: (1, "a"), (2, "b")
reversed([1, 2, 3])                # Iterator: 3, 2, 1
map(lambda x: x*2, [1, 2, 3])      # Iterator: 2, 4, 6
filter(lambda x: x > 1, [1, 2, 3]) # Iterator: 2, 3

# Convert to list if needed
list(enumerate(["a", "b"]))       # [[0, "a"], [1, "b"]]
list(zip([1, 2], ["a", "b"]))     # [[1, "a"], [2, "b"]]

# Boolean tests (work with any iterable)
any([False, True, False])         # True
all([True, True, True])           # True
all([True, False, True])          # False
```

## Range Function

```python
# range() returns an iterator (lazy evaluation)
range(5)                           # Iterator: 0, 1, 2, 3, 4
range(2, 7)                        # Iterator: 2, 3, 4, 5, 6
range(0, 10, 2)                    # Iterator: 0, 2, 4, 6, 8
range(10, 0, -2)                   # Iterator: 10, 8, 6, 4, 2

# Convert to list if needed
list(range(5))                     # [0, 1, 2, 3, 4]

# Use in for loops (iterators work directly)
for i in range(5):
    print(i)
```

## I/O Functions

```python
print(value)                       # Print to stdout
print("Hello", name)               # Multiple arguments
print("Hello", "World", sep="-")   # Custom separator: Hello-World

input("Prompt: ")                  # Read user input (returns string)
```

## See Also

- [Data Types](./types/) - Available data types
- [Slicing](./slicing/) - Indexing and slicing operations
- [String Library](../libraries/stdlib/string/) - String constants
