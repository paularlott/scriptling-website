---
description: Functions for calculating mathematical statistics of numeric data.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/statistics/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/statistics/
status: stable
tags:
    - libraries
    - math
title: statistics
type: API Reference
---
# statistics

The `statistics` library provides functions for calculating mathematical statistics of numeric data, following Python's `statistics` module: averages, central tendency, and measures of spread. Every function takes a single `list` of numbers (`mode` also accepts other values).

## Available Functions

| Function | Description |
|----------|-------------|
| `mean(data)` | Arithmetic mean, always a `float`. |
| `fmean(data)` | Arithmetic mean as a `float`. |
| `geometric_mean(data)` | Geometric mean; values must be positive. |
| `harmonic_mean(data)` | Harmonic mean; values must be positive. |
| `median(data)` | Middle value, or the mean of the two middle values for an even count. |
| `mode(data)` | Most common value. |
| `variance(data)` | Sample variance (needs at least two values). |
| `pvariance(data)` | Population variance. |
| `stdev(data)` | Sample standard deviation (needs at least two values). |
| `pstdev(data)` | Population standard deviation. |

## Example

```python
import statistics

data = [2, 4, 4, 4, 5, 5, 7, 9]

print(statistics.mean(data), statistics.fmean([1, 2, 3]))  # 5.0 2.0
print(statistics.median(data), statistics.median([1, 3, 5]))  # 4.5 3
print(statistics.mode(["a", "b", "b"]))           # b
print(round(statistics.geometric_mean([1, 2, 4, 8]), 3))  # 2.828
print(round(statistics.harmonic_mean([40, 60]), 6))  # 48.0

# Sample statistics (data is a sample of a larger population)
print(round(statistics.variance(data), 3), round(statistics.stdev(data), 3))  # 4.571 2.138
# Population statistics (data is the whole population)
print(statistics.pvariance(data), statistics.pstdev(data))  # 4.0 2.0
```

## Differences from Python

- `data` must be a `list`; tuples, ranges and other iterables raise a type error, so wrap them with `list(...)`.
- `mean()` and `pvariance()` always return a `float` (Python returns an `int` for integer data that divides evenly, e.g. `mean([1, 2, 3])` is `2.0` here).
- `variance()`/`stdev()` take no `xbar` argument, and `pvariance()`/`pstdev()` take no `mu` argument.
- `geometric_mean()` and `harmonic_mean()` raise on zero or negative values (Python returns `0` for a zero).
- `median_low`, `median_high`, `median_grouped`, `multimode`, `quantiles`, and `NormalDist` are not available.

## See Also

- [math](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math.md): mathematical functions and constants.
- [random](https://scriptling.dev/okf/scriptling-libraries/math-numbers/random.md): random number generation, including Gaussian and other distributions.
