---
description: Read-only access to the underlying operating system, architecture, and hostname information.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/time-system/platform/
sources:
    - resource: https://scriptling.dev/reference/libraries/time-system/platform/
status: stable
tags:
    - libraries
    - time
title: platform
type: API Reference
---
# platform

The `platform` library provides read-only access to the underlying platform's identifying data, such as the operating system name, machine architecture, and hostname.

## Available Functions

| Function | Description |
|----------|-------------|
| `architecture()` | Returns bit architecture info as a list. |
| `machine()` | Returns the machine type (e.g., `'arm64'`). |
| `node()` | Returns the computer's network name (hostname). |
| `platform()` | Returns a platform identifier string. |
| `processor()` | Returns the processor name. |
| `python_version()` | Returns the Scriptling version, for Python compatibility. |
| `release()` | Returns the system release. |
| `scriptling_version()` | Returns the Scriptling version string. |
| `system()` | Returns the system/OS name (e.g., `'Darwin'`). |
| `uname()` | Returns a dictionary of combined system information. |
| `version()` | Returns the system version. |

## Functions

### `architecture()`

Returns the bit architecture and linkage format as a two-element list.

**Parameters:** None

**Returns:** `list`: `[bits, linkage]`, e.g. `['64bit', '']`. `linkage` is always an empty string.

```python
import platform

print(platform.architecture())
# Output: ['64bit', '']
```

### `machine()`

Returns the machine type (the Go architecture name).

**Parameters:** None

**Returns:** `str`: e.g. `'amd64'`, `'arm64'`, `'arm'`.

```python
import platform

print(platform.machine())
# Output: 'arm64'
```

### `node()`

Returns the computer's network name (hostname). It may not be fully qualified.

**Parameters:** None

**Returns:** `str`: the hostname, or an empty string if it cannot be determined.

```python
import platform

print(platform.node())
# Output: 'my-computer.local'
```

### `platform()`

Returns a single string identifying the underlying platform, combining the OS name and architecture.

**Parameters:** None

**Returns:** `str`: e.g. `'darwin-arm64'`, `'linux-amd64'`.

```python
import platform

print(platform.platform())
# Output: 'darwin-arm64'
```

### `processor()`

Returns the processor name. In Scriptling this is the same value as `machine()`.

**Parameters:** None

**Returns:** `str`: e.g. `'arm64'`, `'amd64'`.

```python
import platform

print(platform.processor())
# Output: 'arm64'
```

### `python_version()`

Returns the Python version string, for compatibility with scripts written against Python's `platform` module.

**Parameters:** None

**Returns:** `str`: the Scriptling version (Scriptling substitutes its own version here for compatibility).

```python
import platform

print(platform.python_version())
# Output: '1.0.0'
```

### `release()`

Returns the system's release identifier. In Scriptling this is the Scriptling version, used for compatibility.

**Parameters:** None

**Returns:** `str`: the Scriptling version.

```python
import platform

print(platform.release())
# Output: '1.0.0'
```

### `scriptling_version()`

Returns the Scriptling version string. This is the Scriptling-specific equivalent of `python_version()`.

**Parameters:** None

**Returns:** `str`: the current Scriptling version.

```python
import platform

print(platform.scriptling_version())
# Output: '1.0.0'
```

### `system()`

Returns the system/OS name. An empty string is never returned here: unrecognized platforms fall back to the raw Go `GOOS` value.

**Parameters:** None

**Returns:** `str`: `'Darwin'`, `'Linux'`, `'Windows'`, `'FreeBSD'`, or the raw OS identifier on other platforms.

```python
import platform

print(platform.system())
# Output: 'Darwin'
```

### `uname()`

Returns a dictionary combining the most commonly used identifying information in one call.

**Parameters:** None

**Returns:** `dict`: with keys `system`, `node`, `release`, `version`, `machine`, `processor`. Unlike Python, which returns a `namedtuple`, Scriptling returns a plain dictionary.

```python
import platform

info = platform.uname()
print(info["system"])
# Output: 'Darwin'
```

### `version()`

Returns the system's release version. In Scriptling this is the Scriptling version, used for compatibility.

**Parameters:** None

**Returns:** `str`: the Scriptling version.

```python
import platform

print(platform.version())
# Output: '1.0.0'
```

## Python Compatibility

This library implements a subset of Python's `platform` module, using the Scriptling version as a stand-in wherever Python would return real OS release/version strings that Go does not expose directly:

| Function | Notes |
|----------|-------|
| `architecture()` | Returns a list, not a tuple; linkage is always `''`. |
| `machine()` | Maps directly to the Go `GOARCH` value. |
| `node()` | Maps directly to the OS hostname. |
| `platform()` | Takes no arguments (Python's `aliased`/`terse` options are not supported). |
| `processor()` | Same value as `machine()`. |
| `python_version()` | Returns the Scriptling version instead of a Python version. |
| `release()` | Returns the Scriptling version instead of a real OS release string. |
| `scriptling_version()` | Scriptling-specific; has no Python equivalent. |
| `system()` | Maps Go's `GOOS` to Python-style capitalized names. |
| `uname()` | Returns a `dict` instead of a `namedtuple`. |
| `version()` | Returns the Scriptling version instead of a real OS version string. |

## See Also

- [datetime](https://scriptling.dev/okf/scriptling-libraries/time-system/datetime.md) - Date and time types
- [time](https://scriptling.dev/okf/scriptling-libraries/time-system/time.md) - Time access and conversions
- [io](https://scriptling.dev/okf/scriptling-libraries/time-system/io.md) - In-memory I/O streams
