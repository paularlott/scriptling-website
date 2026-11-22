---
title: datetime
description: Date and time objects with construction, formatting, arithmetic, and comparison, using a Python-compatible API.
tags: [libraries, time]
weight: 2

aliases:
  - /reference/libraries/stdlib/datetime/
  - /reference/libraries/datetime/
---

The `datetime` library provides `datetime` and `date` objects for representing points in time, plus `timedelta` durations, following Python's API with the differences listed below.

```python
import datetime
```

## Available Functions

| Function | Description |
|----------|-------------|
| `datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)` | Create a datetime in local time. |
| `datetime.now()` | Current local datetime. |
| `datetime.utcnow()` | Current UTC datetime. |
| `datetime.strptime(date_string, format)` | Parse a string using [format codes](#format-codes). The result is naive (local wall-clock time) unless the format has `%z`, which gives an aware datetime. |
| `datetime.fromisoformat(date_string)` | Parse an ISO 8601 datetime string: naive (local wall-clock time) without an offset, aware with one. |
| `datetime.fromtimestamp(timestamp)` | Local datetime from a Unix timestamp. |
| `datetime.strftime(format, timestamp_or_datetime)` | Scriptling-specific module-level formatter: accepts a Unix timestamp (`int`/`float`) or a datetime. |
| `date(year, month, day)` | Create a date (no time component). |
| `date.today()` | Current local date. |
| `date.fromisoformat(date_string)` | Parse an ISO 8601 date string (`YYYY-MM-DD`). |
| `timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)` | Create a duration. Keyword arguments only. |

## Attributes and Methods

Fields are read-only **attributes**, as in Python: write `dt.year`, not `dt.year()`.

| Member | `datetime` | `date` | `timedelta` | Description |
|--------|:---:|:---:|:---:|-------------|
| `.year`, `.month`, `.day` | Yes | Yes | | Calendar fields (`month` is 1-12). |
| `.hour`, `.minute`, `.second`, `.microsecond` | Yes | | | Time-of-day fields. |
| `.days`, `.seconds`, `.microseconds` | | | Yes | Normalised duration fields, as in Python. |
| `.weekday()` | Yes | Yes | | Day of week, Monday is `0`. |
| `.isoweekday()` | Yes | Yes | | Day of week, Monday is `1`. |
| `.isoformat()` | Yes | Yes | | `YYYY-MM-DDTHH:MM:SS[.ffffff]` or `YYYY-MM-DD`; `timespec=` selects the precision. |
| `.strftime(format)` | Yes | Yes | | Format using [format codes](#format-codes). |
| `.replace(**fields)` | Yes | Yes | | New instance with the given fields changed. |
| `.timestamp()` | Yes | | | Unix timestamp as a `float`. |
| `.total_seconds()` | | | Yes | Duration in seconds as a `float`. |

## Example

```python
import datetime

dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
print(dt)                                   # 2024-01-15 10:30:45
print(dt.year, dt.month, dt.day, dt.hour)   # 2024 1 15 10
print(dt.weekday(), dt.isoweekday())        # 0 1
print(dt.isoformat())                       # 2024-01-15T10:30:45
print(dt.strftime("%A, %B %d, %Y at %I:%M %p"))  # Monday, January 15, 2024 at 10:30 AM
print(dt.replace(year=2025, month=6))       # 2025-06-15 10:30:45

parsed = datetime.datetime.strptime("2024-01-15 10:30:45", "%Y-%m-%d %H:%M:%S")
print(parsed)                               # 2024-01-15 10:30:45
print(datetime.datetime.fromisoformat("2024-01-15T10:30:45"))  # 2024-01-15 10:30:45

ts = dt.timestamp()                         # float seconds since the epoch (local time)
print(datetime.datetime.fromtimestamp(ts))  # 2024-01-15 10:30:45
print(datetime.datetime.strftime("%Y-%m-%d", ts))  # 2024-01-15

d = datetime.date(2024, 1, 15)
print(d, d.year, d.isoformat())             # 2024-01-15 2024 2024-01-15
print(d.strftime("%a %d %b"))               # Mon 15 Jan

now = datetime.datetime.now()               # also datetime.datetime.utcnow(), datetime.date.today()
```

## Arithmetic and Comparison

`datetime` and `date` instances compare with `<`, `>`, `<=`, `>=`, `==`, `!=` against the same type, and accept a `timedelta` for `+` and `-`. Unlike Python, they also accept plain numbers, and subtracting two instances returns a number rather than a `timedelta`:

| Expression | Result |
|------------|--------|
| `datetime - datetime` | Difference in seconds, `float` |
| `datetime + n`, `datetime - n` | `datetime` moved by `n` seconds |
| `date - date` | Difference in whole days, `int` |
| `date + n`, `date - n` | `date` moved by `n` days |
| `datetime`/`date` `+`/`-` `timedelta` | Moved instance (a `date` moves by whole days) |

```python
import datetime

dt1 = datetime.datetime(2024, 1, 15, 10, 30, 45)
dt2 = datetime.datetime(2024, 1, 16, 10, 30, 45)
print(dt1 < dt2, dt1 == dt2)        # True False
print(dt2 - dt1)                    # 86400.0  (seconds, as a float)
print(dt1 + 3600)                   # 2024-01-15 11:30:45
print(dt1 - 3600)                   # 2024-01-15 09:30:45

one_day = datetime.timedelta(days=1)
print(one_day)                      # 1 day, 0:00:00
print(one_day.total_seconds())      # 86400.0
print(dt1 + one_day)                # 2024-01-16 10:30:45
print(dt1 - one_day)                # 2024-01-14 10:30:45

d1 = datetime.date(2024, 1, 15)
d2 = datetime.date(2024, 1, 20)
print(d1 < d2)                      # True
print(d2 - d1)                      # 5  (whole days, as an int)
print(d1 + 7)                       # 2024-01-22
print(d2 - 7)                       # 2024-01-13
print(d1 + datetime.timedelta(weeks=1))  # 2024-01-22
print(d1 - datetime.timedelta(weeks=1))  # 2024-01-08

td = datetime.timedelta(days=1, hours=2, minutes=30)
print(td, td.days, td.seconds)      # 1 day, 2:30:00 1 9000
print(datetime.timedelta(minutes=-5))  # -1 day, 23:55:00
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
| `%Z` | Timezone name (empty for a naive value) | UTC |
| `%z` | Timezone offset (empty for a naive value) | -0700 |
| `%y` | Year without century (00-99) | 24 |
| `%f` | Microsecond (000000-999999) | 123456 |
| `%j` | Day of year (001-366) | 015 |
| `%w` | Weekday number, Sunday is 0 | 1 |
| `%u` | ISO weekday number, Monday is 1 | 1 |
| `%U`, `%W` | Week of year, weeks starting Sunday or Monday | 02 |
| `%G`, `%V` | ISO year and ISO week | 2024, 03 |
| `%e` | Day of month, space padded | 15 |
| `%c`, `%x`, `%X` | Date and time, date, time | Mon Jan 15 10:30:45 2024 |
| `%%` | A literal `%` | % |

`strptime()` accepts the same codes and follows Python's rules: numbers may have fewer digits than the maximum,
names match in any case, and text left over after the format raises `ValueError`.

## Differences from Python

- A naive `datetime` is a local wall-clock time, as in Python: `datetime()`, `now()`, `strptime()` and `fromisoformat()` without an offset all build the same value, and `.timestamp()` reads it in the local zone. Attach a zone with `.replace(tzinfo=datetime.timezone.utc)` when the value is in UTC.
- `datetime + 60` and `datetime - 60` are accepted and mean seconds; Python requires a `timedelta`.
- There is no `fold` attribute, so the repeated hour at the end of daylight saving is always read as its first occurrence.
- Years run from 1 to 9999, and values outside raise `OverflowError` or `ValueError`.
- Format codes follow the C locale (English day and month names). A code that is not recognised is left in the output unchanged.

## See Also

- [time](../time/) - Lower-level timestamp and time tuple functions, including `sleep()`
- [platform](../platform/) - Platform identifying data
- [io](../../text-processing/io/) - In-memory I/O streams
