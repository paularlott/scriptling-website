---
title: Operators
description: Arithmetic, comparison, boolean, bitwise operators and precedence in Scriptling.
weight: 3
---

Scriptling supports a variety of operators for arithmetic, comparison, boolean logic, and bitwise operations.

## Arithmetic Operators

```python
x + y    # Addition
x - y    # Subtraction
x * y    # Multiplication
x ** y   # Exponentiation (power)
x / y    # Division (always returns float)
x // y   # Floor division (integer division)
x % y    # Modulo (remainder)
```

### Examples

```python
10 + 5    # 15
10 - 3    # 7
10 * 3    # 30
2 ** 10   # 1024
10 / 4    # 2.5 (always float)
10 // 3   # 3 (floor division)
10 % 3    # 1 (remainder)

# String operations
"Hello, " + "World"  # "Hello, World"
"ab" * 3             # "ababab"
3 * "ab"             # "ababab"
```

## Augmented Assignment

Combine an operation with assignment:

```python
x += y   # x = x + y
x -= y   # x = x - y
x *= y   # x = x * y
x /= y   # x = x / y
x //= y  # x = x // y
x %= y   # x = x % y
x **= y  # x = x ** y

# Bitwise augmented assignment
x &= y   # x = x & y
x |= y   # x = x | y
x ^= y   # x = x ^ y
x <<= y  # x = x << y
x >>= y  # x = x >> y
```

## Comparison Operators

```python
x == y   # Equal
x != y   # Not equal
x < y    # Less than
x > y    # Greater than
x <= y   # Less than or equal
x >= y   # Greater than or equal
```

### Examples

```python
5 == 5      # True
5 != 3      # True
5 < 10      # True
5 > 10      # False
5 <= 5      # True
5 >= 10     # False

# String comparison (lexicographic)
"apple" < "banana"  # True
"zebra" > "apple"   # True
```

## Boolean/Logical Operators

```python
x and y  # Logical AND - returns first falsy value or last value
x or y   # Logical OR - returns first truthy value or last value
not x    # Logical NOT
```

### Short-circuit Evaluation

```python
# AND returns first falsy or last value
0 and 5      # 0 (short-circuits, 5 not evaluated)
1 and 5      # 5
[] and 5     # []
[1] and 5    # 5

# OR returns first truthy or last value
1 or 5       # 1 (short-circuits)
0 or 5       # 5
None or "default"  # "default"

# Practical patterns
config = user_config or default_config
value = x and y  # Returns x if falsy, otherwise y
```

### Truthiness

**Falsy values:** `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`

**Truthy values:** Everything else

## Chained Comparisons

```python
# Chained comparisons work like mathematical notation
1 < x < 10        # Equivalent to: 1 < x and x < 10
x <= y <= z       # Equivalent to: x <= y and y <= z
a == b == c       # Equivalent to: a == b and b == c

# Practical examples
if 18 <= age <= 65:
    print("Working age")

if 0 < score < 100:
    print("Valid score")

if 1 <= month <= 12:
    print("Valid month")
```

## Bitwise Operators

Work on integers at the binary level:

```python
~x       # Bitwise NOT (one's complement)
x & y    # Bitwise AND
x | y    # Bitwise OR
x ^ y    # Bitwise XOR (exclusive or)
x << y   # Left shift (multiply by 2^y)
x >> y   # Right shift (divide by 2^y, floor)
```

### Examples

```python
print(~5)        # -6 (bitwise NOT)
print(12 & 10)   # 8  (1100 & 1010 = 1000)
print(12 | 10)   # 14 (1100 | 1010 = 1110)
print(12 ^ 10)   # 6  (1100 ^ 1010 = 0110)
print(5 << 2)    # 20 (5 * 2^2 = 5 * 4)
print(20 >> 2)   # 5  (20 / 2^2 = 20 / 4)

# Practical use cases
# Extract lower 4 bits
value = 170  # 0b10101010
lower_bits = value & 15  # 10 (0b1010)

# Set specific bits
flags = 0
flags |= 4   # Set bit 2
flags |= 8   # Set bit 3

# Toggle bits
state = 15   # 0b1111
state ^= 5   # Toggle bits 0 and 2, result: 10 (0b1010)

# Fast multiplication/division
fast_mult = 7 << 3   # 7 * 8 = 56
fast_div = 56 >> 3   # 56 / 8 = 7
```

## Identity Operators

```python
x is y      # True if x and y are the same object
x is not y  # True if x and y are different objects

# Common use: checking for None
if value is None:
    print("No value")

if result is not None:
    print("Got result")
```

## Membership Operators

```python
x in y       # True if x is contained in y
x not in y   # True if x is not contained in y

# Lists
3 in [1, 2, 3]       # True
5 not in [1, 2, 3]   # True

# Strings
"ll" in "hello"      # True
"x" not in "hello"   # True

# Dictionaries (checks keys)
"name" in {"name": "Alice"}  # True
"age" in {"name": "Alice"}   # False
```

## Operator Precedence

From highest to lowest:

| Precedence | Operators |
|------------|-----------|
| 1 (highest) | Parentheses `()` |
| 2 | Function calls, indexing `func()`, `list[0]` |
| 3 | Exponentiation `**` |
| 4 | Unary `-`, `not`, `~` |
| 5 | `*`, `/`, `%` |
| 6 | `+`, `-` |
| 7 | `<<`, `>>` (bitwise shift) |
| 8 | `&` (bitwise AND) |
| 9 | `^` (bitwise XOR) |
| 10 | `\|` (bitwise OR) |
| 11 | `<`, `>`, `<=`, `>=` |
| 12 | `==`, `!=`, `is`, `in` |
| 13 | `and` |
| 14 (lowest) | `or` |

### Examples

```python
# Exponentiation before multiplication
2 + 3 ** 2    # 2 + 9 = 11

# Multiplication before addition
2 + 3 * 4     # 2 + 12 = 14

# Use parentheses for clarity
(2 + 3) * 4   # 20
2 + (3 * 4)   # 14

# Complex expression
result = 2 ** 3 + 4 * 5 - 6 / 2
# = 8 + 20 - 3.0
# = 25.0
```

## See Also

- [Data Types](./types/) - Available data types
- [Control Flow](./control-flow/) - Using operators in conditions
