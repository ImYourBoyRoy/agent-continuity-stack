# Ecosystem application

Use current first-party commands and repository instructions. These notes
describe decisions, not timeless command syntax.

## JavaScript and TypeScript

Use the lockfile's package manager. Prefer a targeted update. Inspect peer
dependency changes, lifecycle scripts, package source and integrity changes,
runtime engines, workspace impact, and built package output.

## Rust

Separate lockfile-compatible resolution from manifest constraint changes and
MSRV migrations. Inspect feature changes, build scripts, native libraries,
source replacements, and target-specific dependencies. Follow repository rules
for local versus remote Cargo execution.

## Python

Use the declared environment and lock manager. Inspect Python constraints,
platform markers, indexes, hashes, wheels, extras, and compiled dependencies.
Do not treat an unrelated active virtual environment as the project state.

## JVM and Android

Keep wrapper, Java or Kotlin, build plugins, version catalogs, platform SDKs,
and native toolchains compatible. Separate build-system upgrades from ordinary
library updates.

## Apple platforms

Treat Xcode, SDK, deployment-target, Swift package, and signing changes as
distinct compatibility surfaces. Do not run signing or distribution operations
merely to update packages.

## Containers, CI, and platforms

Prefer immutable image digests and pinned action references where policy
requires them. Inspect permissions, runners, build contexts, compatibility
dates, configuration defaults, and rollback artifacts.

