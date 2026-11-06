# Agent Continuity Stack Instructions

## Project purpose and boundary

This repository publishes repository-centered continuity through an optional
portable user-global operating contract, memory conventions, client adapters,
lifecycle safeguards, and on-demand Agent Skills for Codex, Cursor, Claude
Code, and Google Antigravity. Keep skill content independent of an individual
workstation, private project, account, or repository owner.

## Authorities

- `GLOBAL_CUSTOM_INSTRUCTIONS.md` is the canonical complete Expert Agent
  Operating Contract. Do not summarize, trim, or independently edit client
  copies.
- `instruction-pack.json` records its integrity and client adapters.
- `manifest.json` owns package inventory and versions.
- Each `skills/<name>/skill-manifest.json` owns that skill's independent
  version.
- `optional_skills/` contains default-uninstalled capabilities declared
  separately in the package manifest.
- `schemas/` owns model-operated lifecycle record contracts.
- `integrations/` owns exact-tested specialist-toolkit boundaries.
- `INSTALL_PROTOCOL.md` owns installation, update, backup, and rollback
  behavior.
- `CLIENT_COMPATIBILITY.md` records version-sensitive discovery assumptions.
- `ARCHITECTURE.md` records durable component, lifecycle, and trust boundaries.
- `MEMORY.md` is private local continuity; keep it Git-ignored. Never stage,
  commit, release, or upload it without explicit user authorization.
- `HANDOFF.md` records the concise current continuation point for another model.

Repository policy and current host safety instructions retain their actual
client-defined precedence.

## Editing rules

- Use the portable Agent Skills core: exact `SKILL.md` with only `name` and
  `description` frontmatter.
- Keep activation descriptions discriminative and procedures in the body or
  directly linked references.
- Do not add an executable remote installer. Installation remains model-driven,
  status-first, explicitly authorized, journaled one client at a time, and
  best-effort recoverable.
- Keep skill installation independent from custom-instruction installation.
  Preserve existing instructions by default and require explicit review for
  guided additions or the complete contract.
- Keep backups, receipts, baselines, and removed copies outside every client
  discovery root.
- Reject symlinks, junctions, reparse points, and unsupported special files in
  copied or restored trees.
- Do not embed personal identity, home paths, emails, private hosts,
  credentials, device IDs, or private project schemas under `skills/`.
- Maintain one workflow owner. Toolkit-managed Astro + Cloudflare implementation
  belongs to Portable Web Toolkit; generic skills may delegate but must not
  reproduce its commands or configuration systems.
- Keep optional skills uninstalled by default and require collision tests before
  adding one to the core tier.
- Update `README.md`, `MEMORY.md`, `HANDOFF.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, manifests, activation cases, and client smoke tests when
  their owned contract changes.
- Increment a skill version for a material change to that skill. Increment the
  package version for a published package-level change.

## Validation

Run from the repository root:

```bash
python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env
python3 tests/run_portable_tests.py
```

Before release, run the client matrix in `tests/CLIENT_SMOKE_MATRIX.md` against
the supported client versions. A copied file is not evidence that a client
loaded it.

Create a release archive only from an identified clean commit. Record the
commit, release date, archive name, and SHA-256 in the release notes.
