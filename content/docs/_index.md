---
title: Documentation
description: Complete documentation for Scriptling - a minimal, sandboxed Python-like scripting language for Go applications.
tags: [docs]
weight: 1
---

Scriptling is a minimal, sandboxed interpreter for Python-like scripting designed for embedding in Go applications. Use the sections below to get started, integrate with Go, or explore tutorials.

## Choose by task

- **New to Scriptling:** Start with [Getting Started](quick-start/) to install the CLI or embed the interpreter, then learn the language from the [Reference](/reference/).
- **Run a server:** Choose the CLI guide for [HTTP](cli/http-server/), [JSON-RPC](cli/jsonrpc-server/), [MCP](cli/mcp-server/), or [plugin](cli/plugin-server/) server modes.
- **Find a library:** Look it up in the [A–Z list](/reference/libraries/#all-libraries-az) or browse the [Library Reference](/reference/libraries/) by capability, and check registration requirements for your runtime.
- **Connect to a database:** Choose a driver or ORM from the [Database Libraries](/reference/libraries/databases/).

## Guides

{{< cards >}}
{{< card link="quick-start/" title="Getting Started" description="Install the CLI or embed Scriptling in Go" >}}
{{< card link="cli/" title="CLI Guide" description="Running scripts, HTTP server mode, MCP server mode, and packages" >}}
{{< card link="go-integration/" title="Go Integration" description="Embed the interpreter, register functions, and create custom libraries" >}}
{{< card link="security/" title="Security Guide" description="Sandbox configuration, path restrictions, and network access control" >}}
{{< card link="plugins/" title="Plugins" description="Extend Scriptling with Go, C, PHP, or any JSON-RPC language" >}}
{{< card link="llm-guide/" title="LLM Script Generation Guide" description="Guidance for generating accurate Scriptling code with LLMs" >}}
{{< card link="tutorials/" title="Tutorials" description="Step-by-step guides: API data, rules engines, MCP servers and plugins" >}}
{{< card link="script-metadata/" title="Script Metadata" description="Declare the scriptling version, libraries and plugins a script needs" >}}
{{< /cards >}}

## Tutorials

Step-by-step guides for real-world scenarios:

{{< page-list section="/docs/tutorials" >}}

## Reference

For language syntax, built-in functions, and library APIs, see the [Reference](/reference/) section.
