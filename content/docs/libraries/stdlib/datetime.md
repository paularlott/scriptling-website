---
title: datetime
weight: 1
---

Date and time manipulation library with Python-compatible API.

```python
import datetime
```

## Overview

The datetime library provides two main classes:

- **`datetime`** - Represents a date and time
- **`date`** - Represents a date (year, month, day only)

Plus the **`timedelta()`** function for working with durations.

## Quick Start

```python
import datetime

# Current datetime
now = datetime.datetime.now()
print(now)  # "2025-11-26 11:15:54"

# Current date
today = datetime.date.today()
print(today)  # "2025-11-26"

# Create specific datetime
dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt)  # "2024-01-15 10:30:45"

# Create specific date
d = datetime.date(2024, 1, 15)
print(d)  # "2024-01-15"
```

## datetime Class

### Creating datetime Instances

#### datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)

Creates a datetime instance for the specified date and time.

**Parameters:**

- `year` (int): Year
- `month` (int): Month (1-12)
- `day` (int): Day (1-31)
- `hour` (int, optional): Hour (0-23), default 0
- `minute` (int, optional): Minute (0-59), default 0
- `second` (int, optional): Second (0-59), default 0
- `microsecond` (int, optional): Microsecond, default 0

```python
import datetime

dt = datetime.datetime(2024, 1, 15)  # "2024-01-15 00:00:00"
dt = datetime.datetime(2024, 1, 15, 10, 30, 45)  # "2024-01-15 10:30:45"
```

#### datetime.now()

Returns the current local datetime as a datetime instance.

```python
import datetime

now = datetime.datetime.now()
print(now)  # "2025-11-26 11:15:54"
print(now.year())  # 2025
print(now.month())  # 11
```

#### datetime.utcnow()

Returns the current UTC datetime as a datetime instance.

```python
import datetime

utc_now = datetime.datetime.utcnow()
print(utc_now)  # "2025-11-26 03:15:54"
```

#### datetime.strptime(date_string, format)

Parses a date string and returns a datetime instance.

**Parameters:**

- `date_string`: String to parse
- `format`: Python-style format string

```python
import datetime

dt = datetime.datetime.strptime("2024-01-15 10:30:45", "%Y-%m-%d %H:%M:%S")
print(dt)  # "2024-01-15 10:30:45"
```

#### datetime.fromtimestamp(timestamp)

Creates a datetime from a Unix timestamp.

**Parameters:**

- `timestamp`: Unix timestamp (integer or float)

```python
import datetime

dt = datetime.datetime.fromtimestamp(1705314645)
print(dt)  # "2024-01-15 10:30:45"
```

#### datetime.strftime(format, timestamp_or_datetime)

Formats a timestamp or datetime as a string.

**Parameters:**

- `format`: Python-style format string
- `timestamp_or_datetime`: Unix timestamp (int/float) or datetime instance

```python
import datetime

formatted = datetime.datetime.strftime("%Y-%m-%d %H:%M:%S", 1705314645)
print(formatted)  # "2024-01-15 10:30:45"
```

### datetime Instance Methods

#### .strftime(format)

Formats the datetime as a string.

```python
import datetime

dt = datetime.datetime.now()
formatted = dt.strftime("%A, %B %d, %Y at %I:%M %p")
print(formatted)  # "Wednesday, November 26, 2025 at 11:15 AM"
```

#### .timestamp()

Returns the datetime as a Unix timestamp (float).

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
ts = dt.timestamp()
print(ts)  # 1705314645.0
```

#### .isoformat()

Returns the datetime in ISO 8601 format.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.isoformat())  # "2024-01-15T10:30:45"
```

#### Component Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `.year()` | int | Year |
| `.month()` | int | Month (1-12) |
| `.day()` | int | Day of month (1-31) |
| `.hour()` | int | Hour (0-23) |
| `.minute()` | int | Minute (0-59) |
| `.second()` | int | Second (0-59) |
| `.weekday()` | int | Day of week (Monday=0, Sunday=6) |
| `.isoweekday()` | int | Day of week (Monday=1, Sunday=7) |

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt.year())     # 2024
print(dt.month())    # 1
print(dt.day())      # 15
print(dt.hour())     # 10
print(dt.minute())   # 30
print(dt.second())   # 45
print(dt.weekday())  # 0 (Monday)
```

#### .replace(**kwargs)

Returns a new datetime with specified fields replaced.

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
new_dt = dt.replace(year=2025, month=6)
print(new_dt)  # "2025-06-15 10:30:45"
```

### datetime Arithmetic and Comparison

datetime instances support arithmetic and comparison operations:

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

