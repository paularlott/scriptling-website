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

The `time` library provides time-related functions for working with Unix timestamps, time tuples, formatting, parsing, and pausing execution, with a Python-compatible API.

```python
import time
```

## Available Functions

| Function | Description |
|----------|-------------|
| `now()` | Returns the current date/time as an ISO 8601 string. |
| `time()` | Returns the current Unix timestamp. |
| `perf_counter()` | Returns a high-resolution monotonic timer. |
| `sleep(seconds)` | Pauses execution for the specified number of seconds. |
| `localtime(secs=None)` | Converts a timestamp or datetime to a local time tuple. |
| `gmtime(secs=None)` | Converts a timestamp or datetime to a UTC time tuple. |
| `mktime(tuple)` | Converts a time tuple to a Unix timestamp. |
| `strftime(format, t=None)` | Formats a time tuple as a string. |
| `strptime(string, format)` | Parses a string into a time tuple. |
| `asctime(t=None)` | Converts a time tuple to a standard format string. |
| `ctime(secs=None)` | Converts a Unix timestamp to a standard format string. |

## Functions

### `time.now()`

Returns the current date and time as an ISO 8601 formatted string.

**Returns:** `str`: the current date and time, formatted as `YYYY-MM-DDTHH:MM:SS.ffffff`.

```python
import time

ts = time.now()  # "2025-11-26T11:58:18.123456"
```

### `time.time()`

Returns the current Unix timestamp.

**Returns:** `float`: seconds since the Unix epoch.

```python
import time

now = time.time()  # 1732435200.123456
```

### `time.perf_counter()`

Returns a high-resolution monotonic timer, useful for benchmarking. The value has no defined absolute meaning: only differences between calls are meaningful.

**Returns:** `float`: seconds since an arbitrary fixed point (program start).

```python
import time

start = time.perf_counter()
# ... some code ...
end = time.perf_counter()
elapsed = end - start
```

### `time.sleep(seconds)`

Pauses execution for the specified number of seconds.

**Parameters:**
- `seconds` (`int` or `float`): Number of seconds to sleep.

**Returns:** `None`

```python
import time

print("Waiting...")
time.sleep(1)      # Sleep 1 second
time.sleep(0.5)    # Sleep 0.5 seconds
print("Done!")
```

### `time.localtime(secs=None)`

Converts a Unix timestamp or datetime instance to a 9-element time tuple representing local time. See [Time Tuple Format](#time-tuple-format) below.

**Parameters:**
- `secs` (`int`, `float`, or `datetime`, optional): Unix timestamp or datetime instance to convert. Default: `None` (uses the current time).

**Returns:** `list`: a 9-element time tuple `[year, month, day, hour, minute, second, weekday, yearday, dst]`.

```python
import time
import datetime

# Current local time tuple
local_tuple = time.localtime()
# [2025, 11, 26, 11, 58, 18, 3, 330, 0]

# Specific timestamp
specific_tuple = time.localtime(1705314645.0)
# [2024, 1, 15, 18, 30, 45, 1, 15, 0]

# From a datetime instance
dt = datetime.datetime.now()
dt_tuple = time.localtime(dt)
```

### `time.gmtime(secs=None)`

Converts a Unix timestamp or datetime instance to a 9-element time tuple representing UTC time. See [Time Tuple Format](#time-tuple-format) below.

**Parameters:**
- `secs` (`int`, `float`, or `datetime`, optional): Unix timestamp or datetime instance to convert. Default: `None` (uses the current time).

**Returns:** `list`: a 9-element time tuple `[year, month, day, hour, minute, second, weekday, yearday, dst]`.

```python
import time
import datetime

# Current UTC time tuple
utc_tuple = time.gmtime()
# [2025, 11, 26, 3, 58, 18, 3, 330, 0]

# Specific UTC timestamp
utc_specific = time.gmtime(1705314645.0)
# [2024, 1, 15, 18, 30, 45, 1, 15, 0]

# From a datetime instance
dt = datetime.datetime.utcnow()
dt_tuple = time.gmtime(dt)
```

### `time.mktime(tuple)`

Converts a time tuple back to a Unix timestamp, interpreting the tuple as local time. Only the first six elements (year through second) are used.

**Parameters:**
- `tuple` (`list`): 9-element time tuple.

**Returns:** `float`: the corresponding Unix timestamp.

```python
import time

tuple = [2024, 1, 15, 18, 30, 45, 1, 15, 0]
timestamp = time.mktime(tuple)
# 1705314645.0
```

### `time.strftime(format, t=None)`

Formats a time tuple according to the given format string.

**Parameters:**
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.
- `t` (`list`, optional): 9-element time tuple. Default: `None` (uses the current local time).

**Returns:** `str`: the formatted time string.

```python
import time

# Format current time
formatted = time.strftime("%Y-%m-%d %H:%M:%S")
# "2025-11-26 11:58:18"

# Format specific time tuple
tuple = time.localtime(1705314645.0)
formatted = time.strftime("%Y-%m-%d %H:%M:%S", tuple)
# "2024-01-15 18:30:45"
```

### `time.strptime(string, format)`

Parses a time string according to the given format and returns a time tuple.

**Parameters:**
- `string` (`str`): Time string to parse.
- `format` (`str`): Python-style format string. See [Format Codes](#format-codes) below.

**Returns:** `list`: a 9-element time tuple.

**Raises:** `Error`: when `string` does not match `format`.

```python
import time

tuple = time.strptime("2024-01-15 10:30:45", "%Y-%m-%d %H:%M:%S")
# [2024, 1, 15, 10, 30, 45, 1, 15, 0]
```

### `time.asctime(t=None)`

Converts a time tuple to a string in a standard fixed format.

**Parameters:**
- `t` (`list`, optional): 9-element time tuple. Default: `None` (uses the current local time).

**Returns:** `str`: formatted as `"Wed Nov 26 11:58:18 2025"`.

```python
import time

# Current time
ascii_time = time.asctime()
# "Wed Nov 26 11:58:18 2025"

# Specific time tuple
tuple = time.localtime(1705314645.0)
ascii_time = time.asctime(tuple)
# "Mon Jan 15 18:30:45 2024"
```

### `time.ctime(secs=None)`

Converts a Unix timestamp to a string in a standard fixed format.

**Parameters:**
- `secs` (`int` or `float`, optional): Unix timestamp. Default: `None` (uses the current time).

**Returns:** `str`: formatted as `"Wed Nov 26 11:58:18 2025"`.

```python
import time

# Current time
ctime_str = time.ctime()
# "Wed Nov 26 11:58:18 2025"

# Specific timestamp
ctime_str = time.ctime(1705314645.0)
# "Mon Jan 15 18:30:45 2024"
```

## Time Tuple Format

Time tuples are 9-element lists with the following structure:

```python
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

## See Also

- [datetime](datetime.md) - Higher-level date/time objects with arithmetic and comparison
- [platform](platform.md) - Platform identifying data
- [io](io.md) - In-memory I/O streams
