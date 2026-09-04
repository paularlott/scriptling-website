---
title: Checking Script Requirements
description: Verify a script's inline metadata block — version, libraries, plugins — before running it in an embedded host.
tags: [go-integration, embedding, metadata]
weight: 14
---

Scripts can declare their requirements in an inline metadata block (`# /// script`): a minimum interpreter version, the libraries they import, and the plugins they expect to be connected. The format is documented in [Script Metadata](/docs/script-metadata/). The CLI checks it automatically before running a script; an embedding host gets the same guarantee from the `metadata` package — parse the block, verify it against the environment the host actually provides, and refuse to run anything unmet.

## The flow

Check after the interpreter is fully wired (libraries registered, loaders set, plugins loaded) and before the first `Eval` — the same position the CLI checks from. A plugin that is loaded has already registered its library, so a resolved dependency never demands the plugin process:

```go
m, ok, err := metadata.Parse(source)
if err != nil {
	return fmt.Errorf("malformed metadata block: %w", err) // a broken block never runs as if it had none
}
if ok {
	if err := m.Verify(metadata.Env{
		HostVersion:   hostVersion,
		Resolves:      resolves,
		PluginVersion: pluginVersion,
	}); err != nil {
		return err // requirements not met — refuse to run
	}
}
_, err = p.Eval(source)
```

`Parse` reports `ok=false` for sources without a block, which run exactly as before.

## Wiring the environment

`Env` is everything `Verify` knows about the host, so the answers reflect what a script could really import.

**HostVersion** is the host application's version, not scriptling's build version. From a script's perspective the host is the interpreter it depends on — a script written against your app's 1.4 API should declare `requires-scriptling = ">=1.4"` and be checked against `1.4.x`. Pass scriptling's `build.Version` only if the host is plain scriptling, as the CLI does.

**Resolves** should mirror what `import` would do: registered libraries first, then whatever loaders the host wired:

```go
resolves := func(name string) bool {
	if p.HasLibrary(name) {
		return true
	}
	if loader != nil {
		_, found, err := loader.Load(name)
		return err == nil && found
	}
	return false
}
```

**PluginVersion** answers "is this plugin loaded, at what version" from the plugin manager:

```go
pluginVersion := func(name string) (string, bool) {
	for _, md := range manager.List() {
		if md.Name == name {
			return md.Version, true
		}
	}
	return "", false
}
```

A nil `PluginVersion` (or one that always reports not-loaded) simply means every `plugins` entry and every unresolved `via` clause fails as "not loaded" — correct for hosts that embed no plugins.

## Reading host configuration from `[tool.*]`

The block can also carry your own tables. Scriptling ignores their contents, but `Parse` surfaces them: `Metadata.Tools` maps each `[tool.<name>]` table to its decoded value, and `Tool(name)` returns one table with its shape normalised — every nested table is `map[string]any` and every array is `[]any`, whichever of the decoder's two array shapes it produced.

```go
m, ok, err := metadata.Parse(source)
if err != nil {
	return err
}
if ok {
	if knot, found := m.Tool("knot"); found {
		// knot["version"], knot["menus"].([]any), ... — your schema, your validation
	}
	if err := m.Verify(metadata.Env{/* ... */}); err != nil {
		return err
	}
}
```

Everything inside `[tool.*]` is accepted by scriptling — unknown keys are not errors there — so a host reading its own tables validates them itself and fails loudly on a malformed declaration. `Verify` never inspects `Tools`: requirements and host configuration are separate concerns sharing one block.

## Reporting failures your way

`Verify` returns one aggregated `*metadata.CheckError` whose `Failures` carry a `Kind` — `FailureVersion`, `FailureLibrary`, `FailurePluginMissing`, `FailurePluginVersion` — with the rendered message for each. Hosts attach their own remedies the way the CLI appends how to load plugins:

```go
var check *metadata.CheckError
if errors.As(err, &check) && check.Has(metadata.FailurePluginMissing) {
	err = fmt.Errorf("%w\nthis host loads plugins configured in its plugins setting", err)
}
```

A runnable version of this whole flow — host version, a registered library satisfying a dependency, an unresolvable `via` entry refused before any code runs — is in [`examples/script-metadata`](https://github.com/paularlott/scriptling/tree/main/examples/script-metadata) in the repository.

## See Also

- [Script Metadata](/docs/script-metadata/) — the block format and keys
- [Embedding Plugins](../plugins/) — loading plugins in a host
- [Library Loader Chain](../loader-chain/) — module resolution to feed `Resolves`
