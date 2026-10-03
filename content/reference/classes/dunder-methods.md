---
title: Dunder Methods
description: The dunder (magic) methods Scriptling classes can define, covering string conversion, length, truthiness, comparison, arithmetic, context managers, membership, finalizers, and iteration.
tags: [reference, classes]
weight: 1
---

Part of [Classes](../).

Scriptling supports the most impactful dunder (magic) methods, making custom classes feel native.

## `__str__` and `__repr__`

Control string representation:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(str(p))   # Point(3, 4)
print(repr(p))  # Point(x=3, y=4)
print(f"{p}")   # Point(3, 4) : f-strings use __str__
```

## `__len__`

Enables `len(obj)`:

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

s = Stack()
s.push(1)
s.push(2)
print(len(s))  # 2
```

## `__bool__`

Controls truthiness in `if`, `while`, and `bool()`:

```python
class Flag:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value

f = Flag(False)
if not f:
    print("falsy")  # printed
```

If `__bool__` is not defined, `__len__` is used as a fallback (empty = falsy).

## `__eq__` and `__lt__`

Enable `==`, `<`, and `sorted()`:

```python
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        return self.minor < other.minor

versions = [Version(2, 0), Version(1, 0), Version(1, 5)]
sorted_v = sorted(versions)
# sorted_v is [1.0, 1.5, 2.0]
```

The full set of comparison dunder methods supported: `__eq__`, `__ne__`, `__lt__`, `__gt__`, `__le__`, `__ge__`.

## Arithmetic Dunder Methods

Arithmetic operators can be overloaded via dunder methods:

```python
class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)

v = Vec(1, 2) + Vec(3, 4)  # Vec(4, 6)
```

Supported: `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`.

## `__enter__` and `__exit__`

Enable the `with` statement (context manager protocol):

```python
class ManagedResource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("opening", self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closing", self.name)
        return False  # don't suppress exceptions

with ManagedResource("db") as r:
    print("using", r.name)
# opening db
# using db
# closing db
```

If `__exit__` returns a truthy value the exception is suppressed.

## `__contains__`

Enables the `in` operator:

```python
class NumberSet:
    def __init__(self, *nums):
        self.nums = list(nums)

    def __contains__(self, item):
        return item in self.nums

ns = NumberSet(1, 2, 3, 5, 8)
print(3 in ns)   # True
print(4 in ns)   # False
print(4 not in ns)  # True
```

## `__del__`

Called when an instance is garbage collected. Use it to release resources like file handles, connections, or locks:

```python
class FileHandle:
    def __init__(self, path):
        self.path = path

    def __del__(self):
        print("closing", self.path)

fh = FileHandle("/tmp/data")
# "closing /tmp/data" printed when fh is garbage collected
```

You can also call `__del__` explicitly: it runs each time it's called:

```python
fh = FileHandle("/tmp/data")
fh.__del__()  # "closing /tmp/data"
fh.__del__()  # "closing /tmp/data": runs again
```

GC finalizers are not prompt and may not run before process exit. Prefer explicit cleanup (calling `__del__` directly or using a `with` statement / context manager) for critical resources.

A destructor collected by the garbage collector runs on the runtime's finalizer goroutine with a hard five-second budget: past it, the destructor is abandoned mid-run. It also runs holding the environment's interpreter lock, serialized against every other goroutine evaluating in the same environment, so a slow `__del__` stalls them all. Keep it short, and do blocking work (IO, RPC, locks) through an explicit cleanup call instead. A destructor that raises or panics cannot crash the host: the error is contained.

`__del__` is inherited like other methods:

```python
class Base:
    def __del__(self):
        print("base cleanup")

class Child(Base):
    pass

c = Child()
# "base cleanup" printed when c is collected
```

## `__iter__` and `__next__`

Enable `for x in obj:` and list comprehensions:

```python
class CountUp:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        return CountUpIterator(self.start, self.stop)

class CountUpIterator:
    def __init__(self, current, stop):
        self.current = current
        self.stop = stop

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration()
        val = self.current
        self.current = self.current + 1
        return val

for n in CountUp(1, 5):
    print(n)  # 1 2 3 4

doubled = [x * 2 for x in CountUp(0, 4)]  # [0, 2, 4, 6]
```

An object can also be its own iterator by returning `self` from `__iter__`:

```python
class Range:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        self.i = 0  # reset on each iteration
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration()
        val = self.i
        self.i = self.i + 1
        return val
```

## Dunder Method Inheritance

Dunder methods are inherited and can be overridden:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Animal({self.name})"

class Dog(Animal):
    pass  # inherits __str__

class Cat(Animal):
    def __str__(self):
        return f"Cat({self.name})"  # overrides __str__

print(str(Dog("Rex")))      # Animal(Rex)
print(str(Cat("Whiskers"))) # Cat(Whiskers)
```

## See Also

- [Classes](../) - Class definition, inheritance, and `super()`
- [Class Decorators & Properties](../decorators/) - `@property`, `@staticmethod`, `@classmethod`
