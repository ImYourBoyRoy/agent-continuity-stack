# Changelog

All notable changes use Semantic Versioning at the package and individual-skill
levels.

## 3.0.0-rc.4 - 2026-07-26

### Changed

- Renamed the project, repository, package identity, schemas, ownership
  markers, state paths, fixtures, and documentation to Agent Continuity Stack
  (`agent-continuity-stack`).
- Positioned the project explicitly as repository-centered continuity rather
  than a runtime memory service, agent orchestrator, or guarantee against all
  context loss.
- Added public architecture, handoff, contribution, security, CI, Dependabot,
  conduct, issue/PR templates, editor defaults, and local-environment hygiene.
- Prepared the initial public Git repository with pinned GitHub Actions,
  inventory-driven archive validation, and staged-secret checks.
- Published the canonical public repository and enabled validation, dependency,
  vulnerability-reporting, secret-scanning, and protected-branch controls.

## 3.0.0-rc.3 - 2026-07-26

### Changed

- Added a public GitHub identity, explicit installation-policy choices, and a
  complete copy-paste model installation prompt to the README.
- Decoupled skill installation from custom-instruction installation.
- Made skills-only with existing instructions preserved the public default.
- Required an explicit choice between preserving instructions, guided
  additions, and the complete canonical contract.
- Added operator-profile intake, privacy disclosure, plan-digest approval, and
  mode-aware smoke-test requirements to public onboarding.
- Updated plan, receipt, and client-status schemas so skills-only operations
  use a null rendered-contract hash and cannot mutate instruction targets.
- Bound packaged skill runtime evidence to exact skill versions and content
  hashes.

## 3.0.0-rc.2 - 2026-07-26

### Changed

- Replaced the unsafe cross-client atomicity claim with independently journaled,
  one-client-at-a-time best-effort lifecycle operations.
- Resolved Codex targets through the active `CODEX_HOME` and documented
  `AGENTS.override.md` precedence.
- Made Cursor's client-managed plain-text User Rules the global contract
  authority; the MDC adapter is project-test-only unless runtime evidence
  establishes otherwise.
- Added explicit Codex ownership markers for preserving merges and removals.
- Added explicit `verified`, `installed-unverified`, and `failed` client-status
  classifications with semantic consistency checks.
- Bound mutable targets to validated client roots plus relative paths, bound
  recovery artifacts to a state root, and added a per-client operation-journal
  schema.
- Made referenced backups immutable, restore-by-copy snapshots and added backup
  hashes to journals and transaction receipts.
- Began adversarial runtime gating; Codex passed positive and near-miss project
  discovery on `0.146.0-alpha.3`.

## 3.0.0-rc.1 - 2026-07-26

### Changed

- Marked v3 as a release candidate until lifecycle and live-client gates pass.
- Defined canonical source integrity separately from per-install rendered
  integrity.
- Required UTF-8/LF normalization and added repository line-ending controls.
- Added machine-readable installation, status, ownership, transaction, and
  rollback schemas.
- Added deterministic read-only helpers and protocol-conformance fixtures.
- Expanded project-documentation and project-instruction foundation behavior.
- Added an exact-tested Portable Web Toolkit integration contract.
- Restored Astro + Cloudflare expertise as optional and default-uninstalled.
- Expanded package, metadata, archive, privacy, and catalog validation.
- Corrected portable YAML quoting for `design-agent-capability` metadata.

### Unchanged boundaries

- Installation remains model-operated and status-first.
- The package contains no standalone installer application.
- The complete Expert Agent Operating Contract remains canonical.
- Live user-global client configuration is never mutated without explicit
  authorization.

## 3.0.0 - Unreleased final

Promotion to final 3.0.0 requires all lifecycle and live-client release gates,
an identified clean release commit, and a published archive checksum.
