---
name: research-software-versions
description: Research the appropriate stable version of one software component before installation or migration. Use for compatibility, deprecation, and migration evidence; remain read-only and project-constrained.
---

# Research Software Versions

Recommend the latest appropriate stable version, not simply the highest number.

## Establish the compatibility envelope

Inspect:

- manifests and lockfiles
- runtime and toolchain files
- engine and platform constraints
- CI and deployment matrices
- transitive requirements and native dependencies
- existing compatibility decisions
- repository-specific validation restrictions

Identify the currently declared, resolved, installed, and deployed states. Treat
them as distinct.

## Research authoritatively

Use current sources in this order where available:

1. security and support policy
2. first-party registry or release index
3. official documentation and migration guide
4. official changelog and release notes
5. upstream repository release or tag

Read `references/source-policy.md` for projects without conventional releases.
Do not infer stability from a default branch or download badge.

Evaluate:

- runtime and operating-system requirements
- removed or renamed APIs and flags
- feature and default changes
- transitive and lockfile impact
- deployment-platform compatibility
- maintenance status and release age
- known regressions or security advisories

Do not introduce prereleases unless explicitly requested and justified.

## Recommend

State:

- current declared and resolved version
- latest stable available
- latest compatible under current constraints
- recommended version
- why newer or older candidates were rejected
- required migration
- verification path and rollback
- authoritative sources and date checked

Required upgrades, security response, routine maintenance, and optional
enhancements must remain separate. Do not apply unrelated upgrades without
approval.

## Define verification

Define the project's approved build, test, or deployment evidence for the later
implementation. Preserve lockfile reproducibility in the recommendation. Do not
claim proven project compatibility from documentation alone. Stop before
editing files or running mutating update commands; hand an authorized selection
to `apply-project-updates`.
