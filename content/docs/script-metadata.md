---
title: Script Metadata
description: Declare script requirements — scriptling version, libraries, plugins — in an inline metadata block.
tags: [docs, metadata, requirements]
weight: 4
---

A script can declare what it needs to run — a minimum scriptling version, the libraries it imports, the plugins it expects to be connected — in a TOML block carried in comments before its first statement. The CLI checks the block before the script executes, so a missing requirement is a clear error instead of an import failure three layers in. The format follows the shape of [PEP 723](https://peps.python.org/pep-0723/) (inline script metadata) with scriptling's own keys.

```python
# /// script
# requires-scriptling = ">=0.24"
#
# dependencies = [
#   "requests",
#   "scriptling.sql via sql >= 0.23",
# ]
#
# plugins = [
#   "knot >= 1.2.3",
# ]
# ///

import requests
import scriptling.sql as sql
```

A script without a block runs exactly as before; the block is opt-in.

## Keys

| Key | Meaning |
|-----|---------|
| `requires-scriptling` | Version constraint matched against the running scriptling version, e.g. `">=0.24"`. Operators: `>=`, `<=`, `>`, `<`, `==`, `!=`. |
| `dependencies` | Libraries the script imports. Each entry is a library name, optionally followed by `via` and the plugin that provides it — `"scriptling.sql via sql >= 0.23"` — using the same optional version constraint as the `plugins` list. |
| `plugins` | External plugin processes that must be loaded, each `"name"` with an optional version constraint: `"knot >= 1.2.3"`. Constraints are matched against the version each plugin declared in its handshake. |
| `[tool.<name>]` | Reserved for tool and host configuration. Scriptling ignores the contents; the parsed tables are surfaced to embedding hosts (see [Tool tables](#tool-tables)). |

Unknown keys — outside the reserved `[tool.*]` tables — are errors, not warnings: a typo like `dependencys` should fail loudly. Versions and constraints are dotted numeric (`0.24`, `1.2.3`).

## Tool tables

Tables under `[tool.<name>]` are yours: scriptling never interprets their contents and the CLI never checks them — they exist so a script can carry configuration for the tool or host that runs it. An embedding host reads them from `Metadata.Tools` after parsing:

```python
# /// script
# requires-scriptling = ">=0.24"
#
# [tool.knot]
# version = "1.0.0"
#
# [[tool.knot.menus]]
# label = "Metrics"
# url = "https://grafana.internal"
# ///
```

Any shape inside `[tool.*]` is accepted — scalars, nested tables, arrays of tables — and unknown keys are not errors there, unlike the block's own keys. A host that gives the tables meaning defines their schema and validates it itself; see [Checking Script Requirements](/docs/go-integration/script-metadata/) for the embedding side.

**Plugin names** match the name a plugin declared in its handshake, and a bare name additionally matches the same name under scriptling's host-owned namespaces: `sql` finds the first-party plugin that declares `scriptling.sql`, and `hello` finds a plugin that declared the bare name `hello` (registered as `plugin.hello`). `knot` matches only `knot` — bare names never match third-party dotted namespaces like `knot.space`. The first-party database plugins declare scriptling's build version, so a constraint like `sql >= 0.23.0` pins the scriptling release the plugin was built with.

## Dependencies or plugins?

The distinction is where the library can come from:

| Declaration | Satisfied by | Missing error says |
|---|---|---|
| `"requests"` | Any provider: built-in, registered library, package module | library is not available |
| `"scriptling.sql via sql"` | The library resolving — compiled into the default build, or the sql plugin loaded | load the plugin, or use a build with it compiled in |
| `"knot >= 1.2.3"` (in `plugins`) | The knot plugin process, at that version | plugin not loaded, or version too old |

Rules of thumb: **if it can be compiled in, declare it as a dependency** and name its plugin — the entry passes on the default build without the plugin, and on `scriptling-slim` with the plugin loaded. **If it only exists as a connected plugin, declare it in `plugins`** — that is also where version constraints matter, because a plugin like knot versions independently, while the database plugins version with scriptling itself (pin them with `requires-scriptling`).

The `via` clause takes the plugin name with an optional constraint, exactly like a `plugins` entry: `"knot.space via knot >= 1.2"`. One nuance: when the library resolves, the `via` clause is never consulted — the constraint only bites when the plugin is loaded but the library still did not resolve.

## How checking works

Dependencies are checked first, by resolution — can this environment actually import the name, taking into account registered libraries, built-in modules, and `--package` bundles? A dependency that resolves is satisfied however the environment provides it. Only an unresolved dependency promotes its declared plugin into the required set; plugins declared directly are always required. One aggregated error then reports everything at once:

```text
Error: script requirements not met:
  - this script needs scriptling >=0.24, but this host is 0.23.1
  - required library "requests" is not available in this environment
  - required plugin "knot" is not loaded
load plugins with --plugin <path>, --plugin-dir, or SCRIPTLING_PLUGIN_DIR
```

`--lint` validates the block itself — malformed TOML, unknown keys, bad constraints — with file and line, without checking requirements, which depend on the environment rather than the source.

## Rules

- At most one block per script, located before the first statement.
- Every line inside the block is a comment; the block must be closed with `# ///` before any code.
- A malformed block is a hard error: a script that tried to declare requirements never runs as if it had none.
- Blocks are checked wherever a named script runs: one-shot script files, fetched `scheme://` scripts, `--code`, server setup scripts (HTTP, JSON-RPC, and MCP stdio — verified once at startup, before anything binds), and package main entries — a `.py` entry directly, a `module.function` entry through the module's source. Interactive stdin has no check.
- Imported modules, webroot and route handler scripts, and MCP tool handler scripts are not checked: the script you name is the unit of requirements.

## Embedding hosts

The check lives in the embeddable `metadata` package; the CLI is just one consumer. Hosts embedding scriptling parse the script source and verify against their own environment — the full guide, including what to pass as the host version and how to feed the resolver from your loaders, is [Checking Script Requirements](/docs/go-integration/script-metadata/). The shape of it:

```go
	m, ok, err := metadata.Parse(source)
	if err != nil {
		return err // malformed block
	}
	if ok {
		err = m.Verify(metadata.Env{
			HostVersion: appVersion, // the host's version, not scriptling's
			Resolves:    func(name string) bool { return interp.HasLibrary(name) },
			PluginVersion: func(name string) (string, bool) {
				for _, md := range manager.List() {
					if md.Name == name {
						return md.Version, true
					}
				}
				return "", false
			},
		})
	}
```

`Verify` returns one aggregated error (`*metadata.CheckError`) whose failures carry kinds — version, library, plugin — so a host can attach its own remedy hints, the way the CLI appends how to load plugins.
