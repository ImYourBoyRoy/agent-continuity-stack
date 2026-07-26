# Model Handoff

## Read first

1. `AGENTS.md`
2. Relevant sections of `README.md`
3. `MEMORY.md`
4. `ARCHITECTURE.md`
5. The authority file for the requested task

Do not begin with a repository-wide scan. Do not read or print `.env`.

## Current state

- Package version: `3.0.0-rc.4`
- Status: release candidate; not globally runtime-verified
- Branch: `main`
- Canonical remote:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack`
- Publication target: GitHub prerelease `v3.0.0-rc.4`
- Initial public commit:
  `a6b1b72059fbca5ebc8c2cd3e1308e2cb36eb118`
- Initial validation: Python `3.10` and `3.14` GitHub jobs passed
- Inventory: 14 core skills and 1 optional, default-uninstalled skill
- Installation: model-operated, status-first, and explicit-approval-only
- Public default: install selected skills while preserving all custom
  instructions

The local repository name is `agent-continuity-stack`. A local `.env`
may exist for maintainer GitHub authentication; it is ignored, mode-restricted,
excluded from release inventory, and never package content.

## Completed

- Consolidated and independently versioned the skill inventory.
- Kept the complete Expert Agent Operating Contract as an optional canonical
  template.
- Added status, plan, journal, ownership, receipt, client-status, and rollback
  schemas.
- Added safe tree, archive, contract, record, and bundle validators.
- Added positive, near-miss, collision, and negative lifecycle fixtures.
- Added exact-tested Portable Web Toolkit ownership boundaries.
- Added public model-install onboarding with preserve, guided-addition, and
  complete-contract modes.
- Added architecture, contribution, security, GitHub workflow, and repository
  hygiene files for public development.
- Renamed the complete package identity to Agent Continuity Stack
  (`agent-continuity-stack`) and bound validators to the canonical repository.
- Enabled repository security controls and protected `main` with the successful
  validation contexts.
- Separated release-candidate publication gates from final stable-promotion
  gates without weakening unresolved runtime, recovery, or platform
  requirements.

## Validation baseline

Run:

```bash
python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env
python3 tests/run_portable_tests.py
```

The last pre-commit run must be recorded in `MEMORY.md`. Source and fixture
success does not prove live installation, client discovery, rollback, or
uninstall.

## Open final stable-promotion gates

- Complete the focused immutable-backup recovery rerun.
- Runtime-test Cursor with authenticated target-version skill discovery.
- Install and runtime-test Claude Code in a disposable environment.
- Prove both Antigravity fragments load in a fresh client session.
- Validate Windows reparse-point and metadata behavior.
- Exercise the public installation prompt end to end across all supported
  clients.
- Review the complete contract's always-on token cost and priority wording.

## Next recommended action

Publish `v3.0.0-rc.4` only after every prerelease integrity gate in
`MERGE_CHECKLIST.md` passes, and disclose every open stable-promotion gate.
Then collect the outstanding live-client, recovery, and platform evidence. Do
not promote RC4 to final `3.0.0` until every final stable-promotion gate passes.

## Handoff discipline

After material work:

- update `MEMORY.md` with durable facts and validation;
- update this file only when the immediate handoff changes;
- update `ARCHITECTURE.md` only for durable system-design changes;
- update `CHANGELOG.md` and versions for published behavior changes;
- leave exact blockers and the next action;
- never include credentials, private paths, logs, or transient model reasoning.
