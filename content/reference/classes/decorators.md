---
title: Class Decorators & Properties
description: Using @property, @staticmethod, @classmethod, and custom function and class decorators with Scriptling classes.
tags: [reference, classes]
weight: 2
---

Part of [Classes](../).

`@property`, `@staticmethod`, and `@classmethod` are supported.

## `@property`

`@property` turns a method into an attribute. The getter receives `self` and is called when the attribute is read. Scriptling users access the value without call parentheses:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return 3.14159 * self._radius * self._radius

c = Circle(5)
print(c.radius)  # 5
print(c.area)    # 78.53975
```

A property without a setter is read-only. Assigning to it raises `AttributeError`:

```python
# c.area = 10  # AttributeError: property is read-only
```

Add a setter with `@<name>.setter`. The setter method must use the same property name and receives `self` plus the assigned value:

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
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):          # read-only: no setter
        return self._celsius * 9 / 5 + 32

t = Temperature(100)
print(t.celsius)    # 100
t.celsius = 0       # calls setter
print(t.fahrenheit) # 32.0
# t.fahrenheit = 50  # AttributeError: property is read-only
```

Use properties when you want attribute syntax with validation, computed values, or private backing fields. A common pattern is to store the real value in an underscore-prefixed field and expose it through a property:

```python
class Account:
    def __init__(self, balance):
        self._balance = 0
        self.balance = balance  # reuse setter validation

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value
```

Properties (with or without setters) are inherited:

```python
class Shape:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

class Square(Shape):
    def __init__(self, side):
        super().__init__("square")
        self._side = side

    @property
    def perimeter(self):
        return self._side * 4

sq = Square(3)
print(sq.name)      # "square" : inherited property
print(sq.perimeter) # 12
```


## `@staticmethod`

A method that receives no `self`. Callable on both the class and instances:

```python
class MathHelper:
    @staticmethod
    def square(x):
        return x * x

print(MathHelper.square(4))  # 16 : called on class
m = MathHelper()
print(m.square(5))           # 25 : called on instance
```

## `@classmethod`

A method that receives the class (`cls`) as its first argument instead of the instance. Useful for factory methods and accessing class-level state:

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, s):
        parts = s.split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

d = Date.from_string("2024-03-15")
print(d.year)   # 2024
print(d.month)  # 3
```

With inheritance, `cls` refers to the actual subclass:

```python
class Animal:
    @classmethod
    def create(cls):
        return cls()  # creates an instance of the subclass

class Dog(Animal):
    def kind(self):
        return "dog"

d = Dog.create()   # creates a Dog, not an Animal
print(d.kind())    # "dog"
```

Class methods can be called on both the class and instances:

```python
Date.from_string("2024-01-01")  # called on class
d = Date(2024, 1, 1)
d.from_string("2024-06-15")     # called on instance: cls is still Date
```

## Custom function decorators

Any callable can be used as a decorator:

```python
def log_calls(fn):
    def wrapper(*args):
        print("calling", fn.__name__)
        return fn(*args)
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(1, 2)  # prints "calling add", returns 3
```

Decorators stack: applied bottom-up (innermost first):

```python
@outer
@inner
def fn(): ...
# equivalent to: fn = outer(inner(fn))
```

## Class decorators

Decorators can also be applied to classes:

```python
def add_greeting(cls):
    cls.greeting = "hi"
    return cls

@add_greeting
class Greeter:
    pass

g = Greeter()
print(g.greeting)  # "hi"
```

## See Also

- [Classes](../) - Class definition, inheritance, and `super()`
- [Decorators](../../decorators/) - Writing and applying decorators in general
- [Dunder Methods](../dunder-methods/) - Customizing class behaviour with magic methods
