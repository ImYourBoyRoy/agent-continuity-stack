# Project Memory

## Project snapshot

- Package: Agent Continuity Stack
- Current package version: `3.1.0`
- Release status: stable release preparation
- Canonical repository:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack`
- License: MIT
- Purpose: distribute one complete Expert Agent Operating Contract and
  portable on-demand skills across Codex, Cursor, Claude Code, and Antigravity.
- Canonical normalized source SHA-256:
  `7d51bfc6bb0bc4440137acdb95e61eb732a2881e058f5a2f9301629bb5e959d5`
- Inventory: 14 core skills and 1 optional, default-uninstalled skill

## Authority map

- `GLOBAL_CUSTOM_INSTRUCTIONS.md`: canonical public contract template and
  first-run personalization intake
- `instruction-pack.json`: source integrity, rendering policy, and adapters
- `INSTALL_PROTOCOL.md`: model-operated status, authorization, transaction,
  update, and rollback protocol
- `manifest.json`: package, skill, schema, and integration inventory
- `release-files.json`: full release payload inventory and hashes
- `skills/*/skill-manifest.json`: independent core skill versions
- `optional_skills/*/skill-manifest.json`: optional skill versions and policy
- `schemas/`: lifecycle record contracts
- `integrations/`: exact-tested specialist boundaries
- `tests/activation_cases.json`: skill routing fixtures
- `tests/CLIENT_SMOKE_MATRIX.md`: client evidence requirements
- `ARCHITECTURE.md`: durable package, lifecycle, and trust boundaries
- `HANDOFF.md`: concise continuation point for another model
- `.github/workflows/validate.yml`: public CI equivalent of local validation

## Current decisions

- The package publishes stable releases only.
- Installation remains model-operated, status-first, explicitly authorized,
  journaled one client at a time, and best-effort recoverable.
- The complete operating contract remains canonical and unshortened when
  selected. Skills-only installation preserves existing instructions by
  default.
- First-run personalization asks for clients, skill scope, skill selection,
  instruction mode, and each optional operator-profile field. Values are never
  inferred and “leave unset” is accepted.
- The public contract uses placeholders; personalized profile values remain
  installation inputs and are not package content.
- Antigravity's two ordered contract fragments are retained because they are a
  client loader-size requirement, not a release-track split.
- Cross-client atomicity is not claimed. The model journals, applies, validates,
  and closes one client at a time.
- `build-astro-on-cloudflare` is optional and default-uninstalled. It defers to
  Portable Web Toolkit when that toolkit owns the project.

## Validation

On 2026-08-08, the stable source validation completed with zero errors and zero
warnings:

- `python3 scripts/validate_bundle.py`
- `python3 scripts/inspect_contract.py source`
- `python3 scripts/inspect_tree.py . --exclude .git --exclude .env`
- `python3 tests/run_portable_tests.py`
- `git diff --check`

The release inventory and canonical contract hashes were refreshed after the
stable metadata and onboarding changes. Archive construction and extracted-suite
validation remain required before publication.

## Known limitations

- Client runtime evidence is reported per client and must not be inferred from
  source validation.
- Cursor authentication, Claude installation, Antigravity fresh-session
  loading, and Windows filesystem behavior require environment-specific proof.
- Model-operated recovery cannot guarantee locks, `fsync`, ACL/xattr
  preservation, or crash-atomic multi-target rollback.
- Legacy remote release/tag cleanup is a separate destructive GitHub operation
  and is not part of package source validation.

## Next action

Build the stable archive from the identified clean release commit, validate the
archive and checksum, publish the stable `v3.1.0` GitHub Release, then update
this memory and `HANDOFF.md` with the commit, archive, digest, and live release
URL.
