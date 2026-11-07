# Model-operated installation protocol

This protocol is authoritative for installing or updating the bundle. It is
designed for a coding model working from a reviewed local checkout. Do not pipe
a remote script into a shell or execute an unaudited installer.

## Default behavior: status only

Unless the operator explicitly asks to install, update, repair, uninstall, or
roll back, perform only read-only inspection:

1. resolve the package root and read `manifest.json`;
2. normalize the canonical contract as declared in `instruction-pack.json` and
   verify its source SHA-256;
3. detect installed client versions rather than inferring them from folders;
4. inspect documented instruction and skill destinations;
5. compare exact content and versions;
6. identify conflicts, unsupported paths, nested links, and special files;
7. report `absent`, `current`, `modified`, `outdated`, `partial`, `conflict`,
   `unsafe-tree`, or `unverified` for each client and skill using
   `schemas/install-status.schema.json`.

The existence of a destination file is not evidence that a client loads it.

## Authorization boundary

Before mutation, list:

- selected clients and whether installation is user-global or project-local;
- exact files and directories to create, merge, replace, or remove;
- detected conflicts and proposed resolution;
- backup root and rollback operation;
- runtime tests that will be attempted.

Require explicit authorization for that scope. Installing skills installs no
custom instructions. Skill installation and operating-contract installation
are independent authorization scopes. The public default is to preserve every
existing instruction source unchanged and install only the selected skills.

Before planning instruction changes, require one explicit mode:

1. `preserve-existing`: install skills only and do not alter instructions;
2. `guided-additions`: propose individually reviewable additions to existing
   instructions without representing them as the canonical package contract;
3. `complete-contract`: install the entire verified
   `GLOBAL_CUSTOM_INSTRUCTIONS.md` through the documented preserving adapter.

Never replace an existing custom-instruction file wholesale merely because the
package contains a preferred template. In `guided-additions` mode, identify
conflicts and show the exact proposed merge before approval. Do not attach the
package contract's ownership, integrity, or runtime-verification claims to a
partial derivative.

Use operator-profile values already supplied in the active user instructions or
a user-designated profile source; do not ask the user to repeat them. Never
infer identity or ownership from machine usernames, Git metadata, environment
files, or unrelated repositories. Profile fields are optional. Do not prompt
for missing fields by default. Ask only when the user requests a specific
missing field or the selected task requires it. Before installing any
personalized value, disclose that values in an always-loaded contract can be
transmitted to, logged by, or retained by each selected model provider.

Record the reviewed operation in an `install-plan` document conforming to
`schemas/install-plan.schema.json`. Plan generation remains read-only. Compute
the plan digest using the canonicalization rule declared by the schema and bind
the operator's approval to that exact digest. A changed plan requires new
approval. A plan with blockers, an unknown client or skill, no effective
operations, or a target outside its resolved client root is not applicable even
if an `apply_authorized` field says otherwise.

## Preflight

1. Reject a package tree containing symlinks, junctions, reparse points,
   devices, sockets, FIFOs, or other unsupported special files.
2. Reject the same conditions in every destination subtree that would be
   copied, replaced, restored, or traversed.
3. Read host and repository policy before editing project scope.
4. Inventory same-name skills from built-in, global, plugin, and repository
   sources. Prefer one clear owner over duplicates.
5. Check available space, permissions, case sensitivity, and path
   normalization.
6. Preserve existing file mode where an instruction file is merged.
7. Do not expose file contents that may contain secrets while reporting status.

## Per-client journal and backups

Do not claim crash-atomic behavior across clients or filesystems. Process one
client at a time and leave later clients unchanged until the current client is
validated or restored:

