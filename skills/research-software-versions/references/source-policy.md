# Version source policy

## Stable release

Prefer a first-party stable registry entry or published release. Confirm whether
the project uses semantic versioning and whether the release is supported on the
consumer's runtime and platform.

## Tags without releases

Check whether tags are documented, immutable, and used by installation or
packaging. A tag can be a valid release signal, but do not assume all tags are
production releases.

## Version files without tags

Treat a repository `VERSION`, package manifest, or changelog as repository-
declared state. Compare it with packaging and installation behavior and report
the missing immutable release signal.

## Default branch

Use branch commits to identify unreleased changes only. Do not recommend an
unreleased commit unless the user explicitly wants source tracking and the
project has an immutable pin, verification plan, and rollback.

## Conflicts

When docs, registry, tag, package metadata, and binaries disagree, report the
conflict. Prefer reproducible machine-readable release evidence while checking
whether the discrepancy is a release-process defect.

