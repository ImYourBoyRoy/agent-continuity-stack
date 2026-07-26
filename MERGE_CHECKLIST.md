# Package and skill release checklist

Use separate gates for public release candidates and final stable promotion.
Publishing a prerelease does not waive, satisfy, or conceal a stable gate.

## Prerelease publication gate

Before publishing a release candidate:

1. Confirm `VERSION`, package manifest version, instruction-pack version,
   release-candidate status, README, memory, and changelog agree.
2. Confirm `.env` and other local credentials are ignored, absent from the
   release inventory, absent from staged/tracked content, and mode-restricted
   when present.
3. Confirm the normalized UTF-8/LF canonical contract matches its source
   SHA-256 and contains all required sections and only permitted placeholders.
4. Confirm rendered-hash fields exist only in runtime plans, receipts,
   ownership, and client-status records.
5. Confirm the model-operated installation protocol remains status-first and
   does not invoke an executable remote installer.
6. Confirm skills-only preserves all instruction sources by default and that
   guided additions or the complete contract require separately reviewable
   authorization.
7. Exercise the public copy-paste prompt against pre-existing custom
   instructions and confirm no wholesale replacement is proposed.
8. Recheck current first-party client paths. Runtime-test supported clients
   when available and label every untested adapter honestly.
9. Confirm rendered Antigravity fragments remain below the rule-file limit and
   reconstruct `rendered_sha256`.
10. Inventory built-in, global, plugin, and repository-local skills for trigger
    or ownership collisions.
11. Keep one primary workflow owner. Confirm the optional Astro + Cloudflare
    fallback is uninstalled by default and defers to Portable Web Toolkit.
12. Confirm every core and optional skill has matching version metadata.
13. Review each skill description for one positive intent and meaningful
    exclusions without embedding its full procedure.
14. Run positive, near-miss, applicable collision, lifecycle-conformance, and
    archive-safety cases.
15. Verify linked references, schemas, read-only helpers, metadata, content
    hashes, and every entry in `release-files.json`.
16. Confirm no personal names, usernames, emails, profiles, home paths, private
    hosts, credentials, device IDs, or private schemas exist under `skills/`.
17. Reject links, junctions, reparse points, unsupported special files,
    undeclared archive payloads, and checksum mismatches.
18. Red-team disclosed limitations, per-client journal recovery, locally
    modified installed content, stale or malicious receipts, duplicate imports,
    interruption, and rollback. Unresolved runtime results must remain
    prominent in the release notes.
19. Run:

    ```bash
    python3 scripts/validate_bundle.py
    python3 scripts/inspect_contract.py source
    python3 scripts/inspect_tree.py . --exclude .git --exclude .env
    python3 tests/run_portable_tests.py
    ```

20. Confirm required GitHub branch protection, Actions permissions, and CI.
21. Create the candidate archive from an identified clean commit.
22. Validate it with `scripts/validate_archive.py`, extract it,
    and rerun the suite.
23. Confirm `LICENSE` is included, generate and independently verify the
    external SHA-256 sidecar, and record the tag, commit, date, archive name,
    and hash in release notes.
24. Stop if the intended remote tag or release already exists. Otherwise create
    an immutable annotated prerelease tag and mark the GitHub Release
    explicitly as a prerelease.

## Final stable promotion gate

Before promoting to final `3.0.0`:

1. Complete the focused immutable-backup recovery rerun.
2. Runtime-test Cursor with authenticated target-version skill discovery.
3. Install and runtime-test Claude Code in a disposable environment.
4. Prove both Antigravity fragments load in a fresh client session.
5. Validate Windows reparse-point and metadata behavior.
6. Exercise the public installation prompt end to end across all supported
   clients.
7. Review the complete contract's always-on token cost and instruction-priority
   wording.
8. Re-run every prerelease integrity gate against the final package identity,
   create an identified clean final release commit, build and verify new
   artifacts, and publish a non-prerelease release.

Likely overlap areas:

- dependency audits and update bots
- version selection versus broad update auditing
- update implementation versus automated dependency tools
- general verification
- README, memory, and instruction maintenance
- critical review versus ordinary implementation
- CLI engineering
- provider-neutral web workflows versus specialist toolkits
- skill and plugin creators
