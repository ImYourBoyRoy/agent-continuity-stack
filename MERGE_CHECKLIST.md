# Package and skill release checklist

Before publishing:

1. Confirm `VERSION`, package manifest version, instruction-pack version,
   release status, README, memory, and changelog agree.
2. Confirm `.env` and other local credentials are ignored, absent from the
   release inventory, absent from staged/tracked content, and mode-restricted
   when present.
3. Confirm the normalized UTF-8/LF canonical contract matches its source
   SHA-256 and contains all required sections and only permitted placeholders.
4. Confirm rendered-hash fields exist only in runtime plans, receipts,
   ownership, and client status records.
5. Confirm the model-operated installation protocol remains status-first and
   does not invoke an executable remote installer.
6. Confirm skills-only preserves all instruction sources by default and that
   guided additions or the complete contract require separately reviewable
   authorization.
7. Exercise the public copy-paste prompt against pre-existing custom
   instructions and confirm no wholesale replacement is proposed.
8. Recheck current first-party global-instruction and skill-discovery paths for
   Codex, Cursor, Claude Code, and Antigravity.
9. Runtime-test automatic contract loading in each supported client version;
   label untested adapters honestly.
10. Confirm rendered Antigravity fragments remain below the rule-file limit and
   reconstruct `rendered_sha256`.
11. Inventory built-in, global, plugin, and repository-local skills for trigger
   or ownership collisions.
12. Keep one primary workflow owner. Confirm the optional Astro + Cloudflare
   fallback is uninstalled by default and defers to Portable Web Toolkit.
13. Confirm every core and optional skill has matching version metadata.
14. Review each skill description for one positive intent and meaningful
    exclusions without embedding its full procedure.
15. Run positive, near-miss, and applicable collision cases.
16. Verify linked references, schemas, read-only helpers, and metadata.
17. Confirm no personal names, usernames, emails, profiles, home paths, private
    hosts, credentials, device IDs, or private schemas exist under `skills/`.
18. Reject links, junctions, reparse points, and unsupported special files in
    the published package.
19. Red-team per-client journal recovery, locally modified installed content,
    stale or malicious receipts, duplicate imports, interruption, and rollback.
20. Confirm each skill content hash and every entry in `release-files.json`.
    Reject undeclared archive payloads and verify the external checksum.
21. Run:

    ```bash
    python3 scripts/validate_bundle.py
    python3 scripts/inspect_contract.py source
    python3 scripts/inspect_tree.py . --exclude .git --exclude .env
    python3 tests/run_portable_tests.py
    ```

22. Validate a candidate archive with `scripts/validate_archive.py`, extract it,
    and rerun the suite.
23. Confirm required GitHub branch protection and Actions permissions before
    publishing the canonical remote.
24. Create the final release archive from a clean, identified commit.
25. Record the release commit, date, archive filename, and SHA-256 in release
    notes.
26. Confirm `LICENSE` is included in both the repository and archive.

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
