#!/usr/bin/env python3
"""Inspect a tree without following links or modifying it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path


REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def is_reparse(metadata: os.stat_result) -> bool:
    return bool(getattr(metadata, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def inspect(root: Path, excluded: set[str] | None = None) -> dict:
    errors: list[str] = []
    entries: list[tuple[str, str, bytes]] = []
    case_names: dict[str, str] = {}
    excluded = excluded or set()

    if not root.exists() and not root.is_symlink():
        return {
            "root": str(root),
            "safe": False,
            "tree_sha256": None,
            "entries": 0,
            "errors": ["root does not exist"],
            "files_modified": False,
        }

    def visit(path: Path, relative: str) -> None:
        if relative in excluded:
            return
        metadata = path.lstat()
        display = relative or "."
        folded = display.casefold()
        previous = case_names.get(folded)
        if previous is not None and previous != display:
            errors.append(f"case-insensitive collision: {previous!r} and {display!r}")
        case_names[folded] = display

        if is_reparse(metadata):
            errors.append(f"{display}: reparse point or junction")
            entries.append(("unsafe", display, b""))
            return
        if stat.S_ISLNK(metadata.st_mode):
            errors.append(f"{display}: symbolic link")
            entries.append(("unsafe", display, b""))
            return
        if stat.S_ISDIR(metadata.st_mode):
            entries.append(("directory", display, b""))
            with os.scandir(path) as iterator:
                children = sorted(iterator, key=lambda item: item.name)
            for child in children:
                child_relative = child.name if not relative else f"{relative}/{child.name}"
                visit(Path(child.path), child_relative)
            return
        if stat.S_ISREG(metadata.st_mode):
            content = path.read_bytes()
            entries.append(("file", display, hashlib.sha256(content).digest()))
            return

        file_type = "unsupported special file"
        if stat.S_ISFIFO(metadata.st_mode):
            file_type = "FIFO"
        elif stat.S_ISSOCK(metadata.st_mode):
            file_type = "socket"
        elif stat.S_ISCHR(metadata.st_mode):
            file_type = "character device"
        elif stat.S_ISBLK(metadata.st_mode):
            file_type = "block device"
        errors.append(f"{display}: {file_type}")
        entries.append(("unsafe", display, b""))

    visit(root, "")
    tree_hash = hashlib.sha256()
    for kind, relative, content_hash in sorted(entries):
        tree_hash.update(kind.encode("utf-8"))
        tree_hash.update(b"\0")
        tree_hash.update(relative.encode("utf-8"))
        tree_hash.update(b"\0")
        tree_hash.update(content_hash)
        tree_hash.update(b"\0")

    return {
        "root": str(root),
        "safe": not errors,
        "tree_sha256": tree_hash.hexdigest(),
        "entries": len(entries),
        "errors": errors,
        "excluded": sorted(excluded),
        "files_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exact POSIX-style relative path to omit from the hash and safety walk",
    )
    arguments = parser.parse_args()
    invalid_exclusions = [
        value
        for value in arguments.exclude
        if not value
        or value.startswith("/")
        or "\\" in value
        or ".." in Path(value).parts
    ]
    if invalid_exclusions:
        parser.error(f"unsafe exclusions: {invalid_exclusions}")
    result = inspect(
        Path(os.path.abspath(arguments.path)),
        set(arguments.exclude),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["safe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
