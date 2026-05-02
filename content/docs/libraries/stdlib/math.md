---
title: math
weight: 1
---

Mathematical functions and constants.

## Available Functions

| Function           | Description                                        |
| ------------------ | -------------------------------------------------- |
| `sqrt(x)`          | Returns the square root of x                       |
| `pow(base, exp)`   | Returns base raised to the power of exp            |
| `fabs(x)`          | Returns the absolute value of x as a float         |
| `floor(x)`         | Rounds x down to the nearest integer               |
| `ceil(x)`          | Rounds x up to the nearest integer                 |
| `trunc(x)`         | Truncates x to the nearest integer toward zero     |
| `sin(x)`           | Returns the sine of x (in radians)                 |
| `cos(x)`           | Returns the cosine of x (in radians)               |
| `tan(x)`           | Returns the tangent of x (in radians)              |
| `asin(x)`          | Returns the arc sine of x (in radians)             |
| `acos(x)`          | Returns the arc cosine of x (in radians)           |
| `atan(x)`          | Returns the arc tangent of x (in radians)          |
| `atan2(y, x)`      | Returns the arc tangent of y/x (in radians)        |
| `log(x)`           | Returns the natural logarithm of x                 |
| `log10(x)`         | Returns the base-10 logarithm of x                 |
| `log2(x)`          | Returns the base-2 logarithm of x                  |
| `exp(x)`           | Returns e raised to the power of x                 |
| `degrees(x)`       | Converts radians to degrees                        |
| `radians(x)`       | Converts degrees to radians                        |
| `hypot(x, y)`      | Returns the Euclidean distance sqrt(x*x + y*y)     |
| `fmod(x, y)`       | Returns the floating-point remainder of x/y        |
| `gcd(a, b)`        | Returns the greatest common divisor                |
| `factorial(n)`     | Returns the factorial of n                         |
| `copysign(x, y)`   | Returns x with the sign of y                       |
| `isnan(x)`         | Returns true if x is NaN (Not a Number)            |
| `isinf(x)`         | Returns true if x is positive or negative infinity |
| `isfinite(x)`      | Returns true if x is neither NaN nor infinite      |
| `tanh(x)`          | Returns the hyperbolic tangent of x                |
| `erf(x)`           | Returns the error function of x                    |
| `erfc(x)`          | Returns the complementary error function of x      |
| `gamma(x)`         | Returns the gamma function of x                    |
| `lgamma(x)`        | Returns the natural log of the absolute gamma      |
| `cbrt(x)`          | Returns the cube root of x                         |
| `nextafter(x, y)`  | Returns the next float after x towards y           |
| `remainder(x, y)`  | Returns the IEEE 754-style remainder of x/y        |
| `log1p(x)`         | Returns log(1+x) accurately for small x            |
| `expm1(x)`         | Returns exp(x)-1 accurately for small x            |
| `comb(n, k)`       | Returns the number of ways to choose k from n      |
| `perm(n[, k])`     | Returns permutations of k items from n             |
| `prod(iterable)`   | Returns the product of all elements in a list      |
| `dist(p, q)`       | Returns the Euclidean distance between two points  |
| `softmax(x)`       | Returns the softmax of a vector                    |
| `dot(a, b)`        | Returns the dot product of two vectors             |
| `matmul(a, b)`     | Matrix-matrix multiply                             |
| `transpose(m)`     | Transpose a 2D matrix                              |
| `mat_add(a, b)`    | Element-wise addition of two matrices              |
| `array(data)`      | Create an efficient FloatArray from a list         |
| `shape(a)`         | Return the shape of a FloatArray as a list of ints |

## Constants

| Constant | Description                            |
| -------- | -------------------------------------- |
| `pi`     | The mathematical constant π            |
| `e`      | The mathematical constant e            |
| `inf`    | Positive infinity                      |
| `nan`    | NaN (Not a Number)                     |
| `tau`    | The mathematical constant τ (2π)      |

## Functions

### math.sqrt(x)

Returns the square root of x.

**Parameters:**

- `x`: Number (integer or float)

**Returns:** Float

**Example:**

