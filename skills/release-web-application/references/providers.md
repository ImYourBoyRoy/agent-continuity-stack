# Provider routing

Use current first-party documentation and repository configuration after
identifying the provider.

## Static or managed site

Verify build command, publish directory, redirects, headers, environment
variables, preview behavior, cache invalidation, and atomic rollback.

## Serverless or edge

Verify runtime compatibility, bindings, compatibility dates, routes, assets,
secrets, observability, limits, and version rollback.

## Container

Verify base-image provenance, immutable digest, build reproducibility, registry,
health checks, resource limits, migrations, rollout strategy, and previous image
availability.

## Generic CI release

Verify the workflow trigger, protected environment, artifact provenance,
permissions, concurrency, approval gates, and exact commit-to-artifact mapping.

Do not substitute a locally remembered CLI command for a repository-owned
release workflow.

