---
title: random
description: Random number generation, compatible with Python's random module.
tags: [libraries, math]
weight: 1

aliases:
  - /reference/libraries/stdlib/random/
  - /reference/libraries/random/
---

The `random` library generates random integers, floats, and samples: including several statistical distributions: with a Python-compatible API.

## Available Functions

| Function | Description |
|----------|-------------|
| `seed([a])` | Initialize the random number generator. |
| `randint(a, b)` | Random integer between `a` and `b` (inclusive). |
| `randrange(start, stop[, step])` | Random integer from a range. |
| `random()` | Random float in `[0.0, 1.0)`. |
| `uniform(a, b)` | Random float between `a` and `b`. |
| `choice(seq)` | Random element from a sequence. |
| `shuffle(x)` | Shuffle a list in place. |
| `sample(population, k)` | `k` unique random elements from a population. |
| `choices(population, weights=None, k=1)` | Weighted random sampling with replacement. |
| `gauss(mu, sigma)` | Random float from a Gaussian distribution. |
| `normalvariate(mu, sigma)` | Alias for `gauss()`. |
| `expovariate(lambd)` | Random float from an exponential distribution. |
| `betavariate(alpha, beta)` | Random float from a beta distribution. |
| `gammavariate(alpha, beta)` | Random float from a gamma distribution. |
| `triangular(low, high[, mode])` | Random float from a triangular distribution. |
| `paretovariate(alpha)` | Random float from a Pareto distribution. |
| `weibullvariate(alpha, beta)` | Random float from a Weibull distribution. |

## Functions

### Core

#### `seed([a])`

Initializes the random number generator.

**Parameters:**
- `a` (`int` or `float`, optional): Seed value. Default: the current time (non-reproducible).

**Returns:** `None`

```python
import random

random.seed(42)  # Reproducible random sequence
num = random.random()
```

### Integers

#### `randint(a, b)`

Returns a random integer `N` such that `a <= N <= b`.

**Parameters:**
- `a` (`int`): Minimum value (inclusive).
- `b` (`int`): Maximum value (inclusive). Must be `>= a`.

**Returns:** `int`

**Raises:** `Error`: if `a > b`.

```python
import random

num = random.randint(1, 100)
print(num)  # Random number between 1 and 100
```

#### `randrange(start, stop[, step])`

Returns a randomly selected integer from `range(start, stop, step)`. Like `randint`, but excludes the endpoint.

**Parameters:**
- `start` (`int`): Start of range, or the exclusive stop if called with a single argument.
- `stop` (`int`, optional): End of range (exclusive).
- `step` (`int`, optional): Step between candidate values. Default: `1`. Cannot be `0`.

**Returns:** `int`

```python
import random

num = random.randrange(100)        # 0-99
num = random.randrange(10, 20)     # 10-19
num = random.randrange(0, 100, 5)  # 0, 5, 10, ..., 95
```

### Real-valued

#### `random()`

Returns a random float in the range `[0.0, 1.0)`.

**Returns:** `float`

```python
import random

num = random.random()
print(num)  # Random float like 0.123456
```

#### `uniform(a, b)`

Returns a random float `N` such that `a <= N <= b`.

**Parameters:**
- `a` (`int` or `float`): Minimum value.
- `b` (`int` or `float`): Maximum value.

**Returns:** `float`

```python
import random

num = random.uniform(1.5, 5.5)
print(num)  # Random float between 1.5 and 5.5
```

### Sequences

#### `choice(seq)`

Returns a random element from a sequence.

**Parameters:**
- `seq` (`list` or `str`): Sequence to choose from. Must not be empty.

**Returns:** `any`: an element from `seq` (a `str` of length 1 if `seq` is a string).

**Raises:** `Error`: if `seq` is empty.

```python
import random

fruits = ["apple", "banana", "cherry", "date"]
fruit = random.choice(fruits)
print(fruit)  # Random fruit from the list
```

#### `shuffle(x)`

Shuffles a list in place using the Fisher-Yates algorithm.

**Parameters:**
- `x` (`list`): List to shuffle. Modified in place.

**Returns:** `None`

```python
import random

cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(cards)
print(cards)  # [3, 7, 1, 9, 2, 5, 8, 4, 6, 10] (random order)
```

#### `sample(population, k)`

Returns `k` unique random elements chosen from `population`, without replacement.

**Parameters:**
- `population` (`list`): Sequence to sample from.
- `k` (`int`): Number of elements to return. Must satisfy `0 <= k <= len(population)`.

**Returns:** `list`: `k` unique elements.

**Raises:** `Error`: if `k` is negative or larger than the population.