```python
import math
result = math.sqrt(16)  # 4.0
```

### math.pow(base, exp)

Returns base raised to the power of exp (base^exp).

**Parameters:**

- `base`: Base number
- `exp`: Exponent

**Returns:** Float

**Example:**

```python
import math
result = math.pow(2, 8)  # 256.0
```

### math.fabs(x)

Returns the absolute value of x as a float.

**Parameters:**

- `x`: Number (integer or float)

**Returns:** Float (always returns floating-point)

**Example:**

```python
import math
result = math.fabs(-5)    # 5.0
result = math.fabs(-3.14) # 3.14
```

> **Note:** For absolute value that preserves integer type, use the builtin `abs()` function instead.

### math.floor(x)

Rounds x down to the nearest integer.

**Parameters:**

- `x`: Number

**Returns:** Integer

**Example:**

```python
import math
result = math.floor(3.7)  # 3
```

### math.ceil(x)

Rounds x up to the nearest integer.

**Parameters:**

- `x`: Number

**Returns:** Integer

**Example:**

```python
import math
result = math.ceil(3.2)  # 4
```

> **Note:** For rounding to nearest integer, use the builtin `round()` function.
> For min/max values, use the builtin `min()` and `max()` functions.

### math.sin(x)

Returns the sine of x (in radians).

**Parameters:**

- `x`: Angle in radians

**Returns:** Float

**Example:**

```python
import math
result = math.sin(0)  # 0.0
result = math.sin(math.pi / 2)  # 1.0
```

### math.cos(x)

Returns the cosine of x (in radians).

**Parameters:**

- `x`: Angle in radians

**Returns:** Float

**Example:**

```python
import math
result = math.cos(0)  # 1.0
result = math.cos(math.pi)  # -1.0
```

### math.tan(x)

Returns the tangent of x (in radians).

**Parameters:**

- `x`: Angle in radians

**Returns:** Float

**Example:**

```python
import math
result = math.tan(0)  # 0.0
result = math.tan(math.pi / 4)  # 1.0
```

### math.log(x)

Returns the natural logarithm (base e) of x.

**Parameters:**

- `x`: Number (must be > 0)

**Returns:** Float

**Example:**

```python
import math
result = math.log(1)  # 0.0
result = math.log(math.e)  # 1.0
```

### math.exp(x)

Returns e raised to the power of x (e^x).

**Parameters:**

- `x`: Number

**Returns:** Float

**Example:**

```python
import math
result = math.exp(0)  # 1.0
result = math.exp(1)  # 2.718281828459045
```

### math.degrees(x)

Converts angle x from radians to degrees.

**Parameters:**

- `x`: Angle in radians

**Returns:** Float

**Example:**

```python
import math
result = math.degrees(math.pi)  # 180.0
result = math.degrees(math.pi / 2)  # 90.0
```

### math.radians(x)

Converts angle x from degrees to radians.

**Parameters:**

- `x`: Angle in degrees

**Returns:** Float

**Example:**

```python
import math
result = math.radians(180)  # 3.141592653589793
result = math.radians(90)   # 1.5707963267948966
```

### math.fmod(x, y)

Returns the floating-point remainder of x divided by y.

**Parameters:**

- `x`: Dividend
- `y`: Divisor (cannot be 0)

**Returns:** Float

**Example:**

```python
import math
result = math.fmod(5.5, 2.0)  # 1.5
result = math.fmod(7.0, 3.0)  # 1.0
```

### math.gcd(a, b)

Returns the greatest common divisor of integers a and b.

**Parameters:**

- `a`: Integer
- `b`: Integer

**Returns:** Integer

**Example:**

```python
import math
result = math.gcd(48, 18)  # 6
result = math.gcd(100, 75) # 25
```

### math.factorial(n)

Returns the factorial of n (n!).

**Parameters:**

- `n`: Non-negative integer (0 ≤ n ≤ 20)

**Returns:** Integer

**Example:**

```python
import math
result = math.factorial(5)  # 120
result = math.factorial(0)  # 1
```

### math.trunc(x)

Truncates x to the nearest integer toward zero.

**Parameters:**

