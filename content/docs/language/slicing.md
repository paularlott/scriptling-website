---
title: Indexing & Slicing
description: Single index access, slice notation, and the slice() builtin in Scriptling.
weight: 9
---

Scriptling supports indexing and slicing for accessing elements of sequences like strings, lists, and tuples.

## Single Index

Access individual elements by position (0-based indexing):

```python
word = "hello"
first = word[0]    # "h"
last = word[4]     # "o"

numbers = [1, 2, 3, 4, 5]
first_num = numbers[0]    # 1
third_num = numbers[2]    # 3
last_num = numbers[4]     # 5
```

### Negative Indexing

Negative indices count from the end:

```python
word = "hello"
last = word[-1]      # "o"
second_last = word[-2]  # "l"

numbers = [1, 2, 3, 4, 5]
last = numbers[-1]   # 5
first = numbers[-5]  # 1
```

## Slice Notation

Extract portions of a sequence:

```python
sequence[start:stop]      # Elements from start to stop-1
sequence[start:stop:step] # Elements from start to stop-1, stepping by step
sequence[:]               # Copy of entire sequence
sequence[::step]          # Every step-th element
```

### Basic Slicing

```python
numbers = [0, 1, 2, 3, 4, 5]

numbers[1:4]       # [1, 2, 3]
numbers[:3]        # [0, 1, 2]
numbers[3:]        # [3, 4, 5]
numbers[:]         # [0, 1, 2, 3, 4, 5] (copy)
```

### Slicing with Step

```python
numbers = [0, 1, 2, 3, 4, 5]

numbers[::2]       # [0, 2, 4] - every second element
numbers[1::2]      # [1, 3, 5] - every second element starting from index 1
numbers[1:8:2]     # [1, 3, 5] - every second element from 1 to 8
```

### Reversing with Negative Step

```python
numbers = [0, 1, 2, 3, 4, 5]

numbers[::-1]      # [5, 4, 3, 2, 1, 0] - reverse the list
numbers[::-2]      # [5, 3, 1] - every second element in reverse
numbers[4:1:-1]    # [4, 3, 2] - reverse from index 4 to 1
```

### String Slicing

```python
text = "Hello World"

text[0:5]          # "Hello"
text[6:]           # "World"
text[:5]           # "Hello"

# With step
text[::2]          # "HloWrd" - every second character
text[::-1]         # "dlroW olleH" - reverse the string
text[1:8:2]        # "el o" - every second character from 1 to 8
```

### Tuple Slicing

```python
coords = (0, 1, 2, 3, 4, 5)

coords[1:4]        # (1, 2, 3)
coords[::2]        # (0, 2, 4)
coords[::-1]       # (5, 4, 3, 2, 1, 0)
```

## The slice() Builtin

Create slice objects programmatically:

```python
# Creating slice objects
s = slice(1, 5)           # Equivalent to [1:5]
s = slice(1, 5, 2)        # Equivalent to [1:5:2]
s = slice(None, None, -1) # Equivalent to [::-1]
s = slice(-3, None)       # Equivalent to [-3:]

# Using slice objects
lst = [0, 1, 2, 3, 4, 5]
s = slice(1, 4)
result = lst[s]           # [1, 2, 3]

s = slice(None, None, -1)
result = lst[s]           # [5, 4, 3, 2, 1, 0]

# Works with strings and tuples too
text = "hello world"
s = slice(0, 5)
result = text[s]          # "hello"

tup = (0, 1, 2, 3, 4)
s = slice(1, 4)
result = tup[s]           # (1, 2, 3)
```

### slice() Parameters

```python
slice(stop)               # Equivalent to slice(0, stop, 1)
slice(start, stop)        # Equivalent to slice(start, stop, 1)
slice(start, stop, step)  # Full control

# Use None for default values
slice(None, 5)            # [:5]
slice(2, None)            # [2:]
slice(None, None, 2)      # [::2]
```

## Modifying Slices (Lists Only)

Lists can be modified by assigning to slices:

```python
lst = [1, 2, 3, 4, 5]

# Replace a slice
lst[1:4] = [10, 20]
print(lst)  # [1, 10, 20, 5]

# Insert elements
lst[1:1] = [100, 200]
print(lst)  # [1, 100, 200, 10, 20, 5]

# Delete elements
lst[2:4] = []
print(lst)  # [1, 100, 20, 5]
```

## Slice Assignment with Step

```python
lst = [1, 2, 3, 4, 5, 6]

# Replace every other element
lst[::2] = [10, 30, 50]
print(lst)  # [10, 2, 30, 4, 50, 6]

# Reverse and replace
lst = [1, 2, 3]
lst[::-1] = [10, 20, 30]
print(lst)  # [30, 20, 10]
```

## Common Patterns

```python
# Get first n elements
first_three = seq[:3]

# Get last n elements
last_three = seq[-3:]

# Remove first element
rest = seq[1:]

# Remove last element
all_but_last = seq[:-1]

# Reverse a sequence
reversed_seq = seq[::-1]

# Every other element
every_other = seq[::2]

# Copy a list
copy = seq[:]

# Remove first and last
middle = seq[1:-1]

# Check if palindrome (for sequences)
is_palindrome = seq == seq[::-1]
```

## See Also

- [Data Types](./types/) - Lists, strings, and tuples
- [Built-in Functions](./builtins/) - len(), reversed(), enumerate()
