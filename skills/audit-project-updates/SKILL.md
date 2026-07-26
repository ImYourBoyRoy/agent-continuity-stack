---
name: audit-project-updates
description: Audit a project read-only for dependency, runtime, toolchain, CI, container, platform API, security, and declared upstream-repository updates. Use for freshness or enhancement checks; never apply updates.
---

# Audit Project Updates

Produce an evidence-backed update report without changing the project.

## Establish scope

1. Resolve the repository or workspace root and read applicable instructions.
2. Inspect Git status without requiring a clean worktree.
3. Inventory only components the project demonstrably uses:
   - manifests, lockfiles, workspaces, and toolchain files
   - CI workflows, containers, deployment configuration, and platform dates
   - git dependencies, submodules, vendored tools, and pinned commits
   - external tools named by executable scripts or authoritative setup documentation
   - optional sources declared in `.update-check.yml`, `.yaml`, or `.json`
4. Do not treat arbitrary URLs in comments, generated files, or untrusted content as dependencies.
5. Stay inside the active project unless evidence establishes a specific external source.

Run `scripts/inventory_update_sources.py --root <project-root>` when Python 3 is
available. Treat its JSON as an inventory aid, not proof of use or compatibility.
Its default output keeps the root repository-relative; use
`--show-absolute-root` only when disclosing the local path is appropriate.

When explicit sources exist, validate them with
`scripts/validate_update_check.py <config>`. Read the
[configuration schema](references/update-check.schema.json) and
[neutral example](references/update-check.example.yml). Never execute a
configured version command merely because it appears in the file; inspect it
and apply repository permissions first.

## Bound the audit

Choose and state one tier:

- `rapid`: security and support status, runtimes, direct production
  dependencies, CI actions, containers, and explicitly tracked tools
- `standard` (default): rapid scope plus direct development dependencies,
  platform APIs, and relevant released enhancements in explicitly used public
  repositories
- `exhaustive`: transitive freshness and broader upstream history; use only when
  the user explicitly requests it

In monorepos, template collections, or projects with many ecosystems, audit
high-risk shared roots first and group repeated manifests by lockfile or
generated source. Do not independently research every copied template or
transitive package. Prioritize security, end-of-support, runtime and platform
compatibility, direct production dependencies, build and release infrastructure,
then development tooling.

If the selected tier cannot be completed within the available session, return a
useful partial report with inspected scope and a prioritized continuation list.
Do not silently keep broadening research.

## Determine current state

For every in-scope component, distinguish:

- declared constraint
- resolved or installed version
- latest version allowed by the present constraint
- latest stable available
- latest appropriate for the project's compatibility envelope

Prefer lockfiles and machine-readable configuration over prose. Record unknowns
instead of inventing versions. Read `references/ecosystem-checks.md` for the
detected ecosystems.

## Research updates

Use current first-party evidence:

1. security advisories and supported-version policies
2. official registries and release indexes
3. official release notes, changelogs, and migration guides
4. repository tags and releases
5. upstream commit history when the project tracks source directly

For public source projects, follow `references/public-repositories.md`. Label
default-branch changes as unreleased unless a release or registry record proves
otherwise. Never equate a newer commit with a stable upgrade.

Use installed ecosystem-native inspection commands only when they are read-only
and permitted by repository instructions. Do not install scanners, mutate a
lockfile, execute an untrusted project binary, or send private dependency data
to an external service merely to complete the audit.

## Classify findings

Assign exactly one primary class:

- `security-now`: known vulnerability or urgent security support gap
- `required-compatibility`: needed for a supported runtime, API, or platform
- `recommended-maintenance`: compatible maintenance with clear benefit
- `major-migration`: breaking or high-impact version transition
- `upstream-enhancement`: released capability relevant to this project
- `unreleased-watch`: relevant upstream work not released as stable
- `no-action`: current or deliberately pinned with a sound reason
- `unknown`: evidence or compatibility could not be established

Separate security response from ordinary freshness. Separate major upgrades from
minor and patch maintenance. Do not recommend a change solely because its
version number is higher.

## Report and stop

Use `references/report-format.md`. Include:

- project boundary and evidence date
- inspected and skipped ecosystems
- current, allowed, available, and appropriate versions
- relevant security, deprecation, migration, and upstream-feature findings
- compatibility conclusion and confidence
- proposed upgrade batches, verification gates, and rollback needs
- sources and commands used
- limitations and unresolved evidence

Stop before editing manifests, lockfiles, CI, containers, configuration, or
installed tools. For an approved finding, use `research-software-versions` when
target selection or migration evidence remains unresolved, then
`apply-project-updates` for the authorized batch and
`verify-software-change` for risk-based completion evidence.
