# Architecture

## Purpose

Agent Continuity Stack provides repository-centered continuity through
provider-neutral Agent Skills, memory conventions, client adapters, lifecycle
safeguards, and an optional complete operating-contract template across Codex,
Cursor, Claude Code, and Google Antigravity. The repository owns package source
and validation; it does not ship an executable installer or grant a model
additional authority.

## Design goals

- Keep skills portable, independently versioned, and progressively disclosed.
- Preserve existing custom instructions unless a user explicitly approves a
  reviewed change.
- Separate source integrity from installation-specific rendered integrity.
- Keep every client operation inspectable, scoped, recoverable, and honestly
  classified.
- Keep public content free of workstation, account, credential, and private
  project assumptions.
- Delegate specialist workflows instead of maintaining competing owners.

## Package layers

```text
Package identity and inventory
  manifest.json + VERSION + release-files.json
        |
        +-- Optional operating contract
        |     GLOBAL_CUSTOM_INSTRUCTIONS.md
        |     instruction-pack.json
        |     CLIENT_COMPATIBILITY.md
        |
        +-- On-demand capabilities
        |     skills/
        |     optional_skills/
        |     integrations/
        |
        +-- Model-operated lifecycle
              INSTALL_PROTOCOL.md
              schemas/
              scripts/
              tests/
```

### Package identity

`manifest.json` declares the package, skill inventory, adapters, schemas, and
integrations. `VERSION` and `instruction-pack.json` must agree with it.
`release-files.json` hashes every publishable file except itself. Local secrets,
project `MEMORY.md`, Git metadata, caches, and release archives are not package
content. Project memory remains local and Git-ignored unless sharing is
explicitly authorized.

### Operating contract

`GLOBAL_CUSTOM_INSTRUCTIONS.md` is one complete canonical template. It is
optional for public users but all-or-nothing when selected. The package supports
three instruction modes:

1. `preserve-existing`: install skills without changing instructions;
2. `guided-additions`: review individual additions without claiming the
   complete contract;
3. `complete-contract`: render and install the complete verified template
   through a client-specific preserving adapter.

The template's source hash never changes during personalization. A separate
`rendered_sha256` identifies the exact installed bytes and exists only in
installation records. Explicit user-profile values may replace template fields;
unanswered fields and the empty profile section are removed before installation.
Rendered instructions must contain no template markers.

### Skills

Each skill is a real directory containing `SKILL.md`, optional resources, UI
metadata where applicable, and `skill-manifest.json`. The package version and
individual skill versions are independent. Optional skills remain uninstalled
until explicitly selected.

The active repository is the default work boundary. Sibling repositories are
not scanned without explicit direction or concrete dependency evidence.

### Integrations

An integration declares a narrow ownership boundary with another project. It
does not install that project. Exact-tested compatibility is tied to a declared
version, commit, and content hash so newer upstream versions cannot silently
inherit an old compatibility claim.

## Installation lifecycle

```text
status-only inspection
        |
        v
reviewable plan + digest ---- blockers ----> stop
        |
  explicit approval
        |
        v
client A: journal -> immutable backup -> stage -> recheck -> commit -> smoke
        |
        +-- failure -> restore client A and stop
        |
        v
client B: same isolated lifecycle
        |
        v
receipt + ownership + client status + rollback instructions
```

Cross-client crash atomicity is not claimed. Each selected client is resolved,
journaled, applied, verified, and closed before another client changes.
Receipts are evidence, not executable absolute-path instructions.

## Trust and security boundaries

- A remote repository, release archive, manifest, or checksum is not trusted
  merely because it exists. Immutable references and signatures improve
  authenticity; checksums establish byte integrity only.
- Downloaded helpers are inspected before execution.
- `.env` is local-only, ignored by Git, excluded from release inventory, and
  never needed by installed skills.
- `MEMORY.md` is local-only, ignored by Git, excluded from release inventory,
  and never staged or uploaded without explicit authorization.
- Claude `CLAUDE.local.md` and `.claude/settings.local.json` are local user
  state and remain Git-ignored.
- Backups and lifecycle records live outside every client discovery root.
- Symlinks, junctions, reparse points, special files, path traversal, ambiguous
  ownership markers, and independently unverified roots are rejected.
- Existing local modifications block replacement unless the user approves the
  exact resolution.
- A copied file is not runtime evidence. Verification requires a fresh client
  session and positive plus near-miss tests.

## Client adapters

Client paths and precedence are version-sensitive:

- Codex resolves the active `CODEX_HOME` and its effective `AGENTS` file.
- Cursor uses client-managed User Rules for the complete global contract;
  project MDC is a disposable test adapter.
- Claude Code uses a root `CLAUDE.md` import of canonical `AGENTS.md`; the
  complete global contract remains a separate user rule.
- Antigravity uses a dedicated global `always_on` rule within current per-file
  and aggregate limits.
- Antigravity CLI has a separate, opt-in skill root.

`CLIENT_COMPATIBILITY.md` owns the current adapter details. Documentation is not
substitute runtime proof for an installed client version.

## Validation and release

The dependency-free helpers validate normalized contract bytes, package trees,
schemas, lifecycle records, archives, and inventory. The portable test suite
also exercises negative cases. Python 3.11 is the minimum validation runtime;
Python 3.10 reached end of life in October 2026. A stable release may be
published after its source, inventory, conformance, archive-safety, clean-
commit, CI, and disclosure gates pass. Live client, recovery, and platform
evidence is reported per surface and must never be inferred from source
validation.

Package-level behavior changes increment the package version. Material skill
changes increment that skill's version and content hash. A release is built only
from a clean identified commit, validated after extraction, and accompanied by
an external SHA-256 sidecar.

## Non-goals

- Installing or updating coding clients.
- Synchronizing live conversations or acting as a runtime memory database.
- Guaranteeing that context can never be lost or become stale.
- Acting as a durable transaction engine.
- Storing credentials or personal rendered profiles.
- Replacing repository policy or host safety controls.
- Combining unrelated projects into one instruction or skill scope.
- Reimplementing specialist toolkit workflows already owned elsewhere.
