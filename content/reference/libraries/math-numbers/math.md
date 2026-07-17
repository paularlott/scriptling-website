---
title: math
description: Mathematical functions and constants.
tags: [libraries, math]
weight: 1

aliases:
  - /reference/libraries/stdlib/math/
  - /reference/libraries/math/
---

The `math` library provides mathematical functions and constants: trigonometry, logarithms, rounding, combinatorics, and basic vector/matrix operations via `FloatArray`.

## Available Functions

| Function | Description |
|----------|-------------|
| `sqrt(x)` | Square root of `x`. |
| `pow(base, exp)` | `base` raised to the power of `exp`. |
| `fabs(x)` | Absolute value of `x` as a float. |
| `floor(x)` | Round `x` down to the nearest integer. |
| `ceil(x)` | Round `x` up to the nearest integer. |
| `trunc(x)` | Truncate `x` toward zero. |
| `sin(x)` | Sine of `x` (radians). |
| `cos(x)` | Cosine of `x` (radians). |
| `tan(x)` | Tangent of `x` (radians). |
| `asin(x)` | Arc sine of `x` (radians). |
| `acos(x)` | Arc cosine of `x` (radians). |
| `atan(x)` | Arc tangent of `x` (radians). |
| `atan2(y, x)` | Arc tangent of `y/x` (radians), quadrant-aware. |
| `log(x)` | Natural logarithm of `x`. |
| `log10(x)` | Base-10 logarithm of `x`. |
| `log2(x)` | Base-2 logarithm of `x`. |
| `exp(x)` | `e` raised to the power of `x`. |
| `degrees(x)` | Convert radians to degrees. |
| `radians(x)` | Convert degrees to radians. |
| `hypot(x, y)` | Euclidean distance `sqrt(x*x + y*y)`. |
| `fmod(x, y)` | Floating-point remainder of `x/y`. |
| `gcd(a, b)` | Greatest common divisor. |
| `factorial(n)` | Factorial of `n`. |
| `copysign(x, y)` | `x` with the sign of `y`. |
| `isnan(x)` | Whether `x` is NaN. |
| `isinf(x)` | Whether `x` is positive or negative infinity. |
| `isfinite(x)` | Whether `x` is neither NaN nor infinite. |
| `tanh(x)` | Hyperbolic tangent of `x`. |
| `erf(x)` | Error function of `x`. |
| `erfc(x)` | Complementary error function of `x`. |
| `gamma(x)` | Gamma function of `x`. |
| `lgamma(x)` | Natural log of the absolute gamma of `x`. |
| `cbrt(x)` | Cube root of `x`. |
| `nextafter(x, y)` | Next float after `x` towards `y`. |
| `remainder(x, y)` | IEEE 754-style remainder of `x/y`. |
| `log1p(x)` | `log(1+x)`, accurate for small `x`. |
| `expm1(x)` | `exp(x)-1`, accurate for small `x`. |
| `comb(n, k)` | Number of ways to choose `k` from `n` (unordered). |
| `perm(n[, k])` | Number of ways to choose `k` from `n` (ordered). |
| `prod(iterable, start=1)` | Product of all elements in a list. |
| `dist(p, q)` | Euclidean distance between two points. |
| `softmax(x)` | Softmax of a vector. |
| `dot(a, b)` | Dot product of two vectors. |
| `matmul(a, b)` | Matrix-matrix multiply. |
| `transpose(m)` | Transpose a 2D matrix. |
| `mat_add(a, b)` | Element-wise addition of two matrices. |
| `array(data)` | Create an efficient `FloatArray` from a list. |
| `shape(a)` | Shape of a `FloatArray` as a list of ints. |

## Constants

| Constant | Description |
|----------|-------------|
| `pi` | The mathematical constant π (`3.141592653589793`). |
| `e` | The mathematical constant e (`2.718281828459045`). |
| `inf` | Positive infinity. |
| `nan` | NaN (Not a Number). |
| `tau` | The mathematical constant τ, equal to 2π (`6.283185307179586`). |

## Functions

### Power and Roots

#### `sqrt(x)`

Returns the square root of `x`.

**Parameters:**
- `x` (`int` or `float`): Value to take the square root of. Must be non-negative.

**Returns:** `float`

```python
import math
result = math.sqrt(16)  # 4.0
```

