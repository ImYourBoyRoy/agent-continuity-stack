---
name: maintain-agent-instructions
description: Create, audit, or edit required project agent instructions and durable Codex, Cursor, Claude Code, or Antigravity guidance. Use for missing AGENTS.md, global contracts, CLAUDE.md, and Rules while preserving precedence, privacy, and rollback.
---

# Maintain Agent Instructions

Keep durable guidance scoped, verifiable, and distinct from on-demand
procedures. When this package's Expert Agent Operating Contract is in scope,
preserve the complete canonical contract; its size alone is not a reason to
replace it with a summary.

## Discover before mutation

1. Identify the clients and versions in scope.
2. Read current first-party discovery and precedence documentation when
   behavior may have changed.
3. Inventory global, repository, nested, override, rule, and managed-policy
   sources actually visible to those clients.
4. Ask each available client to summarize loaded instruction sources when a
   safe diagnostic exists.
5. Treat undocumented filenames as ordinary documentation unless configuration
   proves the client loads them.
6. Report the discovered sources, owners, precedence, conflicts, and proposed
   exact targets before editing.

For an installation or update of this package, read the package
`INSTALL_PROTOCOL.md` and `instruction-pack.json`. Status inspection is the
default. Do not mutate live user-global instructions without explicit
authorization for the named clients and targets.

Use `references/client-routing.md` for the surface map, then verify current
paths rather than assuming the reference is timeless.

Discovery and audit are read-only. Require explicit authorization for the exact
files and scopes to create, merge, move, or replace. Authorization for a
repository file does not imply authorization for global, managed, or sibling
repository guidance.

## Establish the project instruction foundation

Every maintained project requires one canonical project agent instruction file.
Resolve the repository root and inspect `AGENTS.md`, `AGENT.md`, supported
client adapters, and nested instruction files.

If no canonical project file exists, create root `AGENTS.md` unless:

- the current request is strictly read-only;
- repository policy forbids the change; or
- the repository explicitly establishes another canonical filename.

In those cases, report the missing or alternate foundation. Prefer `AGENTS.md`
for portable project guidance. Do not maintain independent, contradictory
`AGENT.md` and `AGENTS.md` bodies; when compatibility requires both, keep one as
a concise router to the declared canonical file.

Include only applicable durable repository guidance:

- purpose, boundary, and important entry points;
- supported build, test, packaging, release, and deployment workflows;
- remote-only, platform-specific, or resource restrictions;
- generated, protected, private, or externally managed paths;
- architectural invariants and recurring hazards;
- project-local skills, tools, subagents, and runbooks;
- mutation, approval, documentation, and memory responsibilities.

Keep current task state, session history, large backlogs, and deep architecture
in their proper artifacts. Update project instructions when durable workflow,
safety, validation, architecture, or tooling rules change.

## Classify every instruction

Place:

- the complete approved operator contract in supported user-global guidance
- other personal interaction preferences in supported user-global guidance
- repository-wide commands and constraints at the repository root
- subtree-specific rules near the governed code
- reusable multi-step procedures in Agent Skills
- deterministic enforcement in linters, hooks, CI, or scripts
- live external data and actions behind authorized integrations
- temporary constraints in the current prompt or thread

Do not maintain independently edited copies merely for symmetry. Use one
canonical content source plus the smallest required client adapters. An adapter
may contain a rendered copy when the host cannot import the canonical source;
verify it against the source hash.

## Preserve precedence and ownership

- Follow the host's actual precedence rather than inventing a universal order.
- Keep stronger managed and repository policy intact.
- Resolve contradictions explicitly.
- Avoid instruction loops such as two files declaring each other authoritative.
- Keep commands beside the repository that owns them.
- Do not put project-specific hosts, devices, paths, package identifiers, or
  release commands in a public global core.
- Never overwrite managed policy. Treat system-, administrator-, organization-,
  and client-managed guidance as read-only unless its own management surface is
  explicitly in scope.

Read `references/instruction-review.md` before consolidating large instruction
sets.

## Protect portability and privacy

Exclude from public or global instruction artifacts:

- personal names, usernames, emails, profiles, and home paths
- credentials, tokens, private keys, and environment dumps
- private hosts, IP addresses, device IDs, and internal project schemas
- assumed client-only tools without a capability fallback
- claims that an instruction file outranks system, administrator, or user
  policy

Use placeholders only in user-facing templates that require configuration.
Prefer repository discovery over persistent placeholders when values already
exist in project metadata.

## Validate

- Capture original content, permissions, and hashes for every authorized target.
- Write through a same-directory temporary file and atomic replacement when the
  platform supports it.
- Preserve a restorable backup or version-control rollback before replacement.
- Inspect the before-and-after diff and reject unrelated instruction churn.
- Check file size, import behavior, aggregate limits, and truncation limits.
- Confirm the intended client discovers the file.
- Start a new session and test the contract identity, one representative rule,
  and one intended repository override.
- Verify procedures activate through skills rather than bloating every session.
- Search for duplicated, stale, contradictory, personal, and machine-specific
  content.
- Report clients that could not be runtime-tested.

If any selected client does not load the complete contract, classify that
client as failed or installed-unverified rather than silently accepting a
summary. Restore only files changed by this operation when rollback is needed.
Do not discard unrelated repository or user changes. Report the recovery
location and any global or managed sources left untouched.

## Output

Report instruction sources, scope and precedence, rules retained or moved,
conflicts resolved, client adapters, privacy scan, runtime evidence, and
remaining compatibility uncertainty.