1. Create a unique operation directory outside every discovery root:
   - Unix: `${XDG_STATE_HOME:-~/.local/state}/agent-continuity-stack/`
   - Windows: `%LOCALAPPDATA%\AgentContinuityStack\`
2. Before any target mutation, create or update a record conforming to
   `schemas/operation-journal.schema.json`. Durably record the approved plan
   digest, package version and archive hash, timestamp, requested scope,
   resolved client root, root-relative target paths, original hashes, portable
   modes or attributes when available, and operation phase.
   Never use an arbitrary absolute path from a receipt as an instruction.
3. Copy every existing target to `backups/<transaction-id>/` without following
   links. Record absent targets explicitly. Treat backup snapshots as immutable
   evidence: recovery and rollback copy from them and never move, consume,
   replace, or delete them while any receipt references them.
4. Stage all new content in the transaction directory and validate it there.
5. Recheck the approved plan digest and original hashes immediately before
   commit. Stop if the plan or any target changed after preflight.
6. Commit with same-filesystem atomic replacement where supported.
7. After each target replacement, advance both target and journal phases. If a
   commit fails,
   restore every target already changed for this client and retain the failed
   operation evidence. Restore by verified copy from the immutable backup, then
   recheck both the restored target and retained backup hashes. If the model or
   host is interrupted, stop other client
   work and recover the incomplete client from the journal at the next run.
8. Validate the client and close its journal before starting the next client.

These steps reduce risk but do not make model-operated filesystem work
crash-atomic. If the operator requires durable locks, write-ahead recovery,
`fsync`, or guaranteed multi-target recovery, use a separately audited
deterministic lifecycle tool. This package does not provide one.

POSIX modes do not capture Windows ACLs, owners, extended attributes, or every
reparse attribute. Warn when the host cannot preserve material metadata and do
not claim exact rollback for metadata that was not recorded and verified.

The model performs these authorized filesystem operations. The package does not
ship a general mutation executor. Use deterministic helpers only to inspect,
hash, normalize in memory, or validate state.

Never store backups, receipts, baselines, removed copies, or recovery data
inside `.agents/skills`, `.cursor/skills`, `.cursor/rules`, `.claude/skills`,
`.claude/rules`, `.gemini/config/skills`, or another discovery directory.

## Render and install the optional operating contract

Perform this section only when `complete-contract` was explicitly authorized.
The full contract is all-or-nothing: if the operator does not accept every
section, use `guided-additions` or `preserve-existing` instead.

Use `GLOBAL_CUSTOM_INSTRUCTIONS.md` without shortening it. The source is a
portable template, not installable output: never copy it directly into a client
when it still contains profile placeholders. Read and write deliberate UTF-8
with LF line endings and no byte-order mark. Verify the canonical normalized
bytes against `source_sha256` before rendering.

Render only these operator-profile placeholders from explicit user-provided or
user-designated profile values:

- `{{operator_name}}`
- `{{operator_email}}`
- `{{personal_site}}`
- `{{github_profile}}`
- `{{pypi_profile}}`

Do not ask the user to repeat values already present in their current
instructions or a user-designated profile source. Ask about missing values only
when the requested operation requires them; otherwise omit them. Reject
unexpected placeholders. Remove each unanswered profile bullet from rendered
output; if no values remain, remove the entire `## Operator Profile` section.
No placeholder may remain in installed instructions.

Use `scripts/render_contract.py` to perform substitutions deterministically.
Create its JSON input in the transaction staging area outside the package and
all client discovery roots, using only explicit values. Use `{}` when no fields
were supplied. The renderer verifies the canonical source hash, refuses
unknown or malformed fields, removes unanswered bullets, writes a new output
file outside the package, and does not overwrite existing output. It does not
ask questions or infer values. Delete the temporary profile JSON and rendered
copy after installation or rollback unless the user asks to keep them.

```bash
python3 scripts/render_contract.py \
  --profile-json <transaction-root>/operator-profile.json \
  --output <transaction-root>/rendered-contract.md
python3 scripts/inspect_contract.py rendered \
  <transaction-root>/rendered-contract.md
```

Show the inspected rendered contract for user review before installation.
For Antigravity, also pass `--antigravity-rule <rule-file>` to the inspector and
confirm the rendered body and size checks pass. A failed check blocks the
operation. Compute `rendered_sha256` from the complete rendered UTF-8/LF bytes.
This value is installation-specific: record it in the plan, transaction
receipt, ownership records, and client status records; do not add a fixed
rendered hash to the package manifest.

Apply the adapter in `CLIENT_COMPATIBILITY.md`:

- Codex: resolve the active `CODEX_HOME`. If `AGENTS.override.md` exists, it is
  the effective user-global file; otherwise use `AGENTS.md`. Preserve unrelated
  content and maintain exactly one contract block between the markers declared
  in `instruction-pack.json`. Refuse an ambiguous or malformed marker layout.
- Claude Code: install one dedicated user rule.
- Antigravity: install one dedicated global rule at the target declared in
  `instruction-pack.json`, with the declared `always_on` frontmatter. Verify
  its body is byte-for-byte the rendered contract and its complete size is
  below the current per-rule byte limit. Inspect the active aggregate rule
  budget before installation.
