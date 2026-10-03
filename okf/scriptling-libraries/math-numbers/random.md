---
description: Random number generation, compatible with Python's random module.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/random/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/random/
status: stable
tags:
    - libraries
    - math
title: random
type: API Reference
---
# random

The `random` library generates random integers, floats, and samples, including several statistical distributions, with an API that follows Python's `random` module.

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
| `sample(population, k)` | `k` unique random elements from a list or set (without replacement). |
| `choices(population, weights=None, k=1)` | `k` elements with replacement, optionally weighted (`weights` and `k` may be positional or keyword). |
| `gauss(mu, sigma)` | Random float from a Gaussian distribution. |
| `normalvariate(mu, sigma)` | Alias for `gauss()`. |
| `expovariate(lambd)` | Random float from an exponential distribution (`lambd` is 1 / mean). |
| `betavariate(alpha, beta)` | Random float from a beta distribution. |
| `gammavariate(alpha, beta)` | Random float from a gamma distribution. |
| `triangular(low, high[, mode])` | Random float from a triangular distribution. |
| `paretovariate(alpha)` | Random float from a Pareto distribution. |
| `weibullvariate(alpha, beta)` | Random float from a Weibull distribution. |

## Example

```python
import random

random.seed(42)                       # reproducible sequence (values differ from CPython's)

roll = random.randint(1, 6)           # 1..6 inclusive
step = random.randrange(0, 100, 5)    # 0, 5, ..., 95
p = random.random()                   # 0.0 <= p < 1.0
t = random.uniform(20.0, 30.0)        # float between the bounds
print(1 <= roll <= 6, step % 5 == 0, 0 <= p < 1, 20 <= t <= 30)  # True True True True

colors = ["red", "green", "blue"]
print(random.choice(colors) in colors)                 # True
print(len(random.choices(colors, weights=[5, 3, 2], k=10)))  # 10 (with replacement)
lottery = random.sample(list(range(1, 50)), 6)         # 6 unique values
print(len(set(lottery)))                               # 6

deck = list(range(1, 53))
random.shuffle(deck)                                   # in place, returns None
print(sorted(deck) == list(range(1, 53)))              # True

noise = random.gauss(0, 1)            # also normalvariate, expovariate(1/mean),
wait = random.expovariate(0.2)        # betavariate, gammavariate, triangular,
peak = random.triangular(0, 10, 7)    # paretovariate, weibullvariate
```

## Differences from Python

- Seeded sequences are reproducible within Scriptling but do not match CPython's values for the same seed.
- `shuffle()` accepts only a `list`.
- There is no `random.Random` class, and `getrandbits`, `randbytes`, `getstate`/`setstate`, `lognormvariate`, `vonmisesvariate` and `binomialvariate` are not available. For security-sensitive values use [secrets](https://scriptling.dev/okf/scriptling-libraries/math-numbers/secrets.md).

## See Also

- [math](https://scriptling.dev/okf/scriptling-libraries/math-numbers/math.md): mathematical functions and constants.
- [statistics](https://scriptling.dev/okf/scriptling-libraries/math-numbers/statistics.md): mean, median, variance, and other statistical functions.
- [uuid](https://scriptling.dev/okf/scriptling-libraries/math-numbers/uuid.md): UUID generation.
