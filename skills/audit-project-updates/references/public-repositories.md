# Public repository evidence

## Establish the relationship

Treat an upstream repository as in scope only when the project records a
dependency, pin, submodule, install source, executable-tool requirement, or
explicit update-source configuration entry.

Record the currently used release, tag, commit, package version, or unknown
state before looking upstream.

## Evidence order

Prefer:

1. published stable release
2. first-party package-registry version
3. signed or documented stable tag
4. repository-owned version manifest
5. changelog
6. commits after the known version
7. default-branch activity

Repositories may use only some of these. Report the strongest evidence that
exists and the missing release signals.

## Compare safely

- Compare the known tag or commit to the current stable release.
- Summarize only changes relevant to the consuming project.
- Check migration notes, supported runtimes, removed behavior, and installer
  changes.
- Label default-branch work `unreleased-watch`.
- Treat a rewritten or moved tag as a supply-chain warning.
- Do not execute upstream installers or binaries during an audit.
- Prefer immutable download identifiers and checksums for later installation.

## Source projects without releases

When no releases exist, report:

- repository-declared version
- last relevant version commit or tag
- newer default-branch changes
- absence of a packaged stable release
- whether the consumer is pinned to a commit or following a branch

Do not convert unreleased enhancements into an upgrade recommendation without a
deliberate source-tracking policy.
