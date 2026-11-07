#!/usr/bin/env python3
"""Read-only integrity checks for canonical and rendered operating contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)


def normalized_utf8(path: Path) -> tuple[bytes, bool]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: invalid UTF-8: {error}") from error
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return normalized, normalized == raw


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_metadata(root: Path) -> dict:
    return json.loads((root / "instruction-pack.json").read_text(encoding="utf-8"))


def source_status(root: Path) -> dict:
    metadata = load_metadata(root)
    source_path = root / metadata["source"]
    content, already_normalized = normalized_utf8(source_path)
    actual = digest(content)
    placeholders = sorted(
        set(PLACEHOLDER_RE.findall(content.decode("utf-8")))
    )
    declared = sorted(metadata["renderable_placeholders"])
    errors: list[str] = []
    if actual != metadata["source_sha256"]:
        errors.append("normalized source SHA-256 does not match metadata")
    if placeholders != declared:
        errors.append("source placeholders do not match permitted placeholders")
    if not already_normalized:
        errors.append("source bytes are not canonical UTF-8/LF")
    return {
        "kind": "contract-source-status",
        "source": metadata["source"],
        "source_sha256": actual,
        "matches_manifest": actual == metadata["source_sha256"],
        "encoding": "utf-8",
        "line_endings": "lf",
        "already_normalized": already_normalized,
        "characters": len(content.decode("utf-8")),
        "bytes": len(content),
        "placeholders": placeholders,
        "errors": errors,
        "files_modified": False,
    }


def rendered_status(
    root: Path,
    rendered_path: Path,
    antigravity_rule: Path | None,
) -> dict:
    metadata = load_metadata(root)
    content, already_normalized = normalized_utf8(rendered_path)
    text = content.decode("utf-8")
    remaining = sorted(set(PLACEHOLDER_RE.findall(text)))
    errors: list[str] = []
    if remaining:
        errors.append("rendered contract contains unresolved placeholders")
    if not text.startswith(f"# {metadata['contract_title']}\n"):
        errors.append("rendered contract title is missing")
    if not already_normalized:
        errors.append("rendered bytes are not canonical UTF-8/LF")

    rule_status = None
    if antigravity_rule:
        antigravity = metadata["clients"]["antigravity"]
        frontmatter = antigravity["frontmatter"]
        expected_prefix = (
            "---\n"
            f"trigger: {frontmatter['trigger']}\n"
            f"description: {frontmatter['description']}\n"
            "---\n"
        ).encode("utf-8")
        rule_content, rule_normalized = normalized_utf8(antigravity_rule)
        maximum_bytes = antigravity["maximum_file_bytes"]
        below_limit = len(rule_content) < maximum_bytes
        body = rule_content[len(expected_prefix) :] if rule_content.startswith(expected_prefix) else None
        body_matches = body == content
        rule_status = {
            "path": str(antigravity_rule),
            "sha256": digest(rule_content),
            "bytes": len(rule_content),
            "below_limit": below_limit,
            "body_matches_rendered_contract": body_matches,
            "already_normalized": rule_normalized,
        }
        if not rule_content.startswith(expected_prefix):
            errors.append("Antigravity rule frontmatter does not match metadata")
        if not below_limit:
            errors.append("Antigravity rule exceeds its declared byte limit")
        if not body_matches:
            errors.append("Antigravity rule body does not match rendered contract")
        if not rule_normalized:
            errors.append("Antigravity rule bytes are not canonical UTF-8/LF")

    return {
        "kind": "rendered-contract-status",
        "rendered_sha256": digest(content),
        "encoding": "utf-8",
        "line_endings": "lf",
        "already_normalized": already_normalized,
        "characters": len(text),
        "bytes": len(content),
        "unresolved_placeholders": remaining,
        "antigravity_rule": rule_status,
        "errors": errors,
        "files_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Package root containing instruction-pack.json",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("source")
    rendered_parser = subparsers.add_parser("rendered")
    rendered_parser.add_argument("path", type=Path)
    rendered_parser.add_argument(
        "--antigravity-rule",
        type=Path,
        help="Dedicated Antigravity global rule to validate against the rendered contract",
    )
    arguments = parser.parse_args()

    try:
        if arguments.command == "source":
            result = source_status(arguments.root.resolve())
        else:
            result = rendered_status(
                arguments.root.resolve(),
                arguments.path.resolve(),
                arguments.antigravity_rule.resolve()
                if arguments.antigravity_rule
                else None,
            )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)], "files_modified": False}))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

