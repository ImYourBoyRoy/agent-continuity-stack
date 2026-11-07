# Cross-client capability surfaces

Use the open Agent Skills core for portable workflows. Treat every additional
surface as an adapter that requires current client documentation.

## Canonical skill

The portable core is:

```text
skill-name/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
└── assets/        # optional
```

Use only `name` and `description` in the shared YAML frontmatter unless the
target clients have verified support for another common field.

## Persistent instructions

- Codex: user-global and project `AGENTS.md`, with documented nested overrides
- Claude Code: user rules or `CLAUDE.md`; current releases also read project
  `AGENTS.md` by default only when no project `CLAUDE.md` is present. A root
  `CLAUDE.md` can import the canonical file with `@AGENTS.md`.
- Cursor: supported User Rules and project Rules
- Antigravity: documented global rules, modular rule files, and workspace rules

Do not claim one filename has identical discovery or precedence in every host.
Publish one canonical content template separately from versioned adapter and
installation instructions.

## Global skills

Global discovery roots differ and may change. Prefer status-first, model-driven
copying of canonical directories into selected client roots. Do not require
symlinks; some host surfaces or SDKs may canonicalize and reject external
symlink targets.

## Client extensions

Invocation policy, hooks, tool dependencies, subagents, workflows, commands,
plugins, and UI metadata are not universally portable. Place them in
client-namespaced adapters and keep the shared skill useful when they are
ignored.

## Tool language

Describe the capability and decision first:

```text
Use the available first-party repository integration; otherwise use a
read-only local CLI; otherwise report the unavailable evidence.
```

Name a specific tool only when the skill is explicitly about that tool or the
tool is declared as a dependency with a fallback.
