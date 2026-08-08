# Model Handoff

## Read first

1. `AGENTS.md`
2. Relevant sections of `README.md`
3. `MEMORY.md` when present; private local state, Git-ignored and excluded
   from release archives
4. `ARCHITECTURE.md`
5. The authority file for the requested task

Do not read or print `.env`.

## Current state

- Package version: `3.1.0`
- Status: stable `v3.1.0` published
- Branch: `main`
- Canonical remote:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack`
- Published release:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack/releases/tag/v3.1.0`
- Release commit: `aea50869de75e3036e250cb9551218687520acbc`
- Release archive: `agent-continuity-stack-3.1.0.zip`
- Release archive SHA-256:
  `af03d6704aedebbab126875666ebccadefdaf293f11f614dba59ff52b01626f5`
- Installation: model-operated, status-first, and explicit-approval-only
- Public default: install selected skills while preserving custom instructions
- Inventory: 14 core skills and 1 optional, default-uninstalled skill

## Completed in this release work

- Added explicit first-run personalization questions to the canonical contract.
- Removed hard-coded client and integration software versions from the README
  compatibility summary.
- Converted package metadata and validation to stable `3.1.0`.
- Replaced multiple release tracks with one stable publication checklist.
- Updated the pinned `actions/setup-python` workflow dependency and synchronized
  the release inventory.
- Preserved the Antigravity two-fragment loader adapter as a functional client
  requirement.
- Updated fixtures, contract hashes, release inventory, and project memory.
- Published the stable annotated tag and GitHub Release with the validated ZIP
  and checksum sidecar.
- Closed the obsolete Dependabot pull request and deleted its remote branch.

## Validation baseline

Run from the repository root:

```bash
python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env
python3 tests/run_portable_tests.py
```

The 2026-08-08 run passed with zero errors and zero warnings. This proves
source, metadata, tree safety, schemas, and portable conformance; it does not
prove every installed client's live discovery.

## Remaining maintenance actions

- Treat deletion of any legacy remote release/tag as a separate explicitly
  identified destructive operation.

## Handoff discipline

- Update `MEMORY.md` and this file when stable package behavior or verified
  compatibility evidence changes.
- Keep credentials, private paths, logs, and transient reasoning out of both
  files.
