---
name: verify-software-change
description: Design and run risk-based verification after software or infrastructure changes, or when asked whether work is fixed or ready. Respect repository-specific remote, hardware, staging, and production constraints.
---

# Verify Software Change

Build the smallest sufficient evidence chain for the actual risk.

## Define the claim

Before running checks, state what must be true. Map each material change to:

- expected behavior
- likely regression surface
- appropriate evidence
- environment required

Read `references/risk-matrix.md` for selecting depth. Do not substitute broad
but irrelevant test volume for targeted evidence.

## Follow project constraints

Read repository instructions and use approved commands. Preserve remote-only,
hardware-bound, sandboxed, staging, production, or resource constraints. Do not
install tools, deploy, access production, or broaden permissions merely to make
verification convenient.

## Execute progressively

1. inspect static consistency and affected references
2. run focused formatter, lint, type, schema, or unit checks
3. test the changed behavior and important failure paths
4. broaden to subsystem, build, packaging, or integration checks when risk
   warrants it
5. use preview, staging, device, or production evidence only when authorized
6. inspect exit status and relevant output
7. classify existing versus introduced warnings and failures

After refactors, check imports, signatures, generated bindings, configuration,
entry points, tests, examples, and documented commands.

## Preserve evidence integrity

- Never fabricate output or convert inspection into an execution claim.
- Do not hide failed attempts or warnings.
- Do not weaken tests to make them pass unless the changed expectation is
  explicitly correct and reviewed.
- Do not discard unrelated work to obtain a clean state.
- Label local, remote, simulated, preview, staging, device, and production
  evidence.
- If a check cannot run, explain why and choose the best non-equivalent evidence
  without calling it equivalent.

## Report

Provide:

- claim evaluated
- commands and environments
- passed behavior
- warnings and failures
- existing versus introduced issues
- areas inspected but not executed
- remaining uncertainty
- readiness conclusion bounded by the evidence
