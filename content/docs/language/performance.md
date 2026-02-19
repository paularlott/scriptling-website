---
title: Performance Guide
description: Tips and best practices for writing efficient Scriptling code.
weight: 12
---

Tips and best practices for writing efficient Scriptling code.

## String Concatenation

### The Problem

String concatenation with `+=` in loops is slow because each operation creates a new string object:

```python
# SLOW - Creates 1000 string objects
result = ""
for i in range(1000):
    result += str(i)  # Each += creates a new string
```

**Performance**: 3.45 ms, 25.9 MB for 10,000 iterations

### Solution: Use join()

```python
# FAST - Efficient and Python-compatible
parts = []
for i in range(1000):
    parts.append(str(i))
result = "".join(parts)
```

**Performance**: ~36 μs for 1000 iterations (70x faster!)

**Why it's fast**: `join()` pre-allocates the exact amount of memory needed and copies all strings once.

### When += is OK

```python
# OK - Fine for small numbers
result = "hello" + " " + "world"
# or
result = "hello"
result += " "
result += "world"
```

**When to use**:
- Concatenating < 10 strings
- Outside of loops
- Readability matters more

## Examples

### Building CSV

```python
# SLOW
csv = ""
for row in data:
    csv += ",".join(row) + "\n"

# FAST - Using join()
lines = []
for row in data:
    lines.append(",".join(row))
csv = "\n".join(lines)
```

### Building HTML

```python
# SLOW
html = "<ul>"
for item in items:
    html += "<li>" + item + "</li>"
html += "</ul>"

# FAST - Using join()
parts = ["<ul>"]
for item in items:
    parts.append("<li>" + item + "</li>")
parts.append("</ul>")
html = "".join(parts)
```

### Building JSON-like Strings

```python
# SLOW
json_str = "["
for i, item in enumerate(items):
    if i > 0:
        json_str += ", "
    json_str += "\"" + item + "\""
json_str += "]"

# FAST - Using join()
parts = ["\"" + item + "\"" for item in items]
json_str = "[" + ", ".join(parts) + "]"

# EVEN BETTER - Use json library
import json
json_str = json.dumps(items)
```

## Recursion vs Iteration

### The Problem

Deep recursion creates many function call frames and environment copies:

```python
# SLOW - Deep recursion
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

result = fib(10)  # 114 μs, 376 KB, 3,983 allocations
```

### Solution: Use Iteration

```python
# FAST - Iterative approach
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

result = fib(10)  # Much faster, constant memory
```

### When Recursion is OK

Recursion is fine for:
- Tree/graph traversal (limited depth)
- Divide-and-conquer algorithms
- Naturally recursive problems with small depth

Avoid recursion for:
- Problems with deep recursion (> 100 levels)
- Problems that can be solved iteratively
- Performance-critical code

## List Operations

### Pre-allocate When Size is Known

```python
# SLOW - Multiple reallocations
items = []
for i in range(1000):
    items.append(i)

# OK - List comprehension (often faster)
items = [i for i in range(1000)]
```

### Avoid Repeated lookups

```python
# SLOW - Looks up data["items"] each time
for i in range(len(data["items"])):
    process(data["items"][i])

# FAST - Cache the reference
items = data["items"]
for i in range(len(items)):
    process(items[i])

# EVEN BETTER - Iterate directly
for item in data["items"]:
    process(item)
```

## Dictionary Operations

### Use get() for Optional Keys

```python
# SLOW - Exception handling overhead
try:
    value = data["key"]
except KeyError:
    value = default

# FAST - No exception overhead
value = data.get("key", default)
```

### Check Membership Efficiently

```python
# FAST - O(1) lookup
if key in data:
    value = data[key]

# Also FAST - Single lookup with default
value = data.get(key)
if value is not None:
    # Use value
```

## General Tips

1. **Profile before optimizing**: Use benchmarks to find real bottlenecks
2. **Readability first**: Optimize only when needed
3. **Use built-in functions**: They're already optimized
4. **Avoid premature optimization**: Write clear code first
5. **Prefer iteration over recursion**: For deep operations
6. **Use join() for string building**: In loops

## Benchmarking Your Code

```python
import time

# Measure execution time
start = time.time()

# Your code here
result = []
for i in range(10000):
    result.append(i)

end = time.time()
print("Took " + str((end - start) * 1000) + " ms")
```

### Benchmark Function

```python
def benchmark(name, func, iterations=1000):
    import time
    start = time.time()
    for _ in range(iterations):
        func()
    end = time.time()
    ms = (end - start) * 1000
    print(name + ": " + str(ms) + " ms (" + str(ms/iterations) + " ms/iter)")

# Usage
benchmark("string += ", func=lambda: slow_concat(), iterations=100)
benchmark("join()    ", func=lambda: fast_concat(), iterations=100)
```

## Summary

| Pattern | Avoid | Prefer |
|---------|-------|--------|
| String building in loops | `result += str(i)` | `"".join(parts)` |
| Deep recursion | `fib(n-1) + fib(n-2)` | Iterative loop |
| Optional dict access | `try/except KeyError` | `dict.get(key, default)` |
| List building | Multiple `append()` in simple cases | List comprehension |
| Repeated lookups | `data["key"]` in loop | Cache reference |

## See Also

- [Built-in Functions](./builtins/) - String and list functions
- [HTTP & JSON](./http/) - Using the json library
