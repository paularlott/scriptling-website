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

### v0.32.0


**breaking**

- Return Python's type names from `type(x)` and `x.type()`: `"int"`, `"str"`, `"bool"`, `"NoneType"`, `"list"`, `"dict"`, `"bytes"`, `"function"`, `"method"`, `"builtin_function_or_method"`, `"module"`, `"type"`, `"FloatArray"`, and for iterators `"range"`, `"map"`, `"filter"`, `"zip"`, `"enumerate"`, `"list_iterator"`, `"count"` and so on. The old names (`"INTEGER"`, `"STRING"`, `"NULL"`, `"ITERATOR"`, ...) no longer match, so `type(x) == "INTEGER"` is now `False`; compare with `int`, `"int"` or `isinstance()` instead ([docs](https://scriptling.dev/okf/scriptling-reference/builtins.md#type))
- Match `isinstance()` type-name strings exactly as `type()` reports them: `isinstance(x, "int")` and `isinstance(None, "NoneType")` work, but `"INTEGER"`, `"Int"`, `"None"` and a class name in the wrong case no longer match


**fixed**

- Fix `type(x).__name__` returning scriptling's upper-case name (`"INTEGER"`) instead of Python's (`"int"`)
- Fix `type()` reporting a module as `"DICT"`, a class and `type(int)` as `"CLASS"`/`"BUILTIN"` instead of `"type"`, and a bound method as `"FUNCTION"` instead of `"method"`
- Fix `"INTEGER" == int` and `"STR" == str` comparing equal


---

### v0.31.0


**changed**

