---
name: engineer-cli-tools
description: Design, implement, package, or review cross-platform CLI tools. Use for command contracts, configuration precedence, structured output, exit codes, logging, resumability, packaging, and CLI tests—not incidental shell commands.
---

# Engineer CLI Tools

Design the command contract before choosing internal architecture.

## Establish the contract

Define:

- users and execution environments
- commands, arguments, flags, stdin, stdout, and stderr
- exit-code semantics
- interactive versus non-interactive behavior
- configuration sources and precedence
- machine-readable output and stability promises
- destructive actions, confirmation, and dry-run behavior
- cancellation, retries, idempotency, and resumability

Preserve existing behavior unless a breaking change is approved.

## Configuration precedence

Use one documented hierarchy appropriate to the project, normally:

```text
explicit CLI flag
environment variable
project configuration
user configuration
built-in default
```

Do not print secrets or include them in command history. Validate configuration
early and identify the source of invalid values without exposing the values.

## Architecture

- Keep argument parsing thin.
- Put business behavior behind testable functions or interfaces.
- Separate filesystem, network, process, and UI adapters.
- Use typed configuration where supported.
- Make repeated operations idempotent when possible.
- Write partial state atomically.
- Bound concurrency and retries.
- Preserve useful diagnostics while keeping normal stdout stable.
- Provide `--json` or equivalent only when consumers benefit from a stable
  schema.

Read the applicable language guide:

- `references/python.md`
- `references/node-typescript.md`
- `references/rust.md`
- `references/powershell.md`

## Cross-platform behavior

- Use platform path libraries rather than concatenating separators.
- Do not assume a POSIX shell, administrator privileges, or executable bits.
- Quote child-process arguments through structured APIs.
- Handle Unicode, spaces, long paths, signals, and terminal absence.
- Discover tools through configuration or PATH and report exact missing
  prerequisites.
- Keep install and uninstall operations reversible and narrowly scoped.

## Test the contract

Test:

- help and version output
- valid and invalid arguments
- exit codes and stderr separation
- precedence conflicts
- paths with spaces and Unicode
- missing tools, files, credentials, and network
- interruption and retry behavior
- JSON schema when provided
- destructive-operation gates

Use the repository's approved validation path. Report untested platforms
explicitly; do not infer cross-platform success from one host.

## Output

Document the command contract, compatibility or breaking changes, configuration
precedence, packaging impact, tests, and remaining platform uncertainty.
