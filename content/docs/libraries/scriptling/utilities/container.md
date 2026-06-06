---
title: scriptling.container
linkTitle: container
weight: 1
---

The `scriptling.container` library provides container lifecycle management for Docker, Podman, and Apple Containers through a unified interface. All operations go through a `ContainerClient` obtained from `Client()`.

## Endpoint Configuration

Docker and Podman endpoints are configured via the `--docker-host` / `--podman-host` CLI flags or the `DOCKER_HOST` / `CONTAINER_HOST` environment variables. See [CLI Basic Usage](../../cli/basic-usage/#container-endpoints) for details.

## Module Functions

| Function | Description |
|---|---|
| `runtimes()` | List available container runtimes |
| `Client(driver, **kwargs)` | Create a container client |

## ContainerClient Methods

| Method | Description |
|---|---|
| `driver()` | Return the active runtime name |
| `login(registry, username, password)` | Authenticate with a container registry |
| `image_pull(image)` | Pull an image from a registry |
| `image_list()` | List locally available images |
| `image_remove(image)` | Remove a local image |
| `exec(name_or_id, command, **kwargs)` | Run a command in a running container and capture output |
| `exec_stream(name_or_id, command, callback, **kwargs)` | Run a command in a running container and stream output line by line |
| `run(image, **kwargs)` | Create and start a container |
| `stop(name_or_id)` | Stop a running container |
| `remove(name_or_id)` | Remove a stopped container |
| `inspect(name_or_id)` | Get container details |
| `list()` | List all containers |
| `volume_create(name, **kwargs)` | Create a named volume |
| `volume_remove(name)` | Remove a named volume |
| `volume_list()` | List named volumes |

## Functions

### container.runtimes()

Returns the names of container runtimes that are currently installed and running on this system.

**Returns:** `list` of strings — subset of `["docker", "podman", "apple"]`

```python
import scriptling.container as container

available = container.runtimes()
print("Available runtimes:", available)
```

### container.Client(driver, **kwargs)

Creates a `ContainerClient` for the specified runtime.

**Parameters:**

- `driver` (string): Runtime to use — `"docker"`, `"podman"`, or `"apple"`
- `socket` (string, optional): Override the endpoint. Accepts a Unix socket path, `unix://` URI, `tcp://` address, or `https://` address (docker/podman only). Defaults to `DOCKER_SOCK` / `PODMAN_SOCK` env vars, then the built-in defaults.

**Returns:** `ContainerClient`

```python
# Local Docker (default socket)
c = container.Client("docker")

# Docker via Lima or custom socket
c = container.Client("docker", socket="unix:///Users/paul/.lima/docker/sock/docker.sock")

# Remote Docker daemon over TCP
c = container.Client("docker", socket="tcp://192.168.1.10:2375")

# Remote Docker over TLS
c = container.Client("docker", socket="https://192.168.1.10:2376")

# Local Podman (default socket)
c = container.Client("podman")

# Podman with user-scoped socket
c = container.Client("podman", socket="unix:///run/user/1000/podman/podman.sock")

# Apple Containers
c = container.Client("apple")
```

## ContainerClient

### login(server, username, password)

Authenticates with a container registry. For Docker/Podman the credentials are stored on the client and injected automatically as `X-Registry-Auth` on subsequent `image_pull` calls for the same registry. For Apple Containers the host CLI credential store is updated via `container registry login`.

**Parameters:**

- `registry` (string): Registry hostname e.g. `"ghcr.io"` or `"registry.example.com"`. Pass `""` to target Docker Hub.
- `username` (string): Registry username
- `password` (string): Registry password or access token

```python
# Docker Hub
c.login("", "myuser", "mytoken")
c.image_pull("myuser/myimage:latest")

# GitHub Container Registry
c.login("ghcr.io", "myuser", "ghp_token")
c.image_pull("ghcr.io/myorg/myimage:latest")

# Private registry
c.login("registry.example.com", "user", "pass")
c.image_pull("registry.example.com/myimage:1.0")
```

### driver()

Returns the name of the active runtime driver.

**Returns:** `str` — `"docker"`, `"podman"`, or `"apple"`

### image_pull(image)

Pulls an image from a registry.

**Parameters:**

- `image` (string): Image reference e.g. `"ubuntu:24.04"`

```python
c.image_pull("ubuntu:24.04")
```

### image_list()

Lists locally available images.

**Returns:** `list` of dicts with keys:

- `id` (str): Image ID (digest for Apple, full ID for Docker/Podman)
- `reference` (str): Image reference e.g. `"ubuntu:24.04"`
- `digest` (str): Content digest e.g. `"sha256:abc123..."`
- `size` (int): Manifest/layer size in bytes

```python
for img in c.image_list():
    print(img["reference"], img["digest"])
```

### image_remove(image)

Removes a local image.

**Parameters:**

- `image` (string): Image reference e.g. `"ubuntu:24.04"`

```python
c.image_remove("ubuntu:24.04")
```

### exec(name_or_id, command, **kwargs)

Runs a command inside an already-running container and captures the full output.

**Parameters:**

- `name_or_id` (string): Container name or ID
- `command` (list): Command and arguments e.g. `["/bin/sh", "-c", "echo hi"]`
- `env` (list, optional): Environment variables e.g. `["KEY=value"]`
- `workdir` (string, optional): Working directory inside the container
- `user` (string, optional): User to run as e.g. `"root"` or `"1000:1000"`

**Returns:** `dict` with keys:

- `stdout` (str): Captured standard output
- `stderr` (str): Captured standard error
- `exit_code` (int): Process exit code

```python
result = c.exec("app", ["/bin/sh", "-c", "cat /etc/os-release"])
print(result["stdout"])
print("exit:", result["exit_code"])
```

### exec_stream(name_or_id, command, callback, **kwargs)

Runs a command inside an already-running container and calls `callback(stream, line)` for each line of output as it arrives. `stream` is `"stdout"` or `"stderr"`.

**Parameters:**

- `name_or_id` (string): Container name or ID
- `command` (list): Command and arguments
- `callback` (callable): Function called with `(stream, line)` for each output line
- `env` (list, optional): Environment variables e.g. `["KEY=value"]`
- `workdir` (string, optional): Working directory inside the container
- `user` (string, optional): User to run as

**Returns:** `dict` with `exit_code` (int). `stdout` and `stderr` are empty strings — output was delivered to the callback.

```python
def on_line(stream, line):
    print(f"[{stream}] {line}")

result = c.exec_stream("app", ["/bin/sh", "-c", "for i in 1 2 3; do echo $i; done"], on_line)
print("exit:", result["exit_code"])
```

### run(image, **kwargs)

Creates and starts a container.

**Parameters:**

- `image` (string): Image reference e.g. `"ubuntu:24.04"`
- `name` (string, optional): Container name
- `ports` (list, optional): Port mappings e.g. `["8080:80"]`
- `env` (list, optional): Environment variables e.g. `["KEY=value"]`
- `volumes` (list, optional): Volume mounts e.g. `["mydata:/data"]`
- `command` (list, optional): Override command e.g. `["/bin/sh", "-c", "echo hi"]`
- `network` (string, optional): Network name
- `privileged` (bool, optional): Run privileged. Default: `False`

**Returns:** `str` — container ID

```python
id = c.run(
    "ubuntu:24.04",
    name="app",
    ports=["8080:80"],
    env=["DEBUG=1"],
    volumes=["mydata:/data"],
)
```

### stop(name_or_id)

Stops a running container gracefully.

**Parameters:**

- `name_or_id` (string): Container name or ID

```python
c.stop("app")
```

### remove(name_or_id)

Removes a stopped container.

**Parameters:**

- `name_or_id` (string): Container name or ID

```python
c.remove("app")
```

### inspect(name_or_id)

Returns details about a container.

**Parameters:**

- `name_or_id` (string): Container name or ID

**Returns:** `dict` with keys:

- `id` (str): Container ID
- `name` (str): Container name
- `status` (str): Current status e.g. `"running"`, `"exited"`
- `image` (str): Image reference
- `running` (bool): `True` if the container is currently running

```python
info = c.inspect("app")
print(info["status"])
print(info["running"])
```

### list()

Lists all containers (running and stopped).

**Returns:** `list` of dicts, each with the same keys as `inspect()`

```python
for item in c.list():
    print(item["name"], item["status"])
```

### volume_create(name, **kwargs)

Creates a named volume.

**Parameters:**

- `name` (string): Volume name
- `size` (string, optional): Volume size e.g. `"20G"` or `"512M"`. Supported by Apple Containers only; silently ignored for Docker and Podman.

```python
c.volume_create("mydata")
c.volume_create("mydata", size="20G")
```

### volume_remove(name)

Removes a named volume.

**Parameters:**

- `name` (string): Volume name

```python
c.volume_remove("mydata")
```

### volume_list()

Lists all named volumes.

**Returns:** `list` of volume name strings

```python
for v in c.volume_list():
    print(v)
```

## Full Example

```python
import scriptling.container as container

c = container.Client("docker")

# Create a volume and run a one-shot ubuntu container
c.volume_create("demo-data")
c.image_pull("ubuntu:24.04")

id = c.run(
    "ubuntu:24.04",
    name="demo",
    volumes=["demo-data:/data"],
    env=["GREETING=hello"],
    command=["/bin/bash", "-c", "echo $GREETING > /data/out.txt"],
)

info = c.inspect("demo")
print(f"Status: {info['status']}")

# Execute a command in the running container
result = c.exec("demo", ["/bin/bash", "-c", "cat /data/out.txt"])
print(result["stdout"])

# Cleanup
c.stop("demo")
c.remove("demo")
c.volume_remove("demo-data")
c.image_remove("ubuntu:24.04")
```
