#!/usr/bin/env python3
"""Validate portable update-source configuration without executing commands."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse


ROOT_KEYS = {"schema", "sources", "policy"}
SOURCE_KEYS = {
    "id",
    "kind",
    "locator",
    "purpose",
    "channel",
    "include_enhancements",
    "credential_source",
    "current",
}
CURRENT_KEYS = {"version", "version_file", "git_ref", "command"}
POLICY_KEYS = {
    "audit_tier",
    "prereleases",
    "major_updates",
    "unreleased",
    "security",
    "cooldown_days",
    "include",
    "exclude",
}
SOURCE_KINDS = {
    "repository",
    "registry",
    "executable",
    "version-file",
    "git-pin",
    "platform",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ConfigError(ValueError):
    pass


def load_document(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json" or text.lstrip().startswith(("{", "[")):
        return json.loads(text)
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise ConfigError(
            "YAML validation requires PyYAML. Install it through the project's "
            "approved environment, use JSON-compatible content, or inspect the "
            "file manually. This validator never installs dependencies."
        ) from error
    return yaml.safe_load(text)


def reject_unknown(value: dict[str, Any], allowed: set[str], location: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ConfigError(f"{location}: unknown fields: {', '.join(unknown)}")


def require_text(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{location}: expected a non-empty string")
    return value


def validate_relative_path(value: Any, location: str) -> None:
    text = require_text(value, location).replace("\\", "/")
    if text.startswith("/") or re.match(r"^[A-Za-z]:/", text):
        raise ConfigError(f"{location}: path must be repository-relative")
    if ".." in PurePosixPath(text).parts:
        raise ConfigError(f"{location}: path must not escape the repository")


def validate_repository_locator(value: str, location: str) -> None:
    if value.startswith("git@"):
        if ":" not in value or value.endswith(":"):
            raise ConfigError(f"{location}: invalid SSH git locator")
        return
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "ssh", "git"} or not parsed.netloc:
        raise ConfigError(
            f"{location}: repository locator must use https, ssh, git, or git@"
        )
    if parsed.scheme == "https" and (parsed.username or parsed.password):
        raise ConfigError(f"{location}: HTTP URL userinfo must not be embedded")


def validate_source(source: Any, index: int) -> str:
    location = f"sources[{index}]"
    if not isinstance(source, dict):
        raise ConfigError(f"{location}: expected an object")
    reject_unknown(source, SOURCE_KEYS, location)

    source_id = require_text(source.get("id"), f"{location}.id")
    if not ID_RE.fullmatch(source_id):
        raise ConfigError(f"{location}.id: use lowercase letters, digits, and hyphens")
    kind = source.get("kind")
    if kind not in SOURCE_KINDS:
        raise ConfigError(f"{location}.kind: unsupported source kind")
    require_text(source.get("purpose"), f"{location}.purpose")

    locator = source.get("locator")
    if locator is None:
        raise ConfigError(f"{location}.locator: required for {kind}")
    if locator is not None:
        locator_text = require_text(locator, f"{location}.locator")
        if kind in {"repository", "git-pin"}:
            validate_repository_locator(locator_text, f"{location}.locator")
        if kind == "version-file":
            validate_relative_path(locator_text, f"{location}.locator")

    if source.get("channel", "stable") not in {"stable", "prerelease", "source"}:
        raise ConfigError(f"{location}.channel: invalid channel")
    if not isinstance(source.get("include_enhancements", False), bool):
        raise ConfigError(f"{location}.include_enhancements: expected boolean")
    if source.get("credential_source", "none") not in {
        "none",
        "existing-environment",
        "existing-client",
    }:
        raise ConfigError(f"{location}.credential_source: invalid value")

    current = source.get("current")
    if kind == "git-pin" and (
        not isinstance(current, dict) or set(current) != {"git_ref"}
    ):
        raise ConfigError(f"{location}.current.git_ref: required for git-pin")
    if current is not None:
        if not isinstance(current, dict):
            raise ConfigError(f"{location}.current: expected an object")
        reject_unknown(current, CURRENT_KEYS, f"{location}.current")
        if len(current) != 1:
            raise ConfigError(f"{location}.current: select exactly one strategy")
        key, value = next(iter(current.items()))
        if key == "version_file":
            validate_relative_path(value, f"{location}.current.version_file")
        elif key == "command":
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(item, str) and item for item in value)
            ):
                raise ConfigError(
                    f"{location}.current.command: expected a non-empty string array"
                )
        else:
            require_text(value, f"{location}.current.{key}")
    return source_id


def validate_policy(policy: Any) -> None:
    if policy is None:
        return
    if not isinstance(policy, dict):
        raise ConfigError("policy: expected an object")
    reject_unknown(policy, POLICY_KEYS, "policy")
    enums = {
        "audit_tier": {"rapid", "standard", "exhaustive"},
        "prereleases": {"exclude", "report-only", "include"},
        "major_updates": {"exclude", "report-only", "include"},
        "unreleased": {"exclude", "report-only", "include"},
        "security": {"immediate", "scheduled"},
    }
    for key, allowed in enums.items():
        if key in policy and policy[key] not in allowed:
            raise ConfigError(f"policy.{key}: invalid value")
    if "cooldown_days" in policy:
        days = policy["cooldown_days"]
        if not isinstance(days, int) or isinstance(days, bool) or not 0 <= days <= 365:
            raise ConfigError("policy.cooldown_days: expected an integer from 0 to 365")
    for key in ("include", "exclude"):
        if key in policy and (
            not isinstance(policy[key], list)
            or not all(isinstance(item, str) and item for item in policy[key])
        ):
            raise ConfigError(f"policy.{key}: expected an array of strings")


def validate_config(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ConfigError("root: expected an object")
    reject_unknown(data, ROOT_KEYS, "root")
    if data.get("schema") != 1:
        raise ConfigError("schema: expected 1")
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise ConfigError("sources: expected an array")
    ids = [validate_source(source, index) for index, source in enumerate(sources)]
    duplicates = sorted({source_id for source_id in ids if ids.count(source_id) > 1})
    if duplicates:
        raise ConfigError(f"sources: duplicate ids: {', '.join(duplicates)}")
    validate_policy(data.get("policy"))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    try:
        data = validate_config(load_document(args.config))
    except (OSError, json.JSONDecodeError, ConfigError) as error:
        print(f"invalid: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "schema": data["schema"],
                "sources": len(data["sources"]),
                "commands_executed": False,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
