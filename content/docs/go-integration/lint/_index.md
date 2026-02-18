---
title: Linting
description: Code analysis for detecting syntax errors without execution.
weight: 6
---

The `lint` package provides code analysis functionality for Scriptling scripts. It can detect syntax errors and potential issues without executing the code, making it safe for untrusted input.

## Basic Linting

```go
import "github.com/paularlott/scriptling/lint"

// Lint inline code
result := lint.Lint(`x = 1 + 2`, nil)
if result.HasIssues() {
    fmt.Println(result.String())
}
```

## Linting Files

```go
// Lint a single file
result, err := lint.LintFile("script.py")
if err != nil {
    log.Fatal(err)
}
if result.HasErrors {
    fmt.Println(result.String())
    os.Exit(1)
}

// Lint multiple files
result, err = lint.LintFiles([]string{"a.py", "b.py", "c.py"})
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Checked %d files, found %d issues\n",
    result.FilesChecked, len(result.Errors))
```

## Lint Options

```go
result := lint.Lint(code, &lint.Options{
    Filename: "myscript.py",  // Used for error messages
})
```

## LintError Type

Each issue found is represented as a `LintError`:

```go
type LintError struct {
    File     string   // Source file name (may be empty)
    Line     int      // 1-based line number
    Column   int      // 1-based column (0 if not available)
    Message  string   // Human-readable description
    Severity Severity // "error", "warning", or "info"
    Code     string   // Optional error code
}
```

## Result Type

The `Result` type contains all findings:

```go
type Result struct {
    Errors      []LintError // All issues found
    FilesChecked int        // Number of files linted
    HasErrors   bool       // True if any severity="error" found
}
```

## Processing Lint Errors

```go
result, _ := lint.LintFile("script.py")

for _, err := range result.Errors {
    fmt.Printf("%s:%d: %s (%s)\n",
        err.File, err.Line, err.Message, err.Severity)

    // Check severity
    if err.Severity == lint.SeverityError {
        // Handle errors
    } else if err.Severity == lint.SeverityWarning {
        // Handle warnings
    }
}

// Quick checks
if result.HasErrors {
    fmt.Println("Script has syntax errors")
}
if result.HasIssues() {
    fmt.Println("Script has lint issues")
}
```

## JSON Output

For integration with other tools, you can output results as JSON:

```go
import "encoding/json"

result, _ := lint.LintFile("script.py")
output, _ := json.MarshalIndent(result, "", "  ")
fmt.Println(string(output))
```

Output:
```json
{
  "errors": [
    {
      "file": "script.py",
      "line": 3,
      "message": "expected token COLON",
      "severity": "error",
      "code": "parse-error"
    }
  ],
  "files_checked": 1,
  "has_errors": true
}
```

## Use Cases

- **Pre-execution validation**: Check scripts before running them
- **CI/CD integration**: Fail pipelines on syntax errors
- **Editor integration**: Real-time syntax checking
- **Security scanning**: Validate untrusted scripts without execution

```go
// Example: Validate script before execution
func safeExecute(p *scriptling.Scriptling, code string) (object.Object, error) {
    // First, lint the code
    result := lint.Lint(code, nil)
    if result.HasErrors {
        return nil, fmt.Errorf("script has syntax errors:\n%s", result.String())
    }

    // Safe to execute
    return p.Eval(code)
}
```

## Complete Example

```go
package main

import (
    "fmt"
    "log"
    "os"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/lint"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    // Script to validate and execute
    script := `
def calculate(a, b):
    return a + b

result = calculate(10, 20)
`

    // Step 1: Lint the script
    result := lint.Lint(script, &lint.Options{Filename: "calculator.py"})
    if result.HasErrors {
        fmt.Println("Script has syntax errors:")
        for _, err := range result.Errors {
            fmt.Printf("  %s:%d: %s\n", err.File, err.Line, err.Message)
        }
        os.Exit(1)
    }

    fmt.Printf("Lint passed: %d file(s) checked, %d issue(s) found\n",
        result.FilesChecked, len(result.Errors))

    // Step 2: Execute the script
    p := scriptling.New()
    stdlib.RegisterAll(p)

    _, err := p.Eval(script)
    if err != nil {
        log.Fatal(err)
    }

    // Get the result
    if val, err := p.GetVarAsInt("result"); err == nil {
        fmt.Printf("Result: %d\n", val)
    }
}
```
