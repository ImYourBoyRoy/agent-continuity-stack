---
name: release-web-application
description: Plan, stage, deploy, validate, or roll back a public web application across hosting providers. Use for release gates, previews, production authorization, smoke tests, observability, and recovery.
---

# Release Web Application

Treat a release as an observable, reproducible, and reversible transition.

When Portable Web Toolkit management is established by repository instructions,
`Web_Toolkit/`, toolkit scripts, or a toolkit site profile, delegate Astro +
Cloudflare readiness and deployment to its `site-readiness` and
`portable-web-toolkit` skills. Do not invent parallel Cloudflare commands,
profiles, gates, or deployment paths.

## Use repository authority

Read repository instructions, release runbooks, CI, deployment configuration,
environment profiles, migration procedures, and rollback mechanisms. Use the
project's supported path instead of inventing a parallel deploy command.

Read the applicable provider note in `references/providers.md` only after the
provider is known.

## Build the release gate

Adapt this sequence:

1. identify the intended commit, artifact, environment, and release owner
2. inspect worktree state and version metadata
3. verify secrets and prerequisites without exposing values
4. run project-approved focused checks
5. build or obtain the immutable artifact through the approved path
6. verify the artifact, migrations, headers, and environment-specific output
7. deploy to preview or staging when available
8. run representative smoke and integration checks
9. identify rollback and data compatibility
10. obtain required production authorization
11. deploy the exact verified artifact
12. verify live routes, logs, metrics, and critical integrations
13. record the released artifact and rollback point

A user may explicitly waive staging; state the resulting risk.

## Infrastructure and data changes

For DNS, caches, redirects, headers, routing, access policy, or schema changes:

- inspect current state
- use a plan or dry run when supported
- explain blast radius and propagation
- verify backups and reversibility
- apply only within authorized scope
- validate live state after mutation

Never treat a configuration upload as successful without checking provider and
live-state evidence.

## Smoke coverage

Choose meaningful checks:

- critical routes and assets
- authentication and authorization
- forms, APIs, queues, and webhooks
- redirects and canonical metadata
- browser console and runtime logs
- responsive behavior
- caches and security headers
- discovery artifacts
- performance or error-rate regression

## Output

Report environment, commit and immutable artifact, commands, approvals, checks,
live evidence, warnings, migrations, rollback mechanism, and unverified
behavior.
