# Node and TypeScript CLI notes

- Preserve the project's package manager, module system, and runtime floor.
- Keep the executable shim thin and put behavior in importable modules.
- Use structured child-process APIs and handle Windows quoting deliberately.
- Avoid relying on shell built-ins for cross-platform behavior.
- Decide whether TypeScript runs from built output or a runtime loader and
  package that choice consistently.
- Keep normal stdout stable and diagnostics on stderr.
- Test packed or installed output, not only source execution.