#### `pow(base, exp)`

Returns `base` raised to the power of `exp`.

**Parameters:**
- `base` (`int` or `float`): Base value.
- `exp` (`int` or `float`): Exponent.

**Returns:** `float`

```python
import math
result = math.pow(2, 8)  # 256.0
```

#### `cbrt(x)`

Returns the cube root of `x`.

**Parameters:**
- `x` (`int` or `float`): Value to take the cube root of.

**Returns:** `float`

```python
import math
result = math.cbrt(27)   # 3.0
result = math.cbrt(-8)   # -2.0
```

### Rounding and Sign

#### `fabs(x)`

Returns the absolute value of `x` as a float.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`: always floating-point, even for integer input.

```python
import math
result = math.fabs(-5)    # 5.0
result = math.fabs(-3.14) # 3.14
```

> **Note:** For absolute value that preserves integer type, use the builtin `abs()` function instead.

#### `floor(x)`

Rounds `x` down to the nearest integer.

**Parameters:**
- `x` (`int` or `float`): Value to round.

**Returns:** `int`

```python
import math
result = math.floor(3.7)  # 3
```

#### `ceil(x)`

Rounds `x` up to the nearest integer.

**Parameters:**
- `x` (`int` or `float`): Value to round.

**Returns:** `int`

```python
import math
result = math.ceil(3.2)  # 4
```

> **Note:** For rounding to nearest integer, use the builtin `round()` function. For min/max values, use the builtin `min()` and `max()` functions.

#### `trunc(x)`

Truncates `x` to the nearest integer toward zero.

**Parameters:**
- `x` (`int` or `float`): Value to truncate.

**Returns:** `int`

```python
import math
result = math.trunc(3.7)   # 3
result = math.trunc(-3.7)  # -3
```

#### `copysign(x, y)`

Returns `x` with the sign of `y`.

**Parameters:**
- `x` (`int` or `float`): Magnitude value.
- `y` (`int` or `float`): Sign value.

**Returns:** `float`: magnitude of `x`, sign of `y`.

```python
import math
result = math.copysign(5, -1)   # -5.0
result = math.copysign(-5, 1)   # 5.0
```

### Trigonometric

#### `sin(x)`

Returns the sine of `x` (in radians).

**Parameters:**
- `x` (`int` or `float`): Angle in radians.

**Returns:** `float`

```python
import math
result = math.sin(0)            # 0.0
result = math.sin(math.pi / 2)  # 1.0
```

#### `cos(x)`

Returns the cosine of `x` (in radians).

**Parameters:**
- `x` (`int` or `float`): Angle in radians.

**Returns:** `float`

```python
import math
result = math.cos(0)        # 1.0
result = math.cos(math.pi)  # -1.0
```

#### `tan(x)`

Returns the tangent of `x` (in radians).

**Parameters:**
- `x` (`int` or `float`): Angle in radians.

**Returns:** `float`

```python
import math
result = math.tan(0)            # 0.0
result = math.tan(math.pi / 4)  # 1.0
```

#### `asin(x)`

Returns the arc sine of `x` in radians.

**Parameters:**
- `x` (`int` or `float`): Value in range `[-1, 1]`.

**Returns:** `float`

```python
import math
result = math.asin(0)  # 0.0
result = math.asin(1)  # 1.5707963267948966 (pi/2)
```

#### `acos(x)`

Returns the arc cosine of `x` in radians.

**Parameters:**
- `x` (`int` or `float`): Value in range `[-1, 1]`.

**Returns:** `float`

```python
import math
result = math.acos(1)  # 0.0
result = math.acos(0)  # 1.5707963267948966 (pi/2)
```

#### `atan(x)`

Returns the arc tangent of `x` in radians.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`: in range `[-pi/2, pi/2]`.

```python
import math
result = math.atan(0)  # 0.0
result = math.atan(1)  # 0.7853981633974483 (pi/4)
```

#### `atan2(y, x)`

Returns the arc tangent of `y/x` in radians, correctly handling the quadrant of the result.

**Parameters:**
- `y` (`int` or `float`): Y coordinate.
- `x` (`int` or `float`): X coordinate.

**Returns:** `float`: in range `[-pi, pi]`.

```python
import math
result = math.atan2(1, 1)   # 0.7853981633974483 (pi/4)
result = math.atan2(-1, 1)  # -0.7853981633974483
```