- **Breaking:** apply `scriptling.SetMemoryLimit` to each interpreter separately instead of the whole process ([docs](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#memory-limit))
- Apply the call-depth limit to `CallFunction`, `CallMethod` and `CreateInstance`
- Run `requests.parallel` on a fixed pool of `max_parallel` workers
- Stream files into zip and tar archives instead of reading each into memory
- Build `scriptling.grep`, `scriptling.sed`, `scriptling.find`, `os.listdir` and `csv.loads` results under the interpreter's limits
- Refuse `json.dumps` of a value nested more than 10,000 levels deep
- Force at most one garbage collection per 100 ms for an interpreter over its memory limit


**added**

- Add per-interpreter memory and value limits, off unless set, and the `MemoryError` exception ([docs](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#script-resource-limits))
- Add `WithMemoryLimit` and `WithMaxValueBytes` options to `scriptling.New`, and `p.SetMemoryLimit` and `p.SetMaxValueBytes`
- Add `p.ResourceUsage()` and `p.ShareResourceGuard()`
- Add `--memory-limit` and `--max-value-bytes` CLI options and `limits.*` in `scriptling.toml` ([docs](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md))
- Add `object` helpers for libraries that create values from script input: `CheckAlloc`, `CheckElements`, `CheckRoom`, `CheckValue`, `TrackSlice`, `TrackMap`, `ReadAllLimited`, `ReadFileLimited`, `BindGuard`, `CurrentGuard` and `RunFromContext` ([docs](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#value-limit))


**removed**

- **Breaking:** remove `scriptling.GetMemoryLimitStats`, `MemoryLimitStats` and `DefaultMemoryLimitCheckInterval`; use `p.ResourceUsage()`


**fixed**

- Fix comprehensions over a huge `range` and `f(*iterator)` ignoring timeouts and allocating their whole result up front
- Fix `secrets.randbits(k)` for k over 63 returning a truncated value; it now raises `OverflowError`
- Fix `str.expandtabs(0)` dividing by zero
- Fix a huge padding or format width, such as `"x".ljust(10**12)`, attempting the allocation; it now raises `MemoryError`
- Fix `requests.parallel` returning an error object instead of a status 0 `Response` for a request that failed before it was sent
- Fix the call-depth counter staying incremented after a call refused for exceeding the limit
- Fix the CLI server starting with its error lost when the setup script fails as the server is signalled to start
- Fix the CLI server resetting its runtime while a previous server's WebSocket handler was still running


---

### v0.30.4


**changed**

- Read 1Password Connect secrets in one request instead of three after an item's first lookup, by remembering vault and item ids for 10 minutes


**added**

- Add 1Password service accounts to the `onepassword` secret provider through the separate [scriptling-onepassword](https://github.com/paularlott/scriptling-onepassword) extension: give `service_account_token` instead of a Connect `address` and `token`; the released CLI supports Connect only ([docs](https://scriptling.dev/okf/scriptling-libraries/utilities/secret.md#1password-service-accounts))
- Add the `scriptlingcmd` package, so a custom CLI with extensions compiled in is a `main.go` calling `scriptlingcmd.Main()` ([docs](https://scriptling.dev/okf/scriptling-libraries/utilities/secret.md#service-accounts-in-embedded-applications-and-custom-builds))
- Add the `scriptling-onepassword` and `scriptling-slim-onepassword` builds, with 1Password service accounts compiled in, to the release and Homebrew ([docs](https://scriptling.dev/okf/scriptling-docs/quick-start/cli.md#1password-builds))


---

### v0.30.3


**breaking**

- Pass everything after the script file to the script in `sys.argv`, flags included, so `scriptling tool.py input.json --verbose` works without `--`; give scriptling's own options before the script file. A `--` straight after the file is still accepted and dropped ([docs](https://scriptling.dev/okf/scriptling-docs/cli/basic-usage.md#pass-arguments-to-a-script))


**fixed**

- Fix a script argument that matches a subcommand name, such as `scriptling tool.py cache` or `scriptling tool.py help`, running that subcommand instead of the script


---

### v0.30.2


**changed**

- Block reserved address ranges (CGNAT, documentation, benchmarking, NAT64, 6to4 and similar) under a network policy unless `allow_reserved_ips = true` ([docs](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md))


**added**

- Add `allow_reserved_ips` network policy option (`AllowReservedIPs` in Go) ([docs](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#network-policy))


**fixed**

- Accept TLS 1.2 on connections made under a network policy


---

### v0.30.0


**breaking**

- Change `client.response_compact(id)` to `client.response_compact(model, previous_response_id=, input=, instructions=)`. It now compacts a conversation into an `output` to continue from, using OpenAI's and xAI's compaction endpoints or, for other providers, a model summary; the old call only stripped reasoning items from a stored response. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/client/responses.md#clientresponse_compactmodel-previous_response_idnone-inputnone-instructionsnone))


**added**

- Add Grok (xAI) as a provider: `ai.Client("", provider=ai.GROK, api_key="xai-...")`, using xAI's native Responses API. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/client.md))
- Add `previous_response_id`, `instructions`, `tools` and `store` to `client.response_create()` and `client.response_stream()`, for multi-turn conversations and tool calling with the Responses API. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/client/responses.md))
- Add `ai.tool_outputs()` to send tool results back to the Responses API, and read Responses API output in `ai.text()` and `ai.tool_calls()`. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/ai.md#aitool_outputstool_results))
- Add `client.supports(capability)`, reporting whether a client uses a native (`"responses"`) or emulated (`"responses_emulated"`) Responses API, and supports `"embeddings"` and `"decision"`. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/client.md#clientsupportscapability))


**changed**

- Continue emulated Responses API conversations (Claude, Gemini, Ollama, Z AI, Mistral) with `previous_response_id`, which was previously ignored, keeping each response's turn in the process for 15 minutes after last use. Responses are only visible to clients with the same provider, base URL and API key.
- Stream tool calls as `function_call` items from emulated `client.response_stream()`, and stream a single response when the client runs `remote_servers` tools on the native Responses API.


**fixed**

- Fix native Responses API streaming returning no events, tool calls through the native Responses API failing, and emulated responses ignoring input messages without a `type` field and the `instructions` of a request.
- Fix Ollama tool calls: parallel calls to the same tool sharing an ID, and all but the last of several streamed calls being dropped.
- Fix tool calls without arguments being sent as `"null"` instead of `{}`.


---

### v0.29.0


**breaking**

- Evaluate parameter defaults once, at definition, as Python does. A mutable default is now shared between calls.
- Pass `*args` as a tuple instead of a list. Code that modifies `args` must copy it first with `list(args)`.
- Keep every `;`-separated statement of a one-line block inside that block. `def f(): return 1; f()` no longer calls `f`; put the call on its own line.
- Raise `OverflowError` when integer arithmetic passes 64 bits, instead of wrapping.
- Change `json.dumps()` output to Python's format: keys in insertion order (was sorted), `", "` and `": "` separators (was compact), non-ASCII escaped. Use `sort_keys=True`, `separators=(",", ":")` and `ensure_ascii=False` for the old shape. ([docs](https://scriptling.dev/okf/scriptling-libraries/data-formats/json.md))
- Return `UUID` objects from the `uuid` functions instead of strings. Use `str(u)` for the text form.
- Return `bytes` from the `base64` encoders instead of a string.
- Return a `timedelta` from `datetime` and `date` subtraction (was a number), and return a struct from `time.gmtime()` and `time.localtime()` with Python's weekday numbering (Monday is 0).
- Follow `posixpath` in `os.path.dirname()`, `basename()` and `splitext()` for empty paths, trailing slashes and dotfiles.
- Uppercase `ß` as `SS` in `str.upper()`.
- Remove subclassing of `defaultdict`: it is now a function that returns a dict.


**changed**

- Iterate dicts in insertion order (was unspecified), including `json.loads()`, `requests` `.json()`, `Counter`, `popitem()` and copies. Dicts built from YAML, TOML, MessagePack and plugin results have sorted keys. ([docs](https://scriptling.dev/okf/scriptling-reference/types.md#dictionary))
- Make dict-building code 10-30% slower than v0.28.0 in return for ordering. Lookups, `get()` and counting are unchanged.
- Deliver `**kwargs` in alphabetical order (was random per call). Call-site order is not kept.
- Rewrite `defaultdict` as an ordinary dict with a default factory: every dict method works, lambda and function factories work, keys keep their types, and it is about twice as fast. ([docs](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/collections.md#defaultdictdefault_factory))
- Make named tuples behave like tuples: indexing, slicing, `len()`, unpacking, ordering, hashing, immutability, keyword construction and `defaults=`.
- Raise catchable Python exceptions: `TypeError` for unhashable keys, unorderable sorts and wrong argument counts, `KeyError` and `IndexError` from `pop()`, the `FileNotFoundError` and `OSError` family from file operations, and Python's types from `assert`, `str.index`, `set.remove` and `min()` of an empty sequence.
- Hash plain instances by identity, and raise `AttributeError` when assigning to a property without a setter.


**added**

- Add generators: `yield` in a function makes a lazy generator that `for`, `list()`, `next()` and `itertools` consume. `yield from` and `send()` are not supported. ([docs](https://scriptling.dev/okf/scriptling-reference/functions.md))
- Add `@dataclass`, `enum.Enum` and `IntEnum`, `functools.lru_cache`, `cache` and `wraps`, user exception classes, and `from typing import ...`.
- Add `obj.__dict__`, a view of an instance's attributes whose writes go through to the object, and make `vars(obj)` the same view. ([docs](https://scriptling.dev/okf/scriptling-reference/classes.md#instance-attributes-as-a-dict-__dict__))
- Add `OrderedDict.move_to_end()` and `popitem(last=False)`, and accept dicts and dict views in `reversed()`.
- Add unpacking forms: `(*a, *b)`, `x = *t, 1`, starred targets in nested groups and `for` headers, `{**d}`, and `f(**d)`. ([docs](https://scriptling.dev/okf/scriptling-reference/syntax.md#assignment))
- Add `/` positional-only parameters, `raise X from e`, `.5` and `1.` float literals, nested and chained assignment targets, and `frozenset`.
- Add `copy.deepcopy()`, `sentinel()`, `csv.DictReader` and `DictWriter`, `math.fsum`, `time.monotonic`, `os.getpid`, number methods such as `bit_count()` and `to_bytes()`, and `int()`, `float()` and `str()` without arguments.
- Add `client.decide()` for Ollama System One decision models. ([docs](https://scriptling.dev/okf/scriptling-libraries/ai/client.md#clientdecidemodel-state-questions-images-keep_alive))


**fixed**

- Fix a subclass's class attribute being discarded when a base class defines the same name.
- Fix arguments written after a `*` unpack being passed before it.
- Fix keyword-only parameters with defaults being unbound when not passed, and a keyword named like a positional-only parameter being rejected when the function takes `**kwargs`.
- Fix `itertools` materialising infinite generators.
- Fix `super().__init__()` failing when no base class defines `__init__`.
- Fix `int(True)`, `float(False)` and `sum()` of booleans, `%g` precision, and UUID comparison and hashing.


---

### v0.28.0


**changed**

**Python 3 behaviour.** Objects, modules, printing and formatting now behave as Python 3 does, with Python's error messages, `__getattr__` and `__format__` support, and `getattr()`/`hasattr()` working exactly like dot access. `pathlib.Path` supports `/`. See [Python Differences](https://scriptling.dev/okf/scriptling-reference/python-differences.md).


**changed**

**Faster imports.** Library files are cached across interpreter instances, so hosts that create an instance per request import 50–77% faster. Edited files are picked up on the next import. See [Loader Chain](https://scriptling.dev/okf/scriptling-docs/go-integration/loader-chain.md#filesystemloader).


**added**

**Methods as values.** `sorted(words, key=str.lower)`, `map(str.strip, lines)` and `add = items.append` work, and `dir([])` lists methods. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#methods-as-values).


**added**

**Extractive text shortening.** `similarity.extract(text, max_chars=, max_sentences=, ratio=)` keeps the most informative sentences of a long text, in order, using TextRank over hashed word vectors (CPU-only, parallel), and de-duplicates repetitive logs instead of ranking them; `similarity.sentences(text)` is the splitter behind it. Use it where a long text would otherwise be cut at a fixed length before going to a model. See [scriptling.similarity](https://scriptling.dev/okf/scriptling-libraries/utilities/similarity.md#extracttext-max_charsnone-max_sentencesnone-rationone).


**added**

**Gossip streams.** `cluster.open_stream()` requests a reply of any size from one node and `cluster.handle_stream()` serves it, for files and state transfers beyond the packet limit. Closing a stream, or stopping its cluster, ends a read in progress. See [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md#clusteropen_streamnode_id-message_type-data).


**added**

**Import syntax.** Parenthesized lists (`from m import (a, b,)`) and PEP 810 `lazy import` are accepted; `lazy` imports run immediately. See [Imports](https://scriptling.dev/okf/scriptling-reference/syntax.md#imports).


**fixed**

**F-strings** with slices (`f"{items[1:3]}"`), `!=`, lambdas or braces inside string literals now evaluate correctly.


**changed**

**`html.escape(s, quote=True)`** gains Python's `quote` argument and escapes a single quote as `&#x27;` (previously `&#39;`), matching CPython.


**fixed**

**`similarity.sentences()` and `similarity.tokenize()`** return an empty list for blank text instead of `None`, so the result can always be iterated or measured with `len()`.


**fixed**

**Standard library matches Python.** `Counter` has the full dict API; keyword arguments such as `re` `flags=`, `int(..., base=)`, `itertools.groupby(key=)`, `random.choices(cum_weights=)` and the `textwrap` options are honoured; bounded `deque`s drop from the opposite end; `json.dumps` writes tuples as arrays; `enumerate()` and `zip()` stop on infinite iterators; `isinstance()` accepts exception types; `dict()` accepts mappings and lets keywords win; TOON integers decode as `int`.


**fixed**

**`format()`** applies zero padding, fill, sign and grouping like f-strings: `format(42, "05d")` is `"00042"`. Unknown format codes raise `ValueError`, and `#` (`0xff`), `_` grouping, `c` and `n` are supported.


**fixed**

**Iterators, comparisons and errors.** `map()`, `filter()`, `any()` and `all()` pull from iterators lazily, so they work with `itertools.count()`, and collecting an endless iterator raises an error instead of exhausting memory. `!=` falls back to `__eq__`; `key=` accepts bound methods and callable objects; `zip(strict=True)` works; `except` accepts a variable or tuple of types and the `LookupError`, `ArithmeticError` and `BaseException` parents; `Counter` takes float counts and compares like Python; `textwrap` splits words exactly as CPython does; `random.sample(range(10**9), k)` no longer expands the range. `itertools.islice()` accepts `None` bounds (`islice(it, 2, None)`) and stops at the right element when given a step. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#iteration-utilities) and [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md#exception-type-hierarchy).


**fixed**

**Gossip HTTP transport.** `transport="http"` nodes now serve the gossip endpoint on `bind_addr`; before, they could send but never receive, so HTTP clusters could not form. `encryption_key` is rejected with this transport (use HTTPS), and a node bound to all interfaces needs `advertise_addr`.


**fixed**

**Apple containers** work with container CLI 1.1 and later (tested on 1.5): image pulls, image and volume listing, container status and image removal. See [scriptling.container](https://scriptling.dev/okf/scriptling-libraries/utilities/container.md).


**fixed**

**Concurrency.** A data race when starting `runtime.background()` tasks is fixed, and a server no longer loses its setup script's error when an earlier server in the same process is still shutting down.


---

### v0.27.3


**fixed**

**Pipeline concurrency recovers after a rate limit.** `client.Pipeline`, `completion_parallel` and `ask_parallel` halve their concurrency when a request hits a 429, but never restored it, so one early rate limit left a long run at reduced parallelism to the end. Concurrency now grows back by one after each run of clean completions, up to `max_parallel`, and slot accounting stays exact while the limit changes. See [AI Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md).


**added**

**Hosts can cap script fan-out.** `ai.SetMaxParallelLimit(n)` caps the `max_parallel` a script may request from `client.Pipeline`, `completion_parallel` and `ask_parallel`, and `extlibs.SetRequestsMaxParallelLimit(n)` does the same for `requests.parallel`. A script asking for more silently gets the cap; 0 removes it. One atomic load when the pipeline or batch is created, nothing per request. See [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#script-resource-limits).


**added**

**Backslash line continuation.** A backslash at the end of a line joins it to the next, as in Python, so a long condition or assignment can be split without wrapping it in parentheses. The continuation line's indentation is ignored. See [Syntax](https://scriptling.dev/okf/scriptling-reference/syntax.md#explicit-line-continuation).


**added**

**Process-wide memory guard for script hosts.** `scriptling.SetMemoryLimit(bytes)` sets a ceiling on heap memory held by objects. While the heap stays above it after a garbage collection, the most recently started script is cancelled and its evaluation returns a `memory limit exceeded` error; `scriptling.GetMemoryLimitStats()` reports the heap, running scripts and cancellations. The guard samples the heap on a timer, so it adds no per-instruction cost to scripts. See [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#script-resource-limits).


---

### v0.27.2


**changed**

**Performance.** Script execution is 15% to 30% faster depending on workload and calls into scripts are up to 20x faster.


**changed**

**Comprehensions are about twice as fast.** List, dict and set comprehensions bind their variable through a slot and iterate `range()` directly.


**changed**

**Function bodies compile on first call.** A module that defines many functions now retains compiled code only for the ones that run, reducing memory for library-heavy hosts.


**added**

**Program cache budget is configurable.** Parsed and compiled scripts are kept in a process-wide cache bounded by 64 MiB by default. The CLI gains `--program-cache-max-bytes` (`SCRIPTLING_PROGRAM_CACHE_MAX_BYTES`, `cache.program_max_bytes` in `scriptling.toml`), and Go hosts get `scriptling.SetProgramCacheMaxBytes` plus `scriptling.GetProgramCacheStats` for hit, miss and eviction counts. See [Command-Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md) and [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#program-cache).
