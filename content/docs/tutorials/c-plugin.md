---
title: Writing a C Plugin
description: Build a multi-threaded C plugin with functions, classes, properties, callbacks, and logging.
weight: 27
---

This tutorial builds a C executable plugin that exposes functions, classes with properties, callbacks, and logging. It uses the Scriptling C SDK: a single header and source file with no external dependencies.

## Prerequisites

- A C11 compiler (gcc, clang, or similar)
- The Scriptling binary installed and on your `PATH`
- The SDK files `scriptling_plugin.h` and `scriptling_plugin.c` from `examples/plugins/hello-c/` in the Scriptling source

## Project Setup

Create a directory for the plugin:

```bash
mkdir -p hello-plugin
cp scriptling_plugin.h scriptling_plugin.c hello-plugin/
cd hello-plugin
```

## Step 1: A Simple Function

Create `main.c` with a single function:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "scriptling_plugin.h"

static sl_value *greet(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    const char *name = (argc > 0) ? sl_as_string(args[0]) : "World";
    char buf[256];
    snprintf(buf, sizeof(buf), "Hello, %s", name);
    return sl_string(buf);
}

int main(void) {
    sl_server *srv = sl_server_new("hello", "1.0.0", "C hello plugin");
    sl_register_func(srv, "greet", greet);
    return sl_server_run(srv);
}
```

Build and test:

```bash
gcc -std=c11 -Wall -Wextra -O2 -o hello main.c scriptling_plugin.c -lm -lpthread
mkdir -p ./plugins && cp hello ./plugins/
scriptling --plugin-dir ./plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

Output:

```text
Hello, Ada
```

The plugin declares the short name `hello`. Scriptling imports it as `plugin.hello`.

## Step 2: Classes with Properties

Add a `Counter` class with a constructor, methods, and read/write properties:

```c
typedef struct {
    int64_t value;
} counter_data;

static void *counter_ctor(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    counter_data *d = calloc(1, sizeof(*d));
    d->value = (argc > 0) ? sl_as_int(args[0]) : 0;
    return d;
}

static void counter_dtor(void *data) {
    free(data);
}

static sl_value *counter_inc(void *data, int argc, sl_value **args, void *ctx) {
    (void)ctx;
    counter_data *d = data;
    int64_t amount = (argc > 0) ? sl_as_int(args[0]) : 1;
    d->value += amount;
    return sl_int(d->value);
}

static sl_value *counter_value_get(void *data, void *ctx) {
    (void)ctx;
    counter_data *d = data;
    return sl_int(d->value);
}

static void counter_value_set(void *data, sl_value *value, void *ctx) {
    (void)ctx;
    counter_data *d = data;
    d->value = sl_as_int(value);
}

static sl_value *counter_label_get(void *data, void *ctx) {
    (void)ctx;
    counter_data *d = data;
    char buf[64];
    snprintf(buf, sizeof(buf), "counter:%lld", (long long)d->value);
    return sl_string(buf);
}
```

Register the class in `main()`:

```c
sl_class *ctr = sl_class_new("Counter");
sl_class_set_constructor(ctr, counter_ctor);
sl_class_set_destructor(ctr, counter_dtor);
sl_class_add_method(ctr, "inc", counter_inc);
sl_class_add_property(ctr, "value", counter_value_get, counter_value_set);
sl_class_add_property(ctr, "label", counter_label_get, NULL);
sl_register_class(srv, ctr);
```

Test:

```bash
scriptling --plugin-dir ./plugins -c '
import plugin.hello
c = plugin.hello.Counter(10)
print(c.value)
print(c.inc(5))
print(c.value)
c.value = 100
print(c.label)
'
```

Output:

```text
10
15
15
counter:100
```

The constructor returns a heap-allocated struct. The SDK passes it as the `void *data` first argument to every method and property callback. The destructor frees it when the instance is released or garbage-collected.

## Step 3: Callbacks

A function can receive a Scriptling callback and invoke it from C:

```c
static sl_value *stream(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    if (argc == 0 || !args[0] || args[0]->type != SL_CALLBACK) {
        return sl_string("error: expected a callback argument");
    }

    const char *tokens[] = {"Hello", ", ", "Ada"};
    for (int i = 0; i < 3; i++) {
        sl_value *items[2] = { sl_string(tokens[i]), sl_int(i) };
        const char *keys[2] = { "token", "index" };
        sl_value *event = sl_dict(keys, items, 2);

        char *err = NULL;
        sl_value *r = sl_callback_call(args[0], 1, &event, &err);
        sl_value_free(event);
        if (err) {
            sl_value *err_v = sl_string(err);
            free(err);
            return err_v;
        }
        sl_value_free(r);
    }

    return sl_string("Hello, Ada");
}
```

