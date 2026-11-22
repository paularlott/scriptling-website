---
description: The Scriptling PHP class in FrankenScriptling - running scripts, passing data, libraries, calling PHP functions and limits.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/frankenscriptling/php-api/
sources:
    - resource: https://scriptling.dev/docs/frankenscriptling/php-api/
status: stable
tags:
    - frankenscriptling
    - php
    - api
title: PHP API
type: Guide
---
# PHP API

`new Scriptling()` creates an isolated VM with its own variables. VMs share
nothing, so each request, user or tenant can have its own. The VM is created
on first use, with the libraries the operator's
[configuration](https://scriptling.dev/okf/scriptling-docs/frankenscriptling/configuration.md) allows.

## Running scripts

```php
$vm = new Scriptling();

echo $vm->eval('2 + 3');                          // 5
echo $vm->eval('[1, "a"]');                       // [1, 'a']
echo $vm->evalWithTimeout(500, 'sum(range(10))'); // 45, or an error after 500 ms
echo $vm->evalFile('/app/scripts/report.py');
```

`eval()` returns the value of the script's last expression as a string,
written as Python's `str()` writes it, and `None` when the script ends with a
statement. To get structured data back, read a variable as JSON (below).

## Passing data

```php
$vm->setVar('name', 'Alice');
$vm->setVarInt('count', 42);
$vm->setVarFloat('rate', 0.1);
$vm->setVarBool('active', true);
$vm->setVarNull('missing');
$vm->setVarJSON('order', json_encode(['items' => [20.00, 5.50], 'country' => 'AU']));

echo $vm->eval(<<<'PY'
subtotal = sum(order["items"])
tax = subtotal * rate if order["country"] == "AU" else 0
result = {"subtotal": subtotal, "total": round(subtotal + tax, 2)}
f"{name}: {result['total']:.2f}"
PY);                                               // Alice: 28.05

$result = json_decode($vm->getVarJSON('result'), true);   // ['subtotal' => 25.5, 'total' => 28.05]
$count  = $vm->getVarInt('count');
```

`getVar()` writes any value as `eval()` does, as Python's `str()`; read
lists and dicts as data with `getVarJSON()`.
`setVarList()` and `setVarDict()` take JSON like `setVarJSON()`, and check
that it is an array or an object. `hasVar()`, `listVars()` (a JSON array of
names) and `unsetVar()` manage variables, and `reset()` clears them all and
closes anything the script left open, such as connections.

## Calling PHP functions

`eval()`, `evalWithTimeout()`, `evalFile()` and `callFunction()` take an
optional last argument: an array of name => PHP callable. Each becomes a
function the script can call during that call:

```php
$php = [
    'get_customer' => fn(int $id) => $customers[$id] ?? null,   // closure
    'upper'        => 'strtoupper',                             // function name
    'greet'        => [$greeter, 'greet'],                      // [object, method]
    'shout'        => 'Greeter::shout',                         // static method
];

echo $vm->eval(<<<'PY'
c = get_customer(42)
f"{upper(c['name'])} owes {c['balance'] * 1.1:.2f}"
PY, $php);
```

- **Values convert both ways.** `None`/`null`, bools, ints, floats and
  strings are themselves; lists and tuples become PHP lists; dicts become
  associative arrays in the same order, and PHP arrays come back as lists or
  dicts. Bytes become a string. Anything else is a `TypeError` in the script.
- **Keyword arguments** become PHP named arguments: `add(1, c=5)` calls
  `$add(1, c: 5)`.
- **PHP exceptions** become exceptions the script can catch: `TypeError` and
  `ArgumentCountError` as `TypeError`, `ValueError` and
  `InvalidArgumentException` as `ValueError`, `DivisionByZeroError` as
  `ZeroDivisionError`, `OutOfRangeException` as `IndexError`, and anything
  else as `RuntimeError`, with the PHP message. Uncaught, it ends the script
  like any other error.
- **`exit()` or a fatal error** in a PHP function ends the request as it would
  in plain PHP.
- **Only during the call.** The functions are removed when the call returns,
  so a later call without the array cannot reach them, and a reference the
  script kept raises `RuntimeError`. Nothing is kept between calls, so worker
  mode does not leak.
- **Not sandboxed.** A PHP function runs as ordinary PHP: the Scriptling
  policy does not apply to what it does. Pass only functions the script
  should be able to use.
- A timeout cannot interrupt a PHP function; the script stops once it returns.

## Script libraries and functions

Register libraries written in Scriptling, then import them:

```php
$vm->registerScriptLibrary('pricing', <<<'PY'
def with_tax(amount, rate=0.1):
    return round(amount * (1 + rate), 2)
PY);
$vm->import('pricing');                 // or importMultiple('["pricing", "other"]')
echo $vm->eval('pricing.with_tax(100)');   // 110.0

$vm->registerScriptFunc('add', 'lambda a, b: a + b');
echo $vm->callFunction('add', '[10, 20]');   // 30
```

`callFunction()` takes the arguments as a JSON array (or `""` for none) and
returns the result as a string, like `eval()`.

To load libraries from files, set an autoload path **before** the first
`eval()`, `import()` or `callFunction()`, since the VM is created then:

```php
$vm = new Scriptling();
$vm->setAutoloadPath('/app/libs');      // import foo loads /app/libs/foo.py or foo/__init__.py
$vm->addAutoloadPath('/app/shared');    // searched in order, first match wins
$vm->import('foo');
```

## Output and errors

```php
$vm->enableOutputCapture();
$vm->eval('print("hi")');
echo $vm->getOutput();                  // hi

$vm->eval('1/0');
if ($vm->hasError()) {
    echo $vm->getLastError();           // division by zero (line 1)
    $vm->clearError();
}
```

A script error does not throw in PHP: the call returns an empty string and
`hasError()` is true until `clearError()`. Without output capture, `print()`
goes to PHP's output.

## Limits

```php
$vm->setMemoryLimit(16 * 1024 * 1024);  // lower this VM's memory limit
$vm->setMaxValueBytes(1024 * 1024);     // lower its largest single value
$usage = json_decode($vm->getResourceUsage(), true);   // memory_bytes, peak_memory_bytes, ...
```

PHP can lower the operator's limits for one VM but not raise them;
`getMemoryLimit()` and `getMaxValueBytes()` return the limit in force, `0`
meaning none. Going over the memory limit cancels the call with an error
containing `memory limit exceeded`, and the VM stays usable.

## Reference

| Method | Returns | Description |
| --- | --- | --- |
| `eval(string $code, array $functions = [])` | `string` | Run code, return the last expression |
| `evalWithTimeout(int $ms, string $code, array $functions = [])` | `string` | `eval()` with a time limit |
| `evalFile(string $path, array $functions = [])` | `string` | Run a script file |
| `callFunction(string $name, string $argsJSON, array $functions = [])` | `string` | Call a script function with JSON arguments |
| `setVar`, `setVarInt`, `setVarFloat`, `setVarBool`, `setVarNull` | `void` | Set a variable |
| `setVarJSON`, `setVarList`, `setVarDict` | `void` | Set a variable from JSON |
| `getVar`, `getVarAsString`, `getVarInt`, `getVarFloat`, `getVarBool` | | Read a variable |
| `getVarJSON(string $name)` | `string` | Read a variable as JSON |
| `hasVar`, `listVars`, `unsetVar`, `reset` | | Manage variables |
| `registerScriptLibrary(string $name, string $source)` | `void` | Register a library written in Scriptling |
| `registerScriptFunc(string $name, string $source)` | `void` | Register a function from a `lambda` or `def` |
| `import(string $name)`, `importMultiple(string $namesJSON)` | `void` | Import libraries |
| `setAutoloadPath`, `addAutoloadPath`, `getAutoloadPath` | | Load libraries from directories |
| `enableOutputCapture()`, `getOutput()` | | Capture `print()` output |
| `hasError()`, `getLastError()`, `clearError()` | | Error state of the last call |
| `setMemoryLimit`, `getMemoryLimit`, `setMaxValueBytes`, `getMaxValueBytes`, `getResourceUsage` | | Resource limits |
| `getScriptlingVersion()`, `getImageVersion()`, `getBuildInfo()` | `string` | Versions; `getBuildInfo()` is JSON with the image, Scriptling, FrankenPHP and PHP versions |
