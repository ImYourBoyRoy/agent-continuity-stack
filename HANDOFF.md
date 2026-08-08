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
- Status: stable release preparation
- Branch: `agent/stable-v3.1.0`
- Canonical remote:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack`
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

## Remaining release actions

- Build and validate the stable archive from the clean release commit.
- Generate and independently verify the external SHA-256 sidecar.
- Commit, push, and publish the stable `v3.1.0` GitHub Release.
- Close and remove the obsolete Dependabot branch after its fix is incorporated.
- Treat deletion of any legacy remote release/tag as a separate explicitly
  identified destructive operation.

## Handoff discipline

- Update `MEMORY.md` and this file with the release commit, archive name,
  checksum, and GitHub URL after publication.
- Keep credentials, private paths, logs, and transient reasoning out of both
  files.