#### `tanh(x)`

Returns the hyperbolic tangent of `x`.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`: in range `[-1, 1]`.

```python
import math
result = math.tanh(0)  # 0.0
result = math.tanh(1)  # 0.7615941559557649
```

#### `degrees(x)`

Converts angle `x` from radians to degrees.

**Parameters:**
- `x` (`int` or `float`): Angle in radians.

**Returns:** `float`

```python
import math
result = math.degrees(math.pi)      # 180.0
result = math.degrees(math.pi / 2)  # 90.0
```

#### `radians(x)`

Converts angle `x` from degrees to radians.

**Parameters:**
- `x` (`int` or `float`): Angle in degrees.

**Returns:** `float`

```python
import math
result = math.radians(180)  # 3.141592653589793
result = math.radians(90)   # 1.5707963267948966
```

#### `hypot(x, y)`

Returns the Euclidean distance `sqrt(x*x + y*y)`.

**Parameters:**
- `x` (`int` or `float`): First coordinate.
- `y` (`int` or `float`): Second coordinate.

**Returns:** `float`

```python
import math
result = math.hypot(3, 4)   # 5.0
result = math.hypot(5, 12)  # 13.0
```

### Logarithmic and Exponential

#### `log(x)`

Returns the natural logarithm (base e) of `x`.

**Parameters:**
- `x` (`int` or `float`): Value. Must be greater than `0`.

**Returns:** `float`

**Raises:** `Error`: if `x` is not greater than `0`.

```python
import math
result = math.log(1)      # 0.0
result = math.log(math.e) # 1.0
```

#### `log10(x)`

Returns the base-10 logarithm of `x`.

**Parameters:**
- `x` (`int` or `float`): Positive value.

**Returns:** `float`

```python
import math
result = math.log10(100)   # 2.0
result = math.log10(1000)  # 3.0
```

#### `log2(x)`

Returns the base-2 logarithm of `x`.

**Parameters:**
- `x` (`int` or `float`): Positive value.

**Returns:** `float`

```python
import math
result = math.log2(8)   # 3.0
result = math.log2(16)  # 4.0
```

#### `log1p(x)`

Returns `log(1+x)`, computed accurately even when `x` is very small.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`

```python
import math
result = math.log1p(0)      # 0.0
result = math.log1p(1e-15)  # 9.999999999999995e-16
```

#### `exp(x)`

Returns `e` raised to the power of `x`.

**Parameters:**
- `x` (`int` or `float`): Exponent.

**Returns:** `float`

```python
import math
result = math.exp(0)  # 1.0
result = math.exp(1)  # 2.718281828459045
```

#### `expm1(x)`

Returns `exp(x)-1`, computed accurately even when `x` is very small.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`

```python
import math
result = math.expm1(0)     # 0.0
result = math.expm1(1e-10) # 1.00000000005e-10
```

### Modular Arithmetic

#### `fmod(x, y)`

Returns the floating-point remainder of `x` divided by `y`.

**Parameters:**
- `x` (`int` or `float`): Dividend.
- `y` (`int` or `float`): Divisor. Cannot be `0`.

**Returns:** `float`

**Raises:** `Error`: if `y` is `0`.

```python
import math
result = math.fmod(5.5, 2.0)  # 1.5
result = math.fmod(7.0, 3.0)  # 1.0
```

#### `remainder(x, y)`

Returns the IEEE 754-style remainder of `x/y`.

**Parameters:**
- `x` (`int` or `float`): Dividend.
- `y` (`int` or `float`): Divisor.

**Returns:** `float`

```python
import math
result = math.remainder(7, 3)    # 1.0
result = math.remainder(7.5, 2)  # -0.5
```

#### `gcd(a, b)`

Returns the greatest common divisor of integers `a` and `b`.

**Parameters:**
- `a` (`int`): First value.
- `b` (`int`): Second value.

**Returns:** `int`

```python
import math
result = math.gcd(48, 18)  # 6
result = math.gcd(100, 75) # 25
```

#### `nextafter(x, y)`

Returns the next floating-point value after `x`, moving towards `y`.

**Parameters:**
- `x` (`int` or `float`): Starting value.
- `y` (`int` or `float`): Direction value.

**Returns:** `float`

```python
import math
result = math.nextafter(1.0, 2.0)  # 1.0000000000000002
result = math.nextafter(1.0, 0.0)  # 0.9999999999999999
```

### Special Functions

#### `erf(x)`

Returns the error function of `x`.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`: in range `[-1, 1]`.

