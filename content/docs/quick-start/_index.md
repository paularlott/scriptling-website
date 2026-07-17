---
title: Getting Started
description: Get up and running with Scriptling.
tags: [quick-start]
weight: 1
---

Scriptling can be used two ways: as a standalone command-line tool, or embedded inside a Go application. Choose the path that's right for you.

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 not-prose">

  <a href="cli/" class="block rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6 hover:border-teal-500 dark:hover:border-teal-500 hover:shadow-lg transition-all no-underline bg-white dark:bg-gray-800">
    <div class="flex items-center gap-3 mb-3">
      <svg class="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 m-0">Using the CLI</h2>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4">Install the Scriptling CLI and start running scripts from the command line. Includes interactive mode, HTTP server, and MCP server capabilities.</p>
    <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 mb-4">
      <li>Install on macOS, Linux, or Windows</li>
      <li>Run scripts, use the REPL, or start a server</li>
      <li>No Go knowledge required</li>
    </ul>
    <span class="text-teal-600 dark:text-teal-400 font-semibold text-sm">Get started &rarr;</span>
  </a>

  <a href="embedding/" class="block rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6 hover:border-teal-500 dark:hover:border-teal-500 hover:shadow-lg transition-all no-underline bg-white dark:bg-gray-800">
    <div class="flex items-center gap-3 mb-3">
      <svg class="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 m-0">Embedding in Go</h2>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4">Add scripting capabilities to your Go application. Register libraries, exchange variables, and create custom extensions.</p>
    <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 mb-4">
      <li>Single dependency, minimal binary size</li>
      <li>Register built-in or custom libraries</li>
      <li>Sandboxed execution with configurable security</li>
    </ul>
    <span class="text-teal-600 dark:text-teal-400 font-semibold text-sm">Get started &rarr;</span>
  </a>

  <a href="vscode/" class="block rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6 hover:border-teal-500 dark:hover:border-teal-500 hover:shadow-lg transition-all no-underline bg-white dark:bg-gray-800">
    <div class="flex items-center gap-3 mb-3">
      <svg class="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 m-0">VSCode Extension</h2>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4">Get syntax highlighting and language support for Scriptling in Visual Studio Code.</p>
    <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 mb-4">
      <li>Syntax highlighting</li>
      <li>Language support</li>
    </ul>
    <span class="text-teal-600 dark:text-teal-400 font-semibold text-sm">Get started &rarr;</span>
  </a>

  <a href="documentation-mcp/" class="block rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6 hover:border-teal-500 dark:hover:border-teal-500 hover:shadow-lg transition-all no-underline bg-white dark:bg-gray-800">
    <div class="flex items-center gap-3 mb-3">
      <svg class="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 m-0">Documentation MCP</h2>
    </div>
    <p class="text-gray-600 dark:text-gray-400 mb-4">Serve Scriptling's documentation to AI agents as OKF knowledge bundles through an MCP server.</p>
    <ul class="text-sm text-gray-500 dark:text-gray-400 space-y-1 mb-4">
      <li>Browse and search docs from any MCP client</li>
      <li>Semantic and keyword search</li>
      <li>Run over stdio or HTTP</li>
    </ul>
    <span class="text-teal-600 dark:text-teal-400 font-semibold text-sm">Get started &rarr;</span>
  </a>

</div>

## Already know what you need?

- [Language Guide](/reference/) - Complete language reference
- [Libraries](../../reference/libraries/) - Library usage and APIs
- [CLI Reference](../cli/) - Full command-line documentation
- [Go Integration](../go-integration/) - Deep dive into embedding
