# Portable Web Toolkit integration

This optional integration was tested against Portable Web Toolkit `0.3.1` at
release commit `cdbc33ff40bedab48fc86bfb7e1ea06a5d81f6f3`. Its `skill-pack.json`
records skill content from base commit
`86dddd9efb64c5b4219afe986699135a51e63f83`.

Compatibility is exact-tested, not an unrestricted version range. Reinspect the
upstream manifest, release notes, and affected skills before claiming
compatibility with a newer release.

## Establish management

Treat the toolkit as authoritative only when at least one corroborated signal
exists:

- repository instructions establish Portable Web Toolkit;
- package scripts invoke `Web_Toolkit` commands;
- a compatible toolkit site profile governs the project;
- an established `Web_Toolkit` link is corroborated by configuration or
  documentation;
- the user explicitly selects Portable Web Toolkit.

A directory name alone is insufficient.

## Ownership

When management is established, consume the toolkit's root `skill-pack.json`
and per-skill `skill.json` files. Let its declared skills and deterministic
tools own:

- site readiness and scaffolding;
- toolkit updates;
- toolkit-managed Cloudflare operations and deployment;
- discovery generation and validation;
- brand and stylesheet validation;
- image and media processing;
- toolkit diagnostics, publication, and maintenance.

The generic `release-web-application`, `web-discovery-artifacts`,
`maintain-web-design-system`, and `prepare-web-assets` skills must defer. They
must not create competing commands, profiles, generators, gates, or pipelines.

## Absence and collision behavior

Do not install Portable Web Toolkit automatically. When it is absent, generic
skills remain provider-neutral. The optional `build-astro-on-cloudflare` skill
may own only the Astro-to-Cloudflare integration boundary when explicitly
selected.

If same-name or overlapping skills are already discoverable, report every
source, scope, version, and precedence. Do not install a duplicate merely to
match another client. Optional skills stay uninstalled unless selected.

