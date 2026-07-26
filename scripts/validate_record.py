#!/usr/bin/env python3
"""Validate package records with the bundled dependency-free JSON Schema subset."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


def resolve_reference(root: dict, reference: str) -> dict:
    if not reference.startswith("#/"):
        raise ValueError(f"external schema reference is unsupported: {reference}")
    current: Any = root
    for component in reference[2:].split("/"):
        current = current[component.replace("~1", "/").replace("~0", "~")]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference is not an object: {reference}")
    return current


def matches_type(value: Any, expected: str) -> bool:
    mapping = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float))
        and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return mapping[expected](value)


def validate_instance(
    value: Any, schema: dict, root: dict, location: str, errors: list[str]
) -> None:
    if "$ref" in schema:
        validate_instance(
            value, resolve_reference(root, schema["$ref"]), root, location, errors
        )
        return

    expected_type = schema.get("type")
    if expected_type is not None:
        choices = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(matches_type(value, choice) for choice in choices):
            errors.append(f"{location}: expected type {choices}")
            return

    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value is not in enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{location}: missing required property {key!r}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            child_location = f"{location}.{key}"
            if key in properties:
                validate_instance(item, properties[key], root, child_location, errors)
            elif additional is False:
                errors.append(f"{location}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                validate_instance(item, additional, root, child_location, errors)

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{location}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_instance(
                    item, item_schema, root, f"{location}[{index}]", errors
                )

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: string is too short")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            errors.append(f"{location}: does not match required pattern")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{location}: invalid date-time")


def plan_digest(record: dict) -> str:
    digest_input = {
        key: value
        for key, value in record.items()
        if key not in {"plan_sha256", "authorization", "apply_authorized"}
    }
    canonical = json.dumps(
        digest_input,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_semantics(
    schema_path: Path, record: Any, errors: list[str]
) -> None:
    if not isinstance(record, dict):
        return
    name = schema_path.name
    hash_pattern = re.compile(r"^[0-9a-f]{64}$")

    if name == "install-plan.schema.json":
        instruction_mode = record.get("instruction_mode")
        rendered_sha256 = record.get("rendered_sha256")
        if instruction_mode == "complete-contract":
            if not isinstance(rendered_sha256, str):
                errors.append(
                    "$.rendered_sha256: complete-contract requires a rendered hash"
                )
        elif rendered_sha256 is not None:
            errors.append(
                "$.rendered_sha256: must be null outside complete-contract mode"
            )
        operations = [
            operation
            for operation in record.get("operations", [])
            if isinstance(operation, dict)
        ]
        contract_kinds = {"instruction", "contract-fragment", "contract-loader"}
        effective_contract_operations = [
            operation
            for operation in operations
            if operation.get("target_kind") in contract_kinds
            and operation.get("action") not in {"skip", "blocked"}
        ]
        if instruction_mode == "preserve-existing" and effective_contract_operations:
            errors.append(
                "$.operations: preserve-existing forbids instruction mutations"
            )
        if instruction_mode == "guided-additions" and any(
            operation.get("target_kind") in {"contract-fragment", "contract-loader"}
            for operation in effective_contract_operations
        ):
            errors.append(
                "$.operations: guided-additions cannot install contract adapters"
            )
        if instruction_mode == "complete-contract" and not effective_contract_operations:
            errors.append(
                "$.operations: complete-contract requires a contract operation"
            )
        actual_digest = plan_digest(record)
        if record.get("plan_sha256") != actual_digest:
            errors.append("$.plan_sha256: does not match canonical plan content")
        authorization = record.get("authorization")
        if isinstance(authorization, dict):
            approved = authorization.get("status") == "approved"
            if record.get("apply_authorized") is not approved:
                errors.append(
                    "$.apply_authorized: must match authorization.status"
                )
            if approved:
                if authorization.get("approved_plan_sha256") != actual_digest:
                    errors.append(
                        "$.authorization.approved_plan_sha256: "
                        "must match plan_sha256"
                    )
                if authorization.get("approved_at") is None:
                    errors.append(
                        "$.authorization.approved_at: required when approved"
                    )
                if record.get("blockers"):
                    errors.append("$.blockers: approved plan cannot contain blockers")
                effective = [
                    operation
                    for operation in record.get("operations", [])
                    if isinstance(operation, dict)
                    and operation.get("action") not in {"skip", "blocked"}
                ]
                if not effective:
                    errors.append(
                        "$.operations: approved plan requires an effective operation"
                    )
            elif (
                authorization.get("approved_plan_sha256") is not None
                or authorization.get("approved_at") is not None
            ):
                errors.append(
                    "$.authorization: pending plan cannot contain approval evidence"
                )
        selected_clients = set(record.get("selected_clients", []))
        for index, operation in enumerate(record.get("operations", [])):
            if (
                isinstance(operation, dict)
                and operation.get("client") not in selected_clients
            ):
                errors.append(
                    f"$.operations[{index}].client: not in selected_clients"
                )
        package_manifest = schema_path.parent.parent / "manifest.json"
        try:
            package = json.loads(package_manifest.read_text(encoding="utf-8"))
            allowed_skills = {
                item["name"]
                for group in ("skills", "optional_skills")
                for item in package.get(group, [])
            }
            unknown = set(record.get("selected_skills", [])) - allowed_skills
            if unknown:
                errors.append(f"$.selected_skills: unknown skills {sorted(unknown)}")
        except (OSError, KeyError, json.JSONDecodeError):
            errors.append("$: cannot resolve package skill inventory")

    for key in ("previous_sha256", "pre_sha256", "post_sha256"):
        for location, value in walk_named_values(record, key):
            if value is not None and (
                not isinstance(value, str) or not hash_pattern.fullmatch(value)
            ):
                errors.append(f"{location}: invalid SHA-256")

    for field in ("client_root", "state_root"):
        for location, value in walk_named_values(record, field):
            if isinstance(value, str) and not is_safe_absolute_root(value):
                errors.append(f"{location}: unsafe or overly broad root")

    for field in (
        "target_relative",
        "backup",
        "staged_path",
        "ownership_record",
    ):
        for location, value in walk_named_values(record, field):
            if value is not None and isinstance(value, str) and not is_safe_relative_path(
                value
            ):
                errors.append(f"{location}: unsafe state-relative path")
    for location, values in walk_named_values(record, "client_status_records"):
        if isinstance(values, list):
            for index, value in enumerate(values):
                if not isinstance(value, str) or not is_safe_relative_path(value):
                    errors.append(f"{location}[{index}]: unsafe relative path")
    for location, backups in walk_named_values(record, "backups"):
        if isinstance(backups, list):
            for index, backup in enumerate(backups):
                if not isinstance(backup, dict):
                    errors.append(f"{location}[{index}]: malformed backup record")
                    continue
                value = backup.get("path")
                if not isinstance(value, str) or not is_safe_relative_path(value):
                    errors.append(f"{location}[{index}].path: unsafe relative path")

    if name == "ownership-record.schema.json":
        is_skill = record.get("content_kind") == "skill"
        has_skill_fields = bool(record.get("skill_name")) and bool(
            record.get("skill_version")
        )
        if is_skill != has_skill_fields:
            errors.append(
                "$: skill_name and skill_version must exist only for skill content"
            )
        if is_skill and record.get("rendered_sha256") is not None:
            errors.append("$.rendered_sha256: skill ownership must use null")
        if not is_skill and record.get("rendered_sha256") is None:
            errors.append(
                "$.rendered_sha256: contract ownership requires rendered hash"
            )

    if name == "client-status.schema.json":
        instruction_mode = record.get("instruction_mode")
        rendered_sha256 = record.get("rendered_sha256")
        instruction_location = record.get("instruction_location")
        if instruction_mode == "complete-contract":
            if not isinstance(rendered_sha256, str):
                errors.append(
                    "$.rendered_sha256: complete-contract requires a rendered hash"
                )
            if not isinstance(instruction_location, str):
                errors.append(
                    "$.instruction_location: complete-contract requires a location"
                )
        elif rendered_sha256 is not None:
            errors.append(
                "$.rendered_sha256: must be null outside complete-contract mode"
            )
        if instruction_mode == "preserve-existing" and instruction_location is not None:
            errors.append(
                "$.instruction_location: preserve-existing must not claim a package instruction"
            )
        status = record.get("status")
        if status == "verified" and not (
            record.get("copied")
            and record.get("loaded")
            and record.get("smoke_passed")
            and record.get("duplicate_loading") == "none"
        ):
            errors.append("$: verified status requires complete runtime evidence")
        if status == "installed-unverified" and record.get("smoke_passed"):
            errors.append(
                "$.smoke_passed: installed-unverified cannot claim smoke success"
            )

    if name == "transaction-receipt.schema.json":
        instruction_mode = record.get("instruction_mode")
        rendered_sha256 = record.get("rendered_sha256")
        if instruction_mode == "complete-contract":
            if not isinstance(rendered_sha256, str):
                errors.append(
                    "$.rendered_sha256: complete-contract requires a rendered hash"
                )
        elif rendered_sha256 is not None:
            errors.append(
                "$.rendered_sha256: must be null outside complete-contract mode"
            )
        mutations = record.get("mutations", [])
        if record.get("outcome") == "complete" and not any(
            isinstance(item, dict) and item.get("result") == "complete"
            for item in mutations
        ):
            errors.append(
                "$.mutations: complete receipt requires a completed mutation"
            )

    if name == "operation-journal.schema.json":
        targets = record.get("targets", [])
        phase = record.get("phase")
        for index, target in enumerate(targets):
            if not isinstance(target, dict):
                continue
            target_phase = target.get("phase")
            if target_phase in {"staged", "committed", "validated"} and not target.get(
                "staged_sha256"
            ):
                errors.append(
                    f"$.targets[{index}].staged_sha256: required for {target_phase}"
                )
            if target_phase in {"committed", "validated"} and not target.get(
                "post_sha256"
            ):
                errors.append(
                    f"$.targets[{index}].post_sha256: required for {target_phase}"
                )
            has_backup = target.get("backup") is not None
            has_backup_hash = target.get("backup_sha256") is not None
            if has_backup != has_backup_hash:
                errors.append(
                    f"$.targets[{index}]: backup path and hash must appear together"
                )
            if target.get("pre_sha256") is not None and not has_backup:
                errors.append(
                    f"$.targets[{index}]: pre-existing target requires retained backup"
                )
        if phase == "complete" and any(
            not isinstance(target, dict) or target.get("phase") != "validated"
            for target in targets
        ):
            errors.append(
                "$.targets: complete journal requires every target validated"
            )
        if phase == "restored" and any(
            not isinstance(target, dict) or target.get("phase") != "restored"
            for target in targets
        ):
            errors.append(
                "$.targets: restored journal requires every target restored"
            )


def is_safe_absolute_root(value: str) -> bool:
    if "\\" in value or re.match(r"^[A-Za-z]:", value):
        path = PureWindowsPath(value)
        normalized = str(path).rstrip("\\").casefold()
        forbidden = {
            "c:",
            "c:\\windows",
            "c:\\program files",
            "c:\\program files (x86)",
            "c:\\users",
        }
        return (
            path.is_absolute()
            and ".." not in path.parts
            and "." not in path.parts
            and normalized not in forbidden
        )
    path = PurePosixPath(value)
    forbidden = {"/", "/etc", "/usr", "/var", "/home", "/users", "/tmp"}
    return (
        path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
        and str(path).rstrip("/").casefold() not in forbidden
    )


def is_safe_relative_path(value: str) -> bool:
    if not value or ":" in value:
        return False
    if "\\" in value:
        path = PureWindowsPath(value)
    else:
        path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and "." not in path.parts
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def walk_named_values(value: Any, wanted: str, location: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key == wanted:
                yield child_location, child
            yield from walk_named_values(child, wanted, child_location)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_named_values(child, wanted, f"{location}[{index}]")


def validate_applicability(
    record: Any,
    allowed_client_roots: list[str],
    allowed_state_roots: list[str],
) -> list[str]:
    if not isinstance(record, dict):
        return ["$: record is not an object"]
    lifecycle_kinds = {
        "install-plan",
        "transaction-receipt",
        "ownership-record",
        "rollback-receipt",
        "operation-journal",
    }
    if record.get("kind") not in lifecycle_kinds:
        return []
    errors: list[str] = []
    client_roots = {
        value
        for _, value in walk_named_values(record, "client_root")
        if isinstance(value, str)
    }
    state_roots = {
        value
        for _, value in walk_named_values(record, "state_root")
        if isinstance(value, str)
    }
    allowed_clients = {normalize_root(value) for value in allowed_client_roots}
    allowed_states = {normalize_root(value) for value in allowed_state_roots}
    if client_roots and not allowed_clients:
        errors.append(
            "$: client roots are not bound to independently resolved allowed roots"
        )
    if state_roots and not allowed_states:
        errors.append(
            "$: state root is not bound to an independently resolved allowed root"
        )
    for root in client_roots:
        if allowed_clients and normalize_root(root) not in allowed_clients:
            errors.append(f"$: unapproved client root {root!r}")
    for root in state_roots:
        if allowed_states and normalize_root(root) not in allowed_states:
            errors.append(f"$: unapproved state root {root!r}")
    return errors


def normalize_root(value: str) -> str:
    if "\\" in value or re.match(r"^[A-Za-z]:", value):
        return str(PureWindowsPath(value)).rstrip("\\").casefold()
    return str(PurePosixPath(value)).rstrip("/") or "/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path)
    parser.add_argument("record", type=Path)
    parser.add_argument("--allowed-client-root", action="append", default=[])
    parser.add_argument("--allowed-state-root", action="append", default=[])
    parser.add_argument(
        "--require-applicable",
        action="store_true",
        help="Fail unless lifecycle roots match independently supplied roots",
    )
    arguments = parser.parse_args()
    try:
        schema = json.loads(arguments.schema.read_text(encoding="utf-8"))
        record = json.loads(arguments.record.read_text(encoding="utf-8"))
        errors: list[str] = []
        validate_instance(record, schema, schema, "$", errors)
        validate_semantics(arguments.schema.resolve(), record, errors)
        applicability_errors = validate_applicability(
            record,
            arguments.allowed_client_root,
            arguments.allowed_state_root,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        errors = [str(error)]
        applicability_errors = []
    result = {
        "schema": str(arguments.schema),
        "record": str(arguments.record),
        "valid": not errors,
        "applicable": not errors and not applicability_errors,
        "errors": errors,
        "applicability_errors": applicability_errors,
        "files_modified": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    failed = bool(errors) or (
        arguments.require_applicable and bool(applicability_errors)
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
