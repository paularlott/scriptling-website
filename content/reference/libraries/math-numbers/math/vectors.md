---
title: Vectors & FloatArray
description: Vector and matrix functions in the math library, and the FloatArray type returned by math.array().
tags: [libraries, math]
weight: 1
---

Part of the [math](../) library. These functions treat lists of numbers as vectors and matrices; `math.array()` converts a list into a `FloatArray` for efficient numerical storage.

## Vector and Matrix Functions

### `dist(p, q)`

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

### `softmax(x)`

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

### `dot(a, b)`

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

### `matmul(a, b)`

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

### `transpose(m)`

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

### `mat_add(a, b)`

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

### `array(data)`

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

### `shape(a)`

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

## See Also

- [math](../): the scalar math functions and constants.
- [statistics](../../statistics/): mean, median, variance, and other statistical functions.
