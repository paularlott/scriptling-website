---
title: Writing a Fetcher Plugin
description: Serve libraries, assets and script sources from a plugin-owned scheme such as demo://.
tags: [tutorials, plugins, go, fetchers]
weight: 28
---

This tutorial builds a fetcher plugin: a Go plugin that owns a URI scheme, so
`demo://` sources — libraries, static assets, whole scripts — resolve to it.
The same binary also registers a function and a class, because a fetcher is
just one more thing a plugin can serve. The complete, runnable version is
[examples/plugins/fetcher-go](https://github.com/paularlott/scriptling/tree/main/examples/plugins/fetcher-go)
in the repository; this page walks through it.

## What a Fetcher Serves

One `RegisterFetcher("demo", ...)` call is the whole contract. From it the
host knows:

- `demo://libs` is a library bundle with the standard layout: modules live
  under `lib/`, nested to any depth (`lib/blah/blah/__init__.py` imports as
  `blah.blah`).
- Every other file the fetcher serves is still there to read — markdown,
  JSON, images — reached from scripts through `scriptling.package` under the
  plugin's name.
- A bare `demo://name` source is a single script file, refetched on every run.

Nothing is transferred that nothing imports: the host asks for each file only
when an import or read actually touches it, and caches none of it.

## Create the Plugin

The plugin serves its files from a map, registers a function and a class over
the same map, and declares the scheme:

```go
package main

import (
    "context"
    "fmt"
    "path"
    "sort"
    "strings"

    "github.com/paularlott/scriptling/object"
    "github.com/paularlott/scriptling/plugin"
)

// The virtual package served at demo://libs: code under lib/, assets anywhere.
var files = map[string]string{
    "lib/greet.py":              "import hub\n\ndef greeting(name):\n    return hub.prefix() + \", \" + name\n",
    "lib/hub/__init__.py":       "def prefix():\n    return \"hello from demo://libs\"\n",
    "lib/fred/__init__.py":      "def value():\n    return \"fred, a one-level package\"\n",
    "lib/blah/__init__.py":      "label = \"blah\"\n",
    "lib/blah/blah/__init__.py": "def value():\n    return \"blah.blah, a two-level package\"\n",
    "docs/getting-started.md":   "# demo://libs\n\nServed on demand by the plugin.\n",
    "data/config.json":          "{\n  \"greeting\": \"hello from data/config.json\"\n}\n",
}

// Single-file script sources: fetching demo://scripts/hello returns the script.
var scripts = map[string]string{
    "demo://scripts/hello": "import greet\nimport sys\nprint(greet.greeting(sys.argv[1] if len(sys.argv) > 1 else \"World\"))\n",
}

type memoryFetcher struct{}

func (memoryFetcher) Read(ctx context.Context, source, path string) ([]byte, error) {
    if content, ok := scripts[source]; ok && path == "" {
        return []byte(content), nil
    }
    content, ok := files[path]
    if !ok {
        return nil, fmt.Errorf("%w: %s", plugin.ErrFetchNotFound, path)
    }
    return []byte(content), nil
}

func (memoryFetcher) Glob(ctx context.Context, source, pattern string) ([]plugin.FetchEntry, error) {
    // The tree the pattern matches against: every file plus every directory
    // leading to one.
    paths := map[string]bool{}
    for name := range files {
        paths[name] = false
        for dir := path.Dir(name); dir != "."; dir = path.Dir(dir) {
            paths[dir] = true
        }
    }
    entries := make([]plugin.FetchEntry, 0, len(paths))
    for name, isDir := range paths {
        if plugin.MatchGlob(pattern, name) {
            entries = append(entries, plugin.FetchEntry{Name: name, IsDir: isDir})
        }
    }
    sort.Slice(entries, func(i, j int) bool { return entries[i].Name < entries[j].Name })
    return entries, nil
}

func main() {
    server := plugin.NewServer("demo", "1.0.0", "Fetcher plugin serving demo:// sources")

    // A function, like any Go plugin: scripts call plugin.demo.asset(...).
    assetBuilder := object.NewFunctionBuilder()
    assetBuilder.Function(func(name string) (string, error) {
        content, ok := files[name]
        if !ok {
            return "", fmt.Errorf("no such file: %s", name)
        }
        return content, nil
    })
    server.RegisterFunc("asset", assetBuilder)

    // A class: plugin.demo.Doc(path) wraps a served document.
    docBuilder := object.NewClassBuilder("Doc").
        Method("__init__", func(self *object.Instance, p string) error {
            content, ok := files[p]
            if !ok {
                return fmt.Errorf("no such document: %s", p)
            }
            self.SetField("path", object.NewString(p))
            self.SetField("content", object.NewString(content))
            return nil
        }).
        Method("title", func(self *object.Instance) string {
            for _, line := range strings.Split(self.Field("content").(*object.String).StringValue(), "\n") {
                if trimmed := strings.TrimSpace(line); strings.HasPrefix(trimmed, "# ") {
                    return strings.TrimPrefix(trimmed, "# ")
                }
            }
            return ""
        })
    server.RegisterClass(docBuilder)

    // The fetcher: this plugin owns the demo scheme.
    server.RegisterFetcher("demo", memoryFetcher{})
    if err := server.Run(); err != nil {
        panic(err)
    }
}
```

`Read` returns bytes or an error wrapping `plugin.ErrFetchNotFound` for a
miss. `Glob` answers pattern matches in one round trip: existence is a
wildcard-free pattern, a listing is `<dir>/*`, a subtree is `<dir>/**`, and
`plugin.MatchGlob` implements the pattern language. Serving from disk?
`plugin.GlobDisk` implements `Glob` with the root containment built in.

## Build It

```bash
go build -o /tmp/scriptling-plugins/fetcher-go ./examples/plugins/fetcher-go
```

## Use It

The plugin's library attaches when it loads — no `--package` needed — and its
function and class import as `plugin.demo`:

```bash
scriptling --plugin /tmp/scriptling-plugins/fetcher-go \
           -c 'import greet; print(greet.greeting("Ada"))'
```

Namespaces nest to any depth, and assets read through `scriptling.package`
with the plugin's name as the package name:

```python
import fred
import blah.blah
import json
import plugin.demo
import scriptling.package as package

print(fred.value())          # fred, a one-level package
print(blah.blah.value())     # blah.blah, a two-level package

config = json.loads(package.read_file("demo", "data/config.json"))
print(config["greeting"])    # hello from data/config.json

print(plugin.demo.asset("docs/getting-started.md").splitlines()[0])
doc = plugin.demo.Doc("docs/configuration.md")
print(doc.title())           # Configuration

print(package.glob("demo", "**/*.md"))
```

Run a script the plugin itself serves (always refetched):

```bash
scriptling --plugin /tmp/scriptling-plugins/fetcher-go demo://scripts/hello Ada
```

## Embedding the Same Plugin

Applications that embed Scriptling get identical behaviour by bridging their
plugin manager into the scheme registry; the runnable host is
[examples/embed-fetcher-plugin](https://github.com/paularlott/scriptling/tree/main/examples/embed-fetcher-plugin),
and the wiring is documented under
[fetcher plugins in the plugin manager docs](/docs/plugins/host-integration/#fetcher-plugins).

## Where to Go Next

- [Plugin Fetchers](/docs/plugins/fetchers/) — the full serving contract,
  error typing, and caching rules.
- [Writing a Go Plugin](/docs/tutorials/go-plugin/) — functions and classes
  without the fetcher half.
- [JSON-RPC Protocol](/docs/plugins/protocol/) — `fetch.read` and
  `fetch.glob` on the wire.
