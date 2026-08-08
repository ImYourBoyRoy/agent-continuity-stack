# Changelog

All notable changes use Semantic Versioning at the package and individual-skill
levels. This project publishes stable releases only.

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
