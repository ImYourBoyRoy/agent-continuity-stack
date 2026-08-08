# Stable package release checklist

This project publishes stable releases only. Do not create parallel release
tracks.

Before publishing a stable release:

1. Confirm `VERSION`, package manifest version, instruction-pack version,
   stable status, README, memory, and changelog agree.
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
21. Create the release archive from an identified clean commit.
22. Validate it with `scripts/validate_archive.py`, extract it,
    and rerun the suite.
23. Confirm `LICENSE` is included, generate and independently verify the
    external SHA-256 sidecar, and record the tag, commit, date, archive name,
    and hash in release notes.
24. Stop if the intended remote tag or release already exists. Otherwise create
    an immutable annotated stable tag and publish a stable GitHub Release with
    the archive and external checksum sidecar.

25. Report each client as verified, installed-unverified, or unavailable.
    Never convert source validation into a claim of live client discovery.

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
