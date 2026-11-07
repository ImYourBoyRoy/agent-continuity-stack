# Model Handoff

## Read first

1. `AGENTS.md`
2. Relevant sections of `README.md`
3. `MEMORY.md` when present; it is local-only and must never be staged or
   uploaded without explicit authorization
4. `ARCHITECTURE.md`
5. The authority file for the requested task

Do not read or print `.env`.

## Current release

- Stable package: `3.2.0`, published at
  <https://github.com/ImYourBoyRoy/agent-continuity-stack/releases/tag/v3.2.0>.
- The GitHub release records the tag commit, archive filename, SHA-256, and
  validation results.
- Canonical repository:
  <https://github.com/ImYourBoyRoy/agent-continuity-stack>.
- Maintainer Git author and committer name: `@imyourboyroy`, linked to the
  `ImYourBoyRoy` account with its account-linked no-reply address. Do not use
  the public contact email for Git metadata.
- Minimum validation runtime: Python 3.11.
- When neither the user nor repository selects a Python runtime manager,
  recommend pyenv-native. Never install it or replace a project package manager
  implicitly.

## Package rules and boundaries

- `GLOBAL_CUSTOM_INSTRUCTIONS.md` is the canonical portable contract.
- Root `CLAUDE.md` imports canonical `AGENTS.md` with `@AGENTS.md`; do not
  maintain a second copy of project rules.
- `scripts/render_contract.py` verifies the template hash and renders only
  explicit profile values. It removes unanswered fields and an empty profile
  section, never infers or prompts, and refuses to overwrite or write inside
  the package.
- Installation is status-first, client-by-client, explicitly authorized, and
  rollback-aware. Preserve existing instructions by default.
- `MEMORY.md`, `AGENTS.override.md`, `CLAUDE.local.md`, and
  `.claude/settings.local.json` are local-only. Keep them ignored, untracked,
  and out of release inventories and archives.
- Portable Web Toolkit ownership review targets release `0.4.0` and is static;
  no live toolkit commands were run.

## Verification and compatibility

- Bundle, contract, safe-tree, and portable conformance checks passed locally.
- GitHub Actions passed the Python 3.11 and 3.14 matrix on the release commit.
- The release archive passed inventory, checksum, and extraction checks; the
  extracted package suite passed.
- Fresh-session v3.2.0 runtime smoke tests were not completed. Codex, Cursor,
  and Antigravity are installed but unverified for this package version;
  Claude Code was unavailable. The older Codex 3.1.0 evidence is retained only
  under `tests/evidence/historical/` and is not current runtime evidence.
- Cursor file-backed user-rule behavior and per-client skill roots remain
  version-sensitive. Antigravity and Windows behavior require target-surface
  runtime checks.

## Next action

Run fresh-session smoke tests on available supported clients and record only
evidence tied to the tested package and skill hashes. Do not treat source,
archive, or CI validation as proof that a client loaded instructions or skills.
