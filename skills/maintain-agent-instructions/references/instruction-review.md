# Instruction review

## Keep

Retain concise rules that:

- prevent repeated material mistakes
- define valid build and verification paths
- protect production, secrets, hardware, or expensive resources
- identify canonical architecture or ownership
- explain a non-obvious repository convention

An explicitly approved user-global operating contract is a separate authority:
review it for contradictions, privacy, and host compatibility, but do not
discard required sections merely to meet a generic brevity target. Use
client-specific imports or adapters when a host imposes a per-file limit.

## Move

Move:

- multi-step task procedures to skills
- executable checks to scripts, hooks, linters, or CI
- architecture explanations to authoritative documentation
- temporary status to issues or handoffs
- external live facts to an integration or current lookup

## Remove or rewrite

Remove:

- generic advice the model already knows
- duplicated or contradictory rules
- stale commands and paths
- unsupported precedence claims
- mandatory ceremony without a demonstrated failure
- personal identity and machine-specific details from public guidance

## Review questions

For each rule, ask:

1. Which tasks need it?
2. Which directory owns it?
3. Can a deterministic tool enforce it?
4. Is it current and testable?
5. Does it expose private or owner-specific information?
6. Will loading it every session justify its token cost, or is it part of an
   explicitly required global contract?
