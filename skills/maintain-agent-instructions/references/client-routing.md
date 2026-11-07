# Client instruction routing

Verify current client documentation before editing. Use this as a conceptual
map, not a promise of timeless paths.

| Client | User-global contract | Durable repository guidance | On-demand procedure |
|---|---|---|---|
| Codex | `~/.codex/AGENTS.md` | `AGENTS.md` and documented nested overrides | Agent Skill |
| Cursor | account-synced User Rules; documented machine-local user rule files (verify format by version) | project `.cursor/rules/*.mdc` or `AGENTS.md` | Agent Skill |
| Claude Code | user `CLAUDE.md` and user rules | `AGENTS.md` by default when no project `CLAUDE.md` exists; use `CLAUDE.md` with `@AGENTS.md` when a bridge is needed | Agent Skill |
| Antigravity | global standalone rules or `~/.gemini/config/rules/*.md` | `AGENTS.md`, `GEMINI.md`, or `.agents/rules/*.md` | Agent Skill |

Keep one canonical portable instruction source. Install or merge its complete
rendered content through each supported surface without overwriting unrelated
policy. Runtime-test imports, size limits, and version-sensitive global Rules.

Client-specific invocation controls, hooks, subagents, workflows, permissions,
and metadata belong in adapters. The shared `SKILL.md` must still work when
those extensions are ignored.