```python
import math
result = math.erf(0)  # 0.0
result = math.erf(1)  # 0.8427007929497149
```

#### `erfc(x)`

Returns the complementary error function of `x`.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`: in range `[0, 2]`.

```python
import math
result = math.erfc(0)  # 1.0
result = math.erfc(1)  # 0.1572992070502851
```

#### `gamma(x)`

Returns the gamma function of `x`.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `float`

```python
import math
result = math.gamma(1)  # 1.0
result = math.gamma(5)  # 24.0 (4!)
```

#### `lgamma(x)`

Returns the natural log of the absolute value of the gamma function of `x`.

**Parameters:**
- `x` (`int` or `float`): Value.

**Returns:** `list`: `[log_abs_gamma, sign]`, where `sign` is `1` or `-1`.

```python
import math
result = math.lgamma(5)  # [3.1780538303479458, 1]
```

#### `isnan(x)`

Returns whether `x` is NaN (Not a Number).

**Parameters:**
- `x` (`int` or `float`): Value to check.

**Returns:** `bool`

```python
import math
result = math.isnan(math.nan)  # True
result = math.isnan(5)         # False
```

#### `isinf(x)`

Returns whether `x` is positive or negative infinity.

**Parameters:**
- `x` (`int` or `float`): Value to check.

**Returns:** `bool`

```python
import math
result = math.isinf(math.inf)   # True
result = math.isinf(-math.inf)  # True
result = math.isinf(5)          # False
```

#### `isfinite(x)`

Returns whether `x` is neither NaN nor infinite.

**Parameters:**
- `x` (`int` or `float`): Value to check.

**Returns:** `bool`

```python
import math
result = math.isfinite(5)         # True
result = math.isfinite(math.inf)  # False
result = math.isfinite(math.nan)  # False
```

### Combinatorics

#### `factorial(n)`

Returns the factorial of `n` (`n!`).

**Parameters:**
- `n` (`int`): Non-negative integer, `0 <= n <= 20`.

**Returns:** `int`

**Raises:** `Error`: if `n` is negative or greater than `20`.

```python
import math
result = math.factorial(5)  # 120
result = math.factorial(0)  # 1
```

#### `comb(n, k)`

Returns the number of ways to choose `k` items from `n` without regard to order (the binomial coefficient).

**Parameters:**
- `n` (`int`): Non-negative integer.
- `k` (`int`): Non-negative integer.

**Returns:** `int`

**Raises:** `Error`: if `n` or `k` is negative, or if the result is too large to fit in an integer.

```python
import math
result = math.comb(5, 2)   # 10
result = math.comb(10, 3)  # 120
```

#### `perm(n[, k])`

Returns the number of ways to choose `k` items from `n` with regard to order.

**Parameters:**
- `n` (`int`): Non-negative integer.
- `k` (`int`, optional): Non-negative integer. Default: `n` (returns `n!`).

**Returns:** `int`. Returns `0` when `k > n` or `k < 0`.

**Raises:** `Error`: if `n` is negative, or if the result is too large to fit in an integer.

```python
import math
result = math.perm(5)    # 120 (5!)
result = math.perm(5, 2) # 20
```

#### `prod(iterable, start=1)`

Returns the product of all elements in a list.

**Parameters:**
- `iterable` (`list`): List of numbers.
- `start` (`int` or `float`, keyword-only, optional): Starting value for the multiplication. Default: `1`.

**Returns:** `int` for all-integer inputs (and no `start` override that forces a float), `float` otherwise.

```python
import math
result = math.prod([1, 2, 3, 4])    # 24
result = math.prod([1.5, 2.0])      # 3.0
result = math.prod([1, 2], start=5) # 10
```

### Vectors and Matrices

#### `dist(p, q)`

Returns the Euclidean distance between two points.

**Parameters:**
- `p` (`list`): First point, as a list of numbers.
- `q` (`list`): Second point, as a list of numbers with the same length as `p`.

**Returns:** `float`

**Raises:** `Error`: if `p` and `q` have different lengths.

```python
import math
result = math.dist([0, 0], [3, 4])        # 5.0
result = math.dist([1, 2, 3], [4, 6, 3])  # 5.0
```

#### `softmax(x)`

Returns the numerically stable softmax of a vector.

**Parameters:**
- `x` (`list` or `FloatArray`): Values to transform. Must be 1D and non-empty.

**Returns:** `list` of `float`, or `FloatArray` if the input was a `FloatArray`: a probability distribution summing to `1.0`.

```python
import math
result = math.softmax([1.0, 2.0, 3.0])
print(result)  # [0.0900..., 0.2447..., 0.6652...]

