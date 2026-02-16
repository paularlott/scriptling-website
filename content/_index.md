---
title: Scriptling
layout: index
description: A minimal, sandboxed Python-like scripting language for Go applications and LLM agents.
---

{{< big-title
  title="Python-like Scripting for Go"
>}}

{{< hero
  title="Simple. Sandboxed. Powerful."
  subtitle="Scriptling is a minimal, sandboxed interpreter with Python-inspired syntax designed for embedding in Go applications. Perfect for LLM agents to execute code and interact with REST APIs, with built-in AI integration and MCP protocol support."
  btn1="Get Started"
  btn1Link="docs/quick-start/"
  btn2="View Docs"
  btn2Link="docs"
  img="/images/mascot.png"
  alt="Scriptling Mascot"
>}}

{{< feature-grid >}}

  {{< feature-row
    reverse=true
    img="/images/mascot.png"
    alt="Python-like Syntax"
    is4=true
  >}}
  ## Python-Inspired Syntax
  Write code that feels familiar with indentation-based blocks, classes with single inheritance, functions, lambda, list comprehensions, and comprehensive error handling.
  {{< /feature-row >}}

  {{< feature-row
    reverse=true
    img="/images/mascot.png"
    alt="Sandboxed Execution"
    is4=true
  >}}
  ## Secure & Sandboxed
  No direct filesystem or network access unless explicitly enabled. Configurable security with path restrictions, network access control, and execution timeouts.
  {{< /feature-row >}}
{{< /feature-grid >}}

{{< feature-grid >}}
  {{< feature-row
    reverse=false
    img="/images/mascot.png"
    alt="Go Integration"
    is4=true
  >}}
  ## Seamless Go Integration
  Register Go functions, exchange variables, and create custom libraries. Direct type mapping between Go and Scriptling makes embedding effortless.
  {{< /feature-row >}}

  {{< feature-row
    reverse=false
    img="/images/mascot.png"
    alt="AI & LLM Ready"
    is4=true
  >}}
  ## Built for AI & LLMs
  Native OpenAI-compatible API support, MCP (Model Context Protocol) server and client, and automatic tool execution for agentic workflows.
  {{< /feature-row >}}
{{< /feature-grid >}}

{{< feature-grid >}}
  {{< feature-row
    reverse=true
    img="/images/mascot.png"
    alt="Rich Library Ecosystem"
    is4=true
  >}}
  ## Rich Library Ecosystem
  25+ built-in libraries including JSON, regex, math, HTTP requests, subprocess, YAML, and specialized libraries for AI, MCP, and concurrent execution.
  {{< /feature-row >}}

  {{< feature-row
    reverse=true
    img="/images/mascot.png"
    alt="CLI & Server"
    is4=true
  >}}
  ## CLI & HTTP Server
  Run scripts directly, use interactive mode, or start an HTTP server with MCP support. Cross-platform binaries for Linux, macOS, and Windows.
  {{< /feature-row >}}
{{< /feature-grid >}}

---

## Why Choose Scriptling?

Scriptling is an open-source (MIT License) scripting language that bridges the gap between Go applications and Python-like scripting. Whether you're building AI agents, automation tools, or need embedded scripting in your Go application, Scriptling provides a secure, fast, and familiar solution.

**Key Use Cases:**
- **AI & LLM Integration** - Let AI agents execute code safely with built-in guardrails
- **Go Embedding** - Add scripting capabilities to your Go applications
- **REST API Automation** - Built-in HTTP client with JSON handling
- **Sandboxed Execution** - Run untrusted code with configurable security
- **MCP Servers** - Build Model Context Protocol servers for LLM tools
