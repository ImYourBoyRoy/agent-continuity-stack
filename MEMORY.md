# Project Memory

## Project snapshot

- Package: Agent Continuity Stack
- Current package version: `3.0.0-rc.5`
- Release status: unreleased RC5 development; latest public prerelease is RC4
- Canonical repository:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack`
- Published prerelease:
  `https://github.com/ImYourBoyRoy/agent-continuity-stack/releases/tag/v3.0.0-rc.4`
- Release tag: `v3.0.0-rc.4`
- Release commit: `0e24499b9455f1956d0e8390bbd49cf62f908e52`
- Release date: `2026-07-26`
- Release archive SHA-256:
  `e159a83df32dacceb29ca93c118b2cf14b293e790ecd1b636fb33f166f059893`
- License: MIT
- Purpose: distribute one complete Expert Agent Operating Contract and portable
  on-demand skills across Codex, Cursor, Claude Code, and Antigravity.
- Canonical normalized source SHA-256:
  `f5c992564ccd9946b5f2dbfc8d933555085a393a0549f4b7d1fe52b062e7ca5d`
- Inventory: 14 core skills and 1 optional, default-uninstalled skill

## Authority map

- `GLOBAL_CUSTOM_INSTRUCTIONS.md`: canonical public contract template
- `instruction-pack.json`: source integrity, rendering policy, and adapters
- `INSTALL_PROTOCOL.md`: model-operated status, authorization, transaction,
  update, and rollback protocol
- `manifest.json`: package, skill, schema, and integration inventory
- `release-files.json`: full release payload inventory and hashes
- `skills/*/skill-manifest.json`: independent core skill versions
- `optional_skills/*/skill-manifest.json`: optional skill versions and policy
- `schemas/`: lifecycle record contracts
- `integrations/`: exact-tested specialist boundaries
- `tests/activation_cases.json`: core and optional routing fixtures
- `tests/CLIENT_SMOKE_MATRIX.md`: required live-client evidence
- `ARCHITECTURE.md`: durable component, lifecycle, and trust boundaries
- `HANDOFF.md`: concise current continuation point for another model
- `.github/workflows/validate.yml`: public CI equivalent of local validation

## Current decisions

- The complete operating contract remains canonical and unshortened when
  selected. Public installation is opt-in; skills-only with existing
  instructions preserved is the default.
- Guided instruction additions are reviewed partial derivatives and must not be
  represented, owned, hashed, or smoke-tested as the complete package contract.
- Installation is performed by an authorized coding model from a reviewed local
  checkout. No standalone or remote executable installer is shipped.
- Status and planning are read-only; mutation requires explicit target and
  scope authorization.
- `source_sha256` covers canonical UTF-8/LF template bytes.
  Installation-specific `rendered_sha256` belongs only in runtime plans,
  receipts, ownership, and status records.
- Antigravity imports two ordered rendered fragments. Each must remain below
  12,000 characters and their concatenation must equal `rendered_sha256`.
- Cursor global Rules and skill roots remain version-sensitive and require live
  smoke tests.
- Cross-client atomicity is not claimed. The model journals, applies, validates,
  and closes one client at a time; receipts are evidence rather than executable
  path instructions.
- Skills are independently versioned.
- `build-astro-on-cloudflare` is optional and default-uninstalled. It defers
  immediately when Portable Web Toolkit management is established.
- Portable Web Toolkit compatibility is exact-tested against `0.3.1`, release
  commit `cdbc33ff40bedab48fc86bfb7e1ea06a5d81f6f3`, with skill content based at
  `86dddd9efb64c5b4219afe986699135a51e63f83`.
- `red-team-technical-plan` owns explicit deep adversarial review; the global
  contract retains proportional review for ordinary material work.
- Public release candidates and final stable promotion use separate gates.
  Prereleases require clean-commit, source, inventory, conformance,
  archive-safety, CI, checksum, and disclosure evidence. Unresolved
  live-client, recovery, platform, and contract-policy evidence continues to
  block final `3.0.0`.

