# Update batching and rollback

## Batch boundaries

Group updates only when they share a compatibility surface or must move
together. Useful batches include:

- runtime plus its package-manager or compiler requirements
- framework plus official adapter packages
- a family of tightly coupled SDK modules
- CI action plus required workflow syntax
- container base plus operating-system package adjustments

Keep independent major migrations separate. Keep security remediation separate
from optional cleanup so urgency and rollback remain clear.

## Baseline

Record:

- relevant Git diff and untracked files
- current resolved versions
- current valid checks
- generated-file ownership
- artifact or deployment version when applicable

Do not require a clean worktree, but identify which changes predate the update.

## Rollback

Prefer the package manager's supported lockfile and manifest restoration path.
Revert only files and generated output owned by the failed batch. Never reset or
discard unrelated work.

For data, infrastructure, or deployment changes, verify backup, downgrade
compatibility, and previous artifact availability before applying the update.

