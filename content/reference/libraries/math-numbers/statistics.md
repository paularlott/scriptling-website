---
title: statistics
description: Functions for calculating mathematical statistics of numeric data.
weight: 1

aliases:
  - /reference/libraries/stdlib/statistics/
  - /reference/libraries/statistics/
---

The `statistics` library provides functions for calculating mathematical statistics of numeric data, compatible with Python's `statistics` module: averages, central tendency, and measures of spread.

## Available Functions

| Function | Description |
|----------|-------------|
| `mean(data)` | Arithmetic mean (average). |
| `fmean(data)` | Arithmetic mean (always returns float). |
| `geometric_mean(data)` | Geometric mean. |
| `harmonic_mean(data)` | Harmonic mean. |
| `median(data)` | Median (middle value). |
| `mode(data)` | Mode (most common value). |
| `variance(data)` | Sample variance. |
| `pvariance(data)` | Population variance. |
| `stdev(data)` | Sample standard deviation. |
| `pstdev(data)` | Population standard deviation. |

## Functions

### Averages

#### `mean(data)`

Calculates the arithmetic mean (average) of `data`.

**Parameters:**
- `data` (`list` of `int`/`float`): Values to average. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty.

```python
import statistics

statistics.mean([1, 2, 3, 4, 5])     # 3.0
statistics.mean([10.5, 20.5, 30.5])  # 20.5
```

#### `fmean(data)`

Calculates the arithmetic mean of `data`. Equivalent to `mean()`; provided for Python compatibility where `fmean` always returns a float.

**Parameters:**
- `data` (`list` of `int`/`float`): Values to average. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty.

```python
import statistics

statistics.fmean([1, 2, 3, 4, 5])  # 3.0
```

#### `geometric_mean(data)`

Calculates the geometric mean of `data`.

**Parameters:**
- `data` (`list` of `int`/`float`): Positive values. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty or contains a non-positive value.

```python
import statistics

statistics.geometric_mean([1, 2, 4, 8])   # ~2.83
statistics.geometric_mean([1, 3, 9, 27])  # 5.196...
```

#### `harmonic_mean(data)`

Calculates the harmonic mean of `data`.

**Parameters:**
- `data` (`list` of `int`/`float`): Positive values. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty or contains a non-positive value.

```python
import statistics

statistics.harmonic_mean([1, 2, 4])  # ~1.71
```

### Central Tendency

#### `median(data)`

Calculates the median (middle value) of `data`.

**Parameters:**
- `data` (`list` of `int`/`float`): Values. Must contain at least one element.

**Returns:** `float`: the middle value for an odd-length list, or the average of the two middle values for an even-length list.

**Raises:** `Error`: if `data` is empty.

```python
import statistics

statistics.median([1, 3, 5, 7, 9])  # 5.0 (odd count)
statistics.median([1, 2, 3, 4])     # 2.5 (even count)
```

#### `mode(data)`

Calculates the mode (most common value) of `data`.

**Parameters:**
- `data` (`list`): Values of any comparable type. Must contain at least one element.

**Returns:** `any`: the most frequent element, same type as the input elements. If multiple values tie for most frequent, one of them is returned (not necessarily the first encountered).

**Raises:** `Error`: if `data` is empty.

```python
import statistics

statistics.mode([1, 2, 2, 3, 3, 3])  # 3
statistics.mode(["a", "b", "b"])     # "b"
```

### Measures of Spread

#### `variance(data)`

Calculates the sample variance of `data` (divides by `n - 1`).

**Parameters:**
- `data` (`list` of `int`/`float`): Values. Must contain at least two elements.

**Returns:** `float`

**Raises:** `Error`: if `data` has fewer than two elements.

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]
statistics.variance(data)  # ~4.57
```

#### `pvariance(data)`

Calculates the population variance of `data` (divides by `n`).

**Parameters:**
- `data` (`list` of `int`/`float`): Values. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty.

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]
statistics.pvariance(data)  # 4.0
```

#### `stdev(data)`

Calculates the sample standard deviation of `data`: the square root of `variance()`.

**Parameters:**
- `data` (`list` of `int`/`float`): Values. Must contain at least two elements.

**Returns:** `float`

**Raises:** `Error`: if `data` has fewer than two elements.

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]
statistics.stdev(data)  # ~2.14
```

#### `pstdev(data)`

Calculates the population standard deviation of `data`: the square root of `pvariance()`.

**Parameters:**
- `data` (`list` of `int`/`float`): Values. Must contain at least one element.

**Returns:** `float`

**Raises:** `Error`: if `data` is empty.

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]
statistics.pstdev(data)  # 2.0
```

## Examples

### Basic Statistics

```python
import statistics

grades = [85, 90, 78, 92, 88, 76, 95, 89]

avg = statistics.mean(grades)
med = statistics.median(grades)
std = statistics.stdev(grades)

print(f"Average: {avg}")
print(f"Median: {med}")
print(f"Std Dev: {std}")
```

### Comparing Sample vs Population Statistics

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]

# Sample statistics (use when data is a sample of a larger population)
sample_var = statistics.variance(data)
sample_std = statistics.stdev(data)

# Population statistics (use when data is the entire population)
pop_var = statistics.pvariance(data)
pop_std = statistics.pstdev(data)
```

## Python Compatibility

This library implements a subset of Python's `statistics` module:

| Function | Supported |
|----------|-----------|
| `mean` | Yes |
| `fmean` | Yes |
| `geometric_mean` | Yes |
| `harmonic_mean` | Yes |
| `median` | Yes |
| `median_low` | No |
| `median_high` | No |
| `median_grouped` | No |
| `mode` | Yes |
| `multimode` | No |
| `variance` | Yes |
| `pvariance` | Yes |
| `stdev` | Yes |
| `pstdev` | Yes |
| `quantiles` | No |
| `NormalDist` | No |

## See Also

- [math](../math/): mathematical functions and constants.
- [random](../random/): random number generation, including Gaussian and other distributions.
