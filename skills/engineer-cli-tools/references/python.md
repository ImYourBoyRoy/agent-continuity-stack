# Python CLI notes

- Follow the repository's package and entry-point conventions.
- Prefer `argparse`, Click, Typer, or another existing framework; do not add a
  framework for a trivial command.
- Keep parsing separate from behavior and return explicit exit statuses.
- Use `pathlib`, structured subprocess arguments, and explicit text encodings.
- Avoid importing expensive optional integrations for `--help` and `--version`.
- Test against the declared minimum and primary Python versions.
- Preserve the active lock and build backend.

