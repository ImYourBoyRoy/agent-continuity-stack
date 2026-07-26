---
name: web-discovery-artifacts
description: Create or validate robots, sitemaps, canonicals, social metadata, JSON-LD, security.txt, llms.txt, indexes, and feeds. Use for public-web discovery and indexing; select only justified artifacts.
---

# Web Discovery Artifacts

Generate consistent discovery output from verified route and metadata sources.

When Portable Web Toolkit manages the project, use its generators and
`discovery-doctor` as the specialist authority. Do not create a second route
inventory, discovery generator, or deployment gate.

## Determine intent

1. Establish whether the site is public, private, staged, or intentionally
   non-indexed.
2. Identify authoritative route, origin, locale, content, ownership, image, and
   update-date sources.
3. Inventory framework integrations and existing generated artifacts.
4. Choose only outputs with a clear consumer and maintenance path.
5. Prefer a supported framework integration over a custom generator when it
   satisfies the requirements.

Do not present `llms.txt` or other emerging conventions as universally adopted
standards.

## Candidate outputs

- `robots.txt`
- `sitemap.xml` or sitemap index
- canonical and alternate-language links
- Open Graph and platform-specific social metadata
- JSON-LD matching visible page content
- `/.well-known/security.txt`
- `llms.txt` or a project-defined AI-readable index
- content or search feeds
- `humans.txt` when the project has a reason to publish it

## Build one source of truth

- Derive related outputs from shared route and metadata data.
- Avoid hand-maintained URL duplication.
- Include only canonical, public, resolvable routes.
- Make environment origin and indexing policy explicit.
- Keep build-time and runtime generation consistent.
- Fail generation on material invalidity only when the repository intends that
  as a build gate.
- Keep structured data factual, page-specific, and aligned with visible content.

Use `references/validation.md` for protocol-specific checks.

## Environment safety

Production should publish the intended canonical origin and crawler policy.
Preview, staging, and development should prevent accidental indexing where
appropriate and must not leak private routes, internal APIs, secret-bearing
URLs, or production-only data.

## Validate

Check:

- syntax and schema
- canonical host and protocol consistency
- route coverage and exclusions
- duplicate, redirected, or broken URLs
- content type and cache behavior
- environment-specific robots and canonical behavior
- image dimensions and resolvability
- JSON-LD correspondence with page content
- security-contact ownership and expiry
- generated-output freshness

When deployment is authorized, verify live responses rather than only build
artifacts. Report selected outputs, source of truth, environment behavior,
checks, and unresolved gaps.
