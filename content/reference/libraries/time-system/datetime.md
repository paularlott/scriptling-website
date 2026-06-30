---
title: datetime
description: Date and time objects with construction, formatting, arithmetic, and comparison, using a Python-compatible API.
weight: 1

aliases:
  - /reference/libraries/stdlib/datetime/
  - /reference/libraries/datetime/
---

The `datetime` library provides `datetime` and `date` objects for representing points in time, plus a `timedelta()` helper for durations, with a Python-compatible API.

```python
import datetime
```

## Available Functions

| Function | Description |
|----------|-------------|
| `datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)` | Creates a datetime instance. |
| `datetime.now()` | Returns the current local datetime. |
| `datetime.utcnow()` | Returns the current UTC datetime. |
| `datetime.strptime(date_string, format)` | Parses a date string into a datetime instance. |
| `datetime.fromtimestamp(timestamp)` | Creates a datetime instance from a Unix timestamp. |
| `datetime.strftime(format, timestamp_or_datetime)` | Formats a timestamp or datetime instance as a string. |
| `date(year, month, day)` | Creates a date instance. |
| `date.today()` | Returns the current local date. |
| `timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)` | Creates a duration, returned as total seconds. |

## Construction

### `datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)`

Creates a datetime instance for the specified date and time, interpreted in local time. `hour`, `minute`, `second`, and `microsecond` may be passed positionally or as keyword arguments.

**Parameters:**
- `year` (`int`): Year.
- `month` (`int`): Month (1-12).
- `day` (`int`): Day (1-31).
- `hour` (`int`, optional): Hour (0-23). Default: `0`.
- `minute` (`int`, optional): Minute (0-59). Default: `0`.
- `second` (`int`, optional): Second (0-59). Default: `0`.
- `microsecond` (`int`, optional): Microsecond. Default: `0`.

**Returns:** `datetime`: the new datetime instance.

**Raises:** `Error`: if an unexpected keyword argument is supplied.

```python
import datetime

dt = datetime.datetime(2024, 1, 15)  # "2024-01-15 00:00:00"
dt = datetime.datetime(2024, 1, 15, 10, 30, 45)  # "2024-01-15 10:30:45"
```

### `datetime.now()`

Returns the current local date and time.

**Returns:** `datetime`: the current local datetime.

```python
import datetime

now = datetime.datetime.now()
print(now)  # "2025-11-26 11:15:54"
print(now.year())  # 2025
print(now.month())  # 11
```

### `datetime.utcnow()`

Returns the current date and time in UTC.

**Returns:** `datetime`: the current UTC datetime.

```python
import datetime

utc_now = datetime.datetime.utcnow()
print(utc_now)  # "2025-11-26 03:15:54"
```

### `datetime.strptime(date_string, format)`

Parses a date string according to the given format and returns a datetime instance.

**Parameters:**
- `date_string` (`str`): String to parse.
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.

**Returns:** `datetime`: the parsed datetime instance.

**Raises:** `Error`: when `date_string` does not match `format`.

```python
import datetime

dt = datetime.datetime.strptime("2024-01-15 10:30:45", "%Y-%m-%d %H:%M:%S")
print(dt)  # "2024-01-15 10:30:45"
```

### `datetime.fromtimestamp(timestamp)`

Creates a datetime instance from a Unix timestamp, interpreted in local time.

**Parameters:**
- `timestamp` (`int` or `float`): Unix timestamp.

**Returns:** `datetime`: the corresponding datetime instance.

```python
import datetime

dt = datetime.datetime.fromtimestamp(1705314645)
print(dt)  # "2024-01-15 10:30:45"
```

### `datetime.strftime(format, timestamp_or_datetime)`

Formats a Unix timestamp or datetime instance as a string. This is a module-level convenience function distinct from the `.strftime()` instance method below.

**Parameters:**
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.
- `timestamp_or_datetime` (`int`, `float`, or `datetime`): Unix timestamp or datetime instance to format.

**Returns:** `str`: the formatted date/time string.

```python
import datetime

formatted = datetime.datetime.strftime("%Y-%m-%d %H:%M:%S", 1705314645)
print(formatted)  # "2024-01-15 10:30:45"
```

### `date(year, month, day)`

Creates a date instance for the specified year, month, and day. Date instances have no time component.

**Parameters:**
- `year` (`int`): Year.
- `month` (`int`): Month (1-12).
- `day` (`int`): Day (1-31).

**Returns:** `date`: the new date instance.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d)  # "2024-01-15"
```

### `date.today()`

Returns the current local date.

**Returns:** `date`: today's date.

```python
import datetime

