---
name: maintain-project-docs
description: Create or update a project's required README and authoritative contributor, operator, API, migration, and troubleshooting documentation. Use when documentation is missing, stale, publication-bound, or affected by material behavior; verify commands and avoid duplicates.
---

# Maintain Project Docs

Update the smallest authoritative documentation surface that keeps the project
usable and truthful.

Agent control files such as `AGENTS.md`, `CLAUDE.md`, and client rules belong to
`maintain-agent-instructions`, even when they use Markdown.

## Establish the README foundation

Every maintained project requires a current `README.md`. Resolve the project
root and inspect applicable instructions, source, manifests, package metadata,
and existing documentation.

If the root README is missing, create it unless:

- the request is strictly read-only;
- repository policy forbids the change; or
- the apparent root is not the maintained project boundary.

In those cases, report the missing foundation rather than silently substituting
another file.

Keep applicable README content ready for its publication surfaces:

- purpose, maturity, features, requirements, and supported platforms;
- installation, imports, quick start, commands, configuration, and API usage;
- copyable examples and verified representative outputs;
- project layout and important entry points;
- build, test, packaging, release, and troubleshooting guidance;
- security, privacy, license, maintainer, and project links.

For Python packages, verify GitHub and PyPI long-description rendering,
supported Python versions, installation, package imports, public APIs, examples,
metadata, license, and publishing instructions. For other ecosystems, apply the
equivalent package or application publication standard.

## Locate authority

1. Read applicable instructions and identify the intended audience.
2. Inventory existing README files, docs, generated references, examples,
   schemas, runbooks, and release notes relevant to the change.
3. Determine which source owns each fact.
4. Prefer updating that source over adding another document.
5. Treat source, configuration, executable help, and verified behavior as
   stronger evidence than stale prose.

Use `references/document-types.md` when deciding where information belongs.

## Write evidence-backed documentation

- Verify commands, paths, filenames, defaults, environment variables, and
  supported platforms.
- Distinguish required steps from optional examples.
- Mark destructive, privileged, networked, or production commands clearly.
- Use placeholders for credentials, domains, usernames, and machine-specific
  paths.
- Keep examples copyable without embedding secrets.
- Preserve established terminology and link to the canonical definition.
- State limitations and unverified platforms honestly.
- Attribute ownership only from repository metadata or explicit direction.
- Keep README changes in the same work cycle as externally visible behavior,
  interface, command, configuration, installation, or publication changes.

## Prevent drift

Search affected docs after renames or behavior changes. Check:

- internal links and anchors
- command names and flags
- configuration keys and precedence
- API signatures and examples
- supported-version statements
- screenshots and generated samples
- duplicated facts in multiple documents

Do not hand-edit generated documentation unless its source is unavailable and
the exception is recorded.

## Validate proportionally

Use available non-destructive checks such as link validation, rendering,
doctests, example compilation, `--help`, schema validation, or the documentation
build. Verify README commands and examples against current public APIs and
metadata.

When Python packaging is in scope, authorized, and permitted by repository
instructions, applicable evidence may include:

```text
python -m build
python -m twine check dist/*
```

Do not install missing build tools merely to run these checks. Do not run
commands that deploy, delete, install system software, rotate secrets, or mutate
production merely to verify prose.

Report authoritative files changed, facts verified, checks performed, generated
artifacts affected, and remaining uncertainty.
