---
title: Control Flow
description: Conditionals, loops, match statements, break, continue, and pass in Scriptling.
weight: 4
---

Scriptling provides standard control flow constructs for conditional execution and iteration.

## If/Elif/Else Statement

```python
if condition:
    # code block
elif other_condition:
    # code block
elif another_condition:
    # code block
else:
    # code block
```

### Examples

```python
# Simple if/else
if x > 10:
    print("large")
else:
    print("small")

# Multiple conditions with elif
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")

# Nested conditions
if x > 0:
    if y > 0:
        print("Both positive")
    else:
        print("x positive, y not")
else:
    print("x not positive")
```

## While Loop

```python
counter = 0
while counter < 10:
    print(counter)
    counter += 1
```

### While with Else

```python
# Else executes if loop completes normally (no break)
n = 5
while n > 0:
    print(n)
    n -= 1
else:
    print("Countdown complete!")
```

## For Loop

Iterate over sequences and iterables:

```python
# Iterate over list
for item in [1, 2, 3]:
    print(item)

# Iterate over string
for char in "hello":
    print(char)

# Iterate over variable
numbers = [10, 20, 30]
for num in numbers:
    print(num)

# Range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Range with start and stop
for i in range(2, 7):
    print(i)  # 2, 3, 4, 5, 6

# Range with step
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Negative step (countdown)
for i in range(10, 0, -2):
    print(i)  # 10, 8, 6, 4, 2
```

### For with Else

```python
# Else executes if loop completes normally (no break)
for item in [1, 2, 3]:
    print(item)
else:
    print("Loop complete!")
```

### Iterating Dictionaries

```python
person = {"name": "Alice", "age": 30}

# Iterate over keys
for key in keys(person):
    print(key, person[key])

# Iterate over key-value pairs
for item in items(person):
    key = item[0]
    value = item[1]
    print(key, value)

# Using tuple unpacking
for item in items(person):
    key, value = item
    print(f"{key}: {value}")
```

## Loop Control

### Break

Exit a loop immediately:

```python
# break - exit loop
for i in [1, 2, 3, 4, 5]:
    if i == 3:
        break
    print(i)  # Prints 1, 2

# In while loop
n = 0
while True:
    print(n)
    n += 1
    if n >= 5:
        break  # Exit infinite loop
```

### Continue

Skip to the next iteration:

```python
# continue - skip to next iteration
for i in [1, 2, 3, 4, 5]:
    if i == 3:
        continue
    print(i)  # Prints 1, 2, 4, 5

# Skip even numbers
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Prints 1, 3, 5, 7, 9
```

### Pass

Do nothing (placeholder):

```python
# pass - do nothing (placeholder)
for i in [1, 2, 3]:
    if i == 2:
        pass  # Placeholder for future code
    else:
        print(i)

# Empty function body
def todo():
    pass  # Implement later

# Empty class
class Placeholder:
    pass
```

## With Statement (Context Managers)

The `with` statement calls `__enter__` on entry and guarantees `__exit__` is called on exit, even if an exception is raised:

```python
with some_resource() as r:
    r.do_something()
# __exit__ is called here automatically
```

### Implementing a Context Manager

```python
class ManagedConnection:
    def __init__(self, host):
        self.host = host
        self.conn = None

    def __enter__(self):
        self.conn = connect(self.host)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False  # don't suppress exceptions

with ManagedConnection("localhost") as conn:
    conn.send(data)
# conn.close() is called automatically
```

### Suppressing Exceptions

If `__exit__` returns a truthy value, the exception is suppressed:

```python
class Suppress:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True  # suppress any exception

with Suppress():
    raise ValueError("ignored")  # suppressed
print("continues here")
```

### Without `as` Binding

```python
with lock_resource():
    do_critical_work()
# resource released even if do_critical_work() raises
```

## Assert Statement

Assert statements verify conditions and raise an `AssertionError` if the condition is falsy:

```python
# Basic assert
assert condition

# Assert with message
assert condition, "message if condition is false"

# Examples
x = 10
assert x > 0, "x must be positive"
assert isinstance(x, int), f"expected int, got {type(x)}"
assert len(results) > 0, "no results returned"
```

The message is only evaluated when the assertion fails. `AssertionError` is catchable by `try/except`:

```python
try:
    assert value > 0, "must be positive"
except:
    print("assertion failed")
```

## Match Statement

Pattern matching for cleaner conditional logic:

### Basic Value Matching

```python
match status:
    case 200:
        print("Success")
    case 404:
        print("Not found")
    case 500:
        print("Server error")
    case _:
        print("Other status")
```

### Type-Based Matching

```python
match data:
    case int():
        print("Got integer")
    case str():
        print("Got string")
    case list():
        print("Got list")
    case dict():
        print("Got dictionary")
    case _:
        print("Other type")
```

### Guard Clauses

```python
match value:
    case x if x > 100:
        print("Large value")
    case x if x > 50:
        print("Medium value")
    case x:
        print("Small value")

# With validation
match user_input:
    case s if len(s) == 0:
        print("Empty input")
    case s if len(s) > 100:
        print("Input too long")
    case s:
        process(s)
```

### Structural Matching

```python
# Dictionary patterns
match response:
    case {"status": 200, "data": payload}:
        process(payload)
    case {"error": msg}:
        print("Error:", msg)
    case _:
        print("Unknown response")

# List patterns
match coords:
    case [x, y]:
        print(f"2D point: {x}, {y}")
    case [x, y, z]:
        print(f"3D point: {x}, {y}, {z}")
    case _:
        print("Unknown dimensions")
```

### Capture Variables

```python
# Capture matched value
match value:
    case x as captured:
        print("Captured:", captured)

# Capture in patterns
match data:
    case {"name": name, "age": age}:
        print(f"Name: {name}, Age: {age}")
```

## Nested Loops

```python
# Nested for loops
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")

# Breaking out of nested loops
found = False
for i in range(5):
    for j in range(5):
        if i * j == 12:
            print(f"Found: {i}, {j}")
            found = True
            break
    if found:
        break
```

## Comprehensions

Create lists from iterables:

### List Comprehensions

```python
# Basic comprehension
squares = [x * x for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# With transformation
uppercased = [s.upper() for s in ["hello", "world"]]
```

## See Also

- [Functions](./functions/) - Function definitions and parameters
- [Operators](./operators/) - Comparison and boolean operators
- [Error Handling](./error-handling/) - Try/except and raise