today = datetime.date.today()
print(today)  # "2025-11-26"
```

### `timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)`

Creates a duration from the given components. Unlike Python's `timedelta`, which returns a distinct object, this returns the total duration as a single float of seconds: ready to use directly in datetime/date arithmetic. All parameters are keyword-only.

**Parameters:**
- `days` (`int` or `float`, optional): Number of days. Default: `0`.
- `seconds` (`int` or `float`, optional): Number of seconds. Default: `0`.
- `microseconds` (`int` or `float`, optional): Number of microseconds. Default: `0`.
- `milliseconds` (`int` or `float`, optional): Number of milliseconds. Default: `0`.
- `minutes` (`int` or `float`, optional): Number of minutes. Default: `0`.
- `hours` (`int` or `float`, optional): Number of hours. Default: `0`.
- `weeks` (`int` or `float`, optional): Number of weeks. Default: `0`.

**Returns:** `float`: the total duration, in seconds.

**Raises:** `Error`: if a positional argument or an unexpected keyword argument is supplied.

```python
import datetime

# One day in seconds
one_day = datetime.timedelta(days=1)
print(one_day)  # 86400.0

# Two hours
two_hours = datetime.timedelta(hours=2)
print(two_hours)  # 7200.0

# Combined duration
duration = datetime.timedelta(days=1, hours=2, minutes=30)
print(duration)  # 95400.0

# Use with datetime arithmetic
now = datetime.datetime.now()
tomorrow = now + datetime.timedelta(days=1)
next_week = now + datetime.timedelta(weeks=1)

# Use with date arithmetic
today = datetime.date.today()
next_month = today + datetime.timedelta(weeks=4)
```

## datetime Methods

These methods are available on any `datetime` instance.

### `.strftime(format)`

Formats the datetime as a string.

**Parameters:**
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.

**Returns:** `str`: the formatted date/time string.

```python
import datetime

dt = datetime.datetime.now()
formatted = dt.strftime("%A, %B %d, %Y at %I:%M %p")
print(formatted)  # "Wednesday, November 26, 2025 at 11:15 AM"
```

### `.timestamp()`

Returns the datetime as a Unix timestamp.

**Returns:** `float`: seconds since the Unix epoch.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
ts = dt.timestamp()
print(ts)  # 1705314645.0
```

### `.isoformat()`

Returns the datetime formatted as an ISO 8601 string.

**Returns:** `str`: formatted as `"YYYY-MM-DDTHH:MM:SS"`.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.isoformat())  # "2024-01-15T10:30:45"
```

### `.year()`

Returns the year.

**Returns:** `int`: the year.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.year())  # 2024
```

### `.month()`

Returns the month.

**Returns:** `int`: the month (1-12).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.month())  # 1
```

### `.day()`

Returns the day of the month.

**Returns:** `int`: the day of month (1-31).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.day())  # 15
```

### `.hour()`

Returns the hour.

**Returns:** `int`: the hour (0-23).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.hour())  # 10
```

### `.minute()`

Returns the minute.

**Returns:** `int`: the minute (0-59).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.minute())  # 30
```

### `.second()`

Returns the second.

**Returns:** `int`: the second (0-59).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.second())  # 45
```

### `.weekday()`

Returns the day of the week, Python-style (Monday is `0`).

**Returns:** `int`: day of week, where Monday=0 and Sunday=6.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.weekday())  # 0 (Monday)
```

### `.isoweekday()`

Returns the day of the week, ISO-style (Monday is `1`).

**Returns:** `int`: day of week, where Monday=1 and Sunday=7.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.isoweekday())  # 1 (Monday)
```

### `.replace(**kwargs)`

Returns a new datetime instance with the specified fields replaced. Accepts `year`, `month`, `day`, `hour`, `minute`, `second`, and `microsecond` as keyword arguments; any field not specified keeps its current value.

**Parameters:**
- `**kwargs` (`int`): One or more of `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond` to replace.

**Returns:** `datetime`: a new datetime instance with the replacements applied.

**Raises:** `Error`: if an unexpected keyword argument is supplied.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
new_dt = dt.replace(year=2025, month=6)
print(new_dt)  # "2025-06-15 10:30:45"
```

## date Methods

These methods are available on any `date` instance.

### `.strftime(format)`

Formats the date as a string. Behaves identically to the `datetime` method of the same name.

**Parameters:**
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.

**Returns:** `str`: the formatted date string.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.strftime("%A, %B %d, %Y"))  # "Monday, January 15, 2024"
```

### `.year()`

Returns the year.

**Returns:** `int`: the year.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.year())  # 2024
```

