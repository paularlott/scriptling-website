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

Time tuples are 9-element lists with the following structure:

```text
[year, month, day, hour, minute, second, weekday, yearday, dst]
```

- `year`: Year (e.g., 2025)
- `month`: Month (1-12)
- `day`: Day of month (1-31)
- `hour`: Hour (0-23)
- `minute`: Minute (0-59)
- `second`: Second (0-59)
- `weekday`: Day of week (0=Sunday, 6=Saturday). This follows Go's convention and differs from Python, where Monday is 0.
- `yearday`: Day of year (1-366)
- `dst`: Daylight saving time flag. Always `0` (not currently determined).

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

- Time tuples are plain 9-element **lists**, not `struct_time`: index them (`t[0]`) rather than using `t.tm_year`. `mktime()` accepts a list.
- The weekday field counts from Sunday (`0`), not Monday, and `dst` is always `0`.
- Only the format codes in the table above are supported by `strftime()`/`strptime()`; others (such as `%I`, `%j`, `%y`, `%Z`) are left in the output unchanged. [datetime](https://scriptling.dev/okf/scriptling-libraries/time-system/datetime.md) formatting also supports `%I`, `%Z` and `%z`.
- `ctime()`/`asctime()` do not pad single-digit days (`"Fri Jan 5 ..."`; Python gives `"Fri Jan  5 ..."`).
- `time.now()` is an addition. `monotonic()`, `time_ns()`, `process_time()` and the other `*_ns` variants are not available; use `perf_counter()`.

## See Also

- [datetime](https://scriptling.dev/okf/scriptling-libraries/time-system/datetime.md) - Higher-level date/time objects with arithmetic and comparison
- [platform](https://scriptling.dev/okf/scriptling-libraries/time-system/platform.md) - Platform identifying data
- [io](https://scriptling.dev/okf/scriptling-libraries/text-processing/io.md) - In-memory I/O streams
