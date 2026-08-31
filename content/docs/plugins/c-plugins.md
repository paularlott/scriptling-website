---
title: C Plugins
description: Build Scriptling plugins in C using the single-header SDK.
tags: [plugins, c, json-rpc]
weight: 4
---

A C plugin is a standalone executable that links against a single-header, single-source SDK and speaks Scriptling's JSON-RPC protocol over stdio. Each incoming request runs in its own thread, matching the concurrency model of the Go plugin server.

## Quick Start

```c
// hello.c
#include "scriptling_plugin.h"

static sl_value *greet(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    const char *name = (argc > 0) ? sl_as_string(args[0]) : "World";
    char buf[256];
    snprintf(buf, sizeof(buf), "Hello, %s", name);
    return sl_string(buf);
}

int main(void) {
    sl_server *srv = sl_server_new("hello", "1.0.0", "My first plugin");
    sl_register_func(srv, "greet", greet);
    return sl_server_run(srv);
}
```

Build and run:

```bash
gcc -std=c11 -O2 -o hello hello.c scriptling_plugin.c -lm -lpthread
mkdir -p ./plugins && cp hello ./plugins/
scriptling --plugin-dir ./plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

## Getting the SDK

Copy two files into your project:

| File | Purpose |
| --- | --- |
| `scriptling_plugin.h` | Public API: types, constructors, registration functions |
| `scriptling_plugin.c` | Implementation: JSON parser, transport, object store, threading |

Both files are in the Scriptling source under `examples/plugins/hello-c/`.

No external dependencies beyond the C standard library and pthreads.

## Values

Scriptling values are `sl_value` tagged unions. Create them with the constructor functions: ownership transfers to the caller:

| Constructor | Scriptling type |
| --- | --- |
| `sl_null()` | `null` |
| `sl_bool(bool)` | `bool` |
| `sl_int(int64_t)` | `int` |
| `sl_float(double)` | `float` |
| `sl_string(const char *)` | `string` |
| `sl_list(items, count)` | `list` |
| `sl_dict(keys, vals, count)` | `dict` |
| `sl_callback(const char *id)` | callback handle |

Accessor helpers (return defaults on type mismatch):

```c
sl_as_bool(v)       // → bool (also converts int)
sl_as_int(v)        // → int64_t (also converts float, bool)
sl_as_float(v)      // → double (also converts int)
sl_as_string(v)     // → const char* (returns "" on mismatch)
sl_list_get(v, idx) // → sl_value* (NULL on out of range)
sl_dict_get(v, key) // → sl_value* (NULL if not found)
```

Free values with `sl_value_free(v)`.

## Server Lifecycle

```c
sl_server *srv = sl_server_new(name, version, description);
// ... register functions, classes, constants ...
int rc = sl_server_run(srv);     // blocks until shutdown
sl_server_free(srv);
```

`sl_server_set_context(srv, ptr)` stores a user pointer passed as the last argument to every handler.

## Functions

```c
sl_value *handler(int argc, sl_value **args, void *ctx) {
    // return an sl_value, or NULL for null
}

sl_register_func(srv, "name", handler);
sl_register_func_help(srv, "name", handler, "name(x) - description");
```

## Classes

```c
// Constructor: returns heap-allocated instance data.
void *my_ctor(int argc, sl_value **args, void *ctx);

// Destructor: frees instance data.
void  my_dtor(void *data);

// Method: receives instance data pointer.
sl_value *my_method(void *data, int argc, sl_value **args, void *ctx);

// Property getter / setter
sl_value *my_prop_get(void *data, void *ctx);
void      my_prop_set(void *data, sl_value *value, void *ctx);