- `x`: Number (integer or float)

**Returns:** Integer

**Example:**

```python
import math
result = math.trunc(3.7)   # 3
result = math.trunc(-3.7)  # -3
```

### math.asin(x)

Returns the arc sine of x in radians.

**Parameters:**

- `x`: Number in range [-1, 1]

**Returns:** Float

**Example:**

```python
import math
result = math.asin(0)    # 0.0
result = math.asin(1)    # 1.5707963267948966 (pi/2)
```

### math.acos(x)

Returns the arc cosine of x in radians.

**Parameters:**

- `x`: Number in range [-1, 1]

**Returns:** Float

**Example:**

```python
import math
result = math.acos(1)    # 0.0
result = math.acos(0)    # 1.5707963267948966 (pi/2)
```

### math.atan(x)

Returns the arc tangent of x in radians.

**Parameters:**

- `x`: Number

**Returns:** Float in range [-pi/2, pi/2]

**Example:**

```python
import math
result = math.atan(0)    # 0.0
result = math.atan(1)    # 0.7853981633974483 (pi/4)
```

### math.atan2(y, x)

Returns the arc tangent of y/x in radians, correctly handling the quadrant.

**Parameters:**

- `y`: Y coordinate
- `x`: X coordinate

**Returns:** Float in range [-pi, pi]

**Example:**

```python
import math
result = math.atan2(1, 1)   # 0.7853981633974483 (pi/4)
result = math.atan2(-1, 1)  # -0.7853981633974483
```

### math.log10(x)

Returns the base-10 logarithm of x.

**Parameters:**

- `x`: Positive number

**Returns:** Float

**Example:**

```python
import math
result = math.log10(100)  # 2.0
result = math.log10(1000) # 3.0
```

### math.log2(x)

Returns the base-2 logarithm of x.

**Parameters:**

- `x`: Positive number

**Returns:** Float

**Example:**

```python
import math
result = math.log2(8)   # 3.0
result = math.log2(16)  # 4.0
```

### math.hypot(x, y)

Returns the Euclidean distance sqrt(x*x + y*y).

**Parameters:**

- `x`: First coordinate
- `y`: Second coordinate

**Returns:** Float

**Example:**

```python
import math
result = math.hypot(3, 4)  # 5.0
result = math.hypot(5, 12) # 13.0
```

### math.copysign(x, y)

Returns x with the sign of y.

**Parameters:**

- `x`: Magnitude value
- `y`: Sign value

**Returns:** Float with magnitude of x and sign of y

**Example:**

```python
import math
result = math.copysign(5, -1)   # -5.0
result = math.copysign(-5, 1)   # 5.0
```

### math.isnan(x)

Returns true if x is NaN (Not a Number).

**Parameters:**

- `x`: Number to check

**Returns:** Boolean

**Example:**

```python
import math
result = math.isnan(math.nan)  # True
result = math.isnan(5)         # False
```

### math.isinf(x)

Returns true if x is positive or negative infinity.

**Parameters:**

- `x`: Number to check

**Returns:** Boolean

**Example:**

```python
import math
result = math.isinf(math.inf)   # True
result = math.isinf(-math.inf)  # True
result = math.isinf(5)          # False
```

### math.isfinite(x)

Returns true if x is neither NaN nor infinite.

**Parameters:**

- `x`: Number to check

**Returns:** Boolean

**Example:**

```python
import math
result = math.isfinite(5)         # True
result = math.isfinite(math.inf)  # False
result = math.isfinite(math.nan)  # False
```

### math.tanh(x)

Returns the hyperbolic tangent of x.

**Parameters:**

- `x`: Number

**Returns:** Float in range [-1, 1]

**Example:**

```python
import math
result = math.tanh(0)    # 0.0
result = math.tanh(1)    # 0.7615941559557649
```

### math.erf(x)

Returns the error function of x.

**Parameters:**

- `x`: Number

**Returns:** Float in range [-1, 1]

**Example:**

```python
import math
result = math.erf(0)    # 0.0
result = math.erf(1)    # 0.8427007929497149
```

### math.erfc(x)

Returns the complementary error function of x.

