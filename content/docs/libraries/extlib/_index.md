---
title: Extended Libraries
description: Python-compatible libraries requiring explicit registration.
weight: 3
---

Extended libraries provide Python-compatible functionality and require explicit registration by the host application.

See the [Go Integration documentation](../go-integration/basics/) for registering libraries.

## Setup

```go
import (
    "github.com/paularlott/scriptling/extlibs"
)

// Register libraries as needed
p.RegisterLibrary("requests", extlibs.RequestsLibrary)
p.RegisterLibrary("html.parser", extlibs.HTMLParserLibrary)

p.RegisterLibrary("yaml", extlibs.YAMllibrary)
p.RegisterLibrary("toml", extlibs.TomlLibrary)
p.RegisterLibrary("glob", extlibs.GlobLibrary)
p.RegisterLibrary("logging", extlibs.LoggingLibrary)
p.RegisterLibrary("os", extlibs.OSLibrary)
p.RegisterLibrary("secrets", extlibs.SecretsLibrary)

// Register os/pathlib with security restrictions
extlibs.RegisterOSLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterPathlibLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterWaitForLibrary(p)
extlibs.RegisterKVLibrary(p)
p.RegisterLibrary("subprocess", extlibs.SubprocessLibrary)
p.RegisterLibrary("sys", extlibs.SysLibrary)
```

## HTTP & Networking

| Library | Description |
|---------|-------------|
| [requests](requests/) | HTTP library for sending requests |

## Parsing & Data

| Library | Description |
|---------|-------------|
| [glob](glob/) | Unix shell-style wildcards |
| [html.parser](html.parser/) | HTML/XHTML parser |
| [yaml](yaml/) | YAML parsing and generation |
| [toml](toml/) | TOML parsing and generation |

## System & Files

| Library | Description |
|---------|-------------|
| [os](os/) | Operating system interfaces |
| [os.path](os.path/) | Pathname manipulations |
| [pathlib](pathlib/) | Object-oriented filesystem paths |
| [sys](sys/) | System-specific parameters |
| [subprocess](subprocess/) | Spawn and manage subprocesses |

## Security

| Library | Description |
|---------|-------------|
| [secrets](secrets/) | Cryptographically strong random numbers |

## Logging

| Library | Description |
|---------|-------------|
| [logging](logging/) | Logging functionality |