sl_class *cls = sl_class_new("MyClass");
sl_class_set_constructor(cls, my_ctor);
sl_class_set_destructor(cls, my_dtor);
sl_class_add_method(cls, "do_thing", my_method);
sl_class_add_property(cls, "name", my_prop_get, NULL);           // read-only
sl_class_add_property(cls, "value", my_prop_get, my_prop_set);   // read/write
sl_register_class(srv, cls);
```

Properties are accessed as attributes from Scriptling:

```python
c = plugin.mylib.MyClass(10)
c.value = c.value + 5
print(c.name)
```

## Constants

```c
sl_constant(srv, "pi", sl_float(3.14159));
sl_constant(srv, "default_name", sl_string("World"));
```

## Callbacks

When Scriptling passes a function as an argument, the SDK represents it as an `sl_value` with `type == SL_CALLBACK`. Invoke it with `sl_callback_call()`:

```c
static sl_value *stream(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    if (argc < 1 || args[0]->type != SL_CALLBACK)
        return sl_string("expected a callback");

    for (int i = 0; i < 3; i++) {
        sl_value *event = sl_int(i);
        char *err = NULL;
        sl_value *result = sl_callback_call(args[0], 1, &event, &err);
        sl_value_free(event);
        if (err) {
            sl_value *err_v = sl_string(err);
            free(err);
            return err_v;
        }
        sl_value_free(result);
    }
    return sl_string("done");
}
```

Call from Scriptling:

```python
import plugin.hello
events = []
result = plugin.hello.stream(lambda e: events.append(e))
```

## Logging

```c
sl_log_info("processing item %d", item_id);
sl_log_warn("low memory: %zu bytes", remaining);
sl_log_error("failed: %s", errmsg);
```

Logs are forwarded through the host's logger. Available levels: `sl_log_trace`, `sl_log_debug`, `sl_log_info`, `sl_log_warn`, `sl_log_error`.

## Custom Wrappers

Replace the auto-generated proxy with custom Scriptling source:

```c
sl_register_func(srv, "greet", greet_handler);
sl_wrapper(srv, "greet",
    "import scriptling.plugin\n"
    "def greet(name):\n"
    "    return scriptling.plugin.call_function(\"plugin.mylib\", \"greet\", name) + \"!\"\n"
);
```

See [Client Wrappers](../go-plugins/client-wrappers/) for details on wrapper source conventions.

## Fetchers

Serve `scheme://` package and script sources on demand. Register a scheme
with a read handler and a list handler before `sl_server_run()`:

```c
static sl_fetch_result *my_read(const char *source, const char *path, void *ctx) {
    /* path == "" means the source itself is a single script file. */
    return sl_fetch_data("# content\n", 10);  /* copies the bytes; host does not cache */
}

static sl_fetch_entry *my_glob(const char *source, const char *path,
                               size_t *count, void *ctx) {
    /* names must stay valid until the handler returns; the SDK frees only
       the array itself. */
    static sl_fetch_entry entries[] = { { "lib", true } };
    sl_fetch_entry *out = malloc(sizeof(entries));
    memcpy(out, entries, sizeof(entries));
    *count = 2;
    return out;
}

sl_register_fetcher(srv, "mylib", my_read, my_glob);
```

Read handler results:

- `sl_fetch_data(ptr, len)`: the file's content (the bytes are copied).
- `sl_fetch_not_found()`: a miss, reported to the host as JSON-RPC code
  `-32001` so a failed module probe is not an error.

The host attaches the plugin's library automatically (the standard `lib/`
layout is synthesized host-side) and asks for individual files as imports
resolve; there is no manifest to serve. It keeps none of them, so every read
reaches your `Read` handler; cache inside the handler if your backend needs
it. The `hello-c` example implements a complete `cdemo://` fetcher. See
[Plugin Fetchers](/docs/plugins/fetchers/) for the host-side behavior.

## Compilation

```bash
gcc -std=c11 -Wall -Wextra -O2 -o myplugin main.c scriptling_plugin.c -lm -lpthread
```

Requires a C11 compiler and pthreads.

## File Layout

```
your-plugin/
  scriptling_plugin.h  : public header
  scriptling_plugin.c  : implementation
  main.c               : your plugin
  Makefile
```

## Thread Safety

Each incoming request is handled in its own pthread. The object store uses a read-write lock for the instance array and a per-object mutex for method serialization. Stdout writes are mutex-protected. The SDK manages all synchronization internally: handler functions do not need their own locking unless they access shared global state outside the object store.

See [JSON-RPC Protocol](../protocol/) for the complete wire format reference.