**Parameters:**

- `x`: Number

**Returns:** Float in range [0, 2]

**Example:**

```python
import math
result = math.erfc(0)    # 1.0
result = math.erfc(1)    # 0.1572992070502851
```

### math.gamma(x)

Returns the gamma function of x.

**Parameters:**

- `x`: Number

**Returns:** Float

**Example:**

```python
import math
result = math.gamma(1)    # 1.0
result = math.gamma(5)    # 24.0 (4!)
```

### math.lgamma(x)

Returns the natural log of the absolute value of the gamma function.

**Parameters:**

- `x`: Number

**Returns:** List `[log_abs_gamma, sign]`

**Example:**

```python
import math
result = math.lgamma(5)  # [3.1780538303479458, 1]
```

### math.cbrt(x)

Returns the cube root of x.

**Parameters:**

- `x`: Number

**Returns:** Float

**Example:**

```python
import math
result = math.cbrt(27)   # 3.0
result = math.cbrt(-8)   # -2.0
```

### math.nextafter(x, y)

Returns the next floating-point value after x towards y.

**Parameters:**

- `x`: Starting value
- `y`: Direction value

**Returns:** Float

**Example:**

```python
import math
result = math.nextafter(1.0, 2.0)  # 1.0000000000000002
result = math.nextafter(1.0, 0.0)  # 0.9999999999999999
```

### math.remainder(x, y)

Returns the IEEE 754-style remainder of x/y.

**Parameters:**

- `x`: Dividend
- `y`: Divisor

**Returns:** Float

**Example:**

```python
import math
result = math.remainder(7, 3)   # 1.0
result = math.remainder(7.5, 2) # -0.5
```

### math.log1p(x)

Returns log(1+x) accurately for small x.

**Parameters:**

- `x`: Number

**Returns:** Float

**Example:**

```python
import math
result = math.log1p(0)    # 0.0
result = math.log1p(1e-15)  # 9.999999999999995e-16
```

### math.expm1(x)

Returns exp(x)-1 accurately for small x.

**Parameters:**

- `x`: Number

**Returns:** Float

**Example:**

```python
import math
result = math.expm1(0)    # 0.0
result = math.expm1(1e-10)  # 1.00000000005e-10
```

### math.comb(n, k)

Returns the number of ways to choose k items from n (binomial coefficient).

**Parameters:**

- `n`: Non-negative integer
- `k`: Non-negative integer

**Returns:** Integer

**Example:**

```python
import math
result = math.comb(5, 2)   # 10
result = math.comb(10, 3)  # 120
```

### math.perm(n[, k])

Returns the number of ways to choose k items from n with order.

**Parameters:**

- `n`: Non-negative integer
- `k` (optional): Non-negative integer. If omitted, returns n!

**Returns:** Integer

**Example:**

```python
import math
result = math.perm(5)    # 120 (5!)
result = math.perm(5, 2) # 20
```

### math.prod(iterable, start=1)

Returns the product of all elements in a list.

**Parameters:**

- `iterable`: List of numbers
- `start` (keyword-only, optional): Starting value for multiplication. Default: 1

**Returns:** Integer for all-integer inputs, float otherwise

**Example:**

```python
import math
result = math.prod([1, 2, 3, 4])  # 24
result = math.prod([1.5, 2.0])    # 3.0
result = math.prod([1, 2], start=5) # 10
```

### math.dist(p, q)

Returns the Euclidean distance between two points.

**Parameters:**

- `p`: List of numbers (first point)
- `q`: List of numbers (second point, same dimension)

**Returns:** Float

**Example:**

```python
import math
result = math.dist([0, 0], [3, 4])  # 5.0
result = math.dist([1, 2, 3], [4, 6, 3])  # 5.0
```

### math.softmax(x)

Returns the numerically stable softmax of a vector.

**Parameters:**

- `x`: List of numbers or 1D FloatArray

**Returns:** List of floats or FloatArray (probability distribution summing to 1.0). Returns FloatArray when input is FloatArray.

**Example:**