a = math.array([1.0, 2.0, 3.0])
result = math.softmax(a)  # Returns FloatArray
```

#### `dot(a, b)`

Returns the dot product of two vectors.

**Parameters:**
- `a` (`list` or `FloatArray`): First vector (1D).
- `b` (`list` or `FloatArray`): Second vector (1D), same length as `a`.

**Returns:** `float`

**Raises:** `Error`: if `a` and `b` have different lengths.

```python
import math
result = math.dot([1, 2, 3], [4, 5, 6])  # 32.0

a = math.array([1.0, 2.0, 3.0])
b = math.array([4.0, 5.0, 6.0])
result = math.dot(a, b)  # 32.0
```

#### `matmul(a, b)`

Matrix-matrix multiply. `a` is `(M x K)`, `b` is `(K x N)`.

**Parameters:**
- `a` (`list` of `list`, or 2D `FloatArray`): Matrix of shape `(M, K)`.
- `b` (`list` of `list`, or 2D `FloatArray`): Matrix of shape `(K, N)`.

**Returns:** `list` of `list` (or `FloatArray` if either input was a `FloatArray`): matrix of shape `(M, N)`.

**Raises:** `Error`: if the inner dimensions don't match.

```python
import math
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = math.matmul(a, b)  # [[19.0, 22.0], [43.0, 50.0]]

fa = math.array([[1.0, 2.0], [3.0, 4.0]])
fb = math.array([[5.0, 6.0], [7.0, 8.0]])
result = math.matmul(fa, fb)  # Returns 2D FloatArray
```

#### `transpose(m)`

Transposes a 2D matrix: rows become columns.

**Parameters:**
- `m` (`list` of `list`, or 2D `FloatArray`): Matrix to transpose.

**Returns:** `list` of `list` (or `FloatArray` if input was a `FloatArray`): the transposed matrix.

```python
import math
m = [[1, 2, 3], [4, 5, 6]]
result = math.transpose(m)  # [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]

fa = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
result = math.transpose(fa)  # Returns 2D FloatArray with shape [3, 2]
```

#### `mat_add(a, b)`

Element-wise addition of two matrices.

**Parameters:**
- `a` (`list` of `list`, or 2D `FloatArray`): First matrix.
- `b` (`list` of `list`, or 2D `FloatArray`): Second matrix, same shape as `a`.

**Returns:** `list` of `list` (or `FloatArray` if either input was a `FloatArray`): element-wise sum.

**Raises:** `Error`: if `a` and `b` have different shapes.

```python
import math
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = math.mat_add(a, b)  # [[6.0, 8.0], [10.0, 12.0]]
```

#### `array(data)`

Creates an efficient `FloatArray` from a list. Accepts a 1D list of numbers, a 2D list of lists, or an existing `FloatArray` (returned unchanged).

**Parameters:**
- `data` (`list` or `FloatArray`): 1D list of numbers, or 2D list of equal-length lists of numbers.

**Returns:** `FloatArray`

```python
import math

a = math.array([1.0, 2.0, 3.0])
print(a[0])    # 1.0
print(len(a))  # 3

m = math.array([[1.0, 2.0], [3.0, 4.0]])
print(m[0])     # [1.0, 2.0]
print(m[0][1])  # 2.0
print(len(m))   # 2 (number of rows)

m[0][1] = 9.0
m[1] = [5.0, 6.0]

result = math.matmul(m, math.array([[1.0], [2.0]]))
```

#### `shape(a)`

Returns the shape of a `FloatArray` as a list of integers.

**Parameters:**
- `a` (`FloatArray`): Array to inspect.

**Returns:** `list` of `int`: one entry per dimension.

```python
import math
a = math.array([1.0, 2.0, 3.0])
print(math.shape(a))  # [3]

