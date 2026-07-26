# Astro and Cloudflare architecture decisions

## Static output

Choose static output when all required routes can be generated ahead of time
and runtime bindings are unnecessary. Confirm dynamic paths, forms,
authentication, preview content, redirects, and headers still have an owner.

## Server rendering

Choose server rendering when requests require runtime data, identity, bindings,
personalization, or dynamic routing. Review runtime API compatibility, caching,
cold-start behavior, error handling, and local emulation.

## Pages versus Workers

Compare current first-party support for the required Astro adapter, assets,
bindings, routing, previews, observability, and organization constraints. Do
not choose from historical familiarity.

## Compatibility set

Verify together:

- Astro, adapter, and Vite versions;
- Node and package-manager requirements;
- Wrangler version;
- compatibility date and flags;
- runtime bindings.

Avoid partially upgrading this set without checking the supported matrix.

## Configuration boundaries

Keep public build-time variables explicit, secrets server-side, local values
ignored or safely templated, typed bindings synchronized, preview and
production origins distinct, and generated configuration derived from one
source.