## Recent material changes

- Converted final-looking v3 metadata to release candidate `3.0.0-rc.1`.
- Added `.gitattributes` and explicit UTF-8/LF/no-BOM integrity policy.
- Corrected canonical versus rendered contract hashing.
- Added seven lifecycle schemas and four deterministic read-only helpers.
- Added schema, rendered-contract, unsafe-tree, archive, and integration
  conformance fixtures.
- Strengthened required README and canonical project-agent-file behavior.
- Added the exact-tested Portable Web Toolkit integration contract.
- Restored Astro + Cloudflare expertise only as an optional fallback.
- Expanded package README, client compatibility, release checklist, and
  validator scope.
- Red-teamed RC1 and rejected final promotion.
- Added skill content hashes and full release-file inventory enforcement.
- Bound plan authorization to canonical content digests and tightened malformed
  lifecycle record rejection.
- Strengthened archive validation for undeclared payloads, CRC, size and
  compression limits, Unicode/case collisions, and Windows extraction hazards.
- Corrected Codex `CODEX_HOME`/override resolution and Cursor User Rules
  authority.
- Added public model-install onboarding and decoupled skills from optional
  custom-instruction installation.
- Renamed the local source root to `agent-continuity-stack`.
- Added architecture, model handoff, contribution, conduct, security, issue,
  pull request, Dependabot, CI, editor, environment-example, and Git-ignore
  foundations for public repository development.
- Separated prerelease publication requirements from final stable-promotion
  requirements while preserving every unresolved final gate.
- Began RC5 development for verified authorship, maintainer links, a
  prerelease-aware badge, and focused GitHub discovery metadata. Published RC4
  remains immutable.
- Added a reciprocal ACS link to Portable Web Toolkit on `main` at
  `c356e7e7b9277eae4f00ed22297f65f56867e958`.
- Featured ACS first in the GitHub profile README at
  `ead0ffdb73303d2f06f8320f16d443f5ab43a81d`.
- Added live `agent-instructions` and `context-engineering` repository topics;
  the existing About description already matched the README authority.
- Reworked Quick Start so the coding agent runs validation, client inspection,
  approved installation, backups, smoke tests, evidence recording, and rollback
  preparation. The user reviews decisions and authorizes mutations rather than
  running implementation commands.
- Configured the authenticated GitHub profile with six ordered pins: ACS,
  Portable Web Toolkit, pyenv-native, OllamaToolkit, WebScraperToolkit, and
  Portfolio Sidekick. GitHub's API verified the order.

## Validation

On 2026-07-26:

- canonical contract comparison with approved source: exact match
- normalized contract source hash: verified
- `python3 scripts/validate_bundle.py`: 14 core, 1 optional, 4,301 catalog
  characters, 0 errors, 0 warnings
- `python3 tests/run_portable_tests.py`: portable source and conformance tests
  passed
- personalized rendered hash differs from source hash: verified
- Antigravity rendered-fragment reconstruction: verified
- valid and invalid lifecycle record fixtures: verified
- symlink, FIFO, case-collision, ZIP traversal, archive symlink, and archive
  case-collision rejection: verified
- RC review ZIP validation, clean extraction, and extracted-suite rerun: passed
- RC review checksum sidecar: generated and independently verified
- disposable RC1 model-conformance exercise: status, install, idempotency,
  conflict, changed-preflight, forced failure, unsafe tree, and rollback
  scenarios passed; 148 schema records validated
- Codex `0.146.0-alpha.3`: fresh-session project contract discovery, explicit
  red-team skill activation, exact skill path, and trivial near-miss passed
- RC2 disposable lifecycle: status-only, 15-target Codex install, idempotency,
  conflict, changed-preflight, unsafe-tree, coherent journals, forced failure,
  and rollback scenarios completed; 44/44 records were schema-valid and
  independently root-applicable
- RC2 recovery exercise exposed a consumed-backup defect; the protocol and
  schemas now require immutable, hashed backup snapshots restored by copy
