---
description: Scriptling release history.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/changelog/
sources:
    - resource: https://scriptling.dev/docs/changelog/
status: stable
tags:
    - docs
    - changelog
title: Changelog
type: Guide
---
# Changelog

## October 2026

### v0.27.2



**Performance.** Script execution is 15% to 30% faster depending on workload and calls into scripts are up to 20x faster.



**Comprehensions are about twice as fast.** List, dict and set comprehensions bind their variable through a slot and iterate `range()` directly.



**Function bodies compile on first call.** A module that defines many functions now retains compiled code only for the ones that run, reducing memory for library-heavy hosts.



**Program cache budget is configurable.** Parsed and compiled scripts are kept in a process-wide cache bounded by 64 MiB by default. The CLI gains `--program-cache-max-bytes` (`SCRIPTLING_PROGRAM_CACHE_MAX_BYTES`, `cache.program_max_bytes` in `scriptling.toml`), and Go hosts get `scriptling.SetProgramCacheMaxBytes` plus `scriptling.GetProgramCacheStats` for hit, miss and eviction counts. See [Command-Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md) and [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#program-cache).


---

## September 2026

### v0.27.1


Rebuild against newer libraries and dependencies.

---

### v0.27.0



**`ai.Client(prompt_caching=...)` controls Claude prompt caching.** The Claude provider sends Anthropic's prompt-caching breakpoints automatically (system prompt, last tool, last message); the new `prompt_caching=False` kwarg turns them off for endpoints that reject `cache_control`. Default stays on. See [AI Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md).



**`os.path` works as an attribute of `os`.** `os.path.exists(...)` after `import os` raised `KeyError: 'path'`; only the standalone `import os.path` form worked. The path module now resolves as an attribute too, exactly like Python (and the attribute form is now covered by tests).



**`json.loads` errors are catchable as `ValueError`.** Python's `JSONDecodeError` subclasses `ValueError`; the standard `except ValueError:` guard now catches malformed-JSON errors.



**`re.split`/`re.sub` argument handling and `re.subn`.** `maxsplit=`/`count=` keyword forms were ignored, `maxsplit` was off by one (Go counts results, Python counts splits), `re.subn` did not exist, and Python backreferences (`\1`, `\g<name>`) in replacement strings were not expanded.



**`collections.deque` is a real deque.** `appendleft`, `popleft`, `extend`, `extendleft`, `rotate`, `clear`, `copy`, and `count` methods with `maxlen` enforcement (the old `deque_appendleft`-style module functions are gone); `len()`, indexing, iteration, and truthiness all work, and `str(d)` renders `deque([...])` like Python.



**`Counter` arithmetic and `namedtuple` repr.** Counters support `+`, `-`, `|` (max-union) and `&` (min-intersection) with Python's positive-only results; namedtuples print as `Point(x=1, y=2)`. Instance `|`/`&` operators now dispatch `__or__`/`__and__` generally.



**`statistics.median` keeps integer inputs integer** (`median([1, 3, 2])` is `2`, not `2.0`, matching Python).



**Regex named groups.** `(?P<name>...)` captures are reachable as `m.group("name")` and via the new `m.groupdict()`, with Python's catchable `IndexError` for unknown names.



**`datetime` attributes and parsing match Python.** `.year`/`.month`/`.day`/`.hour`/`.minute`/`.second`/`.microsecond` are attributes (they were methods, so `dt.year` returned a bound method), `strptime` results work like parsed datetimes, and `fromisoformat` is available on both `date` and `datetime`. `timedelta` is now a real object: `str()` renders Python's format (`1 day, 2:00:00`, including negative-duration day-borrowing), with `total_seconds()` and normalized `days`/`seconds`/`microseconds` fields, and date/datetime arithmetic accepts it directly.



**`itertools` accepts iterators everywhere.** `islice`, `chain`, `cycle`, `takewhile`, `dropwhile`, `accumulate`, `product`, `permutations`, `combinations`, and `zip_longest` all rejected the iterators the builtins produce (`islice(range(10), 2, 6, 2)` errored); all verified against CPython. `cycle(iterable)` now returns a lazily infinite iterator like Python's (the finite `cycle(iterable, n)` form still works), `islice` stays lazy so it can bound infinite iterators, and `product` honors `repeat=`.



**Multiple `if` clauses in comprehensions.** `[x for x in items if a if b]` was a parse error; conditions now chain (equivalent to `if a and b`) across list, set, and dict comprehensions and generator expressions, including with additional `for` clauses.



**Named `%`-formatting.** `"%(name)s=%(n)d" % {...}` — the logging/template idiom — reads values from a dict by key, composes with all width/precision/flag/conversion forms, and raises Python's `KeyError`/`TypeError` on a missing key or non-mapping right side.



**In-place set methods.** `update`, `intersection_update`, `difference_update`, and `symmetric_difference_update` accept any number of iterables (not just sets), mutating in place like Python.



**`dict.fromkeys` and `SomeClass.__name__`.** The type-level default-mapping constructor (`dict.fromkeys(keys, value)`), and class name introspection — `cls.__name__` in classmethods and `SomeClass.__name__` generally — returning the name string, consistent with `type(x)`.



**Callable instances.** `obj(...)` dispatches `__call__`, so functors, strategies, and partial application work; calling an instance without `__call__` raises a catchable `TypeError` like Python's.



**`str.encode()` returns bytes.** It previously produced a list of ints (an old workaround from before the bytes type existed), so `"héllo".encode().decode()` failed; the round-trip works now, with `utf-8` (default), validated `ascii`, and a `ValueError` for unknown encodings.



**`math.isclose`.** Python's float comparison with `rel_tol`/`abs_tol` kwargs, including the NaN and infinity edge semantics.



**Lists and tuples order-compare.** `[1] < [2]` and `(1, 2) < (1, 3)` raised "type mismatch"; both now compare element-wise like Python, and incomparable elements raise `TypeError: '<' not supported between instances of 'int' and 'str'` instead of silently comparing as equal — which also makes `sorted()` on mixed-type lists honest.



**Common error messages are Python-shaped.** `1 + "x"` now says `unsupported operand type(s) for +: 'int' and 'str'`, an undefined name says `name 'x' is not defined`, a missing key prints quoted (`'missing'`), and sort comparison errors match CPython's wording — the error text is the only feedback an LLM gets, so it now reads like Python's.



**`repr` is Python-style everywhere.** The three repr paths disagreed (`repr('hi')` gave single quotes, `%r` and f-string `!r` gave Go-style double quotes, and nothing escaped newlines). One shared implementation now uses Python's rules: single quotes (switching to double when the string contains one), escaped `\n`/`\r`/`\t`, applied consistently across `repr()`, `%r`, `!r`, and the new `=` debug form.



**The f-string `=` debug specifier.** `f"{x=}"` renders `x=7`, preserving source spacing (`f"{x = }"` gives `x = 7`), composing with format specs (`f"{x=:>10}"`) and conversions, exactly like Python 3.8+.



**`%`-formatting applies width, precision and flags to strings.** `"%10s"`, `"%-10s"`, and `"%.3s"` were silently ignored for `%s`/`%r`; they now pad, justify, and truncate like Python (zero-padding stays numeric-only).



**`del a, b` and friends.** Multi-target deletion was a parse error; `del a, b["k"], l[0]` now deletes all targets.



**Numeric underscores.** `1_000_000`, `0xff_f`, `1_000.5`, and `int("1_000")` / `float("1_0.5")` parse with Python's between-digits rule.



**`len(range(n))` works, `splitlines(keepends=True)` is honored.** Range is the one lazy iterator with a defined length (as in Python; `len` of map/enumerate still errors), and the `keepends` keyword was silently ignored — only the positional form worked.



**Floats display exactly like Python.** `print(2.0)` shows `2.0` (was `2`), and `123456789.123` prints as itself instead of `1.23456789123e+08`; `-0.0` and `inf`/`nan` use Python's spellings. The same repr applies inside containers, f-strings and `json.dumps`, which previously emitted Go's encodings.



**MCP numbers keep their integer typing.** JSON-decoded whole numbers (`{"n": 21}`) reached script tool functions as floats, so `n * 2` returned `42.0`; tool arguments, resource reads and prompt responses now convert the way Python's json module does, nested objects and arrays included.



**Slice assignment works.** `l[0:2] = [9, 8, 7]` raised "cannot assign to expression" although the reference documented it; splicing (any length change), insertion, stepped slices, negative steps, and the `ValueError`/`TypeError` mismatch cases now all match Python. See [Slicing](https://scriptling.dev/okf/scriptling-reference/slicing.md).



**`str.startswith` / `str.endswith` accept tuples and offsets.** `"file.py".startswith((".py", ".txt"))` previously raised "prefix: must be a string", and the optional `start`/`end` arguments were rejected; both now match Python, including negative offsets.



**`str.replace` accepts the count argument.** `"aaa".replace("a", "b", 2)` previously failed with an argument-count error; the limit is now honored.



**Bytes literals `b"..."`.** Previously only the `bytes()` builtin could construct bytes; literals now parse, escapes included, and work with `decode`, `len()` and the rest of the bytes API.



**`str.rsplit`.** Split from the right with `maxsplit`, including the `rsplit(None, n)` whitespace form with Python's exact leading-whitespace behavior. See [String Methods](https://scriptling.dev/okf/scriptling-reference/types.md).



**Integer `//` and `%` now follow Python exactly.** Floor division floors toward negative infinity (`-7 // 2` is `-4`) and modulo takes the divisor's sign (`-7 % 2` is `1`), including at parse-time constant folding. Float modulo also works now, with the same sign rule (`5.5 % 3` is `2.5`); it previously raised "unknown operator". See [Operators](https://scriptling.dev/okf/scriptling-reference/operators.md).



**`enumerate(iterable, start=N)` honors the keyword.** The `start=` form was silently ignored and produced 0-based pairs; only the positional form worked. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`sorted()` and `.sort()` are stable.** They used an unstable algorithm that could reorder equal keys on larger inputs; Python guarantees stability and so does Scriptling now, including with `reverse=True`. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`round()` rounds ties to even, like Python.** `round(2.5)` is `2` (was `3`), `round(2.675, 2)` is `2.67` (was `2.68`), and types match Python too: a float stays a float when ndigits is given. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**List and set augmented assignment mutate in place.** `x = y = [1]; x += [2]` now lets `y` observe the update, as in Python; same for `list *= n` and `|=`, `&=`, `-=` and `^=` on sets. See [Operators](https://scriptling.dev/okf/scriptling-reference/operators.md).



**Type annotations are accepted.** Function signatures (`def f(a: int, b: str = "x") -> bool:`), annotated assignments (`count: int = 5`), and generic/string annotations (`dict[str, int]`, `int | None`) all parse; the annotations are ignored, matching their runtime meaning in Python, so annotated Python pastes in unchanged — including MCP tool functions. See [Functions](https://scriptling.dev/okf/scriptling-reference/functions.md).



**Walrus assignment expressions.** `while (chunk := read()):`, `if (n := len(x)) > 10:`, and walrus in comprehension filters, with Python's precedence. A walrus bound inside a comprehension does not leak to the enclosing scope. See [Operators](https://scriptling.dev/okf/scriptling-reference/operators.md).



**Dict merge operators.** `d1 | d2` builds a new dict with the right operand winning conflicts, and `d |= other` merges in place so aliases observe the update, matching Python (PEP 584). See [Operators](https://scriptling.dev/okf/scriptling-reference/operators.md).



**The `...` placeholder.** `def stub(): ...` bodies and `tuple[int, ...]` annotations parse; the expression evaluates to `None`.



**`json.dumps(data, indent=n)` honors a numeric indent.** The kwarg previously only accepted strings, so `indent=2` silently produced compact output; a number now gives that many spaces and `indent=0` newline-separates. See [json](https://scriptling.dev/okf/scriptling-libraries/data-formats/json.md).



**`sum()` accepts Python's optional `start` argument.** `sum(iterable, start)` previously failed; it now offsets the total and can seed a float result. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`list.sort()` is as honest as `sorted()`.** Sorting incomparable elements (dicts without a `key`) silently did nothing where `sorted()` raised; both now use one comparator, so `.sort()` errors the same way and also supports `__lt__` on instances. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`repr(e)` prints the exception's class.** `ValueError: bad input` instead of the generic `EXCEPTION:` wrapper, matching `type(e)`. The LLM guide also now states that custom exception classes are not supported. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`type(e)` reports the exception's class.** `type()` on a caught exception now returns the class it was raised as (`"ValueError"`, `"KeyError"`) instead of the generic `"EXCEPTION"`, so `except` blocks can discriminate without message sniffing. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**A failing tool no longer kills the agent turn.** A tool handler that raises — or a tool name the model invented — now comes back as an `Error: ...` tool result the model can see and recover from, and the other tools in the same batch still run. See [Agent](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md).



**`ToolRegistry.add()` with a duplicate name now replaces the tool.** Previously re-registering a name appended a second identical schema — the model saw two copies of the tool — while silently swapping the handler. `add_schema()` still errors on duplicates.



**The positional-only separator `/` is rejected with a clear parse error.** `def f(a, /, b)` previously parsed with the `/` silently accepted as a parameter named `/`, so every call failed with a confusing argument-count error. The parser now reports `positional-only parameters ('/') are not supported` up front.



**The `@mcp.tool` help example no longer uses `eval()`.** The example used `eval()`, which does not exist in scriptling — copying it produced an error.



**`scriptling pack --list <package>`.** Prints what a package contains before you deploy it: the manifest's name, version and protocols, each convention directory with its file count, and the sha256. The [Python differences](https://scriptling.dev/okf/scriptling-reference/python-differences.md) page was also re-verified end to end: nested classes and `bytes()` work and are now listed as supported, and `input()`'s availability and the `type(x).__name__` divergence are documented precisely.



**`sys.executable`: the running interpreter's path.** Lets a script relaunch its own binary as a subprocess instead of depending on which `scriptling` resolves to on PATH; the MCP examples now launch their stdio servers this way. See [sys](https://scriptling.dev/okf/scriptling-libraries/http-process/sys.md).



**`mcp.Client` HTTP requests time out after 30 seconds by default.** Script-level clients previously inherited the library's 5-minute timeout, so a hung server stalled a script for minutes per call. `mcp.Client(url, timeout=300)` opts a known-slow server back up, and timeouts surface as ordinary catchable exceptions. See [MCP Client](https://scriptling.dev/okf/scriptling-libraries/mcp/client.md).



**`Agent` can use real MCP servers: the `mcp_servers=` argument.** Pass one or more `mcp.Client` clients and the agent gets their tools (namespaced, so a `search` tool on a client with `namespace="shop"` becomes `shop__search`) and skills alongside its own. Each client needs a distinct namespace. See [Agent](https://scriptling.dev/okf/scriptling-libraries/ai/agent.md#mcp-server-integration).



**`tools.Registry.add_schema(name, description, schema, handler)` registers a tool from a full JSON Schema.** For parameter shapes richer than the flat name-to-type map `add()` accepts (nested objects, enums, per-parameter descriptions). Duplicate names are an error instead of a silent overwrite. See [AI Tools](https://scriptling.dev/okf/scriptling-libraries/ai/tools.md).



**Register resources, prompts and skills from script code: `@mcp.resource`, `@mcp.prompt`, `@mcp.skill`.** The tools folder's decorated `.py` files can now register every MCP entry kind, not just tools. One file can mix all four decorators, everything reloads with the tools folder, and the same registrations work in app bundles. See [runtime.mcp](https://scriptling.dev/okf/scriptling-libraries/runtime/mcp.md).



**Booleans order like numbers in `min()`, `max()` and `sorted()`.** `sorted([True, False])` previously failed and `min([True, False])` returned the wrong element; booleans now order as 0 and 1, matching Python. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**`min()` and `max()` honor the `key` function.** Previously `max(records, key=lambda r: r["amount"])` silently returned the first record instead of the largest. A `default` argument is also supported for the single-iterable form. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md).



**App packages can carry skills.** The `skills/` directory joins `tools/`, `resources/`, `prompts/`, `webroot/` and `docs/` as a package convention directory: present means packed and served. See the [Packaging an MCP App](/tutorials/mcp-app-package/) tutorial.



**`client.namespace` on an MCP client.** The client's namespace (empty string when created without one) is now readable as an attribute, so scripts can tell which server a namespaced tool name or skill URI belongs to. See [MCP Client](https://scriptling.dev/okf/scriptling-libraries/mcp/client.md).



**The MCP server can serve skills (SEP-2640).** `--mcp-skills` (env `SCRIPTLING_MCP_SKILLS`) points at a directory of skills — one per subdirectory containing a `SKILL.md` — served per the MCP skills extension via `skills/list` and `skills/get`, with each file readable as a `skill://` resource. See [MCP Server](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md).



**`mcp.Client` can consume skills: `skills()` and `get_skill(uri)`.** `skills()` lists the skills a server exposes (URI, frontmatter, per-file digests) and `get_skill(uri)` fetches one; the content reads with the existing `read_resource`. Works for HTTP and stdio clients alike. See [MCP Client](https://scriptling.dev/okf/scriptling-libraries/mcp/client.md).
