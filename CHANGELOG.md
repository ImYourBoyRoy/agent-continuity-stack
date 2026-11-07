# Changelog

All notable changes use Semantic Versioning at the package and individual-skill
levels. This project publishes stable releases only.

## 3.2.0 - 2026-11-06

### Changed

- Added a root `CLAUDE.md` that imports canonical `AGENTS.md`, avoiding a
  separately maintained Claude instruction copy.
- Tightened contract-rendering rules to reuse explicit profile values, remove
  unanswered optional fields, omit an empty profile section, and reject
  rendered output that still contains template markers.
- Added `scripts/render_contract.py` so installation guidance has a deterministic
  renderer that verifies the canonical hash, accepts only explicit profile
  values, omits unanswered fields, writes private new output, and refuses to
  overwrite or write into the package.
- Changed installation guidance to reuse choices already supplied and ask only
  about material unresolved choices; `preserve-existing` remains the safe
  default.
- Updated Antigravity's global contract adapter to a dedicated modular
  `always_on` rule using the current documented file and token limits.
- Refreshed Cursor guidance to distinguish account-synced User Rules from the
  documented machine-local user rule files; the account-synced surface remains
  the package default until file-backed behavior is runtime-verified.
- Made `MEMORY.md` local-only, Git-ignored, and excluded from release inventory;
  added ignores and release guards for Codex and Claude local instructions and
  settings.
- Raised the validation-helper minimum to Python 3.11 after Python 3.10 reached
  end of life in October 2026.
- Updated the pinned `actions/setup-python` dependency to v7.1.0 using its
  verified upstream commit SHA; `actions/checkout` remains pinned to v7.0.1.
- Refreshed the Portable Web Toolkit ownership review to release `0.4.0` and
  archived the v3.1.0 Codex smoke evidence instead of treating it as evidence
  for this package version.
- Changed maintainer links and repository-facing Git author/committer attribution
  to the `@imyourboyroy` GitHub identity.
- Added pyenv-native as the project-preferred Python runtime-manager
  recommendation when no user or repository choice exists, with explicit
  permission and package-manager boundaries.
- Extended Git ignores to nested Claude local settings and corrected the smoke
  prompt to preserve one canonical `AGENTS.md` with a Claude import router.
- Updated Antigravity's Workflow note because the documented 2026-10-19 cutoff
  has passed.
- Incremented independent skill versions and refreshed content hashes for the
  instruction-maintenance, memory-maintenance, and client-routing changes.

### Validation

- Bundle, canonical-contract, safe-tree, and portable conformance checks passed
  locally. The suite covers complete, partial, and empty profile rendering,
  local-state ignore and index guards, and archive rejection cases.
- Fresh-session v3.2.0 client runtime smoke tests were not completed in this
  release environment. See the release notes and README for per-client status.

## 3.1.0 - 2026-08-08

### Changed

- Promoted the package to the stable `v3.1.0` release line.
- Added explicit first-run personalization questions to the canonical Expert
  Agent Operating Contract, while keeping profile values as private inputs.
- Kept installation model-operated, status-first, explicitly authorized, and
  best-effort recoverable.
- Removed hard-coded client software versions from the README compatibility
  summary so the package version remains the current release indicator.
- Replaced multiple release tracks with one stable publication gate.
- Updated the validation workflow to the current pinned `setup-python` action
  and synchronized the release inventory.
- Preserved the Antigravity two-fragment adapter because it is a client loading
  requirement, not a release-track split.

### Validation

- Stable package, contract, source-tree, and portable conformance checks pass.
- The release archive passes inventory, extraction-safety, checksum, and
  extracted-suite validation.
- Client runtime coverage remains reported per client and is not inferred from
  source validation.
