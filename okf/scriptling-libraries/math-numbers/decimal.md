---
description: Exact decimal arithmetic for money, with explicit rounding.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/decimal/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/decimal/
status: stable
tags:
    - libraries
    - math
    - money
title: decimal
type: API Reference
---
# decimal

The `decimal` library provides `Decimal`, a number that holds decimal fractions exactly. Use it for money and
anything else where `0.1 + 0.2` must be `0.3`. It follows Python's `decimal` module for ordinary arithmetic.

## Example

```python
from decimal import Decimal, ROUND_HALF_UP

lines = [("Widget", "19.99", 3), ("Gadget", "5.01", 1)]
subtotal = sum(Decimal(price) * qty for _, price, qty in lines)
tax = (subtotal * Decimal("0.075")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

print(subtotal)                  # 64.98
print(tax)                       # 4.87
print(f"{subtotal + tax:,.2f}")  # 69.85
```

Build a `Decimal` from text or an `int`. A `float` is taken at its exact binary value, so `Decimal(0.1)` is not
`Decimal("0.1")`: write `Decimal(str(x))` to take a float as it prints.

## Available Members

| Member | Description |
|--------|-------------|
| `Decimal(value="0")` | A decimal number from a `str`, `int`, `float` or `Decimal`. |
| `+ - * / // % **`, unary `-`, `abs()` | Arithmetic between decimals, and between a decimal and an `int`. Mixing with a `float` raises `TypeError`. |
| Comparisons, `hash()`, `sorted()`, `min()`, `max()`, `sum()` | Decimals compare and hash consistently with integers, so `Decimal("1.0") == 1`. |
| `.quantize(exp, rounding=None)` | Round to the exponent of `exp`: `d.quantize(Decimal("0.01"))` rounds to cents. |
| `.normalize()`, `.to_integral_value(rounding=None)` | Strip trailing zeros; round to a whole number. |
| `.is_zero()`, `.is_signed()`, `.copy_abs()`, `.copy_negate()` | Inspection and sign helpers. |
| `int(d)`, `float(d)`, `round(d)`, `round(d, n)`, `str(d)`, `f"{d:.2f}"` | Conversions and formatting. `round(d, n)` returns a `Decimal`. |
| `ROUND_HALF_UP`, `ROUND_HALF_EVEN`, `ROUND_HALF_DOWN`, `ROUND_UP`, `ROUND_DOWN`, `ROUND_CEILING`, `ROUND_FLOOR`, `ROUND_05UP` | Rounding modes for `quantize` and the context. |
| `getcontext()` | The arithmetic context: `.prec` (significant digits, default 28) and `.rounding` (default `ROUND_HALF_EVEN`). |
| `InvalidOperation`, `DivisionByZero`, `Overflow` | Exceptions. `DivisionByZero` is also a `ZeroDivisionError`. |

Trailing zeros are kept, as in Python: `Decimal("1.10") + Decimal("2.20")` is `Decimal('3.30')`.

## Differences from Python

- There is no `NaN` or `Infinity`: an operation that would produce one raises `InvalidOperation`, `DivisionByZero` or `Overflow`.
- `getcontext().prec` may be at most 10,000, and a number written with more than 100,000 digits raises `MemoryError`.
- `int(d)` raises `OverflowError` for a value outside the 64-bit integer range.
- `json.dumps()` raises `TypeError` for a `Decimal`, as in Python: pass `default=str`, or convert with `str()` or `float()`.
- `localcontext()`, `as_tuple()`, `sqrt()`, `ln()`, `exp()` and the other mathematical functions are not available.