m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(math.shape(m))  # [2, 3]
```

## FloatArray

The `FloatArray` type, returned by `math.array()`, provides efficient storage and operations for numerical data, avoiding per-element boxing overhead.

### FloatArray Methods

#### `.tolist()`

Converts a `FloatArray` to a plain list.

**Parameters:** None

**Returns:** `list` of `float` (1D), or `list` of `list` of `float` (2D).

```python
import math

a = math.array([1.0, 2.0, 3.0])
plain = a.tolist()  # [1.0, 2.0, 3.0]

m = math.array([[1.0, 2.0], [3.0, 4.0]])
rows = m.tolist()   # [[1.0, 2.0], [3.0, 4.0]]
```

#### `.shape()`

Returns the shape of the `FloatArray` as a list of integers. Method equivalent of `math.shape()`.

**Parameters:** None

**Returns:** `list` of `int`

```python
import math

a = math.array([1.0, 2.0, 3.0])
print(a.shape())  # [3]

m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(m.shape())  # [2, 3]
```

### FloatArray Operators

#### `+` (concatenation)

Concatenates two `FloatArray`s. For 1D arrays, joins the elements. For 2D arrays with matching column counts, stacks the rows.

**Parameters:**
- `other` (`FloatArray`): Array to concatenate. For 2D arrays, must have the same number of columns.

**Returns:** `FloatArray`

```python
import math

a = math.array([1.0, 2.0])
b = math.array([3.0, 4.0])
c = a + b  # math.array([1.0, 2.0, 3.0, 4.0])

m = math.array([[1.0, 2.0], [3.0, 4.0]])
row = math.array([[5.0, 6.0]])
result = m + row  # shape [3, 2]
```

### FloatArray List Comprehensions

`FloatArray` supports list comprehensions for both 1D and 2D arrays:

```python
import math

a = math.array([1.0, 2.0, 3.0, 4.0])
doubled = [v * 2 for v in a]    # [2.0, 4.0, 6.0, 8.0]
big = [v for v in a if v > 2.5] # [3.0, 4.0]

m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
firsts = [row[0] for row in m]  # [1.0, 4.0]
rows_as_lists = [row.tolist() for row in m]
```

## Constants

### `pi`

The mathematical constant π (pi).

**Value:** `float`: `3.141592653589793`

```python
import math
pi = math.pi  # 3.141592653589793
```

### `e`

The mathematical constant e (Euler's number).

**Value:** `float`: `2.718281828459045`

```python
import math
e = math.e  # 2.718281828459045
```

### `inf`

Positive infinity.

**Value:** `float`: `inf`

```python
import math
result = math.inf  # inf
result = math.isinf(math.inf)  # True
```

### `nan`

NaN (Not a Number).

**Value:** `float`: `nan`

```python
import math
result = math.nan  # nan
result = math.isnan(math.nan)  # True
```

### `tau`

The mathematical constant τ (tau), equal to 2π.

**Value:** `float`: `6.283185307179586`

```python
import math
tau = math.tau  # 6.283185307179586
```

## Usage Example

```python
import math

result = math.sqrt(16)      # 4.0
power = math.pow(2, 8)      # 256.0
absolute = math.fabs(-5)    # 5.0 (float)
int_abs = abs(-5)           # 5 (use builtin for integer-preserving abs)

floor_val = math.floor(3.7) # 3
ceil_val = math.ceil(3.2)   # 4

sin_val = math.sin(0)       # 0.0
log_val = math.log(1)       # 0.0
exp_val = math.exp(1)       # 2.718281828459045

degrees_val = math.degrees(math.pi)  # 180.0
radians_val = math.radians(180)      # 3.141592653589793

mod_val = math.fmod(5.5, 2.0)  # 1.5
gcd_val = math.gcd(48, 18)     # 6
fact_val = math.factorial(5)   # 120

# Calculate circle area
radius = 5
area = math.pi * math.pow(radius, 2)
print("Area: " + str(area))  # Area: 78.53981633974483

# Calculate hypotenuse using Pythagoras
a = 3
b = 4
hypotenuse = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
print("Hypotenuse: " + str(hypotenuse))  # Hypotenuse: 5.0
```

## See Also

- [statistics](../statistics/): mean, median, variance, and other statistical functions.
- [random](../random/): random number generation.
