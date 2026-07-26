# Contributing

Contributions are welcome when they preserve portability, narrow ownership, and
honest validation claims.

Participation is governed by `CODE_OF_CONDUCT.md`.

## Before changing anything

1. Read `AGENTS.md`, `README.md`, `MEMORY.md`, and `ARCHITECTURE.md`.
2. Inspect the relevant skill manifest, activation cases, integration boundary,
   or lifecycle schema.
3. Check for an existing skill or specialist owner before adding capability.
4. Keep credentials, personal profiles, private paths, and machine-specific
   assumptions out of public source.

## Change rules

- Keep `SKILL.md` frontmatter limited to portable `name` and `description`.
- Keep procedures concise and move conditional detail into directly linked
  resources.
- Preserve existing custom instructions by default.
- Do not add an executable remote installer.
- Do not add symlinks, junctions, reparse points, generated archives, or special
  files.
- Increment an individual skill version and content hash for material skill
  changes.
- Increment the package version for publishable package behavior changes.
- Update documentation, fixtures, smoke cases, and manifests in the same change
  as their owned behavior.

## Validation

Run from the repository root:

```bash
python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env
python3 tests/run_portable_tests.py
```

If lifecycle behavior or a client adapter changes, also run the applicable
disposable conformance scenarios and live-client smoke matrix. A copied file is
not proof of discovery.

## Pull requests

Keep each pull request focused. Describe:

- the problem and ownership boundary;
- behavior and version changes;
- security, compatibility, and rollback effects;
- validation performed and untested surfaces;
- documentation, activation, and memory updates.

Do not include secrets or sensitive vulnerability details in an issue or pull
request. Follow `SECURITY.md` for private reporting.