Test:

```bash
scriptling --plugin-dir ./plugins -c '
import plugin.hello
events = []
result = plugin.hello.stream(lambda e: events.append(e))
print(result)
for e in events:
    print(e["token"], e["index"])
'
```

Output:

```text
Hello, Ada
Hello 0
,  1
Ada 2
```

Callbacks are only valid while the outer function call is still running.

## Step 4: Logging

Use `sl_log_info`, `sl_log_debug`, `sl_log_warn`, and `sl_log_error` to route messages through the host logger:

```c
static sl_value *work(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    const char *name = (argc > 0) ? sl_as_string(args[0]) : "anonymous";
    sl_log_info("work started for %s", name);
    sl_log_debug("args received: %d", argc);
    char buf[256];
    snprintf(buf, sizeof(buf), "done:%s", name);
    return sl_string(buf);
}
```

Test with debug logging enabled:

```bash
scriptling --plugin-dir ./plugins --log-level debug -c '
import plugin.hello
print(plugin.hello.work("Ada"))
'
```

Output:

```text
INF work started for Ada
DBG args received: 1
done:Ada
```

## Step 5: Constants

Register constant values that appear as module attributes:

```c
sl_constant(srv, "default_name", sl_string("World"));
```

```python
print(plugin.hello.default_name)   # "World"
```

## Full Example

The complete `main.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "scriptling_plugin.h"

static sl_value *greet(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    const char *name = (argc > 0) ? sl_as_string(args[0]) : "World";
    char buf[256];
    snprintf(buf, sizeof(buf), "Hello, %s", name);
    return sl_string(buf);
}

static sl_value *work(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    const char *name = (argc > 0) ? sl_as_string(args[0]) : "anonymous";
    sl_log_info("work started for %s", name);
    char buf[256];
    snprintf(buf, sizeof(buf), "done:%s", name);
    return sl_string(buf);
}

typedef struct {
    int64_t value;
} counter_data;

static void *counter_ctor(int argc, sl_value **args, void *ctx) {
    (void)ctx;
    counter_data *d = calloc(1, sizeof(*d));
    d->value = (argc > 0) ? sl_as_int(args[0]) : 0;
    return d;
}

static void counter_dtor(void *data) { free(data); }

static sl_value *counter_inc(void *data, int argc, sl_value **args, void *ctx) {
    (void)ctx;
    counter_data *d = data;
    int64_t amount = (argc > 0) ? sl_as_int(args[0]) : 1;
    d->value += amount;
    return sl_int(d->value);
}

static sl_value *counter_value_get(void *data, void *ctx) {
    (void)ctx;
    return sl_int(((counter_data *)data)->value);
}

static void counter_value_set(void *data, sl_value *value, void *ctx) {
    (void)ctx;
    ((counter_data *)data)->value = sl_as_int(value);
}

static sl_value *counter_label_get(void *data, void *ctx) {
    (void)ctx;
    char buf[64];
    snprintf(buf, sizeof(buf), "counter:%lld", (long long)((counter_data *)data)->value);
    return sl_string(buf);
}

int main(void) {
    sl_server *srv = sl_server_new("hello", "1.0.0", "C hello plugin");

    sl_register_func(srv, "greet", greet);
    sl_register_func(srv, "work", work);

    sl_class *ctr = sl_class_new("Counter");
    sl_class_set_constructor(ctr, counter_ctor);
    sl_class_set_destructor(ctr, counter_dtor);
    sl_class_add_method(ctr, "inc", counter_inc);
    sl_class_add_property(ctr, "value", counter_value_get, counter_value_set);
    sl_class_add_property(ctr, "label", counter_label_get, NULL);
    sl_register_class(srv, ctr);

    sl_constant(srv, "default_name", sl_string("World"));

    return sl_server_run(srv);
}
```

## Build and Deploy

```bash
gcc -std=c11 -Wall -Wextra -O2 -o hello main.c scriptling_plugin.c -lm -lpthread
cp hello ./plugins/
scriptling --plugin-dir ./plugins script.py
```

## What's Next

- [C Plugins](/docs/plugins/c-plugins/): full API reference for the C SDK
- [JSON-RPC Protocol](/docs/plugins/protocol/): wire format details
- [Go Plugins](/docs/plugins/go-plugins/): the Go plugin server for comparison
