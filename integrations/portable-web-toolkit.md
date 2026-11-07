# Portable Web Toolkit integration

This optional integration was reviewed and statically validated against
Portable Web Toolkit `0.4.0` at release commit
`1675019d3eec9dbdb81bcff93e3e918b3e29fc34`. Its `skill-pack.json` declares
skill pack `1.4.0`, source base commit
`fffa17c8f95e3613b0b1530107e06e010fe16675`, and SHA-256
`76b9f37dee5d96bcb80cbf666dcbef8c1dda4629a05a4ded5142de0882bb2fa7`.
This review checks the release manifest and ownership boundaries; it does not
claim live toolkit command execution.

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
and per-skill `skill.json` files. For the reviewed `0.4.0` release, toolkit
ownership includes `discovery-doctor`, `wcag-auditor`, `site-onboarding`, and
`site-maintenance` alongside its other declared skills. Let its declared
skills and deterministic tools own:

- site readiness and scaffolding;
- toolkit updates;
- toolkit-managed Cloudflare operations and deployment;
- discovery generation and validation;
- brand and stylesheet validation;
- image and media processing;
- toolkit diagnostics, publication, and maintenance.

Treat this ownership map as specific to the pinned release above. A newer
toolkit version requires a fresh manifest and overlap review before updating
the compatibility record.

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

