# Client compatibility

Compatibility assumptions checked against first-party documentation on
2026-11-06. Reverify discovery and precedence against the installed client
before installation or a future package release. Runtime compatibility is
reported separately from documentation and source validation.

## Shared skill format

The canonical skill directories use an exact `SKILL.md` entrypoint with only
portable `name` and `description` frontmatter. Copy selected directories into
the client root; do not require symlinks.

| Client | User skill root | Project skill root |
|---|---|---|
| Codex | `~/.agents/skills` | `.agents/skills` |
| Cursor | Candidate `~/.cursor/skills`; runtime-test the target version | Candidate `.cursor/skills`; runtime-test the target version |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| Antigravity | `~/.gemini/config/skills` | `.agents/skills` |

Antigravity CLI's separate `~/.gemini/antigravity-cli/skills` root is opt-in.
Do not populate both Antigravity roots merely because both directories exist.

## Optional complete global operating contract

`GLOBAL_CUSTOM_INSTRUCTIONS.md` is the canonical source. Verify its normalized
UTF-8/LF `source_sha256`, then render only its
operator-profile placeholders from explicit, verified values. Do not summarize,
silently omit sections, or insert project-specific data.

Installing skills does not install or modify custom instructions. Apply one of
the following adapters only after the operator explicitly selects
`complete-contract`. Existing custom instructions must be preserved according
to `INSTALL_PROTOCOL.md`.

Compute `rendered_sha256` after personalization. Record it in the plan,
transaction receipt, ownership record, and client status—not as a fixed package
value.

Use only explicit user-provided values or a user-designated profile source.
Remove unanswered profile fields from the rendered contract, remove the whole
Operator Profile section when empty, and reject any rendered output containing
template markers.

| Client | Complete-contract adapter |
|---|---|
| Codex | Resolve the active `CODEX_HOME`; merge the marked contract block into `AGENTS.override.md` when it exists, otherwise `AGENTS.md`. |
| Claude Code | Copy the complete rendered contract to `~/.claude/rules/expert-agent-operating-contract.md`. |
| Antigravity | Install one dedicated global rule at `~/.gemini/config/rules/expert-agent-operating-contract.md` with `trigger: always_on`. |
| Cursor | Import the complete rendered contract into the account-synced User Rules in Customize > Rules. Use a file-backed user rule only after confirming its current format and runtime discovery. |

### Codex

Codex loads user-global guidance from the active `CODEX_HOME`, not necessarily
`~/.codex`. `AGENTS.override.md` takes precedence over `AGENTS.md` when present.
Its instruction chain has a configurable aggregate size limit, commonly
32 KiB. Inspect the effective file and aggregate budget before merging, use the
declared ownership markers, and runtime-test the complete instruction chain.
Refuse installation when the merged global content would crowd out applicable
repository safety instructions under the active byte limit.

### Claude Code

Claude Code v2.1.277 and later reads `AGENTS.md` by default when no project
`CLAUDE.md` or `CLAUDE.local.md` is present. If a project `CLAUDE.md` exists,
Claude reads its `CLAUDE.md` files instead of `AGENTS.md` by default. This
repository therefore keeps a root `CLAUDE.md` containing only `@AGENTS.md`, a
documented import that loads the canonical project instructions without a
second copy. Keep any Claude-specific additions below that import and avoid
duplicating shared rules.

The import is also the compatibility path for older Claude Code sessions that
do not load `AGENTS.md` directly. Confirm it with `/context all` in a fresh
session. Claude Code treats instructions as context rather than enforced
configuration; use hooks or other deterministic checks for requirements that
must be enforced.

Claude Code loads user-level rules from `~/.claude/rules/` for every project.
The complete global contract remains a dedicated rule so it does not replace
the user's `~/.claude/CLAUDE.md`. Keep `CLAUDE.local.md` and
`.claude/settings.local.json` out of version control.

### Antigravity

Current Antigravity documentation discovers modular global rules from
`~/.gemini/config/rules/*.md`. Each rule needs YAML frontmatter with a valid
`trigger`; `always_on` loads the full rule every turn. The current per-rule
limit is 24,000 bytes after inline includes, and active global plus always-on
rules share a 20,000-token budget.

Install the complete rendered contract as
`~/.gemini/config/rules/expert-agent-operating-contract.md` with:

```yaml
---
trigger: always_on
description: Complete Expert Agent Operating Contract; always apply.
---
```

The rule body must exactly equal the rendered contract. Verify the complete
file is below 24,000 bytes and review the active aggregate rule budget. The
previous two-fragment import through `~/.gemini/GEMINI.md` is a legacy adapter;
remove its imports or fragments only when package ownership and unchanged
hashes are proven and the migration is explicitly approved.

Antigravity's documented legacy Workflow cutoff was 2026-10-19. That date has
passed; this package uses portable Agent Skills and does not install Workflows.
Verify any residual legacy behavior in the target client instead of assuming
the old Workflow surface remains available.

### Cursor

Cursor documents account-synced User Rules under Customize > Rules. Its current
help also documents machine-local user rule files under `~/.cursor/rules/`
(`%USERPROFILE%\.cursor\rules` on Windows), which do not sync. The package
metadata uses the account-synced User Rules as its default target. Treat the
file-backed format and its behavior as version-sensitive until a fresh-session
test proves discovery; do not assume project `.mdc` files and user rule files
share a format. Never edit Cursor's internal settings database. Project
`.cursor/rules/*.mdc` remains appropriate for disposable project-level tests.
Cursor skill roots also remain candidate paths until the exact IDE or CLI build
demonstrates discovery.

## Runtime evidence

For every selected client, start a new session in a disposable repository and
ask it to identify:

1. the global operating-contract title;
2. the required project foundation files;
3. its default critical-review behavior;
4. the distinction between project instructions, memory, and on-demand skills.

Then test one positive and one near-miss skill prompt. A copied file or a
successful command exit is not proof that the client loaded it.

Record the result with `schemas/client-status.schema.json`. Until a target
version passes, describe its paths as adapter candidates rather than universal
guarantees.

## First-party references

- Codex instruction discovery: <https://developers.openai.com/codex/guides/agents-md/>
- Cursor Rules: <https://cursor.com/docs/rules>
- Cursor user rule storage: <https://prod.cursor.com/help/customization/rules>
- Claude Code memory and rules: <https://code.claude.com/docs/en/memory>
- Antigravity rules: <https://antigravity.google/docs/rules/>
- Antigravity skills: <https://antigravity.google/docs/skills>
- Antigravity Workflows migration: <https://antigravity.google/docs/migration/workflows-to-skills>
- Agent Skills specification: <https://agentskills.io/specification>
