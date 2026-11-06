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
from pathlib import Path


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
    assert not any(
        Path(item["path"]).name.casefold() == "memory.md"
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


def test_local_memory_is_ignored_and_unpublishable() -> None:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / "scripts"))
    from validate_bundle import validate_git_index

    with tempfile.TemporaryDirectory(prefix="portable-memory-index-") as temporary:
        repository = Path(temporary)
        subprocess.run(
            ["git", "init", "--quiet", str(repository)], check=True
        )
        (repository / ".gitignore").write_text(
            "[Mm][Ee][Mm][Oo][Rr][Yy].[Mm][Dd]\n", encoding="utf-8"
        )
        ignored = ("MEMORY.md", "nested/mEmOrY.Md")
        for relative in ignored:
            path = repository / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("local-only fixture\n", encoding="utf-8")
        result = subprocess.run(
            ["git", "-C", str(repository), "check-ignore", "--no-index", "--stdin"],
            input="\n".join(ignored) + "\n",
            text=True,
            capture_output=True,
            check=True,
        )
        assert set(result.stdout.splitlines()) == set(ignored)
        subprocess.run(
            ["git", "-C", str(repository), "add", "--force", ignored[1]],
            check=True,
        )
        errors: list[str] = []
        validate_git_index(repository, errors)
        assert errors == [
            "Git index tracks a prohibited local-only MEMORY.md file"
        ]


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
    source = json.loads(run("scripts/inspect_contract.py", "source").stdout)
    assert source["matches_manifest"] is True
    assert source["already_normalized"] is True
    assert source["errors"] == []

    with tempfile.TemporaryDirectory(prefix="portable-rendered-contract-") as temporary:
        area = Path(temporary)
        rendered_text = contract.decode("utf-8")
        values = {
            "operator_name": "Example Operator",
            "operator_email": "operator@example.invalid",
            "personal_site": "https://example.invalid",
            "github_profile": "https://github.com/example",
            "pypi_profile": "https://pypi.org/user/example",
        }
        for key, value in values.items():
            rendered_text = rendered_text.replace(f"{{{{{key}}}}}", value)
        rendered = area / "rendered.md"
        rendered.write_text(rendered_text, encoding="utf-8", newline="\n")
        split_at = rendered_text.index(
            metadata["clients"]["antigravity"]["split_before_heading"]
        )
        part_one = area / "part-1.md"
        part_two = area / "part-2.md"
        part_one.write_text(rendered_text[:split_at], encoding="utf-8", newline="\n")
        part_two.write_text(rendered_text[split_at:], encoding="utf-8", newline="\n")
        result = json.loads(
            run(
                "scripts/inspect_contract.py",
                "rendered",
                str(rendered),
                "--part",
                str(part_one),
                "--part",
                str(part_two),
            ).stdout
        )
        assert result["rendered_sha256"] != metadata["source_sha256"]
        assert result["fragment_reconstruction_matches"] is True
        assert result["unexpected_placeholders"] == []
        assert result["errors"] == []


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

        private_payloads = {**payloads, "nested/mEmOrY.Md": b"local-only\n"}
        private_inventory = {
            **inventory,
            "files": [
                {
                    "path": name,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "bytes": len(content),
                }
                for name, content in sorted(private_payloads.items())
            ],
        }
        private_archive = area / "private-memory.zip"
        with zipfile.ZipFile(private_archive, "w") as archive:
            for name, content in private_payloads.items():
                archive.writestr(f"package/{name}", content)
            archive.writestr(
                "package/release-files.json",
                json.dumps(private_inventory, sort_keys=True).encode("utf-8"),
            )
        run("scripts/validate_archive.py", str(private_archive), expected=1)

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
    assert manifest["version"] == "3.0.0-rc.4"
    optional = {item["name"]: item for item in manifest["optional_skills"]}
    assert optional["build-astro-on-cloudflare"]["install_by_default"] is False

    integration = json.loads(
        (ROOT / "integrations" / "portable-web-toolkit.json").read_text("utf-8")
    )
    assert integration["tested_version"] == "0.3.1"
    assert integration["compatibility"] == "exact-tested"
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
    test_local_memory_is_ignored_and_unpublishable()
    test_update_audit_boundaries()
    test_contract_integrity()
    test_record_schemas()
    test_tree_inspection()
    test_archive_validation()
    test_boundaries_and_integration()
    print("agent continuity source and conformance tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
