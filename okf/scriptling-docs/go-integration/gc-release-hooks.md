---
description: Best-effort cleanup hooks for Go-owned Scriptling objects.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/go-integration/gc-release-hooks/
sources:
    - resource: https://scriptling.dev/docs/go-integration/gc-release-hooks/
status: stable
tags:
    - go-integration
    - embedding
    - go
title: GC Release Hooks
type: Guide
---
# GC Release Hooks

## Resources a Script Opens

A library that opens something for a script, a client, a connection, a child process or a file handle, registers it with `evaluator.TrackResource` so it does not outlive the script's use of it. The interpreter running the script then closes it on `Reset()`, `ResetEnv()` and `Close()`, and once the object the script holds is garbage collected:

```go
func connect(ctx context.Context, url string) object.Object {
    conn := dial(url)
    inst := object.NewInstanceWithData(connClass, nil, conn)
    conn.release = evaluator.TrackResource(ctx, inst, conn.Close)
    return inst
}

// close() from the script: forget it, then close it.
func (c *Conn) Close() {
    c.once.Do(func() {
        c.release()
        c.raw.Close()
    })
}
```

`close` must be safe to call more than once and from any goroutine, and neither it nor `release` may hold on to the object the script holds (`inst`), or that object could never be collected. Pass a `nil` owner to have only the interpreter close it.

## GC Release Hooks

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
- A script-defined `__del__` collected by the finalizer runs with a five-second budget (past it the destructor is abandoned), under the environment's interpreter lock (serialized against concurrent evaluation in that environment), and inside a panic boundary that contains failures without crashing the host.

Prefer explicit cleanup first, and use GC release hooks as a fallback.
