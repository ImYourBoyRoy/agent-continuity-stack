---
name: build-astro-on-cloudflare
description: Design, implement, review, or migrate the Astro-to-Cloudflare Pages or Workers boundary when Portable Web Toolkit does not manage the project. Use for adapters, rendering, bindings, compatibility dates, output, emulation, and deployment configuration—not generic UI or Cloudflare infrastructure.
---

# Build Astro on Cloudflare

Own only the Astro-to-Cloudflare boundary. This is an optional,
default-uninstalled fallback skill.

## Detect specialist ownership first

Before proposing architecture or commands:

1. read repository instructions, manifests, scripts, configuration, and
   deployment documentation;
2. inspect the signals in the package's Portable Web Toolkit integration
   contract when that package context is available;
3. determine whether another established project tool or runbook owns this
   boundary.

If Portable Web Toolkit management is established, stop and defer to its
manifest-declared skills and deterministic tools. Do not create parallel
readiness, site-profile, discovery, deployment, asset, or Cloudflare-mutation
systems.

## Establish the current boundary

Identify:

- Astro, adapter, Vite, Node, package-manager, and Wrangler versions;
- static or server output;
- Pages or Workers deployment;
- compatibility date and flags;
- bindings, public variables, and secret boundaries;
- local, preview, staging, and production workflows.

Verify version-sensitive choices through current Astro and Cloudflare
first-party sources. Do not assume Pages and Workers are interchangeable.

## Choose the architecture

Read [architecture decisions](references/architecture-decisions.md) for a
material choice between static and server output or Pages and Workers.

Prefer the established supported path unless evidence justifies migration.
Explain benefits, compatibility constraints, data or routing impact, rollback,
and required authorization before changing deployment architecture.

## Implement safely

- Preserve the lockfile and repository configuration authority.
- Keep secrets in the platform secret store or ignored local environment.
- Type bindings through the project's supported mechanism.
- Keep preview and production values explicit.
- Avoid Node-only APIs unless the configured runtime supports them.
- Do not copy stale Wrangler flags or compatibility dates from examples.
- Defer DNS, account policy, security products, and generic Worker design to
  authoritative platform tooling.

## Validate

Follow repository-approved local, remote, staging, and production constraints:

1. validate configuration and package compatibility;
2. run the approved Astro check and build path;
3. inspect output, routes, assets, bindings, and SSR behavior;
4. use local emulation or preview where authorized;
5. verify staging before production when deployment is requested.

Do not deploy merely because implementation was requested. Report architecture,
versions, evidence, configuration changes, secret expectations, validation
environment, deployment state, and rollback.
