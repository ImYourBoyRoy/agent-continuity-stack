---
name: maintain-project-memory
description: Create, audit, compact, or synchronize the required MEMORY.md and related continuity artifacts. Use after meaningful project work, before a resumable handoff, or when project memory is missing, stale, unsafe, or duplicative.
---

# Maintain Project Memory

Maintain a concise, current `MEMORY.md` for every maintained project. Use it to
route future work without treating it as stronger evidence than source, Git,
manifests, tests, builds, or verified runtime behavior.

## Establish the foundation

Resolve the repository root, read project instructions and relevant README
sections, inspect Git status, and locate `MEMORY.md`. If it is absent, create it
unless the current request is strictly read-only or the repository forbids the
change; in those cases, report the missing required foundation.

Keep `MEMORY.md` as the continuity index. Delegate deep or specialized content:

- issues or `TASKS.md` own large backlogs and acceptance criteria
- ADRs or `ARCHITECTURE.md` own deep durable design decisions
- runbooks own repeatable operations
- `README.md` owns stable usage and onboarding facts
- `CHANGELOG.md` owns release history
- temporary handoffs own short-lived execution state

Link or summarize those authorities without copying them. Read
`references/artifact-selection.md` when ownership is unclear.

## Synchronize compactly

Include only applicable:

- project snapshot and useful working-directory map
- current goals, active work, and exact next action
- architecture notes, decisions, and conventions
- verified resources and dated software-version findings
- important commands and workflows
- known issues, risks, and blockers
- recent material changes
- validation performed and its environment

Label observations, inferences, and proposals. Timestamp volatile external facts.
Replace stale status instead of appending an endless transcript.

After meaningful work, synchronize completed and remaining work, important path
changes, discoveries, decisions, risks, validation, and the next recommended
action. Do not update memory merely to restate a trivial conversation.

## Safety and privacy

- Never record credentials, tokens, private keys, secret values, personal data,
  or sensitive production content.
- Avoid absolute personal paths, private hosts, device IDs, and environment
  dumps.
- Do not claim a model's private memory or chat history is an authoritative
  project source.
- Keep durable guidance in version-controlled, human-reviewable artifacts.
- Let current source, Git state, tests, and runtime evidence override old notes.

## Handoff check

Before finishing substantial work, make sure another contributor can identify:

1. what is complete
2. what is incomplete
3. what evidence exists
4. what must not be repeated or assumed
5. the safest next action

Report the memory file used, stale material removed or flagged, related
authorities updated, sensitive details excluded, and the next action.