- Cursor: the package targets the account-synced plain-text User Rules under
  Customize > Rules. Provide the complete rendered contract for an
  operator-reviewed import and do not edit Cursor's internal settings storage.
  For a disposable project-level runtime test, generate one `.mdc` file with:

  ```yaml
  ---
  description: Complete Expert Agent Operating Contract; always apply.
  alwaysApply: true
  ---
  ```

  followed by the complete rendered contract.

When updating a legacy Antigravity installation that used the two-fragment
`GEMINI.md` adapter, plan migration to the dedicated rule separately. Remove
old imports or fragments only when receipts and hashes prove they are
package-owned and unchanged, and only after the new rule is validated. If
ownership cannot be proven, preserve the old content and report the duplicate
loading risk for review.

## Install skills

For every selected skill:

1. compare `skill-manifest.json` versions and tree hashes;
2. copy the entire real directory without following links;
3. do not copy a package-level backup or receipt into the skill root;
4. preserve a locally modified installed skill unless replacement is explicitly
   authorized;
5. validate `SKILL.md`, linked resources, scripts, and client discovery;
6. do not install the optional Antigravity CLI copy unless selected.

Optional skills are never selected implicitly. In particular,
`build-astro-on-cloudflare` remains uninstalled unless explicitly selected and
must defer when Portable Web Toolkit management is established.

`adopt` means recording ownership of byte-identical pre-existing content after
explicit approval; it never rewrites that content. Do not adopt a modified,
ambiguous, or merely same-version target.

## Validate and record

After each client operation:

1. compare installed hashes with staged hashes and ownership records;
2. start new client sessions because several clients cache instructions;
3. run `tests/CLIENT_SMOKE_MATRIX.md`;
4. classify every client as `verified`, `installed-unverified`, or `failed`;
5. write transaction, ownership, and client-status records conforming to the
   bundled schemas;
6. when `complete-contract` was selected, never report full success while that
   client's global contract is absent, truncated, or undiscovered; for other
   modes, report instruction state separately without implying contract
   installation.

## Update

An update begins with the same status-only comparison. Read `CHANGELOG.md`,
compare each installed skill version independently, preserve local changes, and
apply only an authorized version transition. Do not reinstall unchanged skills
or duplicate the operating contract.

## Rollback

Receipts are evidence, not executable path instructions. Rollback begins from a
selected receipt but independently resolves the current client root, maps only
the approved relative targets, and rejects traversal, changed ownership, or
paths outside that root:

1. verify current targets and warn about post-install modifications;
2. preserve post-install modifications in a new recovery directory;
3. verify backup hashes and restore original files and permissions, or remove
   only a package-owned target recorded as originally absent;
4. validate that no unrelated target changed;
5. start new client sessions and retest instruction discovery;
6. retain both the original receipt and rollback receipt.

Never delete or restore a target solely because a receipt contains its path.
Re-derive the target from the current client root, approved operation, ownership
record, and expected hashes.

All mutable records address content as a validated `client_root` plus a
non-absolute `target_relative`. Backup, staging, ownership-record, and
client-status-record paths are relative to the validated `state_root`. Reject
roots that are filesystem, system-directory, or user-directory umbrellas.
Reject empty, absolute, dot-segment, traversal, drive, or alternate-data-stream
relative paths.

Schema validity is not authorization or proof that a declared root is genuine.
Immediately before staging, commit, recovery, rollback, or uninstall, resolve
the actual roots independently from the active client and host, then require:

```text
python3 scripts/validate_record.py <schema> <record> --allowed-client-root <resolved-client-root> --allowed-state-root <resolved-state-root> --require-applicable
```

Repeat `--allowed-client-root` for a plan containing more than one independently
resolved client root. Do not derive an allowed root from the record being
validated.

Uninstall is not equivalent to rollback. Uninstall removes only content owned
by this package and must not delete a pre-existing instruction file or skill.
Refuse automatic removal when the current installed hash differs from the
ownership record unless the operator explicitly authorizes preservation and
removal of the modified content.

## Read-only helpers and conformance evidence

The scripts in `scripts/` do not install or uninstall:

```text
inspect_contract.py
inspect_tree.py
validate_archive.py
validate_record.py
validate_bundle.py
```

Use deterministic unit tests for hashes, normalization, schemas, tree and
archive safety, metadata, and fragment reconstruction. Exercise installation,
partial failure, rollback, interruption, and uninstall as model-conformance
scenarios in disposable homes. Do not describe fixture or source tests as proof
that a live client's lifecycle behavior passed.
