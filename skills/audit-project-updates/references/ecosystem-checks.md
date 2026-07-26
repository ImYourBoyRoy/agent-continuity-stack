# Ecosystem update checks

Use only installed tools and read-only modes allowed by repository instructions.
Never install an audit utility implicitly.

## JavaScript and TypeScript

Inspect the active package-manager lockfile, workspaces, `engines`, runtime
files, framework config, and CI. Prefer the matching package manager's outdated
report. Distinguish direct, development, optional, peer, and transitive
dependencies.

## Rust

Inspect workspace manifests, `Cargo.lock`, `rust-toolchain*`, MSRV policy, target
configuration, native dependencies, and CI. A resolver dry run may still be
disallowed by repository policy; do not run it merely because Cargo supports
one. Separate lockfile-compatible updates from manifest constraint changes and
MSRV migrations.

## Python

Identify the package manager and lock format before invoking anything. Inspect
`requires-python`, environment files, indexes, dependency groups, platform
markers, and compiled wheels. Do not assume the active shell environment
belongs to the project.

## JVM and Android

Inspect Gradle wrapper, plugin versions, catalogs, Java/Kotlin requirements,
Android Gradle Plugin, compile/target SDK, NDK, and CI images. Avoid running a
Gradle build during a read-only audit unless repository instructions permit it.

## Apple platforms

Inspect Xcode requirements, deployment targets, Swift Package pins, CocoaPods
locks, signing-independent tool versions, and CI images. Treat SDK and Xcode
upgrades as platform migrations.

## Containers and CI

Inspect image tags and digests, Dockerfile syntax, build actions, reusable
workflows, runner images, and deployment actions. Report mutable tags and
unreviewed major action changes separately.

## Hosted platforms and APIs

Inspect compatibility dates, API versions, runtime channels, deprecation
notices, SDK support, and deployment configuration. A platform default change
can be more important than a package version.

