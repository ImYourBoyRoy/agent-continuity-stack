#!/usr/bin/env python3
"""Validate the stable source bundle without third-party packages."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from inspect_tree import inspect as inspect_tree


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDER_RE = re.compile(r"\{\{([a-z0-9_]+)\}\}")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PRIVATE_IPV4_RE = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
)
EMBEDDED_CREDENTIAL_RE = re.compile(
    r"https?://[^/\s:@]+:[^/\s@]+@|https?://[^/\s@]+@",
    re.IGNORECASE,
)
PORTABILITY_PATTERNS = {
    "absolute Linux home": re.compile(r"/home/[A-Za-z0-9_.-]+/"),
    "absolute macOS home": re.compile(r"/Users/[A-Za-z0-9_.-]+/"),
    "absolute Windows user": re.compile(
        r"[A-Za-z]:\\Users\\[A-Za-z0-9_. -]+\\", re.IGNORECASE
    ),
    "template marker": re.compile(
        r"\{\{[^}]+\}\}|\[TODO(?::[^\]]*)?\]", re.IGNORECASE
    ),
    "email address": re.compile(
        r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])"
    ),
}
TOP_LEVEL_PRIVACY_PATTERNS = {
    key: value for key, value in PORTABILITY_PATTERNS.items() if key != "template marker"
}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: missing opening YAML delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path}: missing closing YAML delimiter") from error

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}: unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in fields:
            raise ValueError(f"{path}: duplicate frontmatter field {key!r}")
        fields[key] = value
    return fields, "\n".join(lines[end + 1 :])


def parse_openai_metadata(text: str, path: Path) -> dict[str, str]:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines or lines[0].strip() != "interface:":
        raise ValueError(f"{path}: expected interface mapping")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if not line.startswith("  ") or ":" not in line:
            raise ValueError(f"{path}: unsupported metadata line {line!r}")
        key, value = line.strip().split(":", 1)
        value = value.strip()
        if len(value) < 2 or value[0] != '"' or value[-1] != '"':
            raise ValueError(f"{path}: {key} must be a quoted string")
        if key in fields:
            raise ValueError(f"{path}: duplicate metadata field {key!r}")
        fields[key] = value[1:-1]
    expected = {"display_name", "short_description", "default_prompt"}
    if set(fields) != expected:
        raise ValueError(
            f"{path}: interface fields mismatch "
            f"missing={sorted(expected - set(fields))} "
            f"extra={sorted(set(fields) - expected)}"
        )
    if not 12 <= len(fields["short_description"]) <= 80:
        raise ValueError(f"{path}: short_description must be 12-80 characters")
    return fields


def read_json(path: Path, errors: list[str]) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        errors.append(f"{path}: invalid JSON or UTF-8: {error}")
        return None


def manifest_versions(
    entries: object, label: str, errors: list[str]
) -> dict[str, str]:
    if not isinstance(entries, list) or not all(
        isinstance(item, dict) for item in entries
    ):
        errors.append(f"manifest {label} must be versioned objects")
        return {}
    versions: dict[str, str] = {}
    for entry in entries:
        name = entry.get("name", "")
        version = entry.get("version", "")
        if name in versions:
            errors.append(f"manifest contains duplicate {label} entry {name}")
        versions[name] = version
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append(f"manifest {label} name is invalid: {name!r}")
        if not SEMVER_RE.fullmatch(version):
            errors.append(f"manifest {label} {name} has invalid version {version!r}")
    return versions


def is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def inspect_package_types(root: Path, errors: list[str]) -> None:
    case_paths: dict[str, str] = {}
    text_suffixes = {".md", ".json", ".yaml", ".yml", ".py"}
    for directory, names, files in os.walk(root, followlinks=False):
        names[:] = [name for name in names if name != ".git"]
        current = Path(directory)
        for name in [*names, *files]:
            path = current / name
            metadata = path.lstat()
            relative = path.relative_to(root)
            relative_text = relative.as_posix()
            folded = relative_text.casefold()
            previous = case_paths.get(folded)
            if previous is not None and previous != relative_text:
                errors.append(
                    f"case-insensitive collision: {previous!r} and {relative_text!r}"
                )
            case_paths[folded] = relative_text
            if is_reparse(metadata):
                errors.append(f"{relative}: reparse point or junction")
            elif stat.S_ISLNK(metadata.st_mode):
                errors.append(f"{relative}: symlink is not package content")
            elif not (stat.S_ISDIR(metadata.st_mode) or stat.S_ISREG(metadata.st_mode)):
                errors.append(f"{relative}: unsupported special file")
            elif stat.S_ISREG(metadata.st_mode) and (
                path.suffix in text_suffixes
                or path.name in {"VERSION", "LICENSE", ".gitattributes"}
            ):
                content = path.read_bytes()
                if content.startswith(b"\xef\xbb\xbf"):
                    errors.append(f"{relative}: UTF-8 BOM is forbidden")
                try:
                    text = content.decode("utf-8")
                except UnicodeDecodeError as error:
                    errors.append(f"{relative}: invalid UTF-8: {error}")
                    continue
                if "\r" in text:
                    errors.append(f"{relative}: text is not LF-normalized")


def validate_release_inventory(root: Path, errors: list[str]) -> None:
    inventory_path = root / "release-files.json"
    inventory = read_json(inventory_path, errors)
    if not isinstance(inventory, dict):
        return
    if (
        inventory.get("schema") != 1
        or inventory.get("hash_algorithm") != "sha256"
        or inventory.get("excluded") != ["release-files.json"]
    ):
        errors.append("release-files.json has invalid metadata")
        return
    declared_entries = inventory.get("files")
    if not isinstance(declared_entries, list):
        errors.append("release-files.json files must be an array")
        return
    declared: dict[str, dict] = {}
    forbidden_names = {
        ".env",
        ".env.local",
        "id_rsa",
        "id_ed25519",
    }
    forbidden_suffixes = {
        ".key",
        ".pem",
        ".p12",
        ".pfx",
        ".pyc",
        ".zip",
        ".tar",
        ".gz",
        ".7z",
    }
    for entry in declared_entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            errors.append("release-files.json contains a malformed entry")
            continue
        relative = entry.get("path")
        if (
            not isinstance(relative, str)
            or not relative
            or relative.startswith("/")
            or "\\" in relative
            or ".." in Path(relative).parts
        ):
            errors.append(f"release-files.json contains unsafe path {relative!r}")
            continue
        if relative in declared:
            errors.append(f"release-files.json duplicates {relative!r}")
        path_parts = Path(relative).parts
        if (
            any(part in forbidden_names or part == "__pycache__" for part in path_parts)
            or Path(relative).suffix.lower() in forbidden_suffixes
        ):
            errors.append(f"release inventory contains forbidden file {relative!r}")
        declared[relative] = entry

    actual: dict[str, dict] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(root).parts:
            continue
        relative_path = path.relative_to(root)
        relative = relative_path.as_posix()
        if relative == "release-files.json":
            continue
        if any(
            part == ".env" or (part.startswith(".env.") and part != ".env.example")
            for part in relative_path.parts
        ):
            continue
        content = path.read_bytes()
        actual[relative] = {
            "path": relative,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
        }
    if declared != actual:
        missing = sorted(set(actual) - set(declared))
        extra = sorted(set(declared) - set(actual))
        changed = sorted(
            path
            for path in set(actual) & set(declared)
            if actual[path] != declared[path]
        )
        errors.append(
            "release inventory mismatch: "
            f"missing={missing} extra={extra} changed={changed}"
        )


def validate_skill(
    skill_root: Path,
    name: str,
    version: str,
    optional: bool,
    errors: list[str],
    warnings: list[str],
) -> int:
    skill_path = skill_root / "SKILL.md"
    try:
        text = skill_path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text, skill_path)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        errors.append(str(error))
        return 0

    if set(fields) != {"name", "description"}:
        errors.append(f"{skill_path}: frontmatter must contain name and description")
    if fields.get("name") != name:
        errors.append(f"{skill_path}: name does not match directory")
    description = fields.get("description", "")
    if not 80 <= len(description) <= 1024:
        errors.append(f"{skill_path}: description length is outside 80-1024")
    if len(text.splitlines()) > 500:
        errors.append(f"{skill_path}: exceeds 500 lines")
    if len(body.strip()) < 120:
        errors.append(f"{skill_path}: body is unexpectedly small")

    skill_manifest_path = skill_root / "skill-manifest.json"
    skill_manifest = read_json(skill_manifest_path, errors)
    content_status = inspect_tree(skill_root, {"skill-manifest.json"})
    content_hash = content_status.get("tree_sha256")
    expected_manifest = {
        "schema": 2,
        "name": name,
        "version": version,
        "content_hash_definition": (
            "inspect_tree sha256 excluding skill-manifest.json"
        ),
        "content_sha256": content_hash,
    }
    if optional:
        expected_manifest.update({"tier": "optional", "install_by_default": False})
    if skill_manifest != expected_manifest:
        errors.append(f"{skill_manifest_path}: does not match package manifest")

    for match in LINK_RE.finditer(body):
        target = match.group(1).split("#", 1)[0]
        if not target or "://" in target or target.startswith("#"):
            continue
        linked = (skill_root / target).resolve()
        try:
            linked.relative_to(skill_root.resolve())
        except ValueError:
            errors.append(f"{skill_path}: linked resource escapes skill: {target}")
            continue
        if not linked.exists():
            errors.append(f"{skill_path}: missing linked resource: {target}")

    metadata_path = skill_root / "agents" / "openai.yaml"
    try:
        metadata = parse_openai_metadata(
            metadata_path.read_text(encoding="utf-8"), metadata_path
        )
        if f"${name}" not in metadata["default_prompt"]:
            errors.append(
                f"{metadata_path}: default_prompt must explicitly mention ${name}"
            )
    except (OSError, UnicodeDecodeError, ValueError) as error:
        errors.append(str(error))

    forbidden_auxiliary = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md"}
    for path in skill_root.rglob("*"):
        if path.is_dir():
            continue
        if path.name in forbidden_auxiliary:
            errors.append(f"{path}: auxiliary documentation does not belong in a skill")
        try:
            file_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"{path}: unreadable UTF-8: {error}")
            continue
        if path.suffix == ".json":
            read_json(path, errors)
        for label, pattern in PORTABILITY_PATTERNS.items():
            if pattern.search(file_text):
                errors.append(f"{path}: contains {label}")
        if PRIVATE_IPV4_RE.search(file_text):
            errors.append(f"{path}: contains a private IPv4 address")
        if EMBEDDED_CREDENTIAL_RE.search(file_text):
            errors.append(f"{path}: contains an embedded URL credential")

    if optional and "default-uninstalled" not in body:
        warnings.append(f"{skill_path}: optional skill should state default-uninstalled")
    return len(name) + len(description) + len(f"skills/{name}/SKILL.md") + 3


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    warnings: list[str] = []
    inspect_package_types(root, errors)
    validate_release_inventory(root, errors)

    manifest_data = read_json(root / "manifest.json", errors)
    manifest = manifest_data if isinstance(manifest_data, dict) else {}
    if manifest.get("schema") != 4:
        errors.append("manifest schema must be 4")
    if manifest.get("package") != "agent-continuity-stack":
        errors.append("manifest package identity must be agent-continuity-stack")
    if (
        manifest.get("repository")
        != "https://github.com/ImYourBoyRoy/agent-continuity-stack"
    ):
        errors.append("manifest canonical repository is missing or incorrect")
    package_version = manifest.get("version", "")
    if not SEMVER_RE.fullmatch(package_version):
        errors.append("manifest package version is not valid Semantic Versioning")
    if manifest.get("release_status") != "stable":
        errors.append("stable manifest must declare stable release status")

    version_path = root / "VERSION"
    if not version_path.is_file():
        errors.append("missing VERSION")
    elif version_path.read_text(encoding="utf-8").strip() != package_version:
        errors.append("VERSION does not match manifest package version")

    if manifest.get("license") != "MIT" or not (root / "LICENSE").is_file():
        errors.append("manifest must declare MIT and LICENSE must exist")
    for required in (
        ".env.example",
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        "ARCHITECTURE.md",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "AGENTS.md",
        "HANDOFF.md",
        "README.md",
        "MEMORY.md",
        "SECURITY.md",
        ".github/workflows/validate.yml",
    ):
        if not (root / required).is_file():
            errors.append(f"missing required project file: {required}")

    ignore_path = root / ".gitignore"
    if ignore_path.is_file():
        ignore_text = ignore_path.read_text(encoding="utf-8")
        if ".env" not in ignore_text or "!.env.example" not in ignore_text:
            errors.append(".gitignore must ignore local environments except example")

    local_environment = root / ".env"
    if local_environment.exists():
        metadata = local_environment.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            errors.append(".env must be a regular local-only file")
        elif metadata.st_mode & 0o077:
            errors.append(".env permissions must not grant group or other access")

    attributes = (root / ".gitattributes").read_text(encoding="utf-8")
    for pattern in ("*.md", "*.json", "*.yaml", "*.yml", "*.py", "VERSION", "LICENSE"):
        if f"{pattern} text eol=lf" not in attributes:
            errors.append(f".gitattributes missing LF rule for {pattern}")

    core_versions = manifest_versions(manifest.get("skills"), "skill", errors)
    optional_versions = manifest_versions(
        manifest.get("optional_skills"), "optional skill", errors
    )
    core_actual = {
        path.name
        for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    optional_actual = {
        path.name
        for path in (root / "optional_skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if set(core_versions) != core_actual:
        errors.append(
            "core skill manifest mismatch: "
            f"missing={sorted(set(core_versions) - core_actual)} "
            f"extra={sorted(core_actual - set(core_versions))}"
        )
    if set(optional_versions) != optional_actual:
        errors.append(
            "optional skill manifest mismatch: "
            f"missing={sorted(set(optional_versions) - optional_actual)} "
            f"extra={sorted(optional_actual - set(optional_versions))}"
        )

    instruction_data = read_json(root / "instruction-pack.json", errors)
    instruction = instruction_data if isinstance(instruction_data, dict) else {}
    contract_path = root / instruction.get(
        "source", "GLOBAL_CUSTOM_INSTRUCTIONS.md"
    )
    try:
        raw_contract = contract_path.read_bytes()
        if raw_contract.startswith(b"\xef\xbb\xbf"):
            errors.append("canonical operating contract contains a UTF-8 BOM")
        contract_text = raw_contract.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        errors.append(f"canonical operating contract is unreadable: {error}")
        raw_contract = b""
        contract_text = ""
    if "\r" in contract_text:
        errors.append("canonical operating contract is not LF-normalized")
    actual_hash = hashlib.sha256(raw_contract).hexdigest()
    if instruction.get("schema") != 2:
        errors.append("instruction-pack schema must be 2")
    if instruction.get("package_version") != package_version:
        errors.append("instruction-pack package version does not match manifest")
    if instruction.get("package") != manifest.get("package"):
        errors.append("instruction-pack package identity does not match manifest")
    contract_policy = manifest.get("global_contract", {})
    if (
        contract_policy.get("required_for_global_install") is not False
        or contract_policy.get("install_by_default") is not False
        or contract_policy.get("preserve_existing_instructions_by_default")
        is not True
    ):
        errors.append(
            "manifest global contract must be opt-in and preserve instructions"
        )
    if (
        instruction.get("required_in_package") is not True
        or instruction.get("install_by_default") is not False
        or instruction.get("installation_requires_explicit_opt_in") is not True
    ):
        errors.append("instruction-pack must declare explicit opt-in installation")
    if instruction.get("source_sha256") != actual_hash:
        errors.append("canonical operating-contract SHA-256 mismatch")
    if instruction.get("encoding") != "utf-8" or instruction.get(
        "line_endings"
    ) != "lf":
        errors.append("instruction-pack must declare UTF-8/LF")
    if instruction.get("byte_order_mark") != "forbidden":
        errors.append("instruction-pack must forbid a byte-order mark")
    if instruction.get("rendered_integrity", {}).get(
        "package_contains_fixed_rendered_hash"
    ) is not False:
        errors.append("package must not contain a fixed rendered contract hash")
    actual_placeholders = set(PLACEHOLDER_RE.findall(contract_text))
    declared_placeholders = set(instruction.get("renderable_placeholders", []))
    if actual_placeholders != declared_placeholders:
        errors.append(
            "operating-contract placeholder mismatch: "
            f"missing={sorted(actual_placeholders - declared_placeholders)} "
            f"extra={sorted(declared_placeholders - actual_placeholders)}"
        )

    manifest_clients = set(manifest.get("clients", {}))
    instruction_clients = set(instruction.get("clients", {}))
    if instruction_clients != manifest_clients - {"antigravity-cli"}:
        errors.append("manifest and instruction-pack client declarations conflict")

    antigravity = instruction.get("clients", {}).get("antigravity", {})
    split_marker = antigravity.get("split_before_heading", "")
    if not split_marker or contract_text.count(split_marker) != 1:
        errors.append("Antigravity split heading must occur exactly once")
    else:
        split_at = contract_text.index(split_marker)
        segments = (contract_text[:split_at], contract_text[split_at:])
        maximum = antigravity.get("maximum_segment_characters", 0)
        if maximum != 12000 or any(len(segment) >= maximum for segment in segments):
            errors.append("Antigravity source segment exceeds safe limit")
        if "".join(segments).encode("utf-8") != raw_contract:
            errors.append("Antigravity source segments do not reconstruct contract")
        if len(antigravity.get("segments", [])) != 2:
            errors.append("Antigravity adapter must declare two segments")

    activation_data = read_json(root / "tests" / "activation_cases.json", errors)
    activation = activation_data if isinstance(activation_data, dict) else {}
    if activation.get("schema") != 2:
        errors.append("activation case schema must be 2")
    if set(activation.get("cases", {})) != set(core_versions):
        errors.append("core activation cases do not match core skill inventory")
    if set(activation.get("optional_cases", {})) != set(optional_versions):
        errors.append("optional activation cases do not match optional inventory")
    for label in ("cases", "optional_cases"):
        for name, cases in activation.get(label, {}).items():
            if not cases.get("should_trigger") or not cases.get("should_not_trigger"):
                errors.append(f"activation cases incomplete for {name}")
            if label == "optional_cases" and not cases.get("collision"):
                errors.append(f"optional activation collision case missing for {name}")

    catalog_characters = 0
    for name in sorted(core_actual):
        catalog_characters += validate_skill(
            root / "skills" / name,
            name,
            core_versions.get(name, ""),
            False,
            errors,
            warnings,
        )
    for name in sorted(optional_actual):
        catalog_characters += validate_skill(
            root / "optional_skills" / name,
            name,
            optional_versions.get(name, ""),
            True,
            errors,
            warnings,
        )
    if catalog_characters > 8000:
        errors.append("selected source skill catalog estimate exceeds 8,000 characters")
    elif catalog_characters > 6000:
        warnings.append("selected source skill catalog estimate exceeds 6,000 characters")

    declared_schemas = set(manifest.get("schemas", []))
    actual_schemas = {
        str(path.relative_to(root)) for path in (root / "schemas").glob("*.json")
    }
    if declared_schemas != actual_schemas:
        errors.append("declared schema inventory does not match schemas directory")
    for relative in sorted(actual_schemas):
        schema = read_json(root / relative, errors)
        if not isinstance(schema, dict) or schema.get("type") != "object":
            errors.append(f"{relative}: schema must describe an object")

    declared_evidence = set(manifest.get("runtime_evidence", []))
    evidence_root = root / "tests" / "evidence"
    actual_evidence = {
        path.relative_to(root).as_posix()
        for path in evidence_root.glob("*.json")
    } if evidence_root.is_dir() else set()
    if declared_evidence != actual_evidence:
        errors.append("runtime evidence inventory does not match tests/evidence")
    for relative in sorted(actual_evidence):
        evidence = read_json(root / relative, errors)
        if not isinstance(evidence, dict):
            continue
        if evidence.get("package_version") != package_version:
            errors.append(f"{relative}: package version mismatch")
        if evidence.get("source_sha256") != actual_hash:
            errors.append(f"{relative}: contract source hash mismatch")
        if evidence.get("status") != "verified":
            errors.append(f"{relative}: packaged runtime evidence must be verified")
        for skill in evidence.get("verified_skills", []):
            if not isinstance(skill, dict):
                errors.append(f"{relative}: malformed verified skill evidence")
                continue
            name = skill.get("name", "")
            if name in core_versions:
                skill_root = root / "skills" / name
                expected_version = core_versions[name]
            elif name in optional_versions:
                skill_root = root / "optional_skills" / name
                expected_version = optional_versions[name]
            else:
                errors.append(f"{relative}: evidence names unknown skill {name!r}")
                continue
            skill_metadata = read_json(skill_root / "skill-manifest.json", errors)
            if not isinstance(skill_metadata, dict):
                continue
            if skill.get("version") != expected_version:
                errors.append(f"{relative}: evidence skill version mismatch for {name}")
            if skill.get("content_sha256") != skill_metadata.get("content_sha256"):
                errors.append(f"{relative}: evidence skill hash mismatch for {name}")

    integration_entries = manifest.get("integrations", [])
    for entry in integration_entries:
        metadata_path = root / entry.get("metadata", "")
        metadata = read_json(metadata_path, errors)
        if not isinstance(metadata, dict):
            continue
        if metadata.get("id") != entry.get("id"):
            errors.append(f"{metadata_path}: integration id mismatch")
        if metadata.get("compatibility") != "exact-tested":
            errors.append(f"{metadata_path}: compatibility must be exact-tested")
        for hash_field in (
            "release_commit",
            "skill_content_base_commit",
            "manifest_sha256",
        ):
            value = metadata.get(hash_field, "")
            expected_length = 64 if hash_field == "manifest_sha256" else 40
            if not re.fullmatch(f"[0-9a-f]{{{expected_length}}}", value):
                errors.append(f"{metadata_path}: invalid {hash_field}")

    root_text_files = [
        root / "README.md",
        root / "AGENTS.md",
        root / "ARCHITECTURE.md",
        root / "CODE_OF_CONDUCT.md",
        root / "HANDOFF.md",
        root / "CONTRIBUTING.md",
        root / "SECURITY.md",
        root / "MEMORY.md",
        root / "INSTALL_PROTOCOL.md",
        root / "CLIENT_COMPATIBILITY.md",
        root / "MERGE_CHECKLIST.md",
        root / "CHANGELOG.md",
    ]
    for path in root_text_files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in TOP_LEVEL_PRIVACY_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: contains {label}")
        if PRIVATE_IPV4_RE.search(text):
            errors.append(f"{path}: contains a private IPv4 address")
        if EMBEDDED_CREDENTIAL_RE.search(text):
            errors.append(f"{path}: contains an embedded URL credential")

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    print(
        json.dumps(
            {
                "core_skills": len(core_actual),
                "optional_skills": len(optional_actual),
                "catalog_characters": catalog_characters,
                "errors": len(errors),
                "warnings": len(warnings),
            }
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
