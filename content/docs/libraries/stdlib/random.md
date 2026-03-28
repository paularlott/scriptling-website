---
title: random
weight: 1
---

Random number generation functions. Python-compatible.

## Available Functions

| Function                       | Description                                    |
| ------------------------------ | ---------------------------------------------- |
| `seed([a])`                    | Initialize the random number generator         |
| `randint(a, b)`                | Random integer between a and b (inclusive)     |
| `randrange(start, stop[, step])` | Random element from range                    |
| `random()`                     | Random float between 0.0 and 1.0               |
| `uniform(a, b)`                | Random float between a and b                   |
| `gauss(mu, sigma)`             | Gaussian distribution random float             |
| `normalvariate(mu, sigma)`     | Gaussian distribution (alias for gauss)        |
| `expovariate(lambd)`           | Exponential distribution random float          |
| `choice(seq)`                  | Random element from a sequence                 |
| `shuffle(list)`                | Shuffle a list in place                        |
| `sample(population, k)`        | k unique random elements from population       |

## Functions

### random.seed([a])

Initializes the random number generator.

**Parameters:**

- `a` (optional): Seed value (integer or float). If omitted, current time is used.

**Returns:** None

**Example:**

```python
import random

random.seed(42)  # Reproducible random sequence
num = random.random()
```

### random.randint(a, b)

Returns a random integer between a and b (inclusive).

**Parameters:**

- `a`: Minimum value (integer)
- `b`: Maximum value (integer)

**Returns:** Integer

**Example:**

```python
import random

num = random.randint(1, 100)
print(num)  # Random number between 1 and 100
```

### random.random()

Returns a random float between 0.0 and 1.0.

**Returns:** Float

**Example:**

```python
import random

num = random.random()
print(num)  # Random float like 0.123456
```

### random.uniform(a, b)

Returns a random float N such that a <= N <= b.

**Parameters:**

- `a`: Minimum value (number)
- `b`: Maximum value (number)

**Returns:** Float

**Example:**

```python
import random

num = random.uniform(1.5, 5.5)
print(num)  # Random float between 1.5 and 5.5
```

### random.choice(seq)

Returns a random element from a sequence.

**Parameters:**

- `seq`: List to choose from

**Returns:** Element from the list

**Example:**

```python
import random

fruits = ["apple", "banana", "cherry", "date"]
fruit = random.choice(fruits)
print(fruit)  # Random fruit from the list
```

### random.shuffle(x)

Shuffles a list in place.

**Parameters:**

- `x`: List to shuffle (modified in place)

**Returns:** None

**Example:**

```python
import random

cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(cards)
print(cards)  # [3, 7, 1, 9, 2, 5, 8, 4, 6, 10] (random order)
```

### random.sample(population, k)

Returns k unique random elements from population.

**Parameters:**

- `population`: List to sample from
- `k`: Number of elements to return

**Returns:** List of k unique elements

**Example:**

```python
import random

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sample = random.sample(numbers, 3)
print(sample)  # [4, 7, 2] (3 random unique elements)
```

### random.randrange(start, stop[, step])

Returns a randomly selected element from a range.

**Parameters:**

- `start`: Start of range (or stop if only one argument)
- `stop`: End of range (exclusive)
- `step` (optional): Step value. Default: 1

**Returns:** Integer

**Example:**

```python
import random

# Single argument (0 to stop)
num = random.randrange(100)  # 0-99

# With start and stop
num = random.randrange(10, 20)  # 10-19

# With step
num = random.randrange(0, 100, 5)  # 0, 5, 10, ..., 95
```

### random.gauss(mu, sigma)

Returns a random float from a Gaussian (normal) distribution.

**Parameters:**

- `mu`: Mean of the distribution
- `sigma`: Standard deviation

**Returns:** Float

**Example:**

```python
import random

# Generate values from normal distribution (mean=0, std=1)
value = random.gauss(0, 1)
```

### random.normalvariate(mu, sigma)

Alias for `gauss()`. Returns a random float from a Gaussian distribution.

**Parameters:**

- `mu`: Mean of the distribution
- `sigma`: Standard deviation

**Returns:** Float

### random.expovariate(lambd)

Returns a random float from an exponential distribution.

**Parameters:**

- `lambd`: Rate parameter (1.0 divided by the desired mean)

**Returns:** Float

**Example:**

```python
import random

# Exponential with mean 5 (lambd = 1/5)
wait_time = random.expovariate(0.2)
```

## Usage Example

```python
import random

# Set seed for reproducibility
random.seed(42)

# Random integer
dice_roll = random.randint(1, 6)
print("Dice roll:", dice_roll)

# Random float
probability = random.random()
print("Probability:", probability)

# Random float in range
temperature = random.uniform(20.0, 30.0)
print("Temperature:", temperature)

# Random choice
colors = ["red", "green", "blue", "yellow", "purple"]
color = random.choice(colors)
print("Random color:", color)

# Random sample
lottery = random.sample(list(range(1, 50)), 6)
print("Lottery numbers:", lottery)

# Shuffle a deck
deck = list(range(1, 53))  # Cards 1-52
random.shuffle(deck)
print("Shuffled deck:", deck[:5], "...")  # First 5 cards
```
