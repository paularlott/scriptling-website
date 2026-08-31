---
title: logging
description: Python-style logging, backed by structured slog-based loggers.
tags: [libraries, logging]
weight: 4
aliases:
  - /reference/libraries/extlib/logging/
  - /reference/libraries/logging/
---

The `logging` library provides Python-style logging functionality, compatible with the basic Python `logging` interface. It uses the [paularlott/logger](https://github.com/paularlott/logger) library under the hood with `slog` integration. Reach for it instead of `print()` whenever a script's output needs levels, structured output, or to flow through the embedder's own logging pipeline.

## Available Functions

| Function | Description |
|----------|-------------|
| `getLogger(name=None)` | Get a named logger instance. |
| `debug(msg)` | Log a debug message with the default logger. |
| `info(msg)` | Log an info message with the default logger. |
| `warning(msg)` | Log a warning message with the default logger. |
| `warn(msg)` | Alias for `warning()` (Python compatibility). |
| `error(msg)` | Log an error message with the default logger. |
| `critical(msg)` | Log a critical message with the default logger (mapped to `error` level). |

## Constants

| Constant | Description |
|----------|-------------|
| `logging.DEBUG` | Debug level (`10`). |
| `logging.INFO` | Info level (`20`). |
| `logging.WARNING` | Warning level (`30`). |
| `logging.WARN` | Alias for `WARNING` (`30`). |
| `logging.ERROR` | Error level (`40`). |
| `logging.CRITICAL` | Critical level (`50`). |

## Functions

### `getLogger(name=None)`

Create and return a logger object with the specified name. The name is used as the group name in the underlying logger and is displayed as a nested group in log output, e.g. `[scriptling.componentName]`.

**Parameters:**
- `name` (`str`, optional): Logger name. Default: `None` (uses `"scriptling"`).

**Returns:** `Logger`: an object with `debug()`, `info()`, `warning()`, `warn()`, `error()`, and `critical()` methods.

```python
import logging

logger = logging.getLogger("myApp")

logger.debug("debug message")
logger.info("info message")
logger.warning("warn message")
logger.error("error message")
logger.critical("critical message")
```

### `debug(msg)`

Log a debug message using the default (module-level) logger.

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.debug("Starting up")
```

### `info(msg)`

Log an info message using the default logger.

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.info("This is an info message")
```

### `warning(msg)`

Log a warning message using the default logger.

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.warning("Watch out!")
```

### `warn(msg)`

Alias for `warning()`, provided for Python compatibility.

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.warn("Watch out!")
```

### `error(msg)`

Log an error message using the default logger.

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.error("Something went wrong")
```

### `critical(msg)`

Log a critical message using the default logger. Critical messages are mapped to the `error` level in the underlying Go logger (there is no separate critical level).

**Parameters:**
- `msg` (`str`): Message to log.

**Returns:** `bool`: always `True`.

```python
import logging

logging.critical("Unrecoverable failure")
```

## Environment Isolation

Each Scriptling environment gets its own logger instance:

- Multiple environments can have different loggers without interfering with each other.
- Loggers can have different output destinations, levels, and formats.
- The logger instance is tied to the environment it was registered with.

```go
// Environment 1
p1 := scriptling.New()
logger1 := logslog.New(logslog.Config{Writer: os.Stdout}).WithGroup("app1")
extlibs.RegisterLoggingLibrary(p1, logger1)

// Environment 2 (different logger)
p2 := scriptling.New()
logger2 := logslog.New(logslog.Config{Writer: someOtherWriter}).WithGroup("app2")
extlibs.RegisterLoggingLibrary(p2, logger2)
```

## Configuration

The default logger is configured with level `INFO`, console (human-readable) format, output to stdout, and group `"scriptling"`. Loggers created with `getLogger()` inherit these settings unless the embedder configures otherwise.

## Using with the `scriptling` CLI

When running scripts via the `scriptling` CLI, the `logging` library is automatically wired to the CLI's own logger. Two flags control both the server's internal logging and any output produced through `logging.*`/`logger.*` calls in scripts:

| Flag | Environment Variable | Config Path | Values | Default |
|------|----------------------|--------------|--------|---------|
| `--log-level` | `SCRIPTLING_LOG_LEVEL` | `log.level` | `trace`, `debug`, `info`, `warn`, `error` | `info` |
| `--log-format` | `SCRIPTLING_LOG_FORMAT` | `log.format` | `console` (coloured), `json` | `console` |

These flags apply to every execution mode (script file, `--code`, `--interactive`, `--server`, `--mcp-tools`, `--mcp-exec-script`, `--lint`).

```bash
# Show debug output while running a script
scriptling --log-level debug app.py

# JSON-formatted logs for ingestion into a log aggregator
scriptling --log-level info --log-format json --server :8000 app.py

# Via environment variables (useful for .env files or container deployments)
SCRIPTLING_LOG_LEVEL=debug SCRIPTLING_LOG_FORMAT=json scriptling --server :8000 app.py
```

When `--log-level debug` is set, the HTTP and MCP servers emit additional diagnostics such as incoming requests, dispatched handlers, MCP tool invocations, and WebSocket lifecycle events.

The same options can be set in `scriptling.toml`:

```toml
[log]
level = "debug"
format = "json"
```

Priority order (highest to lowest): command-line flag, environment variable, config file, default.

## Python Compatibility

Compared to Python's `logging` module, this is a simplified implementation focused on basic logging:

- No configuration API: loggers use the default configuration.
- No handlers: output always goes to the configured writer (stdout by default).
- No formatters: output format is fixed.
- No filtering: all messages at the configured level are shown.
- No hierarchy: named loggers are independent except for the shared group prefix.
- No file logging.

Log messages integrate with Scriptling's output capture system alongside `print()` and other script output.

## See Also

- [sys](../sys/): Access argv and stdin
- [secrets](../secrets/): Generate tokens, separate from logging concerns
