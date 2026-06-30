# Library Reference Page Style Guide

This defines the canonical structure for every page under `content/reference/libraries/**`
that documents a single importable library (e.g. `os.md`, `json.md`, `requests.md`,
`scriptling/runtime/sandbox.md`). It does not apply to category index pages (`_index.md`)
or to `cheat-sheet.md`, which are intentionally different (overview/links, and quick patterns).

Don't use em dashes anywhere in this guide or in the docs it describes. Use a period, comma,
or colon instead, whichever reads best in context.

There are two page kinds:

- **Standard library page**: documents an importable module with functions/constants.
  Use the template below.
- **Umbrella page**: a namespace that exists only to group submodules (e.g. `scriptling.ai`,
  `scriptling.runtime`, `scriptling.mcp`, `scriptling.net`). These have no functions of their
  own beyond re-exports; use the short "Umbrella page" variant at the end of this doc instead
  of forcing them into the function-table template.

## Front matter

```yaml
---
title: <Display Name>           # e.g. "os", "requests", "Sandbox"
description: <one sentence, what it's for>
weight: <n>
aliases:                        # only if the page moved
  - /old/path/
---
```

Drop fields that don't apply (e.g. `aliases`). Don't add a `requires_registration` field.
Registration status is a one-line tag in the body (see below), not front matter.

## Body structure, in order

1. **Overview**: 1-3 sentences on what the library does and when you'd reach for it. No code yet.

2. **Registration note**: the full explanation of CLI-vs-Go registration lives once at
   [Libraries](/reference/libraries/) (the category index). Don't repeat it on leaf pages at all,
   not even as a one-liner, that's still bloat repeated 70 times for one fact a reader only needs
   once. The only exception: a library with filesystem/network/process/secrets implications gets
   one sentence folded into the opening of its **Security Considerations** section (see step 5),
   because that's the one place registration mechanics and risk are the same reader's concern at
   the same time. Everything else (standard libraries, and extended libraries with no security
   angle) gets no registration mention in the body at all.

3. **Available Functions**: a table, always, even for a 2-function library:

   ```markdown
   | Function | Description |
   |----------|-------------|
   | `read_file(path)` | Read a file's contents as a string. |
   ```

   If the library has constants (e.g. `math.pi`), add a separate **Constants** table
   immediately after, same two-column format (`Constant`, `Description`, with the value
   shown in the description, e.g. "The ratio of circumference to diameter (`3.14159...`)").

4. **Functions**: one `###` subsection per function, in the same order as the table above.
   For libraries with more than ~12 functions, group related functions under `##` thematic
   headers (e.g. "Combinatorics", "Path Operations") with `###` functions underneath.
   `math.md` and `itertools.md` already do this; keep it for libraries of similar size.

   Each function subsection:

   ````markdown
   ### `function_name(param1, param2=default)`

   One or two sentences describing behavior, including edge cases worth calling out.

   **Parameters:**
   - `param1` (`type`): Description.
   - `param2` (`type`, optional): Description. Default: `value`.

   **Returns:** `type`. Description.

   **Raises:** `ExceptionType`. When this happens. *(omit this line entirely if nothing is raised beyond normal Scriptling errors)*

   ```python
   example showing realistic usage, not just the signature
   ```
   ````

   Rules:
   - Always show the type in backticks for params and returns: `` `str` ``, `` `int` ``, `` `list` ``, `` `dict` ``, `` `Match` ``, etc.
   - Optional/defaulted parameters: show the default in the signature *and* state it again in the description ("Default: `0`"). Both, always, don't pick one.
   - Every function gets at least one runnable code example. Don't defer all examples to a single section at the end of the page.
   - "Returns:" is required even when the return is `None`, write `**Returns:** \`None\``.
   - No em dashes. Use a period or comma instead.

5. **Security Considerations** (only if the library has any of: filesystem access, network
   access, process execution, secrets/credential access, or arbitrary code execution): one
   short paragraph naming the specific risk, plus a link to the relevant mitigation. If the
   library is extended, open with that one-line registration mention (see step 2):

   ```markdown
   ## Security Considerations

   This is an extended library, requiring registration in Go (see [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries)).

   `os` provides read/write access to the host filesystem. Access is restricted to the
   `allowedPaths` passed to `RegisterOSLibrary`. For a full risk breakdown across all
   libraries, see the [Security Guide](/docs/security/).
   ```

   Don't restate the entire security guide on every page, one paragraph, link out.

6. **Examples** (optional): only for libraries where a multi-function workflow is genuinely
   illustrative beyond the per-function examples (e.g. a retry pattern for `requests`). Skip
   this section if the per-function examples already cover usage; don't pad pages with a
   redundant "Examples" section just to have one.

7. **Python Compatibility** (optional): always use this exact heading, never "Differences from
   Python" or any other variant, even if the section is entirely about gaps/caveats rather than
   a coverage table. Keep it where it already adds real signal (e.g. `os.md`'s coverage table,
   `regex.md`'s RE2 limitations). Don't add it to libraries with no Python equivalent (e.g.
   `scriptling.runtime.*`).

   Two content shapes both belong under this one heading, and a page can use either or both:
   - **Coverage table** (`datetime.md`, `sys.md`): a `Feature`/`Supported` table, mainly for
     libraries that implement a subset of a larger Python module.
   - **Caveats list** (`toml.md`, `logging.md`): prose bullets on behavioral differences for
     things that *are* implemented but don't behave identically to Python. Open with one sentence
     naming what's being compared to (e.g. "Compared to Python's `tomllib`/`tomli-w`:") if it's
     not obvious from the library name alone, rather than putting that detail in the heading.
   If a page genuinely needs both (a coverage table for what's supported, plus caveats on the
   supported subset), put the table first, then the caveats list, under the one heading. Don't
   split them into two headings.

8. **See Also**: links to related libraries/guides, 2-4 bullets max.

## Umbrella page variant

For a namespace page that only links to submodules (no functions of its own):

1. Overview (1-2 sentences: what this namespace groups together).
2. Registration note (same rule as step 2 above; umbrella libs still need registering).
3. A bullet list of submodules, each linking to its page, with a one-line description.
4. A short "Quick Start" code block showing the most common submodule in action.
5. See Also.

No function table is needed at the umbrella level, that detail lives on each submodule's page.

## Parameter/return phrasing reference

Use these exact forms everywhere, don't vary the wording:

| Situation | Phrasing |
|---|---|
| Required param | `` - `name` (`type`): Description. `` |
| Optional param | `` - `name` (`type`, optional): Description. Default: `value`. `` |
| Return value | `**Returns:** \`type\`. Description.` |
| No return value | `**Returns:** \`None\`` |
| Exception | `**Raises:** \`ExceptionType\`. Condition.` |