```python
import random

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sample = random.sample(numbers, 3)
print(sample)  # [4, 7, 2] (3 random unique elements)
```

#### `choices(population, weights=None, k=1)`

Selects `k` items from `population` with replacement, optionally weighted.

**Parameters:**
- `population` (`list`): Sequence to sample from. Must not be empty.
- `weights` (`list`, optional): Weights matching `population`'s length, positional or keyword. Default: uniform weights. Must be non-negative and finite, with a positive total.
- `k` (`int`, optional): Number of items to select, positional or keyword. Default: `1`. Must be non-negative.

**Returns:** `list`: `k` selected items (may repeat).

```python
import random

colors = ["red", "green", "blue"]
result = random.choices(colors, weights=[5, 3, 2], k=10)
print(result)  # 10 selections, red more likely

result = random.choices(colors, k=5)  # uniform selection
```

### Distributions

#### `gauss(mu, sigma)`

Returns a random float from a Gaussian (normal) distribution.

**Parameters:**
- `mu` (`int` or `float`): Mean of the distribution.
- `sigma` (`int` or `float`): Standard deviation.

**Returns:** `float`

```python
import random

value = random.gauss(0, 1)  # mean=0, std=1
```

#### `normalvariate(mu, sigma)`

Alias for `gauss()`.

**Parameters:**
- `mu` (`int` or `float`): Mean of the distribution.
- `sigma` (`int` or `float`): Standard deviation.

**Returns:** `float`

```python
import random

value = random.normalvariate(0, 1)
```

#### `expovariate(lambd)`

Returns a random float from an exponential distribution.

**Parameters:**
- `lambd` (`int` or `float`): Rate parameter (`1.0` divided by the desired mean). Cannot be `0`.

**Returns:** `float`

**Raises:** `Error`: if `lambd` is `0`.

```python
import random

wait_time = random.expovariate(0.2)  # mean of 5 (lambd = 1/5)
```

#### `betavariate(alpha, beta)`

Returns a random float from a beta distribution.

**Parameters:**
- `alpha` (`int` or `float`): Shape parameter. Must be positive.
- `beta` (`int` or `float`): Shape parameter. Must be positive.

**Returns:** `float`: in range `[0, 1]`.

```python
import random

result = random.betavariate(0.5, 2.0)  # skewed toward 0
```

#### `gammavariate(alpha, beta)`

Returns a random float from a gamma distribution.

**Parameters:**
- `alpha` (`int` or `float`): Shape parameter. Must be positive.
- `beta` (`int` or `float`): Scale parameter. Must be positive.

**Returns:** `float`

```python
import random

result = random.gammavariate(2.0, 3.0)  # shape=2, scale=3
```

#### `triangular(low, high[, mode])`

Returns a random float from a triangular distribution.

**Parameters:**
- `low` (`int` or `float`): Minimum value.
- `high` (`int` or `float`): Maximum value.
- `mode` (`int` or `float`, optional): Peak value. Default: the midpoint of `low` and `high`.

**Returns:** `float`

```python
import random

result = random.triangular(0, 10, 7)  # peak at 7
result = random.triangular(0, 1)      # peak at midpoint (0.5)
```

#### `paretovariate(alpha)`

Returns a random float from a Pareto distribution.

**Parameters:**
- `alpha` (`int` or `float`): Shape parameter. Must be positive.

**Returns:** `float`

```python
import random

result = random.paretovariate(2.0)
```

#### `weibullvariate(alpha, beta)`

Returns a random float from a Weibull distribution.

**Parameters:**
- `alpha` (`int` or `float`): Scale parameter. Must be positive.
- `beta` (`int` or `float`): Shape parameter. Must be positive.

**Returns:** `float`

```python
import random

result = random.weibullvariate(1.0, 1.5)  # scale=1, shape=1.5
```

## Usage Example

```python
import random

random.seed(42)

dice_roll = random.randint(1, 6)
print("Dice roll:", dice_roll)

probability = random.random()
print("Probability:", probability)

temperature = random.uniform(20.0, 30.0)
print("Temperature:", temperature)

colors = ["red", "green", "blue", "yellow", "purple"]
color = random.choice(colors)
print("Random color:", color)

lottery = random.sample(list(range(1, 50)), 6)
print("Lottery numbers:", lottery)

deck = list(range(1, 53))
random.shuffle(deck)
print("Shuffled deck:", deck[:5], "...")
```

## See Also

- [math](../math/): mathematical functions and constants.
- [statistics](../statistics/): mean, median, variance, and other statistical functions.
- [uuid](../uuid/): UUID generation.
