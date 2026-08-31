---
title: Documentation
description: Complete documentation for Scriptling - a minimal, sandboxed Python-like scripting language for Go applications.
tags: [docs]
weight: 1
---

Scriptling is a minimal, sandboxed interpreter for Python-like scripting designed for embedding in Go applications. Use the sections below to get started, integrate with Go, or explore tutorials.

## Choose by task

- **Learn the language:** Start with the [Language Guide](/reference/), then use its syntax, types, control-flow, function, and class references.
- **Use the command line:** Follow the [CLI Guide](cli/) for scripts, packages, policies, and runtime options.
- **Embed Scriptling in Go:** Use [Go Integration](go-integration/) to create an interpreter and expose host functions, classes, and libraries.
- **Run a server:** Choose the CLI guide for [HTTP](cli/http-server/), [JSON-RPC](cli/jsonrpc-server/), [MCP](cli/mcp-server/), or [plugin](cli/plugin-server/) server modes.
- **Find a library:** Browse the [Library Reference](/reference/libraries/) by capability and check registration requirements for your runtime.
- **Build or use plugins:** Start with the [Plugins Guide](plugins/) for supported plugin models and host integration.
- **Connect to a database:** Choose a driver or ORM from the [Database Libraries](/reference/libraries/databases/).

## Guides

{{< cards >}}
{{< card link="quick-start/" title="Getting Started" description="Install the CLI or embed Scriptling in Go" >}}
{{< card link="cli/" title="CLI Guide" description="Running scripts, HTTP server mode, MCP server mode, and packages" >}}
{{< card link="go-integration/" title="Go Integration" description="Embed the interpreter, register functions, and create custom libraries" >}}
{{< card link="security/" title="Security Guide" description="Sandbox configuration, path restrictions, and network access control" >}}
{{< card link="plugins/" title="Plugins" description="Extend Scriptling with Go, C, PHP, or any JSON-RPC language" >}}
{{< card link="llm-guide/" title="LLM Script Generation Guide" description="Guidance for generating accurate Scriptling code with LLMs" >}}
{{< /cards >}}

## Tutorials

Step-by-step guides for real-world scenarios:

- [Fetching and Processing API Data](tutorials/api-data-fetching/): HTTP requests, JSON processing, and file output
- [Embedding a Rules Engine](tutorials/embedding-rules-engine/): Go integration with custom functions
- [Building an MCP Tool Server](tutorials/mcp-tool-server/): Custom tools for AI assistants

## Reference

For language syntax, built-in functions, and library APIs, see the [Reference](/reference/) section.
