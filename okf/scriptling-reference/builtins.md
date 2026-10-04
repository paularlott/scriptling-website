---
description: Every Scriptling built-in function, A to Z, with type conversion, math, string, list, dictionary, attribute and iteration functions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/builtins/
sources:
    - resource: https://scriptling.dev/reference/builtins/
status: stable
tags:
    - reference
    - builtins
    - abs
    - all
    - any
    - append
    - bin
    - bool
    - bytes
    - callable
    - chr
    - copy
    - delattr
    - dict
    - dir
    - divmod
    - enumerate
    - filter
    - float
    - format
    - getattr
    - hasattr
    - hash
    - help
    - hex
    - id
    - int
    - isinstance
    - issubclass
    - items
    - iter
    - keys
    - len
    - list
    - map
    - max
    - min
    - next
    - oct
    - ord
    - pow
    - print
    - range
    - repr
    - reversed
    - round
    - set
    - setattr
    - slice
    - sorted
    - sort
    - str
    - sum
    - tuple
    - type
    - values
    - yield_now
    - zip
title: Built-in Functions
type: Reference
---
# Built-in Functions

Scriptling provides many built-in functions that are always available without importing.

## All Built-ins A–Z

| Function | Purpose |
|---|---|
| [`abs(x)`](#math-functions) | Absolute value |
| [`all(iterable)`](#iteration-utilities) | True if every item is truthy |
| [`any(iterable)`](#iteration-utilities) | True if any item is truthy |
| [`append(list, x)`](#list-functions) | Function form of `list.append` |
| [`bin(n)`](#number-formatting) | Binary string, `"0b1010"` |
| [`bool(x)`](#bool) | Convert to `True`/`False` |
| [`bytes(...)`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) | Immutable byte string |
| [`callable(x)`](#callable) | True if `x` can be called |
| [`chr(n)`](#character-conversion) | Character for a code point |
| [`classmethod`](https://scriptling.dev/okf/scriptling-reference/classes/decorators.md#classmethod) | Decorator for class methods |
| [`copy(x)`](#copy) | Shallow copy |
| [`delattr(obj, name)`](#object-and-attribute-functions) | Delete an attribute |
| [`dict(...)`](#dict) | Create a dictionary |
| [`dir([obj])`](#dir) | Names defined on an object, or all builtins |
| [`divmod(a, b)`](#math-functions) | `(quotient, remainder)` |
| [`enumerate(iterable, start=0)`](#iteration-utilities) | Pairs of `(index, item)` |
| [`filter(fn, iterable)`](#iteration-utilities) | Items for which `fn` is truthy |
| [`float(x)`](#float) | Convert to float |
| [`format(value, spec)`](#object-and-attribute-functions) | Format one value, as in an f-string |
| [`frozenset([iterable])`](#frozenset) | Immutable, hashable set |
| [`getattr(obj, name[, default])`](#object-and-attribute-functions) | Read an attribute by name |
| [`hasattr(obj, name)`](#object-and-attribute-functions) | True if the attribute exists |
| [`hash(x)`](#object-and-attribute-functions) | Hash value of a hashable object |
| [`help([name])`](#object-and-attribute-functions) | Show help for a function or library |
| [`hex(n)`](#number-formatting) | Hexadecimal string, `"0xff"` |
| [`id(x)`](#object-and-attribute-functions) | Identity of an object |
| [`int(x[, base])`](#int) | Convert to integer |
| [`isinstance(x, type)`](#isinstance) | Type check, including subclasses |
| [`issubclass(cls, base)`](#issubclass) | Class inheritance check |
| [`items(d), keys(d), values(d)`](#dictionary-functions) | Function forms of the dict view methods |
| [`iter(x), next(it[, default])`](#iterator-protocol) | Create and advance iterators |
| [`len(x)`](#list-functions) | Number of items |
| [`list(iterable)`](#list) | Create a list |
| [`map(fn, iterable, ...)`](#iteration-utilities) | Apply `fn` to each item |
| [`max(...), min(...)`](#math-functions) | Largest / smallest, with `key=` and `default=` |
| [`oct(n)`](#number-formatting) | Octal string, `"0o10"` |
| [`ord(c)`](#character-conversion) | Code point of a character |
| [`pow(x, y[, mod])`](#math-functions) | Power, optionally modular |
| [`print(*values, sep=" ")`](#io-functions) | Write to standard output |
| [`property`](https://scriptling.dev/okf/scriptling-reference/classes/decorators.md#property) | Decorator for computed attributes |
| [`range(...)`](#range-function) | Lazy sequence of integers |
| [`repr(x)`](#object-and-attribute-functions) | Developer representation, strings quoted |
| [`reversed(seq)`](#iteration-utilities) | Iterate in reverse |
| [`round(x[, digits])`](#math-functions) | Round half to even |
| [`sentinel(name, *, repr=None)`](#sentinel) | Unique marker value, equal only to itself |
| [`set(iterable)`](#set) | Create a set |
| [`setattr(obj, name, value)`](#object-and-attribute-functions) | Set an attribute by name |
| [`slice(start, stop[, step])`](../slicing/#the-slice-builtin) | Slice object for indexing |
| [`sorted(iterable, key=, reverse=)`](#list-functions) | New sorted list |
| [`staticmethod`](https://scriptling.dev/okf/scriptling-reference/classes/decorators.md#staticmethod) | Decorator for static methods |
| [`str(x)`](#str) | Convert to string |
| [`sum(iterable[, start])`](#math-functions) | Sum of items |
| [`super()`](https://scriptling.dev/okf/scriptling-reference/classes.md#the-super-function) | Call the parent class |
| [`tuple(iterable)`](#tuple) | Create a tuple |
| [`type(x)`](#type) | Type name of a value |
| [`yield_now()`](#yield_now) | Let other tasks run |
| [`zip(*iterables)`](#iteration-utilities) | Combine iterables item by item |

The exception types (`Exception`, `ValueError`, `KeyError`, ...) are also builtins; see [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md).

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
int("42")        # 42
int(3.14)        # 3 (truncates toward zero)
int(-3.9)        # -3 (truncates toward zero)
int(42)          # 42 (no change)
```

Optional `base` argument (2 to 36) for base conversion from a string:

```python
int("ff", 16)    # 255
int("0xff", 16)  # 255 (0x prefix stripped automatically)
int("1010", 2)   # 10
int("0b1010", 2) # 10 (0b prefix stripped automatically)
int("77", 8)     # 63
int("z", 36)     # 35
int("1_000")     # 1000 (underscores between digits, as in Python)
```

A string that is not a valid integer raises `ValueError`, with Python's message:

```python
try:
    int("abc")
except ValueError as e:
    print(e)   # invalid literal for int() with base 10: 'abc'
```

### float()

Convert to float:

```python
float("3.14") # 3.14
float(42)     # 42.0
float("42")   # 42.0
float("1e3")  # 1000.0
float("inf")  # inf (also "-inf", "nan")
```

An invalid string raises `ValueError`: `could not convert string to float: '1.5abc'`.

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

### frozenset()

Create an immutable set. Frozen sets cannot be modified (`add`, `update`, … raise `AttributeError`) and are hashable by content, so — unlike regular sets — they can be used as dict keys and set members:

```python
fs = frozenset([1, 2])
fs | {3}                      # frozenset({1, 2, 3}) — operators follow the
                              # left operand's type, as in Python
d = {frozenset("ab"): 1}      # legal: hashable key
d[frozenset("ba")]            # 1 — equal frozensets hash equally
isinstance(fs, frozenset)     # True; isinstance(fs, set) is False
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
type(None)      # "NULL"
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

### issubclass()

Check if a class is a subclass of another:

```python
class Animal:
    pass

class Dog(Animal):
    pass

issubclass(Dog, Animal)    # True
issubclass(Animal, Animal) # True (a class is a subclass of itself)
issubclass(Animal, Dog)    # False
```

### callable()

Check if a value can be called as a function:

```python
callable(len)             # True
callable(lambda x: x)     # True
callable(42)              # False
callable("hello")         # False
```

## Sentinel Values

### sentinel()

Creates a unique marker value, like Python 3.15's `sentinel()` builtin (PEP 661). Each call returns a new value that is equal only to itself, so it can never collide with real data — including `None`:

```python
MISSING = sentinel("MISSING")

def fetch(key, default=MISSING):
    if default is MISSING:
        return load(key)          # no default was given
    return default

fetch("a")          # loads the value: None is a real default too
fetch("a", None)    # returns None, the caller's choice
```

Check a sentinel with `is`. `==` agrees with identity (true only against the same sentinel), and `repr` defaults to the name:

```python
MISSING is MISSING                   # True
MISSING is sentinel("MISSING")       # False: every call is a new sentinel
MISSING == "MISSING"                 # False
repr(MISSING)                        # "MISSING"

NOT_GIVEN = sentinel("x", repr="<NOT_GIVEN>")
repr(NOT_GIVEN)                      # "<NOT_GIVEN>"
MISSING.__name__                     # "MISSING"
```

Sentinels are truthy, hashable by identity (they work as set members and dict keys), not callable, and unsupported operations — ordering (`<`, `>=`), `len()`, indexing, iterating — raise `TypeError`, as does a name that is not a string.

## Number Methods

Numbers have Python's value methods, on the value itself, as a bound method value, and through the type:

```python
(5).bit_length()          # 3 (binary digits; (-5).bit_length() is 3 too)
(255).bit_count()         # 8 (population count)
(5).is_integer()          # True — always, for ints (Python 3.12)
(2.0).is_integer()        # True; (2.5).is_integer() is False

(2.0).hex()               # "0x1.0000000000000p+1" — exact hex float
float.fromhex("0x1.8p+1") # 3.0 (also float.fromhex("0x1.8") == 1.5)
(0.1).as_integer_ratio()  # [3602879701896397, 36028797018963968] — exact;
                          # ratios beyond int64 raise OverflowError

bl = (5).bit_length       # bound method value
bl()                      # 3
int.bit_count(7)          # 3 — unbound, like str.lower
```

Numbers keep no other methods: arithmetic goes through the operators and the `math` library, as before.

## Math Functions

```python
abs(-5)                   # 5
min(3, 1, 2)              # 1
max(3, 1, 2)              # 3
min(words, key=len)       # shortest word: key computes the comparison value,
                          # the item whose key wins is returned (ties keep the first)
max(records, key=lambda r: r["amount"])  # record with the highest amount
max([], default=None)     # None: default is returned for an empty iterable
                          # (single iterable only, not multiple arguments)
min([True, False])        # False: booleans order as 0 and 1 (False < True),
                          # against each other and mixed with numbers, like Python
round(3.7)                # 4
round(2.5)                # 2 (ties go to the even digit, like Python)
round(3.14159, 2)         # 3.14
pow(2, 10)                # 1024
pow(2, 10, 1000)          # 24 (modular: 2^10 % 1000)
divmod(17, 5)             # (3, 2) - returns (quotient, remainder)
sum([1, 2, 3, 4, 5])      # 15
sum([1.5, 2.5, 3.0])      # 7.0
sum([1, 2], 10)           # 13: optional start value, as in Python
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
```

String transformation is done with methods on the `str` type, not free functions. See [string](https://scriptling.dev/okf/scriptling-libraries/text-processing/string.md) for the full list:

```python
"hello".upper()                          # "HELLO"
"HELLO".lower()                          # "hello"
"hello world".capitalize()               # "Hello world"
"hello world".title()                    # "Hello World"
"a,b,c".split(",")                       # ["a", "b", "c"]
"a.b.c".rsplit(".", 1)                   # ["a.b", "c"] (split from the right)
"-".join(["a", "b", "c"])                # "a-b-c"
"hello world".replace("world", "python") # "hello python"
"  hello  ".strip()                      # "hello"
"??hello??".strip("?")                   # "hello"
"  hello  ".lstrip()                     # "hello  "
"  hello  ".rstrip()                     # "  hello"
"hello".startswith("he")                 # True (also: tuple prefixes, start/end offsets)
"hello".endswith("lo")                   # True
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
"{name} is {age}".format(name="Ada", age=36)   # "Ada is 36" (named fields)
"{:>6.2f}".format(3.14159)         # "  3.14" (format specs)
"{{literal}}".format()             # "{literal}" (escaped braces)

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
"a.b.c".rsplit(".", 1)             # ["a.b", "c"] (from the right; rsplit(None, 1) splits whitespace)
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
sorted([3, 1, 4, 1, 5])            # [1, 1, 3, 4, 5] (stable: equal keys keep their order)
sorted(["banana", "apple"])        # ["apple", "banana"]
sorted([3, 1, 2], reverse=True)    # [3, 2, 1]
sorted([(2, "b"), (1, "a")])       # [(1, "a"), (2, "b")]  (tuples/lists compare element-by-element)

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

# Set operations — the argument may be any iterable, and union /
# intersection / difference accept several (folded left, as in Python)
s1 = set([1, 2])
s2 = set([2, 3])
s1.union(s2)                # {1, 2, 3}
s1.union([2, 3])            # {1, 2, 3}
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
keys(person)                       # dict_keys(['name', 'age'])  (a view object)
values(person)                     # dict_values(['Alice', 30])  (a view object)
items(person)                      # dict_items([('name', 'Alice'), ('age', 30)])  (a view object)

# Iterate over dictionary (views are iterable)
for item in items(person):
    key = item[0]
    value = item[1]
    print(key, value)

# Materialize a view into a list when needed
list(keys(person))                 # ["name", "age"]
```

`keys()`, `values()`, and `items()` may also be called as methods: `person.keys()`, `person.values()`, `person.items()`.

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
# These return iterators
enumerate(["a", "b"])              # Iterator: (0, "a"), (1, "b")
enumerate(["a", "b"], start=1)     # Iterator: (1, "a"), (2, "b")
zip([1, 2], ["a", "b"])            # Iterator: (1, "a"), (2, "b")
reversed([1, 2, 3])                # Iterator: 3, 2, 1
map(lambda x: x*2, [1, 2, 3])      # Iterator: 2, 4, 6
filter(lambda x: x > 1, [1, 2, 3]) # Iterator: 2, 3

# Convert to list if needed
list(enumerate(["a", "b"]))       # [(0, 'a'), (1, 'b')]
list(zip([1, 2], ["a", "b"]))     # [(1, 'a'), (2, 'b')]

# strict=True: inputs of different lengths raise ValueError
list(zip([1, 2], "abc", strict=True))  # ValueError: zip() argument 2 is longer than argument 1

# Boolean tests (work with any iterable)
any([False, True, False])         # True
all([True, True, True])           # True
all([True, False, True])          # False
```

Given an iterator, `map()`, `filter()`, `zip()`, `enumerate()`, `any()` and `all()` pull one item at a time, so they work on endless iterators such as `itertools.count()`:

```python
import itertools
next(filter(lambda n: n * n > 50, itertools.count()))   # 8
any(map(lambda n: n > 3, itertools.count()))             # True
```

Collecting an endless iterator, with `list()`, `sorted()`, `sum()`, a comprehension or a generator expression (which Scriptling builds eagerly), raises an error rather than running out of memory. Bound it first with `itertools.islice()` or `zip()`, or break out of a `for` loop.

## Iterator Protocol

`iter()` and `next()` expose the iterator protocol directly, enabling manual iteration and working with custom iterable classes.

```python
# iter(): create an iterator from any iterable
it = iter([10, 20, 30])
next(it)   # 10
next(it)   # 20
next(it)   # 30

# next() with a default: no exception on exhaustion
next(it, "done")   # "done"

# next() without default raises StopIteration when exhausted
try:
    next(it)
except StopIteration:
    print("exhausted")

# iter() works on lists, tuples, strings, sets, dicts, and
# instances with __iter__ or __next__
it = iter("abc")
next(it)   # "a"

# Manual iteration pattern
data = [1, 2, 3]
it = iter(data)
while True:
    val = next(it, None)
    if val is None:
        break
    print(val)

# Custom iterable class
class Counter:
    def __init__(self, n):
        self.n = n
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration()
        v = self.i
        self.i = self.i + 1
        return v

for x in Counter(3):   # works in for loops too
    print(x)           # 0, 1, 2

it = iter(Counter(2))
next(it)   # 0
next(it)   # 1
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

`input()` is not a core builtin: it is only available when the `sys` library is registered with a stdin reader (for example, by the `scriptling` CLI in interactive or server stdin mode). It is absent in a bare embedded interpreter unless the embedder provides it.

## Object and Attribute Functions

```python
class Point:
    def __init__(self):
        self.x = 1

p = Point()
getattr(p, "x")                  # 1
getattr(p, "z", 0)               # 0: default when the attribute is missing
hasattr(p, "x")                  # True
setattr(p, "y", 5)               # p.y is now 5
delattr(p, "y")                  # removes p.y

repr("a")                        # "'a'" (strings are quoted)
format(3.14159, ".2f")           # "3.14": same specs as f-strings
format(42, "05d")                # "00042"
format("x", ">3")                # "  x"

hash("a") == hash("a")           # True: equal values hash equally
id(p) == id(p)                   # True: identity of an object
help("len")                      # prints the help text for len
```

`getattr(obj, "name")` is exactly `obj.name`: it returns bound methods and property values and consults `__getattr__`. Without a default it raises `AttributeError` for a missing attribute, and `hasattr` returns `False` only when that `AttributeError` occurs. `delattr` on a missing attribute also raises `AttributeError`. All four also work on dictionaries and library modules, treating keys as attributes.

`format(value, spec)` follows Python: numbers and strings take the spec, a class can define `__format__(self, spec)`, and any other value accepts only an empty spec (raising `TypeError` otherwise), so format `str(x)` when you want to pad it.

## Methods as Values

Methods of strings, lists, dicts, tuples, sets and bytes can be used without calling them, as in Python. Through a value they are bound to it; through the type they take the value as their first argument:

```python
sorted(["banana", "Apple"], key=str.lower)   # ['Apple', 'banana']
list(map(str.strip, [" a ", "b "]))         # ['a', 'b']

items = []
add = items.append                           # bound to items
add(1)                                       # items is now [1]

dict.fromkeys(["x", "y"], 0)                 # {'x': 0, 'y': 0}
hasattr([], "append")                        # True
dir("")                                      # ['capitalize', 'casefold', ...]
```

Numbers have no methods in Scriptling; use the builtins (`abs`, `round`, `int`, `float`) and the `math` library instead.

## Introspection

### dir()

Returns a sorted list of names for an object:

```python
# No argument: builtin names (unlike Python, not the local scope)
names = dir()          # ['AttributeError', 'Exception', ..., 'abs', 'all', ...]

# Instance: fields + methods (including inherited)
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return "woof"

d = Dog("Rex")
dir(d)   # ['__init__', 'bark', 'name']

# Class: method names
dir(Dog)   # ['__init__', 'bark']

# Dict: dict method names (not keys)
dir({"x": 1, "y": 2})   # ['clear', 'copy', 'fromkeys', 'get', 'items', ...]
```

## Copying

### copy()

Returns a shallow copy of an object. Nested objects are not copied: use `copy.deepcopy()` from the `copy` library for that. For native-backed instances, hidden Go-only state is not copied.

### copy.deepcopy()

`import copy` gives `copy.copy(x)` (same as the builtin) and `copy.deepcopy(x)`. The deep copy recurses through lists, tuples, dicts, sets and instances; it is cycle-safe, keeps shared references shared (two references to one list stay one list in the copy), returns all-atomic tuples, frozen sets and functions unchanged, and calls a class's `__deepcopy__(self, memo)` when defined:

```python
import copy

src = {"items": [1, 2], "meta": {"on": True}}
dup = copy.deepcopy(src)
dup["items"].append(3)
src["items"]          # [1, 2] — untouched

shared = [7]
holder = {"a": shared, "b": shared}
h = copy.deepcopy(holder)
h["a"] is h["b"]      # True — sharing preserved

cyc = [1]
cyc.append(cyc)
c = copy.deepcopy(cyc)
c[1] is c             # True — cycle handled
```

```python
# List copy: mutations don't affect the original
original = [1, 2, 3]
c = copy(original)
c.append(4)
len(original)   # 3
len(c)          # 4

# Dict copy
d = {"a": 1}
dc = copy(d)
dc["b"] = 2
len(d)    # 1
len(dc)   # 2

# Set copy
s = set([1, 2, 3])
sc = copy(s)
sc.add(4)
len(s)    # 3
len(sc)   # 4

# Instance copy: fields are copied, class is shared
class Box:
    def __init__(self, v):
        self.v = v

b = Box(10)
c = copy(b)
c.v = 99
b.v   # 10 (unchanged)
c.v   # 99

# Tuples and scalars are returned as-is (immutable)
copy((1, 2, 3))   # (1, 2, 3)
copy(42)          # 42
```

## Concurrency

### yield_now()

Briefly release the interpreter lock and yield the thread, letting other goroutines run before continuing. Use it inside a long, purely CPU-bound loop that never hits a naturally-blocking call, so shared-environment threads ([`runtime.background(..., shared=True)`](https://scriptling.dev/okf/scriptling-libraries/runtime.md)) and registered handlers can make progress.

Blocking builtins: `time.sleep`, `input()`, file reads/writes, socket send/receive/accept, WebSocket send/receive, subprocess, HTTP requests, AI completions/streaming, all container daemon calls, plugin calls, file provisioning, `wait_for` polling, `grep`/`sed` scans, messaging sends/downloads, `Queue` operations, `WaitGroup.wait()`, `Promise.wait()`/`get()`, `gossip send_request()`: already release the lock while they block, so you only need `yield_now()` for tight compute loops.

```python
import scriptling.runtime as runtime

def cruncher():
    # ... CPU-bound work ...
    pass

runtime.background("cruncher", "cruncher", shared=True)

while working:
    do_a_chunk_of_work()
    yield_now()   # let the shared thread run
```

## See Also

- [Data Types](https://scriptling.dev/okf/scriptling-reference/types.md) - Available data types
- [Slicing](https://scriptling.dev/okf/scriptling-reference/slicing.md) - Indexing and slicing operations
- [String Library](https://scriptling.dev/okf/scriptling-libraries/text-processing/string.md) - String constants