```python
import math
result = math.softmax([1.0, 2.0, 3.0])
print(result)  # [0.0900..., 0.2447..., 0.6652...]

# With FloatArray input
a = math.array([1.0, 2.0, 3.0])
result = math.softmax(a)  # Returns FloatArray
```

### math.dot(a, b)

Returns the dot product of two vectors.

**Parameters:**

- `a`: List of numbers or 1D FloatArray
- `b`: List of numbers or 1D FloatArray (same length)

**Returns:** Float

**Example:**

```python
import math
result = math.dot([1, 2, 3], [4, 5, 6])  # 32.0

# With FloatArray inputs
a = math.array([1.0, 2.0, 3.0])
b = math.array([4.0, 5.0, 6.0])
result = math.dot(a, b)  # 32.0
```

### math.matmul(a, b)

Matrix-matrix multiply. a is (M x K), b is (K x N). Returns (M x N) matrix.

**Parameters:**

- `a`: Matrix as list of lists or 2D FloatArray (M x K)
- `b`: Matrix as list of lists or 2D FloatArray (K x N)

**Returns:** Matrix as list of lists or 2D FloatArray (M x N). Returns FloatArray when either input is FloatArray.

**Example:**

```python
import math
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = math.matmul(a, b)  # [[19.0, 22.0], [43.0, 50.0]]

# With FloatArray inputs
fa = math.array([[1.0, 2.0], [3.0, 4.0]])
fb = math.array([[5.0, 6.0], [7.0, 8.0]])
result = math.matmul(fa, fb)  # Returns 2D FloatArray
```

### math.transpose(m)

Transpose a 2D matrix. Rows become columns.

**Parameters:**

- `m`: Matrix as list of lists or 2D FloatArray

**Returns:** New transposed matrix. Returns FloatArray when input is FloatArray.

**Example:**

```python
import math
m = [[1, 2, 3], [4, 5, 6]]
result = math.transpose(m)  # [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]

# With FloatArray input
fa = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
result = math.transpose(fa)  # Returns 2D FloatArray with shape [3, 2]
```

### math.mat_add(a, b)

Element-wise addition of two matrices.

**Parameters:**

- `a`: Matrix as list of lists or 2D FloatArray
- `b`: Matrix as list of lists or 2D FloatArray (same shape)

**Returns:** New matrix with element-wise sums. Returns FloatArray when either input is FloatArray.

**Example:**

```python
import math
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = math.mat_add(a, b)  # [[6.0, 8.0], [10.0, 12.0]]
```

### math.array(data)

Create an efficient FloatArray from a list. Accepts a 1D list of numbers or a 2D list of lists. Returns a FloatArray that avoids per-element boxing overhead.

**Parameters:**

- `data`: List of numbers (1D) or list of lists of numbers (2D), or an existing FloatArray

**Returns:** FloatArray

**Example:**

```python
import math

# 1D array
a = math.array([1.0, 2.0, 3.0])
print(a[0])      # 1.0
print(len(a))    # 3

# 2D array
m = math.array([[1.0, 2.0], [3.0, 4.0]])
print(m[0])      # [1.0, 2.0]
print(m[0][1])   # 2.0
print(len(m))    # 2 (number of rows)

# Assignment
m[0][1] = 9.0
m[1] = [5.0, 6.0]

# Works with math operations
result = math.matmul(m, math.array([[1.0], [2.0]]))
```

## FloatArray

The `FloatArray` type is returned by `math.array()`. It provides efficient storage and operations for numerical data.

### FloatArray Methods

#### .tolist()

Convert a FloatArray to a plain list. For 1D arrays, returns a list of floats. For 2D arrays, returns a list of lists.

**Parameters:** None

**Returns:** List of floats (1D) or list of lists of floats (2D)

**Example:**

```python
import math

# 1D
a = math.array([1.0, 2.0, 3.0])
plain = a.tolist()  # [1.0, 2.0, 3.0]

# 2D
m = math.array([[1.0, 2.0], [3.0, 4.0]])
rows = m.tolist()   # [[1.0, 2.0], [3.0, 4.0]]
```

#### .shape()

Return the shape of the FloatArray as a list of integers. This is the method equivalent of `math.shape()`.

