---
name: apply-project-updates
description: Apply an authorized dependency, runtime, toolchain, CI, container, SDK, or tracked-tool update in reversible batches. Use after targets are selected; do not audit broadly or upgrade everything automatically.
---

# Apply Project Updates

Implement only the approved update set and preserve a defensible rollback path.

## Confirm the selected batch

Require:

- exact components or an explicitly selected audit batch
- target versions, tags, or immutable commits when known
- compatibility and migration evidence
- repository-approved validation commands
- authorization for manifest, lockfile, toolchain, or infrastructure changes

If the request says only “update everything,” run or request a bounded audit
before mutation. Do not silently choose every available major version.

## Capture the baseline

1. Resolve the repository and applicable instructions.
2. Inspect Git status and preserve unrelated work.
3. Record current manifests, lockfiles, toolchains, generated files, and
   relevant validation results.
4. Identify the files and artifacts each approved updater may rewrite.
5. Establish the rollback mechanism before running a mutating command.

Use `references/batching-and-rollback.md` to design the batch.

## Apply through project authority

- Use the repository's active package manager and supported update mechanism.
- Preserve one lockfile and do not switch package managers.
- Prefer exact component updates over broad resolver churn.
- Inspect installer or migration scripts before execution.
- Never pipe an unaudited remote script into a shell.
- Do not install global tools or modify the host toolchain unless separately
  authorized.
- Do not commit, push, deploy, publish, release, or open a pull request unless
  that external action is separately authorized.
- Respect remote-only builds, hardware requirements, staging gates, and CI
  ownership.
- Keep security response, compatibility work, routine maintenance, and major
  migrations in separate batches.

Read `references/ecosystem-application.md` for the detected ecosystem.

## Inspect the delta

After each mutation, inspect:

- direct and transitive version changes
- added, removed, yanked, or source-switched packages
- changed checksums or integrity records
- runtime, platform, or compiler requirements
- generated configuration or bindings
- feature and default changes
- migration edits
- unexpected unrelated manifest or lockfile churn

Stop and explain unexplained source changes, mutable references, registry
changes, or excessive resolver churn.

## Verify before continuing

Run the smallest project-approved checks that exercise the batch. Broaden based
on risk. Do not begin the next batch while the current one has unexplained
failures.

Classify:

- passed and ready
- passed with existing warnings
- failed because of the update
- blocked by environment or policy
- compatibility uncertain

On failure, repair only when the migration remains within the approved scope.
Otherwise restore the batch's own changes without discarding unrelated work.

## Report

Provide:

- approved batch and resulting versions
- commands and files changed
- dependency-graph and lockfile delta
- migrations applied
- validation and environments
- warnings, failures, and deferred updates
- rollback performed or retained
- next batch requiring approval
