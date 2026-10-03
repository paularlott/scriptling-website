---
description: Mathematical functions and constants.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/math/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/math/
status: stable
tags:
    - libraries
    - math
title: math
type: API Reference
---
# math

The `math` library provides mathematical functions and constants: trigonometry, logarithms, rounding, combinatorics, and basic vector/matrix operations via `FloatArray`.

**In this section**

- [Vectors & FloatArray](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math/vectors.md): `dist`, `dot`, `matmul`, `transpose`, `mat_add`, `softmax`, `array`, `shape`, and the `FloatArray` type.

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
| `log(x)` | Natural logarithm of `x` (no `base` argument; see below). |
| `log10(x)` | Base-10 logarithm of `x`. |
| `log2(x)` | Base-2 logarithm of `x`. |
| `exp(x)` | `e` raised to the power of `x`. |
| `degrees(x)` | Convert radians to degrees. |
| `radians(x)` | Convert degrees to radians. |
| `hypot(x, y)` | Euclidean distance `sqrt(x*x + y*y)` (two arguments only). |
| `fmod(x, y)` | Floating-point remainder of `x/y`. |
| `gcd(a, b)` | Greatest common divisor of exactly two integers. |
| `factorial(n)` | Factorial of `n`, for `0 <= n <= 20`. |
| `copysign(x, y)` | `x` with the sign of `y`. |
| `isnan(x)` | Whether `x` is NaN. |
| `isinf(x)` | Whether `x` is positive or negative infinity. |
| `isfinite(x)` | Whether `x` is neither NaN nor infinite. |
| `tanh(x)` | Hyperbolic tangent of `x`. |
| `erf(x)` | Error function of `x`. |
| `erfc(x)` | Complementary error function of `x`. |
| `gamma(x)` | Gamma function of `x`. |
| `lgamma(x)` | `[log(abs(gamma(x))), sign]` as a list (differs from Python). |
| `cbrt(x)` | Cube root of `x`. |
| `nextafter(x, y)` | Next float after `x` towards `y`. |
| `remainder(x, y)` | IEEE 754-style remainder of `x/y`. |
| `log1p(x)` | `log(1+x)`, accurate for small `x`. |
| `expm1(x)` | `exp(x)-1`, accurate for small `x`. |
| `comb(n, k)` | Number of ways to choose `k` from `n` (unordered). |
| `perm(n[, k])` | Number of ways to choose `k` from `n` (ordered). |
| `prod(iterable, start=1)` | Product of all elements in a list; `start` is keyword-only. |
| `dist(p, q)` | Euclidean distance between two points (see [Vectors](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math/vectors.md)). |
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

Functions from `dist` to `shape` are documented on [Vectors & FloatArray](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math/vectors.md). Everything else behaves like Python's `math` module, apart from the differences below. Python functions not in the table (for example `lcm`, `isqrt`, `fsum`, `isclose`, `sinh`, `cosh`, `modf`, `frexp`) are not available.

## Example

```python
import math

print(math.sqrt(16), math.pow(2, 8), math.cbrt(-8))    # 4.0 256.0 -2.0
print(math.floor(3.7), math.ceil(3.2), math.trunc(-3.7))  # 3 4 -3
print(math.fabs(-5), abs(-5))                          # 5.0 5
print(math.degrees(math.pi), math.radians(180))        # 180.0 3.141592653589793
print(math.hypot(3, 4), math.atan2(1, 1))              # 5.0 0.7853981633974483
print(math.log(math.e), math.log10(1000), math.log2(8))  # 1.0 3.0 3.0
print(math.fmod(5.5, 2.0), math.remainder(7.5, 2))     # 1.5 -0.5
print(math.gcd(48, 18), math.factorial(5))             # 6 120
print(math.comb(5, 2), math.perm(5, 2), math.prod([1, 2, 3, 4]))  # 10 20 24
print(math.isnan(math.nan), math.isinf(-math.inf), math.isfinite(5))  # True True True

area = math.pi * 5 ** 2
print(f"Area: {area:.2f}")                             # Area: 78.54
```

## Differences from Python

- **`lgamma(x)`** returns a two-element list `[log_abs_gamma, sign]`, where `sign` is `1` or `-1`, rather than a single float: `math.lgamma(5)` is `[3.1780538303479458, 1]`.
- **`factorial(n)`** accepts `0 <= n <= 20` only; larger values raise `factorial: result too large`. **`comb(n, k)`** and **`perm(n[, k])`** likewise raise when the result does not fit in a 64-bit integer (`math.comb(100, 50)` fails). `perm(n, k)` returns `0` when `k > n`.
- **`log(x)`** takes one argument. For other bases use `log10`, `log2`, or `math.log(x) / math.log(base)`.
- **`gcd(a, b)`** and **`hypot(x, y)`** take exactly two arguments, not any number.
- **`sqrt(x)`** of a negative number returns `nan` instead of raising `ValueError`. `log(x)` with `x <= 0` and `fmod(x, 0)` still raise.
- **`prod(iterable, start=...)`** returns a float when `start` is given, even for integers: `math.prod([1, 2], start=5)` is `10.0`. Without `start`, an all-integer list gives an `int`.
- **`fabs(x)`** always returns a float (as in Python); use the builtin `abs()` to keep integers as integers.

## See Also

- [Vectors & FloatArray](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math/vectors.md): `dist`, `dot`, `matmul`, `softmax`, and the `FloatArray` type.
- [statistics](https://scriptling.dev/okf/scriptling-libraries/math-numbers/statistics.md): mean, median, variance, and other statistical functions.
- [random](https://scriptling.dev/okf/scriptling-libraries/math-numbers/random.md): random number generation.
