---
title: Extended Libraries
description: Python-compatible libraries requiring explicit registration.
weight: 3
---

Extended libraries provide Python-compatible functionality and require explicit registration by the host application.

## Setup

```go
import (
    "github.com/paularlott/scriptling/extlibs"
)

// Register libraries as needed
p.RegisterLibrary("requests", extlibs.RequestsLibrary)

// Register os/pathlib with security restrictions
extlibs.RegisterOSLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterPathlibLibrary(p, []string{"/tmp", "/data"})
```

## HTTP & Networking

| Library | Description |
|---------|-------------|
| [requests](requests/) | HTTP library for sending requests |
| [http](http/) | HTTP client with advanced features |

## System & Files

| Library | Description |
|---------|-------------|
| [sys](sys/) | System-specific parameters |
| [os](os/) | Operating system interfaces |
| [os.path](os.path/) | Pathname manipulations |
| [pathlib](pathlib/) | Object-oriented filesystem paths |
| [glob](glob/) | Unix shell-style wildcards |
| [subprocess](subprocess/) | Spawn and manage subprocesses |

## Security

| Library | Description |
|---------|-------------|
| [secrets](secrets/) | Cryptographically strong random numbers |

## Parsing & Logging

| Library | Description |
|---------|-------------|
| [html.parser](html.parser/) | HTML/XHTML parser |
| [logging](logging/) | Logging functionality |
| [yaml](yaml/) | YAML parsing and generation |
| [toml](toml/) | TOML parsing and generation |

## Utilities

| Library | Description |
|---------|-------------|
| [wait_for](wait_for/) | Wait for resources to become available |
| [kv](kv/) | Persistent key-value store |

## Usage Example

```python
import json
import requests

# HTTP request
response = requests.get("https://api.example.com/data", timeout=10)
if response.status_code == 200:
    data = response.json()
    print(data)
```
