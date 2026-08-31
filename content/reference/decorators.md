---
title: Decorators
description: Using decorators to wrap functions and classes, decorator factories with arguments, stacking, and built-in decorators in Scriptling.
tags: [reference, decorators, functions, classes]
weight: 7
---

Decorators modify or extend functions and classes by wrapping them with another callable. Scriptling supports the `@` syntax familiar from Python.

## Basic Function Decorator

A decorator is a function that takes a function and returns a (usually modified) function:

```python
def double_result(fn):
    def wrapper(*args):
        return fn(*args) * 2
    return wrapper

@double_result
def add(a, b):
    return a + b

print(add(3, 4))  # 14
```

The `@` syntax is equivalent to:

```python
def add(a, b):
    return a + b
add = double_result(add)
```

## Decorators with Arguments

When a decorator needs configuration, use a factory function that returns the actual decorator:

```python
def repeat(times):
    def decorator(fn):
        def wrapper(*args):
            results = []
            for i in range(times):
                results.append(fn(*args))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return "Hello, " + name

print(greet("World"))  # ["Hello, World", "Hello, World", "Hello, World"]
```

The pattern is: `@factory(args)` calls the factory, which returns a decorator, which wraps the function. Three levels of nesting.

## Stacking Decorators

Multiple decorators apply bottom-up (innermost first):

```python
def add_one(fn):
    def wrapper(*args):
        return fn(*args) + 1
    return wrapper

def double(fn):
    def wrapper(*args):
        return fn(*args) * 2
    return wrapper

@add_one
@double
def value():
    return 5

print(value())  # 11
# Evaluated as: add_one(double(value))()
# value() = 5 → double wraps: 10 → add_one wraps: 11
```

## Identity Decorators

A decorator can return the function unchanged — useful for registration patterns:

```python
_registry = {}

def register(fn):
    _registry[fn.__name__] = fn
    return fn

@register
def my_handler():
    return "handled"

# my_handler is still callable normally
print(my_handler())       # "handled"
print(_registry.keys())   # ["my_handler"]
```

## The Registration Pattern (Decorator with Arguments)

Combining factory decorators with a registry is the idiomatic way to declare metadata alongside a function:

```python
_tools = {}

def tool(description, params=None):
    def decorator(fn):
        _tools[fn.__name__] = {
            "description": description,
            "params": params,
            "fn": fn,
        }
        return fn
    return decorator

@tool("Calculate expression", params={"expr": "Math expression"})
def calc(expr):
    return eval(expr)

# calc is callable normally AND registered with metadata
print(calc("2+3"))             # 5
print(_tools["calc"]["description"])  # "Calculate expression"
```

This pattern is used by `scriptling.runtime.mcp` for [MCP tool registration](/reference/libraries/runtime/mcp/).

## Accessing `fn.__name__`

Every named function exposes its name via `__name__`:

```python
def my_function():
    pass

print(my_function.__name__)  # "my_function"
```

This is how decorators identify which function they're wrapping without requiring the name to be passed explicitly.

## Class Decorators

Decorators can also wrap classes:

```python
def add_version(cls):
    cls.version = "1.0"
    return cls

@add_version
class App:
    pass

a = App()
print(a.version)  # "1.0"
```

## Built-in Decorators

### `@property`

Turns a method into a read-only attribute:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)  # 5  (no parentheses needed)
print(c.area)    # 78.53975
```

### `@property.setter`

Add a setter to a property:

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

t = Temperature(100)
t.celsius = 0       # uses the setter
print(t.celsius)    # 0
```

### `@staticmethod`

Declares a method that doesn't receive `self`:

```python
class MathUtils:
    @staticmethod
    def square(x):
        return x * x

print(MathUtils.square(4))  # 16
print(MathUtils().square(4))  # 16 (also works on instances)
```

### `@classmethod`

Declares a method that receives the class as its first argument:

```python
class Counter:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1
        return cls.count

print(Counter.increment())  # 1
print(Counter.increment())  # 2
```

## Limitations

- **Function objects don't support attribute assignment.** `fn.tag = "value"` will error. Use a registry dict instead (see the registration pattern above).
- **Lambdas can't be decorated with `@` syntax** — they have no name or statement form to attach the decorator to. Wrap manually: `my_lambda = decorator(lambda x: x)`.
- **No type annotations on parameters.** Scriptling doesn't support `def f(x: int)` syntax. Metadata must be passed explicitly (e.g. via decorator arguments).

## See Also

- [Functions](../functions/) — Function definition, parameters, closures
- [Classes](../classes/#decorators) — `@property`, `@staticmethod`, `@classmethod`
- [runtime.mcp](/reference/libraries/runtime/mcp/) — MCP tool registration via decorators
