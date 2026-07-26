# Rust CLI notes

- Follow workspace structure and the repository's supported Rust toolchain.
- Keep parsing in the binary crate and test behavior through library functions
  where practical.
- Use typed errors internally and concise actionable diagnostics at the boundary.
- Define exit behavior intentionally.
- Avoid panics for ordinary input, filesystem, process, or network failures.
- Keep feature flags and optional native dependencies explicit.
- Validate packaged binaries on each claimed target through the approved build
  infrastructure.

