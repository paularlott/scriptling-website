---
description: Time access and conversions, including timestamps, time tuples, formatting, and sleeping.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/time-system/time/
sources:
    - resource: https://scriptling.dev/reference/libraries/time-system/time/
status: stable
tags:
    - libraries
    - time
title: time
type: API Reference
---
# time

The `time` library provides time-related functions for working with Unix timestamps, time tuples, formatting, parsing, and pausing execution, following Python's `time` module with the differences listed below.

```python
import time
```

## Available Functions

| Function | Description |
|----------|-------------|
| `now()` | Scriptling-specific: current local date/time as an ISO 8601 string (`YYYY-MM-DDTHH:MM:SS.ffffff`). |
| `time()` | Current Unix timestamp as a `float`. |
| `perf_counter()` | High-resolution monotonic timer; only differences between calls are meaningful. |
| `sleep(seconds)` | Pauses execution for the specified number of seconds. |
| `localtime(secs=None)` | Local [time tuple](#time-tuple-format) for a timestamp or `datetime` (default: now). |
| `gmtime(secs=None)` | UTC [time tuple](#time-tuple-format) for a timestamp or `datetime` (default: now). |
| `mktime(tuple)` | Unix timestamp for a local time tuple (only the first six fields are used). |
| `strftime(format, t=None)` | Format a time tuple (default: current local time) using [format codes](#format-codes). |
| `strptime(string, format)` | Parse a string into a time tuple; raises if it does not match. |
| `asctime(t=None)` | Time tuple as `"Mon Jan 15 10:30:45 2024"`. |
| `ctime(secs=None)` | Timestamp as a local `asctime()`-style string. |

## Example

```python
import time

now = time.time()                 # float seconds since the epoch
stamp = time.now()                # Scriptling-specific: ISO 8601 string, e.g. "2025-11-26T11:58:18.123456"

start = time.perf_counter()
time.sleep(0.1)                   # seconds, int or float
print(time.perf_counter() - start >= 0.1)   # True

t = time.gmtime(1705314645)       # UTC time tuple (a list)
print(t)                          # [2024, 1, 15, 10, 30, 45, 1, 15, 0]
print(time.strftime("%Y-%m-%d %H:%M:%S", t))  # 2024-01-15 10:30:45
print(time.asctime(t))            # Mon Jan 15 10:30:45 2024

parsed = time.strptime("2024-01-15 10:30:45", "%Y-%m-%d %H:%M:%S")
print(parsed[:6])                 # [2024, 1, 15, 10, 30, 45]

local = time.localtime(now)       # local time tuple; also accepts a datetime
print(abs(time.mktime(local) - now) < 1)   # True: mktime reverses localtime
print(time.ctime(now))            # local time, e.g. "Mon Jan 15 10:30:45 2024"
```

## Time Tuple Format

`localtime()`, `gmtime()` and `strptime()` return a `struct_time`, as in Python: read its fields by name
(`t.tm_year`) or by position (`t[0]`), unpack it, or pass it to `mktime()` and `strftime()`.

| Position | Field | Value |
|:---:|-------|-------|
| 0 | `tm_year` | Year, such as 2025 |
| 1 | `tm_mon` | Month (1-12) |
| 2 | `tm_mday` | Day of month (1-31) |
| 3 | `tm_hour` | Hour (0-23) |
| 4 | `tm_min` | Minute (0-59) |
| 5 | `tm_sec` | Second (0-59) |
| 6 | `tm_wday` | Day of week, Monday is 0 |
| 7 | `tm_yday` | Day of year (1-366) |
| 8 | `tm_isdst` | Daylight saving flag |

## Format Codes

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | Year (4 digits) | 2024 |
| `%m` | Month (01-12) | 01 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour (00-23) | 18 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%A` | Full weekday | Monday |
| `%a` | Abbreviated weekday | Mon |
| `%B` | Full month | January |
| `%b` | Abbreviated month | Jan |
| `%p` | AM/PM | PM |

## Differences from Python

- `strftime()` and `strptime()` take the same [format codes](https://scriptling.dev/okf/scriptling-libraries/time-system/datetime.md#format-codes) as `datetime`.
- `ctime()`/`asctime()` do not pad single-digit days (`"Fri Jan 5 ..."`; Python gives `"Fri Jan  5 ..."`).
- `time.now()` is an addition. `time_ns()`, `process_time()` and the other `*_ns` variants are not available; use `perf_counter()` or `monotonic()`.

## See Also

- [datetime](https://scriptling.dev/okf/scriptling-libraries/time-system/datetime.md) - Higher-level date/time objects with arithmetic and comparison
- [platform](https://scriptling.dev/okf/scriptling-libraries/time-system/platform.md) - Platform identifying data
- [io](https://scriptling.dev/okf/scriptling-libraries/text-processing/io.md) - In-memory I/O streams
