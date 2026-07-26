## Summary

Describe the problem, selected owner, and resulting behavior.

## Scope and compatibility

- Package version change:
- Skill version change:
- Clients or operating systems affected:
- Instruction, integration, security, or rollback impact:

## Validation

- [ ] `python3 scripts/validate_bundle.py`
- [ ] `python3 scripts/inspect_contract.py source`
- [ ] `python3 scripts/inspect_tree.py . --exclude .git --exclude .env`
- [ ] `python3 tests/run_portable_tests.py`
- [ ] Applicable live-client smoke tests
- [ ] Positive, near-miss, and collision cases updated

## Documentation and safety

- [ ] README, memory, architecture, changelog, and handoff are current
- [ ] No secrets, personal paths, private hosts, or machine-specific data
- [ ] Existing custom instructions remain preserved by default
- [ ] Rollback and unverified surfaces are stated
