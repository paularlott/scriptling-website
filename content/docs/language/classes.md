---
title: Classes
description: Class definition, inheritance, super(), and the __init__ method in Scriptling.
weight: 7
---

Scriptling supports object-oriented programming with classes, single inheritance, and the `super()` function.

## Class Definition

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return "Hello, my name is " + self.name

    def is_adult(self):
        return self.age >= 18
```

## Instantiation and Usage

```python
# Create an instance
p = Person("Alice", 30)

# Access fields
print(p.name)  # "Alice"
print(p.age)   # 30

# Call methods
print(p.greet())       # "Hello, my name is Alice"
print(p.is_adult())    # True

# Modify fields
p.age = 31
```

## The __init__ Method

The `__init__` method is the constructor, called when creating a new instance:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(10, 5)
print(rect.area())      # 50
print(rect.perimeter()) # 30
```

## The self Parameter

`self` refers to the current instance and must be the first parameter of instance methods:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get(self):
        return self.count

c = Counter()
c.increment()
c.increment()
print(c.get())  # 2
```

## Inheritance

Scriptling supports single inheritance. A class can inherit from another class:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Generic sound"

    def info(self):
        return "Animal: " + self.name

class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent constructor
        super(Dog, self).__init__(name)
        self.breed = breed

    def speak(self):
        return "Woof!"

class Cat(Animal):
    def __init__(self, name, color):
        super(Cat, self).__init__(name)
        self.color = color

    def speak(self):
        return "Meow!"

# Usage
dog = Dog("Buddy", "Pug")
print(dog.name)    # "Buddy" (inherited field)
print(dog.breed)   # "Pug"
print(dog.speak()) # "Woof!" (overridden method)
print(dog.info())  # "Animal: Buddy" (inherited method)

cat = Cat("Whiskers", "Orange")
print(cat.speak()) # "Meow!"
```

## The super() Function

Call parent class methods from a child class:

### Parameterless super()

```python
class Child(Parent):
    def __init__(self, value):
        super().__init__(value)  # Call parent __init__
```

### Explicit super()

```python
class Child(Parent):
    def __init__(self, value):
        super(Child, self).__init__(value)
```

### Calling Parent Methods

```python
class Animal:
    def speak(self):
        return "Generic sound"

class Dog(Animal):
    def speak(self):
        # Call parent method and extend
        return super(Dog, self).speak() + " and Woof!"

d = Dog("Buddy", "Pug")
print(d.speak())  # "Generic sound and Woof!"
```

## Multiple Levels of Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Mammal(Animal):
    def __init__(self, name, warm_blooded=True):
        super(Mammal, self).__init__(name)
        self.warm_blooded = warm_blooded

class Dog(Mammal):
    def __init__(self, name, breed):
        super(Dog, self).__init__(name)
        self.breed = breed

    def speak(self):
        return "Woof!"

dog = Dog("Buddy", "Golden Retriever")
print(dog.name)           # "Buddy"
print(dog.warm_blooded)   # True
print(dog.breed)          # "Golden Retriever"
```

## Class and Instance Fields

```python
class Account:
    # Class-level field (shared by all instances)
    bank_name = "First National"

    def __init__(self, owner, balance):
        # Instance fields (unique to each instance)
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

a1 = Account("Alice", 100)
a2 = Account("Bob", 200)

print(a1.bank_name)  # "First National"
print(a2.bank_name)  # "First National"

print(a1.balance)    # 100
print(a2.balance)    # 200
```

## Limitations

### No Nested Classes

Classes must be defined at the top level of a module:

```python
# NOT supported
def outer():
    class Inner:  # Error: nested class
        pass

# NOT supported
class Outer:
    class Inner:  # Error: nested class
        pass
```

### No Multiple Inheritance

Only single inheritance is supported:

```python
# NOT supported
class C(A, B):  # Error: multiple inheritance
    pass
```

### No Property Decorators

`@property`, `@staticmethod`, `@classmethod` are not supported:

```python
# NOT supported
class MyClass:
    @property  # Error
    def value(self):
        return self._value
```

### No Operator Overloading

Magic methods like `__add__`, `__eq__` are not supported (except `__init__`):

```python
# NOT supported
class Point:
    def __add__(self, other):  # Error
        return Point(self.x + other.x, self.y + other.y)
```

## Example: Complete Class

```python
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise "Deposit amount must be positive"
        self.balance += amount
        self.transactions.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise "Withdrawal amount must be positive"
        if amount > self.balance:
            raise "Insufficient funds"
        self.balance -= amount
        self.transactions.append(("withdrawal", amount))

    def get_balance(self):
        return self.balance

    def get_statement(self):
        return {
            "owner": self.owner,
            "balance": self.balance,
            "transactions": self.transactions
        }

# Usage
account = BankAccount("Alice", 100)
account.deposit(50)
account.withdraw(30)
print(account.get_balance())  # 120
print(account.get_statement())
```

## See Also

- [Functions](./functions/) - Function definitions
- [Error Handling](./error-handling/) - Using raise in classes
- [Python Differences](./python-differences/) - Class limitations
