---
description: Shell-style lexical analysis — quoting, splitting, and joining command-line tokens.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/text-processing/shlex/
sources:
    - resource: https://scriptling.dev/reference/libraries/text-processing/shlex/
status: stable
tags:
    - libraries
    - text
title: shlex
type: API Reference
---
# shlex

The `shlex` library provides shell-style string quoting and splitting, matching Python's `shlex` module. Use it to safely build command lines for [`subprocess`](https://scriptling.dev/okf/scriptling-libraries/text-processing.md) or to parse shell-like input.

## Available Functions

| Function | Description |
|----------|-------------|
| `quote(s)` | Escape a string for use as a single shell argument. |
| `split(s)` | Split a string into shell-style tokens. |
| `join(split_command)` | Join a list of arguments into a shell-quoted string. |

## Functions

### `quote(s)`

Returns a shell-escaped version of `s`. If the string contains only safe characters (`[a-zA-Z0-9_@%+=:,./-]`) it is returned unchanged; otherwise it is wrapped in single quotes with embedded single quotes escaped.

**Parameters:** `s` (`str`): The string to escape.

**Returns:** `str`: the shell-safe string.

```python
import shlex

shlex.quote("a b c")       # "'a b c'"
shlex.quote("simple")      # "simple"
shlex.quote("it's")        # "'it'\"'\"'s'"
shlex.quote("")            # "''"

# Build a safe command line
cmd = "grep " + shlex.quote(user_input)
```

### `split(s)`

Parses `s` using shell-style rules for quoting and escaping, returning a list of tokens.

- **Single quotes** (`'…'`): everything is literal.
- **Double quotes** (`"…"`): everything is literal except a backslash before `"`, `\`, ``$``, or `` ` ``.
- **Backslash** (outside single quotes): escapes the next character.

**Parameters:** `s` (`str`): The string to split.

**Returns:** `list[str]`: the parsed tokens.

**Raises:** `Error` on unterminated quotes or a trailing backslash.

```python
import shlex

shlex.split("mycommand --flag value")
# ["mycommand", "--flag", "value"]

shlex.split('cmd --flag="quoted value"')
# ["cmd", "--flag=quoted value"]

shlex.split("ls 'My Documents'")
# ["ls", "My Documents"]
```

### `join(split_command)`

Quotes each argument with `quote()` and joins them with spaces, producing a single shell-safe command-line string.

**Parameters:** `split_command` (`list[str]`): The arguments to join.

**Returns:** `str`: the shell-quoted command line.

```python
import shlex

shlex.join(["ls", "-la", "My Documents"])
# "ls -la 'My Documents'"

# round trip
shlex.join(shlex.split("grep 'hello world' file.txt"))
# "grep 'hello world' file.txt"
```

## Security Considerations

`shlex` does not access the filesystem and requires no `allowedPaths`. It is a pure string-processing library.

Use `quote()` to prevent shell injection when constructing command strings for `subprocess`:

```python
import shlex, subprocess

# SAFE: user input is quoted
subprocess.run(shlex.split("echo " + shlex.quote(user_input)))
```

## See Also

- [subprocess](https://scriptling.dev/okf/scriptling-libraries/http-process/subprocess.md): Running external commands
