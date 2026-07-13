---
title: scriptling.nomad
linkTitle: nomad
description: HashiCorp Nomad client covering CSI volumes and jobs.
weight: 1
---

The `scriptling.nomad` library provides a client for the HashiCorp Nomad HTTP API, covering CSI storage volumes and jobs. All operations go through a `NomadClient` obtained from `Client()`.

## Available Functions

| Function | Description |
|----------|-------------|
| `Client(addr, **kwargs)` | Create a Nomad client |

`Client()` returns a `NomadClient` with the following methods:

| Method | Description |
|--------|-------------|
| `csi_volumes_list(**kwargs)` | List CSI volumes |
| `csi_volume_get(id, **kwargs)` | Get details for a CSI volume |
| `csi_volume_register(id, volume, **kwargs)` | Register (create) a CSI volume |
| `csi_volume_deregister(id, **kwargs)` | Deregister (delete) a CSI volume |
| `jobs_list(**kwargs)` | List jobs |
| `job_get(id, **kwargs)` | Get the full specification and status for a job |
| `job_register(job)` | Register (create or update) a job |
| `job_stop(id, **kwargs)` | Stop a job |
| `wait_job_stopped(id, **kwargs)` | Wait for a job to reach the "dead" status |
| `job_validate(job)` | Validate a job specification without submitting it |
| `job_plan(id, job, **kwargs)` | Dry-run a job registration and return the scheduler plan |
| `jobs_parse(hcl, **kwargs)` | Convert an HCL job specification into Nomad's JSON job format |

## Functions

### `Client(addr, token="", insecure=False, timeout=10)`

Creates a `NomadClient` bound to a Nomad HTTP API endpoint.

**Parameters:**
- `addr` (`str`): Nomad HTTP API address, e.g. `"http://127.0.0.1:4646"`.
- `token` (`str`, optional): ACL token, sent as the `X-Nomad-Token` header on every request. Default: `""`.
- `insecure` (`bool`, optional): Skip TLS certificate verification. Default: `False`.
- `timeout` (`float`, optional): Per-request HTTP timeout in seconds. Default: `10`.

**Returns:** `NomadClient`: a client bound to the given address.

```python
import scriptling.nomad as nomad

c = nomad.Client("https://nomad.example.com:4646", token="secret")
c = nomad.Client("https://nomad.example.com:4646", token="secret", timeout=5)
```

### `NomadClient.csi_volumes_list(namespace="*", plugin_id="")`

Lists CSI volumes.

**Parameters:**
- `namespace` (`str`, optional): Namespace to list, `"*"` for all namespaces. Default: `"*"`.
- `plugin_id` (`str`, optional): Filter by CSI plugin ID. Default: `""`: no filter.

**Returns:** `list` of `dict`, each with keys:
- `id` (`str`): Volume ID.
- `name` (`str`): Volume name.
- `namespace` (`str`): Namespace.
- `plugin_id` (`str`): CSI plugin ID.
- `provider` (`str`): CSI provider name.
- `schedulable` (`bool`): Whether the volume can currently be scheduled.
- `controllers_healthy` (`int`): Number of healthy controller plugins.
- `nodes_healthy` (`int`): Number of healthy node plugins.

```python
for v in c.csi_volumes_list(plugin_id="ceph-csi"):
    if v["id"].startswith("qaannon") or v["id"].startswith("qaprod"):
        print(v["id"])
```

### `NomadClient.csi_volume_get(id, namespace="")`

Returns full details for a single CSI volume.

**Parameters:**
- `id` (`str`): Volume ID.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.

**Returns:** `dict`: the full volume specification and status, as returned by the Nomad API.

```python
vol = c.csi_volume_get("qaprod-data-01")
print(vol["Provider"])
```

### `NomadClient.csi_volume_register(id, volume, namespace="")`

Registers (creates) a CSI volume.

**Parameters:**
- `id` (`str`): Volume ID.
- `volume` (`dict`): Volume specification in Nomad's CSI volume JSON format.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.

**Returns:** `None`

```python
c.csi_volume_register("qaprod-data-01", {
    "Name": "qaprod-data-01",
    "PluginID": "ceph-csi",
    "Capacity": 10 * 1024 * 1024 * 1024,
    "AccessMode": "single-node-writer",
    "AttachmentMode": "file-system",
})
```

### `NomadClient.csi_volume_deregister(id, namespace="", force=False)`

Deregisters (deletes) a CSI volume.

**Parameters:**
- `id` (`str`): Volume ID.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.
- `force` (`bool`, optional): Force detach any remaining claims first. Default: `False`.

**Returns:** `None`

```python
c.csi_volume_deregister("qaprod-orphaned-01", force=True)
```

### `NomadClient.jobs_list(namespace="*", prefix="")`

Lists jobs.

**Parameters:**
- `namespace` (`str`, optional): Namespace to list, `"*"` for all namespaces. Default: `"*"`.
- `prefix` (`str`, optional): Filter by job ID prefix. Default: `""`: no filter.