### `.month()`

Returns the month.

**Returns:** `int`: the month (1-12).

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.month())  # 1
```

### `.day()`

Returns the day of the month.

**Returns:** `int`: the day of month (1-31).

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.day())  # 15
```

### `.weekday()`

Returns the day of the week, Python-style (Monday is `0`).

**Returns:** `int`: day of week, where Monday=0 and Sunday=6.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.weekday())  # 0 (Monday)
```

### `.isoweekday()`

Returns the day of the week, ISO-style (Monday is `1`).

**Returns:** `int`: day of week, where Monday=1 and Sunday=7.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.isoweekday())  # 1 (Monday)
```

### `.isoformat()`

Returns the date formatted as an ISO 8601 string.

**Returns:** `str`: formatted as `"YYYY-MM-DD"`.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.isoformat())  # "2024-01-15"
```

### `.replace(**kwargs)`

Returns a new date instance with the specified fields replaced. Accepts `year`, `month`, and `day` as keyword arguments; any field not specified keeps its current value.

**Parameters:**
- `**kwargs` (`int`): One or more of `year`, `month`, `day` to replace.

**Returns:** `date`: a new date instance with the replacements applied.

**Raises:** `Error`: if an unexpected keyword argument is supplied.

```python
import datetime

d = datetime.date(2024, 1, 15)
new_d = d.replace(year=2025, month=6)
print(new_d)  # "2025-06-15"
```

## Arithmetic and Comparison

`datetime` and `date` instances support comparison operators (`<`, `>`, `<=`, `>=`, `==`, `!=`) against instances of the same type, and arithmetic with numbers or `timedelta()` values.

For `datetime`, subtraction of two instances returns the difference in seconds as a `float`, and addition takes a number of seconds (`int` or `float`):

```python
import datetime

dt1 = datetime.datetime(2024, 1, 15, 10, 30, 45)
dt2 = datetime.datetime(2024, 1, 16, 10, 30, 45)

# Comparison
print(dt1 < dt2)   # True
print(dt1 == dt2)  # False

# Subtraction (returns seconds as float)
diff = dt2 - dt1
print(diff)  # 86400.0 (one day in seconds)

# Addition (add seconds)
dt3 = dt1 + 3600  # One hour later
print(dt3)  # "2024-01-15 11:30:45"

# Using timedelta
one_day = datetime.timedelta(days=1)
tomorrow = dt1 + one_day
print(tomorrow)  # "2024-01-16 10:30:45"
```

For `date`, subtraction of two instances returns the difference in whole days as an `int`, and addition takes a number of days (`int`) or a `timedelta()` value (`float` seconds, converted to whole days):

```python
import datetime

d1 = datetime.date(2024, 1, 15)
d2 = datetime.date(2024, 1, 20)

# Comparison
print(d1 < d2)   # True

# Subtraction (returns days as int)
diff = d2 - d1
print(diff)  # 5 (days)

# Addition (add days)
next_week = d1 + 7
print(next_week)  # "2024-01-22"

# Using timedelta
one_week = datetime.timedelta(weeks=1)
next_week = d1 + one_week
print(next_week)  # "2024-01-22"
```

## Format Codes

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | Year (4 digits) | 2024 |
| `%m` | Month (01-12) | 01 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour (00-23) | 18 |
| `%I` | Hour (01-12) | 06 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%A` | Full weekday | Monday |
| `%a` | Abbreviated weekday | Mon |
| `%B` | Full month | January |
| `%b` | Abbreviated month | Jan |
| `%p` | AM/PM | PM |
| `%Z` | Timezone name | MST |
| `%z` | Timezone offset | -0700 |

## Python Compatibility

This library implements a Python-like `datetime` API:

| Feature | Supported |
|---------|-----------|
| `datetime.datetime()` | Yes |
| `datetime.datetime.now()` | Yes |
| `datetime.datetime.utcnow()` | Yes |
| `datetime.datetime.strptime()` | Yes |
| `datetime.datetime.fromtimestamp()` | Yes |
| `datetime.date()` | Yes |
| `datetime.date.today()` | Yes |
| `datetime.timedelta()` | Yes (returns total seconds as a `float` rather than a `timedelta` object) |
| Comparison operators | Yes |
| Arithmetic operators | Yes |
| `.replace()` | Yes |
| `.strftime()` | Yes |
| `.isoformat()` | Yes |
| `.timestamp()` | Yes |

## See Also

- [time](../time/) - Lower-level timestamp and time tuple functions, including `sleep()`
- [platform](../platform/) - Platform identifying data
- [io](../io/) - In-memory I/O streams
