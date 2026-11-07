# Agent Continuity Stack

[![Validate](https://github.com/ImYourBoyRoy/agent-continuity-stack/actions/workflows/validate.yml/badge.svg)](https://github.com/ImYourBoyRoy/agent-continuity-stack/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ImYourBoyRoy/agent-continuity-stack?label=release)](https://github.com/ImYourBoyRoy/agent-continuity-stack/releases)

> Keep project rules and context consistent across coding agents.

Version `3.2.0` is the current stable release for repository-centered
instructions, skills, memory conventions, client adapters, and lifecycle
safeguards across Codex, Cursor, Claude Code, and Google Antigravity. This is not a
runtime memory service, agent orchestrator, or guarantee of identical behavior
across every client installation.

Current release:
[v3.2.0](https://github.com/ImYourBoyRoy/agent-continuity-stack/releases/tag/v3.2.0).

## Repository identity

Repository and package ID: `agent-continuity-stack`

Canonical repository:
[ImYourBoyRoy/agent-continuity-stack](https://github.com/ImYourBoyRoy/agent-continuity-stack)

GitHub description:

> Repository-centered instructions, skills, memory conventions, client
> adapters, and lifecycle safeguards for consistent work across AI coding
> agents.

Topics: `agent-skills`, `agent-memory`, `ai-agents`, `coding-agents`, `codex`,
`cursor`, `claude-code`, `antigravity`, `developer-tools`, and
`workflow-automation`, `agent-instructions`, and `context-engineering`.

## Synopsis

The package supports continuity through three coordinated layers:

1. `GLOBAL_CUSTOM_INSTRUCTIONS.md` is the complete Expert Agent Operating
   Contract template. It is canonical and must not be shortened when a user
   explicitly chooses the complete contract. Public installation is opt-in:
   installing skills does not authorize replacing or merging existing custom
   instructions.
2. `skills/` contains progressively disclosed workflows. Each skill is
   independently versioned and follows the portable Agent Skills format,
   including project-instruction, documentation, memory, verification, update,
   and release workflows.
3. Client adapters, lifecycle schemas, integrity checks, ownership records,
   rollback procedures, and runtime smoke tests make installation reviewable and
   honest across supported coding agents.

Repository policy and host-managed safety instructions retain the precedence
assigned by each client. The global contract does not grant tools, permissions,
or authority withheld by the host or repository. Continuity is
repository-centered: the package does not synchronize live conversations or
provide a shared runtime memory database.

## Current compatibility status

| Surface | Source/structure | Live runtime |
|---|---|---|
| Codex | Current package checks validate source and adapters | Existing smoke evidence is for v3.1.0 / Codex 0.146.0-alpha.3 only; no v3.2.0 runtime proof yet |
| Cursor | Current docs and source structure reviewed; skill roots remain version-sensitive | Live discovery must be verified in the target environment |
| Claude Code | Root `CLAUDE.md` imports canonical `AGENTS.md`; current discovery rules reviewed | Claude Code is not installed in this environment; pending |
| Antigravity | Dedicated global always-on rule adapter reviewed against current docs | No live discovery proof for this package version; pending |
| Model-operated lifecycle | Schemas and conformance fixtures | Best-effort disposable exercise; never crash-atomic across clients |

Stable publication requires the gates in `MERGE_CHECKLIST.md`.

## Requirements

- A reviewed local checkout or immutable release archive.
- A coding agent with filesystem access explicitly authorized for the selected
  clients and scope.
- Python 3.11 or newer only for the dependency-free validation helpers.
- The target coding client for runtime discovery and smoke testing.

The skills themselves are Markdown and do not require Python. Do not execute a
remote installation script or install every supported client automatically.

## Quick start

Open the reviewed checkout in the selected coding client and give the coding
agent this prompt. The agent performs the inspection and commands; the user
reviews decisions and authorizes mutations rather than acting as a command
runner.

```text
Work from this reviewed checkout. Read AGENTS.md, README.md,
INSTALL_PROTOCOL.md, CLIENT_COMPATIBILITY.md, and the applicable repository
instructions.

Perform the package inspection yourself without changing client state:

python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env \
  --exclude MEMORY.md --exclude AGENTS.override.md \
  --exclude CLAUDE.local.md --exclude .claude/settings.local.json
python3 tests/run_portable_tests.py

Then inspect my installed coding-client versions, resolve their actual
instruction and skill roots, inventory existing instructions and skills, and
report status only. Do not install, merge, replace, update, create backups, or
change client configuration until I approve the exact plan, targets, conflict
handling, backup locations, tests, and rollback.

Do not ask me to run commands, inspect files, create backups, perform the
installation, or execute smoke tests. Those are the coding agent's
responsibilities within the authorized environment. Ask me only for decisions,
missing information that cannot be discovered safely, or authorization for the
reviewed mutation plan.
```

Status and planning are read-only. After approval, the coding agent executes
the approved work itself, creates and verifies backups, performs fresh-session
smoke tests, records lifecycle evidence, and reports the completed result and
rollback path.

## Resolve installation choices

Resolve choices from the user's request and explicitly designated preferences
before asking questions. Do not ask the user to repeat supplied choices. Ask
only when a materially important choice remains unresolved and has no safe
documented default.

| Decision | Safe choices |
|---|---|
| Clients | Any explicit subset of Codex, Cursor, Claude Code, and Antigravity |
| Skill scope | User-global, one or more named repositories, or both |
| Skill set | All core skills, a named subset, and separately named optional skills |
| Existing instructions | Preserve unchanged; guided additions; or explicitly install the complete contract |
| Operator profile | Use explicit values already available from the user or a user-designated profile; omit unanswered optional fields |

`preserve unchanged` is the public default. Treat the operator profile as
optional personalization: reuse explicit values already available, omit
unanswered fields, and do not prompt for missing optional values by default.
`guided additions` means the model
proposes individually reviewable provisions for the user's existing
instructions; it is not the canonical complete contract and must not be
recorded or smoke-tested as one. `install the complete contract` installs the
entire verified template through the client adapter and requires explicit
approval.

Operator-profile fields are optional:

- name;
- email;
- personal site;
- GitHub profile;
- PyPI profile.

Use explicit values already present in the user's instructions or a
user-designated profile source; do not ask the user to repeat them. Do not
prompt for missing optional values by default. Remove every unanswered field
from the rendered instructions, and remove the entire Operator Profile section
when no values remain. An installed contract must contain no `{{...}}` template
markers. Never infer identity or ownership from a username, Git metadata,
environment file, or neighboring repository. Explain that included values in
always-loaded instructions may be sent to selected model providers.

Do not copy the raw template into a client. Create the profile JSON and rendered
contract in transaction staging outside the package and every client discovery
root, then use the deterministic renderer and inspector:

```bash
python3 scripts/render_contract.py \
  --profile-json <transaction-root>/operator-profile.json \
  --output <transaction-root>/rendered-contract.md
python3 scripts/inspect_contract.py rendered \
  <transaction-root>/rendered-contract.md
```

Use `{}` for a profile with no supplied fields. The renderer never prompts or
infers values, rejects unexpected fields, omits unanswered profile bullets,
and refuses to write personalized output inside the package. Show the inspected
result for review before installing it. Remove temporary profile and rendered
files after installation or rollback unless the user asks to keep them.

## Copy-paste installation prompt

Give the following prompt to a coding model. Replace `<PACKAGE_SOURCE>` with a
local package root or canonical GitHub repository URL, and replace
`<RELEASE_TAG_OR_COMMIT>` with an immutable reviewed release tag or commit. Do
not paste credentials into the prompt.

```text
Safely prepare and, only after my separate approval, install Agent Continuity
Stack from <PACKAGE_SOURCE> at <RELEASE_TAG_OR_COMMIT>.

If the source is remote, acquire that exact tag or commit into a temporary
location without executing repository code. Do not install from a moving branch
such as main. Inspect downloaded helpers before running them, verify a published
archive checksum or signed release/tag when available, and report when
authenticity evidence is absent. A checksum proves byte integrity, not that the
publisher or content is trustworthy.

After the source is locally staged, treat README.md, INSTALL_PROTOCOL.md,
CLIENT_COMPATIBILITY.md, manifest.json,
instruction-pack.json, VERSION, release-files.json, and the external release
checksum as the package authorities. Do not run a remote install script. Do not
assume client paths from documentation or folder existence.

Phase 1 is read-only:
1. Validate the package, its file inventory, contract source hash, and archive
   checksum when an archive/sidecar is provided.
2. Detect the actual installed versions and effective instruction/skill roots
   for Codex, Cursor, Claude Code, and Antigravity. Mark absent or unverified
   clients honestly.
3. Inventory existing user-global and project-local instructions, skills,
   duplicates, ownership markers, local modifications, precedence, instruction
   budgets, and unsafe trees. Do not expose secrets in the report.
4. Resolve client selection, skill scope and set, and Antigravity CLI support
   from my request and user-designated preferences. Do not ask me to repeat
   choices I have already supplied. Ask only about an unresolved choice that
   materially changes the plan and has no safe documented default.
5. Use `preserve-existing` as the default instruction mode. Do not ask me to
   choose a different mode unless my request calls for changing existing
   instructions; `guided-additions` and `complete-contract` require explicit
   selection. The available modes are:
   A. Preserve all existing custom instructions and install skills only
      (default).
   B. Preserve existing instructions and propose specific, line-by-line
      compatible additions for my approval. Do not call this the complete
      package contract.
   C. Install the complete Expert Agent Operating Contract using
      the documented preserving adapter. Never replace an unrelated instruction
      file wholesale.
6. For B or C, show the current effective instruction sources and
   conflicts first. For B, ask which behavior categories I actually want,
   propose exact additions, and default unselected categories to no change. For
   C, require my acceptance of the complete template. Reuse explicit operator
   values already available in my instructions or user-designated profile; do
   not ask me to repeat them. Ask only for a missing value I specifically want
   included or that the selected task requires. Remove unanswered fields, omit
   the whole profile section when empty, and reject any rendered file that still
   contains a template marker. Build a temporary JSON profile from only those
   explicit values, run `scripts/render_contract.py` and
   `scripts/inspect_contract.py rendered`, and show the rendered result for
   review. Keep those files outside the package and client discovery roots;
   remove them after installation or rollback. Explain provider exposure
   before installing personal values. Never infer values or ownership from Git
   or repository data.
7. Produce a client-by-client plan with exact targets, operations, independently
   resolved allowed roots, package and skill versions, hashes, immutable backup
   location outside discovery roots, recovery/rollback steps, and smoke tests.
   Validate the plan with --require-applicable and independently supplied
   allowed roots. Stop for my approval of the exact plan digest.

Do not mutate anything during Phase 1. Approval to inspect or plan is not
approval to install.

After I explicitly approve the exact plan:
8. Apply one selected client at a time. Recheck hashes and plan digest before
   mutation; preserve locally modified content; reject links, reparse points,
   special files, traversal, ambiguous markers, and unsupported targets.
9. Use immutable verified backups and lifecycle records outside every skill or
   rule discovery directory. Restore the current client before proceeding if
   its operation fails.
10. Start a fresh session in each selected client and execute
    tests/CLIENT_SMOKE_MATRIX.md. Test instruction discovery only for instruction
    mode C. For installed skills, run positive and near-miss activation tests,
    confirm the active repository is the default boundary, check that unrelated
    sibling repositories are not explored, and verify critical findings against
    source.
11. Report each client as verified, installed-unverified, or failed. A copied
    file is not proof of discovery. Include exact rollback instructions and
    unresolved compatibility issues. Do not claim global success while any
    selected surface is unverified.
```

The prompt intentionally separates inspection, authorization, installation,
and runtime proof. A model that cannot perform a selected client's new-session
smoke test must finish with `installed-unverified`, not silently treat copying
as success.

## Package layout

```text
GLOBAL_CUSTOM_INSTRUCTIONS.md   canonical public contract template
CLAUDE.md                       Claude Code import of canonical AGENTS.md
instruction-pack.json           source integrity and client adapters
manifest.json                   package, skill, schema, and integration inventory
release-files.json              complete file-and-hash inventory (excluding itself)
ARCHITECTURE.md                 durable package, lifecycle, and trust design
MEMORY.md                       private local project state; Git-ignored and excluded from releases
HANDOFF.md                      concise continuation point for another model
skills/                         default core skills
optional_skills/                default-uninstalled skills
schemas/                        model-operated lifecycle record contracts
integrations/                   exact-tested specialist-toolkit boundaries
scripts/                        validation and isolated contract-rendering helpers
tests/                          fixtures, activation cases, and smoke matrix
INSTALL_PROTOCOL.md             authorization, transaction, and rollback protocol
CLIENT_COMPATIBILITY.md         version-sensitive client surfaces
```

## Public development

The repository includes least-privilege GitHub Actions validation,
dependency-update configuration for pinned Actions, issue and pull-request
templates, contribution guidance, a code of conduct, editor defaults, and
private security-reporting guidance.

A local `.env` is optional maintainer state, never package content. It is
ignored by Git, excluded from release inventory, and must remain readable only
by its owner. `MEMORY.md` is private local continuity state and is also
Git-ignored and excluded from releases. User-specific `AGENTS.override.md`,
`CLAUDE.local.md`, and `.claude/settings.local.json` are ignored by Git and
rejected by release validation. `.env.example` documents the optional variable
name without a credential.
Installed skills and validation do not require a GitHub token.

See `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ARCHITECTURE.md`,
and `HANDOFF.md` before making a public release change.

## Core skills

| Skill | Owns |
|---|---|
| `audit-project-updates` | Read-only dependency, toolchain, security, and upstream enhancement audits |
| `apply-project-updates` | Authorized, reversible implementation of selected update batches |
| `research-software-versions` | Compatibility and migration research for one selected component |
| `verify-software-change` | Risk-based evidence for completion claims |
| `engineer-cli-tools` | Cross-platform CLI contracts, architecture, packaging, and tests |
| `maintain-agent-instructions` | Required project instructions and scoped client guidance |
| `maintain-project-docs` | Required README and authoritative project documentation |
| `maintain-project-memory` | Private local `MEMORY.md` continuity and handoff hygiene |
| `design-agent-capability` | Instructions, skills, scripts, integrations, hooks, and workflow selection |
| `web-discovery-artifacts` | Provider-neutral public-web discovery |
| `maintain-web-design-system` | Provider-neutral design systems and accessibility |
| `prepare-web-assets` | Provider-neutral asset preparation and integration |
| `red-team-technical-plan` | Proportional adversarial review of material technical plans |
| `release-web-application` | Provider-neutral staged and reversible web releases |

## Python runtime recommendation

When a Python project needs a runtime manager and neither the user nor the
repository has selected one, this project recommends
[pyenv-native](https://github.com/ImYourBoyRoy/pyenv-native) for installing and
selecting Python runtimes and managing project virtual environments. The
recommendation was reviewed against upstream `v0.6.0` on 2026-11-05; check the
[current stable release](https://github.com/ImYourBoyRoy/pyenv-native/releases/latest)
before acting. Upstream `v0.6.0` lists Windows, Linux, and macOS as supported;
Android/Termux is experimental.

This is a preference, not a required dependency or automatic installation.
Respect an existing project runtime manager, interpreter pin, package manager,
and lockfile. If `pyenv` is already on `PATH`, identify its implementation and
managed root before proposing a change; do not overwrite or reinterpret an
existing pyenv installation. Do not install pyenv-native, enable its MCP
server, or change a runtime without the user's authorization. Its runtime and
environment tools can change the host or project; inspect the current
[MCP guide](https://github.com/ImYourBoyRoy/pyenv-native/blob/v0.6.0/docs/MCP.md)
and obtain authorization for each requested mutation.

## Optional skills

`build-astro-on-cloudflare` is stable but default-uninstalled. Select it only
for Astro-to-Cloudflare boundary work where Portable Web Toolkit does not
manage the project. It must defer immediately when toolkit management is
established.

## Optional global contract rendering

`instruction-pack.json` records the SHA-256 of the public, unrendered,
UTF-8/LF template. When complete-contract mode is explicitly authorized:

1. verify normalized template integrity;
2. render only permitted operator-profile placeholders;
3. compute the installation-specific `rendered_sha256`;
4. generate client adapters from those rendered bytes;
5. record both source and rendered hashes in plans, receipts, ownership, and
   client status.

The package never contains a fixed rendered hash or rendered personal profile.
Use explicit values already provided by the user or a user-designated profile.
Unanswered optional fields are removed from rendered instructions, and the
Operator Profile section is omitted when empty. The installed output must
contain no placeholder markers. Personalizing an always-loaded contract sends
included values to each selected model provider whenever the contract is
loaded; disclose that consequence before installation.

## Model-operated installation

There is no standalone installer application. The coding model follows
`INSTALL_PROTOCOL.md`, uses the bundled schemas, and may use deterministic
helpers for read-only inspection and validation.

For the approved scope, the model must:

1. detect client versions and actual destinations;
2. report status before mutation;
3. produce a reviewable plan;
4. obtain explicit authorization;
5. preserve existing instructions unless an exact merge or marked block was
   approved;
6. stage every selected target and preserve displaced content outside discovery
   roots;
7. apply one approved client operation at a time;
8. record ownership and recovery information;
9. start new sessions and run runtime smoke tests.

A copied file is not proof that the client loaded it.

## Portable Web Toolkit integration

The exact-tested optional integration targets Portable Web Toolkit `0.4.0` at
the immutable release commit recorded in `integrations/portable-web-toolkit.json`.
The static ownership review covers the current discovery and accessibility
skills, but does not claim live toolkit command execution. A newer toolkit
release requires a new manifest and overlap review. The toolkit is never
installed automatically by this package.

When toolkit management is established, its manifest-declared skills and tools
own Astro + Cloudflare readiness, scaffolding, deployment, discovery, brand,
media, diagnostics, and toolkit maintenance. Generic skills must not create
parallel systems.

## Validation

```bash
python3 scripts/validate_bundle.py
python3 scripts/inspect_contract.py source
python3 scripts/inspect_tree.py . --exclude .git --exclude .env \
  --exclude MEMORY.md --exclude AGENTS.override.md \
  --exclude CLAUDE.local.md --exclude .claude/settings.local.json
python3 tests/run_portable_tests.py
```

When run in a Git checkout, `validate_bundle.py` rejects tracked private local
agent state: any case-variant of `MEMORY.md`, Codex `AGENTS.override.md`, Claude
`CLAUDE.local.md`, or `.claude/settings.local.json`. Release inventory and
archive validation reject those files even when Git is unavailable.

For an archive:

```bash
python3 scripts/validate_archive.py <archive.zip>
```

For a lifecycle record:

```bash
python3 scripts/validate_record.py <schema.json> <record.json>
```

That command establishes structural validity only. Before mutation, add
independently resolved `--allowed-client-root`, `--allowed-state-root`, and
`--require-applicable`; never derive allowed roots from the record itself.

These commands validate source structure, metadata, selected fixtures, and
read-only integrity behavior. They do not prove live client discovery,
installation, rollback, or uninstall.

## Known limitations

- Cursor's account-synced User Rules and documented machine-local user rule
  files have different storage behavior; file-backed format and skill roots
  remain version-sensitive until the target client passes runtime checks.
- Claude Code has not yet been runtime-tested in this environment. The root
  `CLAUDE.md` uses the documented `@AGENTS.md` import for compatibility with
  sessions that do not load `AGENTS.md` directly.
- Antigravity's dedicated always-on rule has not been runtime-tested. Check the
  current 24,000-byte per-file and 20,000-token aggregate rule limits against
  each target environment.
- Model-operated lifecycle operations are reviewable best-effort procedures,
  not crash-atomic multi-client transactions.
- The complete contract is an optional always-loaded context cost. Use the
  portable skills alone when users want workflow coverage without that full
  always-on instruction load.
- The public GitHub installation prompt has source and negative conformance
  coverage but has not completed a four-client live installation exercise.
- Windows reparse-point behavior requires a Windows validation run.

## Release and checksum process

### Stable publication

A stable release requires consistent package authorities, source and fixture
validation, integration and archive-safety checks, disclosed client-runtime
coverage, a clean identified release commit, and a newly built archive with an
independently verified SHA-256 sidecar. Runtime evidence is reported per client;
an unavailable client must remain clearly marked unverified rather than being
represented as tested.

Release notes record the tag, commit, publication date, archive filename,
SHA-256, verified scope, and unresolved compatibility limitations. Publish an
annotated tag and a stable GitHub Release with the archive and sidecar.

An archive cannot contain its own final checksum.

## License and maintenance

The package is available under the [MIT License](LICENSE). The canonical
repository is
[ImYourBoyRoy/agent-continuity-stack](https://github.com/ImYourBoyRoy/agent-continuity-stack).

Maintained by **[@imyourboyroy](https://github.com/ImYourBoyRoy)**:

- GitHub: [@ImYourBoyRoy](https://github.com/ImYourBoyRoy)
- Website: [ImYourBoyRoy.com](https://imyourboyroy.com)
- PyPI: [ImYourBoyRoy](https://pypi.org/user/ImYourBoyRoy/)

Maintainer links are verified project metadata. Operator-profile values remain
optional installation inputs and are never inferred from workstation paths or
unrelated repositories.
