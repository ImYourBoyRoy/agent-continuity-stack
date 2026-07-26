---
name: red-team-technical-plan
description: Stress-test a material technical plan, architecture, migration, integration, release, or automation proposal before implementation. Use for explicit red-team review, hidden assumptions, failure modes, alternatives, and rollback—not trivial edits.
---

# Red-Team Technical Plan

Challenge a proposal constructively before resources or operational trust are
committed. Produce a stronger plan, not criticism for its own sake.

## Establish the decision

Identify:

- objective, success criteria, and non-goals
- active repository and system boundaries
- known constraints and instruction authorities
- proposed architecture, sequence, and irreversible choices
- users, operators, data, systems, and environments exposed
- evidence already available and claims still assumed

Separate observations, verified facts, inferences, preferences, and
speculation. Do not treat popularity, credentials, a previous model's answer,
or the existence of an implementation as proof.

## Choose review depth

Scale the review to consequence:

- light: local, reversible, low-cost change
- standard: persistent project change or meaningful maintenance burden
- deep: security boundary, production data, broad distribution, expensive
  migration, irreversible state, or multi-system automation

Do not manufacture blockers for trivial work. State the selected depth and why.

## Attack the proposal

Test applicable dimensions:

1. **Problem fit** — Does it solve the actual objective, or a convenient proxy?
2. **Scope** — What hidden systems, repositories, users, and lifecycle work are
   implied?
3. **Assumptions** — Which prerequisites are unverified, unstable, or mutually
   inconsistent?
4. **Correctness** — What inputs, edge cases, concurrency, partial failures, or
   stale state break it?
5. **Security and privacy** — What trust boundaries, permissions, secrets,
   supply-chain inputs, personal data, or unsafe defaults are introduced?
6. **Compatibility** — Which versions, platforms, clients, formats, or APIs are
   untested?
7. **Operations** — How are installation, observability, recovery, ownership,
   upgrades, and support handled?
8. **Maintenance** — What duplicates an existing authority or creates a second
   system that will drift?
9. **Economics** — What token, compute, storage, network, licensing, and human
   review costs recur?
10. **Exit** — Can the change be disabled, downgraded, migrated, or removed
    without losing unrelated state?

For high-impact automation, also examine idempotency, transaction boundaries,
retries, rate limits, duplicate processes, configuration corruption, and
operator interruption.

## Compare alternatives

Include the strongest practical alternatives, including:

- do nothing yet
- narrow pilot
- strengthen an existing capability
- simpler manual or deterministic mechanism
- staged migration
- proposed approach with revised safeguards

Compare them against the same criteria. Do not use a straw alternative to make
the preferred proposal look better.

## Verify material claims

Inspect current project evidence and use authoritative, current sources for
version-sensitive claims. Verify critical findings against source or runtime
behavior when possible. Label unverified risks and avoid converting a possible
failure into a claimed fact.

Do not mutate the project unless the user separately authorizes implementation.

## Produce the decision review

Return:

- verdict: proceed, proceed with changes, pilot first, defer, or reject
- strongest aspects worth preserving
- blocking flaws and why they block
- material non-blocking risks
- assumptions requiring evidence
- alternative comparison
- revised design and acceptance criteria
- validation, monitoring, rollback, and stop conditions
- unresolved questions that materially change the decision

Rank findings by consequence and likelihood. End with the smallest defensible
next step.

