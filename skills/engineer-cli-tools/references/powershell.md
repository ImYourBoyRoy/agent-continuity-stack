# PowerShell CLI notes

- Support the project's declared Windows PowerShell or PowerShell version.
- Use advanced-function parameter binding and validation where appropriate.
- Preserve object output for pipeline consumers; format only at presentation
  boundaries.
- Use `-LiteralPath` for user paths and avoid string-built command execution.
- Respect `-WhatIf` and `-Confirm` semantics for mutating operations when
  applicable.
- Keep noninteractive execution free of hidden prompts.
- Test paths with spaces, execution-policy constraints, and non-administrator
  operation.

