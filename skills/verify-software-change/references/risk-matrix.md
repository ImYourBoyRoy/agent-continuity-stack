# Verification risk matrix

| Change | Minimum useful evidence | Broaden when |
|---|---|---|
| Documentation only | links, commands, rendered format | examples are executable |
| Local logic | focused unit tests and static checks | shared interfaces changed |
| Public API | contract tests and consumers | compatibility is uncertain |
| Dependency | targeted behavior plus build | runtime or transitive graph changed |
| Configuration | schema and representative startup | multiple environments consume it |
| Refactor | affected tests plus reference search | boundaries or generated code moved |
| Packaging | packaged-artifact install or inspection | multiple platforms are claimed |
| Data migration | dry run, backup, forward and rollback plan | production data is involved |
| Deployment | staging smoke and observability | production authorization is given |
| Security control | negative tests and bypass attempts | threat boundary is material |

Increase depth for high blast radius, weak rollback, security boundaries,
cross-platform claims, concurrency, persistence, or externally consumed
interfaces. Reduce depth only when the claim itself is narrow.