**Returns:** `list` of `dict`, each with keys:
- `id` (`str`): Job ID.
- `name` (`str`): Job name.
- `namespace` (`str`): Namespace.
- `type` (`str`): Job type, e.g. `"service"`, `"batch"`, `"system"`.
- `status` (`str`): Current status, e.g. `"running"`, `"pending"`, `"dead"`.
- `priority` (`int`): Job priority.

```python
for j in c.jobs_list(prefix="qaannon"):
    print(j["id"], j["status"])
```

### `NomadClient.job_get(id, namespace="")`

Returns the full specification and status for a job.

**Parameters:**
- `id` (`str`): Job ID.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.

**Returns:** `dict`: job specification and status, as returned by the Nomad API.

```python
job = c.job_get("qaprod-api")
print(job["Status"])
```

### `NomadClient.job_register(job)`

Registers (creates or updates) a job.

**Parameters:**
- `job` (`dict`): Job specification in Nomad's JSON job format, e.g. from `jobs_parse()` or `job_get()["Job"]`.

**Returns:** `dict` with keys:
- `EvalID` (`str`): Evaluation ID created for this registration.
- `EvalCreateIndex` (`int`)
- `JobModifyIndex` (`int`)
- `Warnings` (`str`)

```python
parsed = c.jobs_parse(hcl_text)
result = c.job_register(parsed)
print(result["EvalID"])
```

### `NomadClient.job_stop(id, namespace="", purge=False)`

Stops a job.

**Parameters:**
- `id` (`str`): Job ID.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.
- `purge` (`bool`, optional): Fully remove the job from Nomad's state instead of leaving it stopped. Default: `False`.

**Returns:** `dict` with keys `EvalID` (`str`), `EvalCreateIndex` (`int`), `JobModifyIndex` (`int`).

```python
c.job_stop("qaprod-old-job", purge=True)
```

### `NomadClient.wait_job_stopped(id, namespace="", timeout=30)`

Polls a job's status until it reaches `"dead"`, or the timeout elapses.

**Parameters:**
- `id` (`str`): Job ID.
- `namespace` (`str`, optional): Namespace. Default: `""`: Nomad's default namespace.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.

**Returns:** `bool`: `True` if the job is stopped, `False` if the timeout was reached.

```python
c.job_stop("qaprod-old-job")
if not c.wait_job_stopped("qaprod-old-job", timeout=60):
    print("job did not stop in time")
```

### `NomadClient.job_validate(job)`

Validates a job specification without submitting it.

**Parameters:**
- `job` (`dict`): Job specification in Nomad's JSON job format.

**Returns:** `dict` with keys `DriverConfigValidated` (`bool`), `ValidationErrors` (`list`), `Warnings` (`str`).

```python
result = c.job_validate(parsed_job)
if result["ValidationErrors"]:
    print(result["ValidationErrors"])
```

### `NomadClient.job_plan(id, job, diff=False)`

Dry-runs a job registration and returns the resulting scheduler plan, without actually registering the job.

**Parameters:**
- `id` (`str`): Job ID.
- `job` (`dict`): Job specification in Nomad's JSON job format.
- `diff` (`bool`, optional): Include a diff against the current job version. Default: `False`.

**Returns:** `dict`: plan result, including keys such as `JobModifyIndex` (`int`), `Annotations` (`dict`), `FailedTGAllocs` (`dict`).

```python
plan = c.job_plan("qaprod-api", parsed_job, diff=True)
```

### `NomadClient.jobs_parse(hcl, canonicalize=False)`

Converts an HCL job specification into Nomad's JSON job format, so it can be passed to `job_register()`, `job_validate()`, or `job_plan()`.

**Parameters:**
- `hcl` (`str`): Job specification in HCL format.
- `canonicalize` (`bool`, optional): Fill in default values for optional fields. Default: `False`.

**Returns:** `dict`: job specification in Nomad's JSON job format.

```python
parsed = c.jobs_parse(open("job.nomad.hcl").read())
c.job_register(parsed)
```

## Full Example

Reconcile CSI volumes against a source-of-truth list, deregistering anything Nomad has that shouldn't exist:

```python
import scriptling.nomad as nomad

c = nomad.Client("https://nomad.example.com:4646", token="secret")

expected = set(open("expected_volumes.txt").read().split())

for v in c.csi_volumes_list(namespace="*"):
    vid = v["id"]
    if not (vid.startswith("qaannon") or vid.startswith("qaprod")):
        continue
    if vid in expected:
        continue
    print(f"Removing orphaned volume: {vid}")
    c.csi_volume_deregister(vid, force=True)
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.nomad` grants full control over the Nomad cluster reachable at the address and ACL token passed to `Client()`, including deregistering CSI volumes and stopping or registering jobs: this is a significant risk, comparable to direct infrastructure access. There is no allowlist parameter for this library; scope the ACL token to the minimum policy needed for the task, and never register this library for untrusted code. For a full risk breakdown across all libraries, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.container](../container/) - Container lifecycle management for Docker, Podman, and Apple Containers
- [Library Registration](/docs/go-integration/library-registration/) - Registering extended libraries when embedding in Go
- [Security Guide](/docs/security/) - Security guidance for host-provided libraries
