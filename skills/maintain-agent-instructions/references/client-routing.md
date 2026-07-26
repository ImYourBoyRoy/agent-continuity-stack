# Client instruction routing

Verify current client documentation before editing. Use this as a conceptual
map, not a promise of timeless paths.

| Client | User-global contract | Durable repository guidance | On-demand procedure |
|---|---|---|---|
| Codex | `~/.codex/AGENTS.md` | `AGENTS.md` and documented nested overrides | Agent Skill |
| Cursor | supported User Rules; verify global file Rules by version | project Rules | Agent Skill |
| Claude Code | user `CLAUDE.md` or user rules | `CLAUDE.md` and documented nested imports or scopes | Agent Skill |
| Antigravity | global `GEMINI.md` and supported imports | workspace rules | Agent Skill |

Keep one canonical portable instruction source. Install or merge its complete
rendered content through each supported surface without overwriting unrelated
policy. Runtime-test imports, size limits, and version-sensitive global Rules.

Client-specific invocation controls, hooks, subagents, workflows, permissions,
and metadata belong in adapters. The shared `SKILL.md` must still work when
those extensions are ignored.
