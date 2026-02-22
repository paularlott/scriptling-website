---
title: Functions
description: Function definition, parameters, *args, **kwargs, lambdas, and closures in Scriptling.
weight: 5
---

Functions are reusable blocks of code that can accept parameters and return values.

## Function Definition

```python
def function_name(param1, param2):
    # function body
    return result
```

### Examples

```python
# Simple function
def greet(name):
    print("Hello, " + name)

# Function with return
def add(a, b):
    return a + b

# Recursive function
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

# No parameters
def get_pi():
    return 3.14159

# No return (returns None)
def log_message(msg):
    print("[LOG]", msg)
```

## Default Parameters

```python
def greet(name, greeting="Hello", punctuation="!"):
    return greeting + ", " + name + punctuation

# Using defaults
greet("World")  # "Hello, World!"

# Override defaults
greet("Alice", "Hi")  # "Hi, Alice!"
greet("Bob", "Hey", ".")  # "Hey, Bob."
```

## Keyword Arguments

Functions can be called with keyword arguments, which can be mixed with positional arguments:

```python
def greet(name, greeting="Hello", punctuation="!"):
    return greeting + ", " + name + punctuation

# Positional arguments
greet("World")  # "Hello, World!"

# Keyword arguments
greet(name="Alice")  # "Hello, Alice!"
greet(greeting="Hi", name="Bob")  # "Hi, Bob!"

# Mixed positional and keyword
greet("Charlie", greeting="Hey")  # "Hey, Charlie!"
greet("Diana", punctuation=".")  # "Hello, Diana."

# All keyword arguments (order doesn't matter)
greet(punctuation="?", name="Eve", greeting="Howdy")  # "Howdy, Eve?"
```

### Rules

- Positional arguments must come before keyword arguments
- Each parameter can only be specified once
- Keyword arguments work with default parameter values

## Variadic Arguments (*args)

Functions can accept a variable number of positional arguments:

```python
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3))      # 6
print(sum_all(1, 2, 3, 4))   # 10
print(sum_all())             # 0
```

### Mixing with Regular Parameters

```python
def log(level, *messages):
    prefix = "[" + level + "] "
    for msg in messages:
        print(prefix + str(msg))

log("INFO", "System started", "Ready")
# Output:
# [INFO] System started
# [INFO] Ready

log("ERROR", "Failed to connect", "Retrying...", "Attempt 2")
```

**Note**: `*args` must come after regular parameters and default parameters.

## Keyword Arguments Collection (**kwargs)

Functions can accept arbitrary keyword arguments:

```python
def test_kwargs(**kwargs):
    return kwargs

result = test_kwargs(a=1, b=2, c=3)
print(result)  # {"a": 1, "b": 2, "c": 3}
```

### Combining All Parameter Types

```python
def func_with_all(a, b=10, *args, **kwargs):
    print("a:", a)
    print("b:", b)
    print("args:", args)
    print("kwargs:", kwargs)

func_with_all(1, 2, 3, 4, x=5, y=6)
# Output:
# a: 1
# b: 2
# args: [3, 4]
# kwargs: {"x": 5, "y": 6}
```

### Parameter Order

When using multiple parameter types, they must appear in this order:

1. Regular parameters (e.g., `a`, `b`)
2. Default parameters (e.g., `c=10`)
3. Variadic arguments (`*args`)
4. Keyword arguments (`**kwargs`)

## Argument Unpacking

### Positional Argument Unpacking (*)

Unpack a list or tuple into individual arguments:

```python
def sum_three(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
result = sum_three(*numbers)  # Same as sum_three(1, 2, 3)
print(result)  # 6

# Unpacking tuples
coords = (10, 20)
def add_coords(x, y):
    return x + y
print(add_coords(*coords))  # 30

# Partial unpacking
result = sum_three(10, *numbers[1:])  # Same as sum_three(10, 2, 3)
```

### Keyword Argument Unpacking (**)

Unpack a dictionary into keyword arguments:

```python
def create_user(name, age, active=True):
    return {"name": name, "age": age, "active": active}

user_data = {"name": "Alice", "age": 30}
user = create_user(**user_data)
print(user)  # {"name": "Alice", "age": 30, "active": True}

# Override with additional kwargs
user = create_user(**user_data, active=False)
print(user)  # {"name": "Alice", "age": 30, "active": False}
```

### Combining Both

```python
def func_with_all(a, b, *args, **kwargs):
    return {"a": a, "b": b, "args": args, "kwargs": kwargs}

args = [1, 2, 3, 4]
kwargs = {"x": 10, "y": 20}
result = func_with_all(*args, **kwargs)
# {"a": 1, "b": 2, "args": [3, 4], "kwargs": {"x": 10, "y": 20}}
```

## Decorators

Decorators wrap a function with another callable using `@` syntax:

```python
def double_result(fn):
    def wrapper(*args):
        return fn(*args) * 2
    return wrapper

@double_result
def add(a, b):
    return a + b

print(add(3, 4))  # 14
```

Decorators stack — applied bottom-up (innermost first):

```python
@outer
@inner
def fn(): ...
# equivalent to: fn = outer(inner(fn))
```

See [Classes](./classes/) for `@property` and `@staticmethod`.

## Lambda Functions

Anonymous functions for simple operations:

```python
# Basic lambda
square = lambda x: x * x
print(square(5))  # 25

# Multiple parameters
add = lambda a, b: a + b
print(add(3, 4))  # 7

# With default parameters
greet = lambda name, greeting="Hello": greeting + ", " + name
print(greet("World"))  # "Hello, World"

# In sorted
sorted(["ccc", "a", "bb"], key=lambda s: len(s))  # ["a", "bb", "ccc"]

# In map
list(map(lambda x: x * 2, [1, 2, 3]))  # [2, 4, 6]

# In filter
list(filter(lambda x: x > 2, [1, 2, 3, 4]))  # [3, 4]
```

## Return Statement

```python
# Return value
def add(a, b):
    return a + b

# Return None (explicit)
def do_nothing():
    return None

# Return None (implicit)
def log(msg):
    print(msg)
    # No return statement = returns None

# Multiple returns
def classify(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"
```

## Closures

Functions can capture variables from their enclosing scope:

```python
def make_counter(start=0):
    count = [start]  # Use list to allow modification

    def counter():
        count[0] += 1
        return count[0]

    return counter

counter = make_counter(10)
print(counter())  # 11
print(counter())  # 12
print(counter())  # 13
```

## Multiple Assignment

Unpack sequences into multiple variables:

```python
# Basic unpacking
x, y = [1, 2]
a, b, c = (10, 20, 30)

# Extended unpacking with *
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5

*head, tail = [1, 2, 3]
# head=[1,2], tail=3

head, *tail = [1, 2, 3]
# head=1, tail=[2,3]

# With minimal elements
a, *b, c = [1, 2]
# a=1, b=[], c=2

# In loops
for first, *rest in [[1,2,3], [4,5,6,7]]:
    print(f"first={first}, rest={rest}")
```

## See Also

- [Control Flow](./control-flow/) - Loops and conditionals
- [Error Handling](./error-handling/) - Try/except in functions
- [Classes](./classes/) - Methods and class functions
