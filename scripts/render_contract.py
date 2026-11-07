#!/usr/bin/env python3
"""Render the canonical contract using only explicit operator-profile values."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDER_RE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
PROFILE_LINE_RE = re.compile(
    r"^\* (?P<label>[^:`]+): `\{\{(?P<key>[a-z_]+)\}\}`\n?$"
)
EMAIL_RE = re.compile(r"^[^@\s<>`]+@[^@\s<>`]+\.[^@\s<>`]+$")


class RenderError(ValueError):
    """Raised when the template or explicit profile data is invalid."""


def read_json(path: Path) -> dict:
    def object_without_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise RenderError(f"profile JSON contains a duplicate key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=object_without_duplicates,
        )
    except OSError as error:
        raise RenderError("could not read profile JSON") from error
    except UnicodeDecodeError as error:
        raise RenderError("profile JSON must be UTF-8") from error
    except json.JSONDecodeError as error:
        raise RenderError(f"profile JSON is invalid: {error.msg} at line {error.lineno}") from error
    if not isinstance(value, dict):
        raise RenderError("profile JSON must be an object")
    return value


def validate_profile(profile: dict, allowed: set[str]) -> dict[str, str]:
    unknown = set(profile) - allowed
    if unknown:
        raise RenderError(f"profile JSON has unknown fields: {sorted(unknown)}")

    normalized: dict[str, str] = {}
    for key, value in profile.items():
        if not isinstance(value, str):
            raise RenderError(f"profile field {key} must be a string")
        if not value.strip():
            continue
        if value != value.strip():
            raise RenderError(f"profile field {key} has leading or trailing whitespace")
        if any(
            unicodedata.category(character) in {"Cc", "Zl", "Zp"}
            for character in value
        ):
            raise RenderError(f"profile field {key} contains a control character")
        if "`" in value or "{{" in value or "}}" in value:
            raise RenderError(f"profile field {key} contains Markdown or template syntax")

        if key == "operator_email" and not EMAIL_RE.fullmatch(value):
            raise RenderError("operator_email must be a single plain-text email address")
        if key in {"personal_site", "github_profile", "pypi_profile"}:
            try:
                parsed = urlparse(value)
                hostname = parsed.hostname
                port = parsed.port
            except ValueError as error:
                raise RenderError(f"profile field {key} must be an HTTPS URL") from error
            if (
                parsed.scheme != "https"
                or not hostname
                or parsed.username
                or parsed.password
                or (port is not None and not 1 <= port <= 65535)
                or any(character.isspace() for character in value)
            ):
                raise RenderError(f"profile field {key} must be an HTTPS URL")
        normalized[key] = value
    return normalized


def render(root: Path, profile_path: Path) -> tuple[bytes, list[str], list[str]]:
    root = root.resolve()
    resolved_profile_path = profile_path.resolve()
    if resolved_profile_path.is_relative_to(root):
        raise RenderError("profile JSON must be outside the package checkout")

    try:
        metadata = json.loads((root / "instruction-pack.json").read_text(encoding="utf-8"))
        if not isinstance(metadata, dict):
            raise RenderError("instruction-pack.json must contain an object")
        source_name = metadata.get("source")
        if (
            not isinstance(source_name, str)
            or not source_name
            or "\\" in source_name
            or Path(source_name).is_absolute()
            or ".." in Path(source_name).parts
        ):
            raise RenderError("instruction-pack.json has an unsafe contract source path")
        source_path = root / source_name
        if source_path.is_symlink():
            raise RenderError("canonical contract source must not be a symlink")
        source_path = source_path.resolve()
        if not source_path.is_relative_to(root) or not source_path.is_file():
            raise RenderError("canonical contract source must be a package file")
        raw = source_path.read_bytes()
    except RenderError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RenderError("could not read package contract metadata or source") from error

    if raw.startswith(b"\xef\xbb\xbf"):
        raise RenderError("canonical contract contains a UTF-8 BOM")
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RenderError(f"canonical contract is not UTF-8: {error}") from error
    if "\r" in source:
        raise RenderError("canonical contract must use LF line endings")
    if hashlib.sha256(raw).hexdigest() != metadata.get("source_sha256"):
        raise RenderError("canonical contract SHA-256 does not match instruction-pack.json")

    declared_fields = metadata.get("renderable_placeholders")
    if (
        not isinstance(declared_fields, list)
        or any(not isinstance(field, str) for field in declared_fields)
        or len(set(declared_fields)) != len(declared_fields)
    ):
        raise RenderError("instruction-pack.json has an invalid placeholder list")
    allowed = set(declared_fields)
    actual = set(PLACEHOLDER_RE.findall(source))
    if actual != allowed:
        raise RenderError("canonical contract placeholders do not match package metadata")

    profile = validate_profile(read_json(resolved_profile_path), allowed)
    lines = source.splitlines(keepends=True)
    try:
        start = lines.index("## Operator Profile\n")
    except ValueError as error:
        raise RenderError("canonical contract is missing the Operator Profile section") from error
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )

    rendered_profile: list[str] = []
    seen: set[str] = set()
    for line in lines[start + 1 : end]:
        keys = PLACEHOLDER_RE.findall(line)
        if not keys:
            rendered_profile.append(line)
            continue
        match = PROFILE_LINE_RE.fullmatch(line)
        if not match or len(keys) != 1 or keys[0] != match.group("key"):
            raise RenderError("profile placeholders must occupy one complete operator-profile bullet")
        key = match.group("key")
        if key in seen:
            raise RenderError(f"canonical contract repeats profile field: {key}")
        seen.add(key)
        if key in profile:
            rendered_profile.append(line.replace(f"{{{{{key}}}}}", profile[key]))

    if seen != allowed:
        raise RenderError("canonical operator-profile fields do not match package metadata")

    if profile:
        rendered_lines = lines[: start + 1] + rendered_profile + lines[end:]
        included = sorted(profile)
        omitted = sorted(allowed - set(profile))
    else:
        # Drop the whole optional section, including its heading and contents.
        rendered_lines = lines[:start] + lines[end:]
        included = []
        omitted = sorted(allowed)

    rendered_text = "".join(rendered_lines)
    if PLACEHOLDER_RE.search(rendered_text):
        raise RenderError("rendered contract contains an unresolved placeholder")
    return rendered_text.encode("utf-8"), included, omitted


def write_private_new_file(path: Path, content: bytes) -> None:
    path = path.resolve()
    if not path.parent.is_dir():
        raise RenderError("output parent directory must already exist")
    descriptor: int | None = None
    created = False
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        created = True
        with os.fdopen(descriptor, "wb") as output:
            descriptor = None
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
    except FileExistsError as error:
        raise RenderError("output already exists; choose a new staging path") from error
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        if created:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        raise RenderError("could not create rendered contract") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Package root containing instruction-pack.json",
    )
    parser.add_argument("--profile-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    try:
        root = arguments.root.resolve()
        if arguments.output.exists() or arguments.output.is_symlink():
            raise RenderError("output already exists; choose a new staging path")
        output = arguments.output.resolve()
        if output.is_relative_to(root):
            raise RenderError("rendered contract must be written outside the package checkout")
        content, included, omitted = render(root, arguments.profile_json)
        write_private_new_file(output, content)
        result = {
            "kind": "rendered-contract-created",
            "path": str(output),
            "rendered_sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
            "included_fields": included,
            "omitted_fields": omitted,
            "permission_bits": "0600 where supported",
            "package_files_modified": False,
        }
    except RenderError as error:
        print(json.dumps({"errors": [str(error)], "package_files_modified": False}))
        return 1
    except (OSError, ValueError):
        print(
            json.dumps(
                {
                    "errors": ["filesystem operation or input validation failed"],
                    "package_files_modified": False,
                }
            )
        )
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
