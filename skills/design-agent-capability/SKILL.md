---
name: design-agent-capability
description: "Design or consolidate durable agent capabilities: instructions, skills, scripts, integrations, hooks, workflows, subagents, or bundles. Use for repeated workflows or overlap; inventory existing capabilities first."
---

# Design Agent Capability

Choose the smallest durable artifact that solves a demonstrated repeated problem.
This skill chooses and designs the capability type. Once durable instruction
files are selected, use `maintain-agent-instructions` to audit or edit their
actual client and repository surfaces.

## Inventory first

Inspect applicable:

- global and repository instructions
- installed and repository-local skills
- scripts, CLIs, hooks, and CI enforcement
- MCP servers and app connectors
- client-specific commands, workflows, and subagents
- runbooks and templates

Identify ownership and overlap. Prefer strengthening the current owner over
creating another broadly triggered capability.

## Choose the artifact

| Need | Preferred artifact |
|---|---|
| One task or temporary constraint | Prompt/thread context |
| Always-on repository convention | Repository instruction |
| Reusable on-demand procedure or expertise | Agent Skill |
| Deterministic repeatable transformation | Script or CLI |
| External live data or authorized action | MCP/app connector |
| Mechanical lifecycle enforcement | Hook or CI |
| Scheduled or chained operation | Client workflow/automation |
| Isolated delegated role | Client-specific subagent |
| Multi-capability distribution | Client plugin/bundle |

Do not assume every client implements subagents, hooks, plugins, or workflows in
the same way. Read `references/client-surfaces.md` when cross-client support is
required.

## Design a portable skill

1. Use the open Agent Skills core: one directory, exact `SKILL.md`, and YAML
   `name` plus `description`.
2. Put all trigger information in the description.
3. Keep the body imperative, focused, and below 500 lines.
4. Move conditional detail into directly linked `references/`.
5. Add scripts only for deterministic work that is repeatedly reimplemented.
6. Use relative paths within the skill.
7. Describe capabilities before client-specific tool names; provide adapters
   and fallbacks when a tool is optional.
8. Keep exact hosts, paths, credentials, device IDs, repositories, and release
   commands in repository-local overlays.
9. Add optional client metadata only in namespaced locations that other hosts
   can ignore safely.

## Define the contract

Specify:

- discriminative triggers and non-triggers
- required inputs and discovered context
- workflow and decision gates
- allowed mutations and approval boundaries
- tools, optional dependencies, and fallbacks
- failure behavior
- evidence and output contract
- maintenance owner and update source

## Validate

- Run structural validation.
- Scan for personal paths, private hosts, credentials, and client-only
  assumptions.
- Test explicit invocation and representative implicit triggers.
- Test a near-miss prompt that should not trigger.
- Forward-test on a synthetic repository when behavior is complex.
- Confirm instructions do not claim precedence a host does not provide.

Return the inventory, artifact decision, structure, safety boundaries,
portability assessment, tests, and installation options.
