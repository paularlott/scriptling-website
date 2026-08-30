---
title: GC Release Hooks
description: Best-effort cleanup hooks for Go-owned Scriptling objects.
tags: [go-integration, embedding, go]
weight: 18
---

Scriptling exposes a small Go utility for attaching best-effort release hooks to heap objects:

```go
target := &MyResource{}

err := object.SetGCReleaseHook(target, func() {
    cleanupRemoteResource()
})
if err != nil {
    return err
}
```

Use `object.ClearGCReleaseHook(target)` when the resource has already been released explicitly:

```go
releaseRemoteResource()
_ = object.ClearGCReleaseHook(target)
```

## Intended Use

GC release hooks are useful when a Go object owns a secondary resource and should send a cleanup signal if user code drops the object without calling an explicit release method.

Scriptling uses `runtime.SetFinalizer` in two places:

- **All classes with `__del__`** (including pure Scriptling classes, Go builder classes, and plugin proxy objects): when an instance becomes unreachable, the finalizer calls `__del__` on it.
- **Plugin proxy objects**: the finalizer also sends `object.destroy` to the plugin server, which calls the server-side `__del__` to free plugin resources.

## Limits

Go finalizers are not deterministic:

- They are not guaranteed to run promptly.
- They may not run before process exit.
- They must not be the only cleanup path for important resources.
- The hook must not capture the target object, or the object will remain reachable.
- The hook should avoid blocking work directly. Queue cleanup work elsewhere when cleanup may need IO, locks, or RPC.

Prefer explicit cleanup first, and use GC release hooks as a fallback.