**Parameters:** None

**Returns:** List of integers representing dimensions

**Example:**

```python
import math

a = math.array([1.0, 2.0, 3.0])
print(a.shape())  # [3]

m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(m.shape())  # [2, 3]
```

### FloatArray Operators

#### `+` (concatenation)

Concatenate two FloatArrays. For 1D arrays, joins the elements. For 2D arrays with matching column counts, stacks the rows.

**Parameters:**

- `other`: FloatArray (must have same number of columns for 2D)

**Returns:** FloatArray

**Example:**

```python
import math

# 1D concatenation
a = math.array([1.0, 2.0])
b = math.array([3.0, 4.0])
c = a + b  # math.array([1.0, 2.0, 3.0, 4.0])

# 2D row stacking
m = math.array([[1.0, 2.0], [3.0, 4.0]])
row = math.array([[5.0, 6.0]])
result = m + row  # shape [3, 2]
```

### FloatArray List Comprehensions

FloatArray supports list comprehensions for both 1D and 2D arrays:

```python
import math

# 1D: iterate over values
a = math.array([1.0, 2.0, 3.0, 4.0])
doubled = [v * 2 for v in a]          # [2.0, 4.0, 6.0, 8.0]
big = [v for v in a if v > 2.5]       # [3.0, 4.0, 5.0]

# 2D: iterate over rows (each row is a 1D FloatArray)
m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
firsts = [row[0] for row in m]        # [1.0, 4.0]
rows_as_lists = [row.tolist() for row in m]
```

### math.shape(a)

Return the shape of a FloatArray as a list of integers.

**Parameters:**

- `a`: FloatArray

**Returns:** List of integers representing dimensions

**Example:**

```python
import math
a = math.array([1.0, 2.0, 3.0])
print(math.shape(a))  # [3]

m = math.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(math.shape(m))  # [2, 3]
```

## Constants

### math.pi

The mathematical constant π (pi).

**Value:** Float (3.141592653589793)

**Example:**

```python
import math
pi = math.pi  # 3.141592653589793
```

### math.e

The mathematical constant e (Euler's number).

**Value:** Float (2.718281828459045)

**Example:**

```python
import math
e = math.e  # 2.718281828459045
```

### math.inf

Positive infinity.

**Value:** Float (infinity)

**Example:**

```python
import math
result = math.inf  # inf
result = math.isinf(math.inf)  # True
```

### math.nan

NaN (Not a Number).

**Value:** Float (NaN)

**Example:**

```python
import math
result = math.nan  # nan
result = math.isnan(math.nan)  # True
```

### math.tau

The mathematical constant τ (tau), equal to 2π.

**Value:** Float (6.283185307179586)

**Example:**

```python
import math
tau = math.tau  # 6.283185307179586
```

## Usage Example

```python
import math

# Basic operations
result = math.sqrt(16)      # 4.0
power = math.pow(2, 8)      # 256.0
absolute = math.fabs(-5)    # 5.0 (float)

# For integer-preserving abs, use builtin:
int_abs = abs(-5)           # 5

# Rounding
floor_val = math.floor(3.7) # 3
ceil_val = math.ceil(3.2)   # 4
round_val = round(3.5)      # 4 (use builtin round)

# Min/Max (use builtins)
minimum = min(3, 1, 4, 1, 5)  # 1
maximum = max(3, 1, 4, 1, 5)  # 5

# Trigonometric functions
sin_val = math.sin(0)       # 0.0
cos_val = math.cos(0)       # 1.0
tan_val = math.tan(0)       # 0.0

# Logarithmic and exponential
log_val = math.log(1)       # 0.0
exp_val = math.exp(1)       # 2.718281828459045

# Angle conversion
degrees_val = math.degrees(math.pi)  # 180.0
radians_val = math.radians(180)        # 3.141592653589793

# Modular arithmetic
mod_val = math.fmod(5.5, 2.0)  # 1.5
gcd_val = math.gcd(48, 18)     # 6
fact_val = math.factorial(5)   # 120

# Constants
pi = math.pi  # 3.141592653589793
e = math.e    # 2.718281828459045

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
