---
title: Documentation
description: Complete documentation for Scriptling - a minimal, sandboxed Python-like scripting language for Go applications.
tags: [docs]
weight: 1
---

Scriptling is a minimal, sandboxed interpreter for Python-like scripting designed for embedding in Go applications. Use the sections below to get started, integrate with Go, or explore tutorials.

## Guides

{{< cards >}}
{{< card link="quick-start/" title="Getting Started" description="Install the CLI or embed Scriptling in Go" >}}
{{< card link="cli/" title="CLI Reference" description="Running scripts, HTTP server mode, MCP server mode, and packages" >}}
{{< card link="go-integration/" title="Go Integration" description="Embed the interpreter, register functions, and create custom libraries" >}}
{{< card link="security/" title="Security Guide" description="Sandbox configuration, path restrictions, and network access control" >}}
{{< card link="plugins/" title="Plugins" description="Extend Scriptling with Go, C, PHP or any JSON-RPC language; database drivers included" >}}
{{< /cards >}}

## Tutorials

Step-by-step guides for real-world scenarios:

- [Fetching and Processing API Data](tutorials/api-data-fetching/): HTTP requests, JSON processing, and file output
- [Embedding a Rules Engine](tutorials/embedding-rules-engine/): Go integration with custom functions
- [Building an MCP Tool Server](tutorials/mcp-tool-server/): Custom tools for AI assistants

## Reference

For language syntax, built-in functions, and library APIs, see the [Reference](/reference/) section.
