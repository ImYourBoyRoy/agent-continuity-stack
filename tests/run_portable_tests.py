#!/usr/bin/env python3
"""Run offline source, helper, schema, and conformance-fixture tests."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


def run(*arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [PYTHON, *arguments],
        cwd=ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"expected exit {expected}, got {result.returncode}\n"
            f"command: {' '.join(arguments)}\nstdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def canonical_plan_digest(plan: dict) -> str:
    content = {
        key: value
        for key, value in plan.items()
        if key not in {"plan_sha256", "authorization", "apply_authorized"}
    }
    return hashlib.sha256(
        json.dumps(
            content,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def test_bundle_and_inventory() -> None:
    result = run("scripts/validate_bundle.py")
    summary = json.loads(result.stdout.splitlines()[-1])
    assert summary["core_skills"] == 14
    assert summary["optional_skills"] == 1
    assert summary["errors"] == 0
    release_inventory = json.loads((ROOT / "release-files.json").read_text("utf-8"))

    def is_private_agent_state(relative: str) -> bool:
        parts = tuple(part.casefold() for part in PurePosixPath(relative).parts)
        if parts and parts[-1] in {
            "memory.md",
            "agents.override.md",
            "claude.local.md",
        }:
            return True
        return any(
            part == ".claude"
            and index + 1 < len(parts)
            and parts[index + 1] == "settings.local.json"
            for index, part in enumerate(parts)
        )

    assert not any(
        is_private_agent_state(item["path"])
        for item in release_inventory["files"]
    )

    fixture = ROOT / "tests" / "fixtures" / "update-audit"
    run(
        "skills/audit-project-updates/scripts/validate_update_check.py",
        str(fixture / ".update-check.json"),
    )
    result = run(
        "skills/audit-project-updates/scripts/inventory_update_sources.py",
        "--root",
        str(fixture),
    )
    inventory = json.loads(result.stdout)
    kinds = {item["kind"] for item in inventory["surfaces"]}
    required = {
        "rust-manifest",
        "javascript-manifest",
        "container-build",
        "github-workflow",
        "explicit-update-sources",
    }
    assert required <= kinds, (required - kinds, inventory)
    assert inventory["network_used"] is False
    assert inventory["files_modified"] is False
    assert inventory["root"] == "."
    assert inventory["absolute_root_disclosed"] is False
    assert str(fixture) not in result.stdout
    assert inventory["explicit_sources"][0]["id"] == "companion-tool"


def test_git_local_agent_state_guard() -> None:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / "scripts"))
    from validate_bundle import validate_git_index

    with tempfile.TemporaryDirectory(prefix="portable-agent-state-index-") as temporary:
        repository = Path(temporary)
        local_claude = repository / "nested" / ".claude"
        local_claude.mkdir(parents=True)
        (repository / "nested" / "mEmOrY.Md").write_text(
            "local-only\n", encoding="utf-8"
        )
        (repository / "nested" / "AGENTS.override.md").write_text(
            "local-only\n", encoding="utf-8"
        )
        (local_claude / "settings.local.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(
            ["git", "init", "--quiet", str(repository)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(repository), "add", "nested"],
            check=True,
            capture_output=True,
        )
        errors: list[str] = []
        validate_git_index(repository, errors)
        assert errors == [
            "Git index tracks prohibited local-only agent state"
        ]


def test_local_agent_state_is_gitignored() -> None:
    with tempfile.TemporaryDirectory(prefix="portable-local-state-ignore-") as temporary:
        repository = Path(temporary)
        (repository / ".gitignore").write_bytes((ROOT / ".gitignore").read_bytes())
        subprocess.run(
            ["git", "init", "--quiet", str(repository)],
            check=True,
            capture_output=True,
        )
        ignored_paths = (
            "MEMORY.md",
            "nested/mEmOrY.Md",
            "AGENTS.override.md",
            "nested/AGENTS.override.md",
            "CLAUDE.local.md",
            "nested/CLAUDE.local.md",
            ".claude/settings.local.json",
            "nested/.claude/settings.local.json",
        )
        for relative in ignored_paths:
            path = repository / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("local-only\n", encoding="utf-8")
            result = subprocess.run(
                ["git", "-C", str(repository), "check-ignore", "--quiet", relative],
                check=False,
                capture_output=True,
            )
            assert result.returncode == 0, f"Git does not ignore {relative}"

        shared_settings = repository / "nested" / ".claude" / "settings.json"
        shared_settings.write_text("{}\n", encoding="utf-8")
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "check-ignore",
                "--quiet",
                "nested/.claude/settings.json",
            ],
            check=False,
            capture_output=True,
        )
        assert result.returncode == 1, "shared Claude project settings must remain trackable"


def test_update_audit_boundaries() -> None:
    validator = "skills/audit-project-updates/scripts/validate_update_check.py"
    inventory_script = (
        "skills/audit-project-updates/scripts/inventory_update_sources.py"
    )
    with tempfile.TemporaryDirectory(prefix="portable-update-boundaries-") as temporary:
        area = Path(temporary)
        invalid = area / "invalid.json"
        invalid.write_text(
            json.dumps(
                {
                    "schema": 1,
                    "sources": [
                        {
                            "id": "unsafe-source",
                            "kind": "repository",
                            "locator": "https://embedded-token@code.example.org/public/tool.git",
                            "purpose": "Must be rejected",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        run(validator, str(invalid), expected=1)
        invalid.write_text(
            json.dumps(
                {
                    "schema": 1,
                    "sources": [
                        {
                            "id": "incomplete-pin",
                            "kind": "git-pin",
                            "locator": "https://code.example.org/public/tool.git",
                            "purpose": "Must include the current immutable ref",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        run(validator, str(invalid), expected=1)

        outside = area / "outside.txt"
        outside.write_text(
            "https://code.example.org/private/unrelated-tool.git\n",
            encoding="utf-8",
        )
        project = area / "project"
        project.mkdir()
        (project / "README.md").symlink_to(outside)
        result = run(inventory_script, "--root", str(project))
        inventory = json.loads(result.stdout)
        assert inventory["declared_candidates"] == []
        assert str(area) not in result.stdout


def test_contract_integrity() -> None:
    metadata = json.loads((ROOT / "instruction-pack.json").read_text("utf-8"))
    contract = (ROOT / metadata["source"]).read_bytes()
    assert hashlib.sha256(contract).hexdigest() == metadata["source_sha256"]
    contract_text = contract.decode("utf-8")
    normalized_contract_text = " ".join(contract_text.split())
    for required in (
        "## First-run personalization",
        "Use explicit values already supplied in the current user instructions",
        "Do not prompt for missing fields by default",
        "remove the entire Operator Profile section",
    ):
        assert required in normalized_contract_text
    source = json.loads(run("scripts/inspect_contract.py", "source").stdout)
    assert source["matches_manifest"] is True
    assert source["already_normalized"] is True
    assert source["errors"] == []

    readme = (ROOT / "README.md").read_text("utf-8")
    installation_policy = readme.split("## Resolve installation choices", 1)[1].split(
        "## Copy-paste installation prompt", 1
    )[0]
    assert "Resolve choices from the user's request" in installation_policy
    assert "Do not ask the user to repeat supplied choices" in installation_policy
    assert "must ask rather than infer" not in readme
    prompt = readme.split("## Copy-paste installation prompt", 1)[1].split(
        "## Package layout", 1
    )[0]
    assert "Do not ask me to repeat" in prompt
    assert "Use `preserve-existing` as the default instruction mode" in prompt
    assert "Ask me which clients to select" not in prompt

    with tempfile.TemporaryDirectory(prefix="portable-rendered-contract-") as temporary:
        area = Path(temporary)
        profile = area / "operator-profile.json"
        profile.write_text(
            json.dumps(
                {
                    "operator_name": "Example Operator",
                    "github_profile": "https://github.com/example",
                }
            ),
            encoding="utf-8",
        )
        rendered = area / "rendered.md"
        render_result = json.loads(
            run(
                "scripts/render_contract.py",
                "--profile-json",
                str(profile),
                "--output",
                str(rendered),
            ).stdout
        )
        rendered_text = rendered.read_text(encoding="utf-8")
        assert render_result["included_fields"] == [
            "github_profile",
            "operator_name",
        ]
        assert render_result["omitted_fields"] == [
            "operator_email",
            "personal_site",
            "pypi_profile",
        ]
        assert render_result["package_files_modified"] is False
        if os.name == "posix":
            assert stat.S_IMODE(rendered.stat().st_mode) == 0o600
        assert "* Name: `Example Operator`" in rendered_text
        assert "* GitHub: `https://github.com/example`" in rendered_text
        for unanswered in ("* Email:", "* Personal site:", "* PyPI:"):
            assert unanswered not in rendered_text
        assert "{{" not in rendered_text

        complete_values = {
            "operator_name": "Example Operator",
            "operator_email": "operator@example.test",
            "personal_site": "https://example.test",
            "github_profile": "https://github.com/example",
            "pypi_profile": "https://pypi.org/user/example/",
        }
        complete_profile = area / "complete-profile.json"
        complete_profile.write_text(json.dumps(complete_values), encoding="utf-8")
        complete_output = area / "complete-rendered.md"
        complete_result = json.loads(
            run(
                "scripts/render_contract.py",
                "--profile-json",
                str(complete_profile),
                "--output",
                str(complete_output),
            ).stdout
        )
        complete_text = complete_output.read_text(encoding="utf-8")
        assert complete_result["included_fields"] == sorted(complete_values)
        assert complete_result["omitted_fields"] == []
        assert all(value in complete_text for value in complete_values.values())
        assert "{{" not in complete_text

        source_hash = hashlib.sha256(
            (ROOT / metadata["source"]).read_bytes()
        ).hexdigest()
        assert source_hash == metadata["source_sha256"]
        package_output = ROOT / "tests" / "fixtures" / "rendered-in-repo.md"
        run(
            "scripts/render_contract.py",
            "--profile-json",
            str(profile),
            "--output",
            str(package_output),
            expected=1,
        )
        assert not package_output.exists()
        run(
            "scripts/render_contract.py",
            "--profile-json",
            str(profile),
            "--output",
            str(rendered),
            expected=1,
        )

        antigravity = metadata["clients"]["antigravity"]
        frontmatter = antigravity["frontmatter"]
        rule = area / "expert-agent-operating-contract.md"
        rule.write_text(
            "---\n"
            f"trigger: {frontmatter['trigger']}\n"
            f"description: {frontmatter['description']}\n"
            "---\n"
            + rendered_text,
            encoding="utf-8",
            newline="\n",
        )
        result = json.loads(
            run(
                "scripts/inspect_contract.py",
                "rendered",
                str(rendered),
                "--antigravity-rule",
                str(rule),
            ).stdout
        )
        assert result["rendered_sha256"] != metadata["source_sha256"]
        assert result["antigravity_rule"]["body_matches_rendered_contract"] is True
        assert result["antigravity_rule"]["below_limit"] is True
        assert result["unresolved_placeholders"] == []
        assert result["errors"] == []

        empty_profile = area / "empty-profile.json"
        empty_profile.write_text("{}\n", encoding="utf-8")
        empty_profile_output = area / "empty-profile.md"
        empty_result = json.loads(
            run(
                "scripts/render_contract.py",
                "--profile-json",
                str(empty_profile),
                "--output",
                str(empty_profile_output),
            ).stdout
        )
        empty_profile_text = empty_profile_output.read_text(encoding="utf-8")
        assert empty_result["included_fields"] == []
        assert empty_result["omitted_fields"] == sorted(
            metadata["renderable_placeholders"]
        )
        assert "## Operator Profile" not in empty_profile_text
        assert "## Authorship and Ownership" in empty_profile_text
        assert "{{" not in empty_profile_text
        result = json.loads(
            run(
                "scripts/inspect_contract.py",
                "rendered",
                str(empty_profile_output),
            ).stdout
        )
        assert result["unresolved_placeholders"] == []
        assert result["errors"] == []

        invalid_profile = area / "unknown-profile-field.json"
        invalid_profile.write_text('{"unknown_field": "value"}\n', encoding="utf-8")
        invalid_output = area / "invalid.md"
        result = json.loads(
            run(
                "scripts/render_contract.py",
                "--profile-json",
                str(invalid_profile),
                "--output",
                str(invalid_output),
                expected=1,
            ).stdout
        )
        assert "unknown fields" in result["errors"][0]
        assert not invalid_output.exists()

        invalid_email = area / "invalid-email.json"
        invalid_email.write_text(
            '{"operator_email": "not an email"}\n', encoding="utf-8"
        )
        result = json.loads(
            run(
                "scripts/render_contract.py",
                "--profile-json",
                str(invalid_email),
                "--output",
                str(invalid_output),
                expected=1,
            ).stdout
        )
        assert "single plain-text email" in result["errors"][0]
        assert not invalid_output.exists()

        in_package_profile = ROOT / "tests" / "fixtures" / "private-profile.json"
        run(
            "scripts/render_contract.py",
            "--profile-json",
            str(in_package_profile),
            "--output",
            str(invalid_output),
            expected=1,
        )


def test_portable_web_toolkit_boundary() -> None:
    metadata = json.loads(
        (ROOT / "integrations" / "portable-web-toolkit.json").read_text("utf-8")
    )
    assert metadata["tested_version"] == "0.4.0"
    assert metadata["skill_pack_version"] == "1.4.0"
    assert metadata["compatibility"] == "exact-tested"
    assert len(metadata["release_commit"]) == 40
    assert len(metadata["manifest_sha256"]) == 64
    assert {
        "discovery-doctor",
        "wcag-auditor",
        "site-onboarding",
        "site-maintenance",
    } <= set(metadata["toolkit_owned_skills"])
    expected_deferrals = {
        "release-web-application",
        "web-discovery-artifacts",
        "maintain-web-design-system",
        "prepare-web-assets",
    }
    assert set(metadata["deferring_generic_skills"]) == expected_deferrals
    assert metadata["optional_fallback_skill"] == "build-astro-on-cloudflare"


def test_record_schemas() -> None:
    records = ROOT / "tests" / "fixtures" / "records"
    mapping = {
        "install-status": "install-status",
        "install-plan": "install-plan",
        "transaction-receipt": "transaction-receipt",
        "client-status": "client-status",
        "ownership-record": "ownership-record",
        "rollback-receipt": "rollback-receipt",
        "operation-journal": "operation-journal",
    }
    for schema_name, record_name in mapping.items():
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / f"{schema_name}.schema.json"),
            str(records / f"{record_name}.json"),
        )
    run(
        "scripts/validate_record.py",
        str(ROOT / "schemas" / "install-plan.schema.json"),
        str(records / "install-plan.json"),
        "--allowed-client-root",
        "/disposable-home/skills",
        "--allowed-state-root",
        "/disposable-state",
        "--require-applicable",
    )
    run(
        "scripts/validate_record.py",
        str(ROOT / "schemas" / "client-status.schema.json"),
        str(
            ROOT
            / "tests"
            / "evidence"
            / "historical"
            / "codex-0.146.0-alpha.3-linux-project.json"
        ),
    )

    with tempfile.TemporaryDirectory(prefix="portable-invalid-record-") as temporary:
        invalid = Path(temporary) / "invalid.json"
        invalid.write_text('{"schema_version": 1}', encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        valid_plan = json.loads(
            (records / "install-plan.json").read_text(encoding="utf-8")
        )
        all_skip = json.loads(json.dumps(valid_plan))
        all_skip["operations"][0]["action"] = "skip"
        all_skip["apply_authorized"] = True
        all_skip["plan_sha256"] = canonical_plan_digest(all_skip)
        all_skip["authorization"] = {
            "status": "approved",
            "approved_plan_sha256": all_skip["plan_sha256"],
            "approved_at": "2026-07-26T20:00:01Z",
        }
        invalid.write_text(json.dumps(all_skip), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        implicit_contract = json.loads(json.dumps(valid_plan))
        implicit_contract["rendered_sha256"] = "a" * 64
        implicit_contract["plan_sha256"] = canonical_plan_digest(implicit_contract)
        invalid.write_text(json.dumps(implicit_contract), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        preserve_mutation = json.loads(json.dumps(valid_plan))
        preserve_mutation["operations"][0]["target_kind"] = "instruction"
        preserve_mutation["plan_sha256"] = canonical_plan_digest(preserve_mutation)
        invalid.write_text(json.dumps(preserve_mutation), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        broad_root = json.loads(json.dumps(valid_plan))
        broad_root["operations"][0].update(
            {"client_root": "/etc", "target_relative": "passwd"}
        )
        broad_root["plan_sha256"] = canonical_plan_digest(broad_root)
        invalid.write_text(json.dumps(broad_root), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        false_binding = json.loads(json.dumps(valid_plan))
        false_binding["state_root"] = "/home/alice/.ssh"
        false_binding["operations"][0].update(
            {
                "client_root": "/home/alice/.ssh",
                "target_relative": "authorized_keys",
                "backup": "authorized_keys",
            }
        )
        false_binding["plan_sha256"] = canonical_plan_digest(false_binding)
        invalid.write_text(json.dumps(false_binding), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            "--allowed-client-root",
            "/disposable-home/skills",
            "--allowed-state-root",
            "/disposable-state",
            "--require-applicable",
            expected=1,
        )

        invalid.write_text(
            json.dumps(
                {
                    **valid_plan,
                    "selected_clients": ["unknown-client"],
                    "blockers": ["unsafe target"],
                    "apply_authorized": True,
                    "authorization": {
                        "status": "approved",
                        "approved_plan_sha256": "0" * 64,
                        "approved_at": "2026-07-26T20:00:01Z",
                    },
                }
            ),
            encoding="utf-8",
        )
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "install-plan.schema.json"),
            str(invalid),
            expected=1,
        )

        incoherent_journal = json.loads(
            (records / "operation-journal.json").read_text(encoding="utf-8")
        )
        incoherent_journal["phase"] = "complete"
        incoherent_journal["targets"][0].update(
            {
                "phase": "planned",
                "staged_sha256": None,
                "post_sha256": None,
            }
        )
        invalid.write_text(json.dumps(incoherent_journal), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "operation-journal.schema.json"),
            str(invalid),
            expected=1,
        )

        empty_receipt = json.loads(
            (records / "transaction-receipt.json").read_text(encoding="utf-8")
        )
        empty_receipt["mutations"] = []
        empty_receipt["backups"] = ["../../victim"]
        invalid.write_text(json.dumps(empty_receipt), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "transaction-receipt.schema.json"),
            str(invalid),
            expected=1,
        )

        invalid_transaction = json.loads(
            (records / "transaction-receipt.json").read_text(encoding="utf-8")
        )
        invalid_transaction["mutations"][0].update(
            {
                "client_root": "/",
                "target_relative": "../../victim",
                "action": "delete-anything",
                "post_sha256": "not-a-hash",
            }
        )
        invalid_transaction["backups"] = ["../../victim"]
        invalid.write_text(json.dumps(invalid_transaction), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "transaction-receipt.schema.json"),
            str(invalid),
            expected=1,
        )

        invalid_ownership = json.loads(
            (records / "ownership-record.json").read_text(encoding="utf-8")
        )
        invalid_ownership.update(
            {
                "content_kind": "global-contract",
                "rendered_sha256": None,
            }
        )
        invalid.write_text(json.dumps(invalid_ownership), encoding="utf-8")
        run(
            "scripts/validate_record.py",
            str(ROOT / "schemas" / "ownership-record.schema.json"),
            str(invalid),
            expected=1,
        )


def test_tree_inspection() -> None:
    with tempfile.TemporaryDirectory(prefix="portable-tree-inspection-") as temporary:
        area = Path(temporary)
        safe = area / "safe"
        safe.mkdir()
        (safe / "file.txt").write_text("safe\n", encoding="utf-8")
        result = json.loads(run("scripts/inspect_tree.py", str(safe)).stdout)
        assert result["safe"] is True
        assert result["files_modified"] is False

        root_link = area / "root-link"
        root_link.symlink_to(safe, target_is_directory=True)
        run("scripts/inspect_tree.py", str(root_link), expected=1)
        root_link.unlink()

        outside = area / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        (safe / "link").symlink_to(outside)
        run("scripts/inspect_tree.py", str(safe), expected=1)
        (safe / "link").unlink()

        (safe / "Name.txt").write_text("one\n", encoding="utf-8")
        (safe / "name.txt").write_text("two\n", encoding="utf-8")
        run("scripts/inspect_tree.py", str(safe), expected=1)
        (safe / "Name.txt").unlink()
        (safe / "name.txt").unlink()

        if hasattr(os, "mkfifo"):
            fifo = safe / "fixture.fifo"
            os.mkfifo(fifo)
            run("scripts/inspect_tree.py", str(safe), expected=1)
            fifo.unlink()


def test_archive_validation() -> None:
    with tempfile.TemporaryDirectory(prefix="portable-archive-validation-") as temporary:
        area = Path(temporary)
        safe_archive = area / "safe.zip"
        payloads = {
            "manifest.json": b"{}\n",
            "VERSION": b"0.0.0-test\n",
            "LICENSE": b"test\n",
        }
        inventory = {
            "schema": 1,
            "hash_algorithm": "sha256",
            "excluded": ["release-files.json"],
            "files": [
                {
                    "path": name,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                }
                for name, content in sorted(payloads.items())
            ],
        }
        with zipfile.ZipFile(safe_archive, "w") as archive:
            for name, content in payloads.items():
                archive.writestr(f"package/{name}", content)
            archive.writestr(
                "package/release-files.json",
                json.dumps(inventory, sort_keys=True).encode("utf-8"),
            )
        result = json.loads(
            run("scripts/validate_archive.py", str(safe_archive)).stdout
        )
        assert result["safe"] is True

        memory_archive = area / "private-memory.zip"
        private_memory = b"private local notes\n"
        memory_payloads = {
            **payloads,
            "mEmOrY.Md": private_memory,
            "nested/AGENTS.override.md": b"local override\n",
            ".claude/settings.local.json": b"{}\n",
        }
        memory_inventory = {
            "schema": 1,
            "hash_algorithm": "sha256",
            "excluded": ["release-files.json"],
            "files": [
                {
                    "path": name,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                }
                for name, content in sorted(memory_payloads.items())
            ],
        }
        with zipfile.ZipFile(memory_archive, "w") as archive:
            for name, content in memory_payloads.items():
                archive.writestr(f"package/{name}", content)
            archive.writestr(
                "package/release-files.json",
                json.dumps(memory_inventory, sort_keys=True).encode("utf-8"),
            )
        memory_result = run(
            "scripts/validate_archive.py", str(memory_archive), expected=1
        )
        assert "prohibited private local agent state" in memory_result.stdout

        undeclared = area / "undeclared.zip"
        with zipfile.ZipFile(undeclared, "w") as archive:
            for name, content in payloads.items():
                archive.writestr(f"package/{name}", content)
            archive.writestr(
                "package/release-files.json",
                json.dumps(inventory, sort_keys=True).encode("utf-8"),
            )
            archive.writestr("package/unlisted.env", "secret=value\n")
        run("scripts/validate_archive.py", str(undeclared), expected=1)

        traversal = area / "traversal.zip"
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr("../escape.txt", "unsafe\n")
        run("scripts/validate_archive.py", str(traversal), expected=1)

        collision = area / "collision.zip"
        with zipfile.ZipFile(collision, "w") as archive:
            archive.writestr("package/Name.txt", "one\n")
            archive.writestr("package/name.txt", "two\n")
        run("scripts/validate_archive.py", str(collision), expected=1)

        symlink_archive = area / "symlink.zip"
        symlink = zipfile.ZipInfo("package/link")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(symlink_archive, "w") as archive:
            archive.writestr(symlink, "target")
        run("scripts/validate_archive.py", str(symlink_archive), expected=1)


def test_boundaries_and_integration() -> None:
    assert not (ROOT / "scripts" / "install_skills.py").exists()
    manifest = json.loads((ROOT / "manifest.json").read_text("utf-8"))
    assert manifest["package"] == "agent-continuity-stack"
    assert manifest["version"] == "3.2.0"
    optional = {item["name"]: item for item in manifest["optional_skills"]}
    assert optional["build-astro-on-cloudflare"]["install_by_default"] is False

    integration = json.loads(
        (ROOT / "integrations" / "portable-web-toolkit.json").read_text("utf-8")
    )
    assert integration["tested_version"] == "0.4.0"
    assert integration["compatibility"] == "exact-tested"
    assert "no live cross-project runtime" in integration["validation_notes"]
    assert integration["install_automatically"] is False
    assert len(integration["release_commit"]) == 40
    assert len(integration["skill_content_base_commit"]) == 40

    optional_skill = (
        ROOT / "optional_skills" / "build-astro-on-cloudflare" / "SKILL.md"
    ).read_text("utf-8")
    assert "default-uninstalled" in optional_skill
    assert "If Portable Web Toolkit management is established" in optional_skill


def main() -> int:
    test_bundle_and_inventory()
    test_git_local_agent_state_guard()
    test_local_agent_state_is_gitignored()
    test_update_audit_boundaries()
    test_contract_integrity()
    test_portable_web_toolkit_boundary()
    test_record_schemas()
    test_tree_inspection()
    test_archive_validation()
    test_boundaries_and_integration()
    print("agent continuity source and conformance tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
