# Client compatibility

Release-candidate assumptions checked against first-party documentation on
2026-07-26. Reverify discovery and precedence against the installed client
before final release or installation.

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

| Client | Complete-contract adapter |
|---|---|
| Codex | Resolve the active `CODEX_HOME`; merge the marked contract block into `AGENTS.override.md` when it exists, otherwise `AGENTS.md`. |
| Claude Code | Copy the complete rendered contract to `~/.claude/rules/expert-agent-operating-contract.md`. |
| Antigravity | Split at the declared heading into two ordered files below 12,000 characters, then import both from `~/.gemini/GEMINI.md`. |
| Cursor | Import the complete rendered contract into the client-managed plain-text User Rules field. Use an MDC file only for a disposable project-level test. |

### Codex

Codex loads user-global guidance from the active `CODEX_HOME`, not necessarily
`~/.codex`. `AGENTS.override.md` takes precedence over `AGENTS.md` when present.
Its instruction chain has a configurable aggregate size limit, commonly
32 KiB. Inspect the effective file and aggregate budget before merging, use the
declared ownership markers, and runtime-test the complete instruction chain.
Refuse installation when the merged global content would crowd out applicable
repository safety instructions under the active byte limit.

### Claude Code

Claude Code loads user-level rules from `~/.claude/rules/` for every project.
Using a dedicated rule avoids overwriting an existing `~/.claude/CLAUDE.md`.
Project `CLAUDE.md` files and repository policy remain separate.

### Antigravity

Antigravity documents `~/.gemini/GEMINI.md` as the global rule and allows
relative `@file` references. Rule files have a 12,000-character limit, smaller
than this contract. Split the canonical source immediately before
`## Critical Reasoning and Red Teaming` into:

- `~/.gemini/expert-agent-operating-contract.part-1.md`
- `~/.gemini/expert-agent-operating-contract.part-2.md`

Place these two lines in `GEMINI.md` in the same order:

```text
@expert-agent-operating-contract.part-1.md
@expert-agent-operating-contract.part-2.md
```

Each rendered segment must remain under 12,000 characters, and their
byte-for-byte concatenation must match `rendered_sha256`. Treat complete import
resolution as a release gate.

### Cursor

Cursor's documented always-global surface is plain-text User Rules in Settings;
User Rules do not use MDC. Do not treat `~/.cursor/rules/` as a supported global
authority without exact-version runtime evidence, and never edit Cursor's
internal settings database. Project `.cursor/rules/*.mdc` remains appropriate
for disposable discovery tests. Cursor skill roots remain candidate paths until
the exact IDE or CLI build demonstrates discovery.

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
- Cursor Rules: <https://docs.cursor.com/context/rules>
- Claude Code memory and rules: <https://code.claude.com/docs/en/memory>
- Antigravity rules: <https://antigravity.google/docs/rules-workflows?app=antigravity>
- Antigravity skills: <https://antigravity.google/docs/skills>
- Agent Skills specification: <https://agentskills.io/specification>