## date Class

### Creating date Instances

#### date(year, month, day)

Creates a date instance for the specified date.

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d)  # "2024-01-15"
```

#### date.today()

Returns the current local date as a date instance.

```python
import datetime

today = datetime.date.today()
print(today)  # "2025-11-26"
```

### date Instance Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `.strftime(format)` | string | Format date as string |
| `.year()` | int | Year |
| `.month()` | int | Month (1-12) |
| `.day()` | int | Day of month (1-31) |
| `.weekday()` | int | Day of week (Monday=0, Sunday=6) |
| `.isoweekday()` | int | Day of week (Monday=1, Sunday=7) |
| `.isoformat()` | string | ISO 8601 format ("2024-01-15") |
| `.replace(**kwargs)` | date | Return date with replaced fields |

```python
import datetime

d = datetime.date(2024, 1, 15)
print(d.year())      # 2024
print(d.month())     # 1
print(d.day())       # 15
print(d.weekday())   # 0 (Monday)
print(d.strftime("%A, %B %d, %Y"))  # "Monday, January 15, 2024"
```

### date Arithmetic and Comparison

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

## timedelta Function

### timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

Creates a duration and returns the total duration in seconds.

**Parameters (all optional, keyword-only):**

- `days`: Number of days
- `seconds`: Number of seconds
- `microseconds`: Number of microseconds
- `milliseconds`: Number of milliseconds
- `minutes`: Number of minutes
- `hours`: Number of hours
- `weeks`: Number of weeks

**Returns:** Float (total duration in seconds)

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

## Format Codes

| Code | Description         | Example |
| ---- | ------------------- | ------- |
| `%Y` | Year (4 digits)     | 2024    |
| `%m` | Month (01-12)       | 01      |
| `%d` | Day (01-31)         | 15      |
| `%H` | Hour (00-23)        | 18      |
| `%I` | Hour (01-12)        | 06      |
| `%M` | Minute (00-59)      | 30      |
| `%S` | Second (00-59)      | 45      |
| `%A` | Full weekday        | Monday  |
| `%a` | Abbreviated weekday | Mon     |
| `%B` | Full month          | January |
| `%b` | Abbreviated month   | Jan     |
| `%p` | AM/PM               | PM      |
| `%Z` | Timezone name       | MST     |
| `%z` | Timezone offset     | -0700   |

## Complete Example

```python
import datetime

# Current date and time
now = datetime.datetime.now()
print(f"Now: {now}")
print(f"Year: {now.year()}, Month: {now.month()}, Day: {now.day()}")
print(f"Hour: {now.hour()}, Minute: {now.minute()}, Second: {now.second()}")
print(f"Weekday: {now.weekday()} (0=Monday)")
print(f"ISO format: {now.isoformat()}")

# Date arithmetic
tomorrow = now + datetime.timedelta(days=1)
next_week = now + datetime.timedelta(weeks=1)
print(f"Tomorrow: {tomorrow}")
print(f"Next week: {next_week}")

# Working with dates only
today = datetime.date.today()
print(f"Today: {today}")
print(f"Formatted: {today.strftime('%A, %B %d, %Y')}")

# Parsing and formatting
dt = datetime.datetime.strptime("2024-12-25", "%Y-%m-%d")
print(f"Christmas: {dt.strftime('%A, %B %d, %Y')}")

# Comparison
if now > dt:
    print("Christmas has passed")
else:
    print("Christmas is coming")

# Create specific datetime
meeting = datetime.datetime(2025, 1, 15, 14, 30)
print(f"Meeting: {meeting}")
print(f"Meeting timestamp: {meeting.timestamp()}")

# Date difference
christmas = datetime.date(2024, 12, 25)
new_year = datetime.date(2025, 1, 1)
days_between = new_year - christmas
print(f"Days between Christmas and New Year: {days_between}")
```

## Python Compatibility

This library implements a Python-like datetime API:

| Feature | Supported |
| ------- | --------- |
| `datetime.datetime()` | ✅ |
| `datetime.datetime.now()` | ✅ |
| `datetime.datetime.utcnow()` | ✅ |
| `datetime.datetime.strptime()` | ✅ |
| `datetime.datetime.fromtimestamp()` | ✅ |
| `datetime.date()` | ✅ |
| `datetime.date.today()` | ✅ |
| `datetime.timedelta()` | ✅ |
| Comparison operators | ✅ |
| Arithmetic operators | ✅ |
| `.replace()` | ✅ |
| `.strftime()` | ✅ |
| `.isoformat()` | ✅ |
| `.timestamp()` | ✅ |
