---
description: Binary data type and constructor.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/data-formats/bytes/
sources:
    - resource: https://scriptling.dev/reference/libraries/data-formats/bytes/
status: stable
tags:
    - libraries
    - data-formats
title: bytes
type: API Reference
---
# bytes

`bytes` is Scriptling's binary data type — an immutable sequence of byte values (0–255). It is the canonical representation for raw binary data and is returned by [`hashlib.digest()`](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hashlib.md), [`hmac.digest()`](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hmac.md), [`base64.b64decode()`](https://scriptling.dev/okf/scriptling-libraries/math-numbers/base64.md), and [`msgpack.packb()`](https://scriptling.dev/okf/scriptling-libraries/data-formats/msgpack.md).

`bytes` is a global builtin (no `import` required). The constructor accepts a string, a list/tuple of ints, another `bytes` value, or nothing (empty).

## Constructor

### `bytes(source="", encoding="utf-8")`

**Parameters:**
- `source` (`str`, `bytes`, `list`, `tuple`, or `None`): Source data. A string is encoded as UTF-8; a list/tuple must contain ints in the range 0–255; a `bytes` value is copied; `None` or omitted yields empty bytes.
- `encoding` (`str`, optional): Encoding to use when `source` is a string. Only `"utf-8"` (the default) is supported.

**Returns:** `bytes`: an immutable binary value.

```python
b = bytes("hi")          # b'hi'
b = bytes([104, 105])    # b'hi'
b = bytes()              # b'' (empty)
b = bytes(b)             # a copy of b
```

## Static Constructors

| Function | Description |
|----------|-------------|
| `bytes.fromhex(hex_string)` | Build `bytes` from a hex string. |
| `bytes.frombase64(b64_string)` | Build `bytes` from a Base64 string. |

```python
b = bytes.fromhex("6869")       # b'hi'
b = bytes.frombase64("aGk=")    # b'hi'
```

## Methods on `bytes` values

| Method | Description |
|--------|-------------|
| `.decode(encoding="utf-8")` | Decode to a `str`. Only `"utf-8"` is supported. |
| `.hex()` | Encode as a lowercase hex `str`. |
| `.base64()` | Encode as a Base64 `str`. |
| `.length()` | Return the number of bytes (same as `len(b)`). |

```python
b = bytes([104, 105, 0x30, 0x39])

b.decode()   # "hi09"
b.hex()      # "68693039"
b.base64()   # "aGkwOQ=="
b.length()   # 4
len(b)       # 4
```

## Operators

`bytes` supports the operators you'd expect from an immutable sequence:

| Expression | Result |
|------------|--------|
| `b[i]` | The byte value at index `i` as an `int` (0–255). Negative indices count from the end. Out-of-range returns `None`. |
| `b[i:j]`, `b[i:j:k]` | A new `bytes` value sliced by index. Negative step reverses. |
| `b1 + b2` | Concatenation. Mixing with `str` raises a `TypeError`. |
| `b * n`, `n * b` | Repetition. `n <= 0` yields empty bytes. |
| `b1 == b2`, `!=`, `<`, `>`, `<=`, `>=` | Lexicographic comparison against another `bytes` value. |
| `i in b` | Membership of a byte value (`i` is an `int` 0–255). |
| `b1 in b` | Subsequence containment. |
| `len(b)`, `bool(b)` | Length / truthiness (empty `bytes` is falsy). |
| `for x in b` | Iteration yields `int` byte values. |

## Strict separation from `str`

`bytes` is **not** implicitly convertible to `str`. Mixing them in concatenation, comparison, or formatting raises a `TypeError`. Convert explicitly with `.decode()`:

```python
b = bytes("hi")

# OK
s = b.decode()              # "hi"
greeting = "value=" + b.decode()

# Raises TypeError
"x" + b
b + "y"
```

For debug/print contexts (REPL display, `print()`, f-string interpolation without a format spec, `%s` formatting, error messages) a `bytes` value renders as its Python-style repr — e.g. `b'hi'` or `b'\x00\xff'` — so it can always be displayed without raising, and the output is recognisable as binary rather than text.

## See Also

- [msgpack](https://scriptling.dev/okf/scriptling-libraries/data-formats/msgpack.md): binary serialisation built on `bytes`.
- [base64](https://scriptling.dev/okf/scriptling-libraries/math-numbers/base64.md): Base64 encode/decode.
- [hashlib](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hashlib.md): `.digest()` returns `bytes`.
- [hmac](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hmac.md): `.digest()` returns `bytes`.