- RC3 public onboarding and instruction-mode schema changes: bundle validation
  passed with 14 core skills, 1 optional skill, 0 errors, and 0 warnings;
  portable source and conformance tests passed
- Public-repository pre-commit validation on Python `3.14.3`: bundle,
  canonical-contract, safe-tree, and portable conformance checks passed
- Five GitHub YAML files parsed successfully; the validation workflow pins
  official `actions/checkout` `v7.0.1` and `actions/setup-python` `v6.2.0`
  commits and grants read-only contents permission
- Generated an inventory-driven RC3 archive in a temporary directory: 130
  regular files, no unsafe entries, and extracted bundle/tests passed
- Prepared local `main` with 130 staged public files and the verified canonical
  remote; `.env` remained ignored at mode `0600`, and both exact-token and
  common credential-pattern scans found no staged credential
- RC4 comprehensive identity migration: folder, display name, package ID,
  schema URNs, ownership markers, state paths, fixtures, documentation, and
  validator expectations use `agent-continuity-stack`; old-identity scan found
  zero publishable references
- RC4 inventory-driven archive round trip: 130 regular files, 191 total entries,
  no unsafe entries, and extracted bundle/conformance tests passed
- Published the initial public `main` commit
  `a6b1b72059fbca5ebc8c2cd3e1308e2cb36eb118`; local and remote heads matched
- Initial GitHub validation passed on Python `3.10` and `3.14`; the Dependabot
  configuration run also passed
- Enabled private vulnerability reporting, dependency alerts, automated
  security fixes, secret scanning, push protection, and read-only default
  workflow permissions
- Protected `main` with strict required Python `3.10` and `3.14` checks, linear
  history, conversation resolution, and force-push/deletion prevention;
  administrator enforcement remains disabled for maintainer recovery
- RC4 prerelease-policy pre-commit validation: bundle validation passed with 14
  core skills, 1 optional skill, 0 errors, and 0 warnings; canonical-contract,
  safe-tree, and portable conformance validation passed; `.env` remained
  ignored, untracked, and mode `0600`; package version authorities agreed on
  `3.0.0-rc.4`.
- Published GitHub prerelease `v3.0.0-rc.4` on 2026-07-26 from commit
  `0e24499b9455f1956d0e8390bbd49cf62f908e52`. The annotated tag resolves to
  that commit; the release is non-draft and explicitly marked as a prerelease.
  Both the ZIP and checksum sidecar are uploaded, and GitHub's recorded ZIP
  digest matches the independently verified SHA-256.
- Post-publication record pre-commit validation: bundle, canonical-contract,
  safe-tree, and portable conformance checks passed with 0 errors and 0
  warnings.
- RC5 authorship, discovery, and agent-operated Quick Start pre-commit
  validation: bundle validation passed with 14 core skills, 1 optional skill, 0
  errors, and 0 warnings; canonical-contract, safe-tree, and portable
  conformance checks passed. Verified maintainer identity remains outside
  `skills/` and `optional_skills/`.

These are source and conformance results, not live installation or rollback
evidence.

## Risks and next action

- Cursor CLI is present but unauthenticated; Claude Code is not installed;
  Antigravity has no noninteractive agent surface proven here. Those live
  client-status records remain pending.
- The complete contract's 13,898-byte always-on cost and instruction-precedence
  wording remain explicit operator decisions; the canonical contract was not
  changed during RC2 hardening.
- Model-operated recovery cannot guarantee locks, `fsync`, ACL/xattr
  preservation, or crash-atomic multi-target rollback; no mutation executor
  exists.
- The immutable-backup correction still requires a focused recovery rerun.
- The RC4 copy-paste GitHub installation prompt has source/conformance coverage
  but not a complete four-client live installation exercise.
- Windows reparse-point behavior needs a Windows validation run.
- RC4 is published as an explicitly labeled prerelease. Its publication is not
  completion of any open stable-promotion gate.

Next: collect the remaining live-client, recovery, platform, and
contract-review evidence before promoting final `3.0.0`.
