#!/usr/bin/env python3
"""Validate a release ZIP, its payload inventory, and extraction safety."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath


DRIVE_RE = re.compile(r"^[A-Za-z]:")
WINDOWS_DEVICE_RE = re.compile(
    r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$", re.IGNORECASE
)
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000


def validate(path: Path) -> dict:
    errors: list[str] = []
    exact: set[str] = set()
    portable_names: dict[str, str] = {}
    regular_entries: dict[str, zipfile.ZipInfo] = {}
    total_uncompressed = 0

    with zipfile.ZipFile(path) as archive:
        for entry in archive.infolist():
            name = entry.filename
            normalized_name = name.replace("\\", "/")
            pure = PurePosixPath(normalized_name)

            if pure.name.casefold() == "memory.md":
                errors.append(f"archive contains prohibited private memory file: {name}")

            if name in exact:
                errors.append(f"duplicate entry: {name}")
            exact.add(name)
            portable_key = unicodedata.normalize("NFC", normalized_name).casefold()
            previous = portable_names.get(portable_key)
            if previous is not None and previous != normalized_name:
                errors.append(
                    f"portable-name collision: {previous!r} and {normalized_name!r}"
                )
            portable_names[portable_key] = normalized_name

            unsafe_component = any(
                component.endswith((" ", "."))
                or ":" in component
                or WINDOWS_DEVICE_RE.fullmatch(component)
                for component in pure.parts
            )
            if (
                normalized_name.startswith("/")
                or DRIVE_RE.match(normalized_name)
                or ".." in pure.parts
                or "." in pure.parts
                or "\\" in name
                or unsafe_component
            ):
                errors.append(f"unsafe extraction path: {name}")

            unix_mode = (entry.external_attr >> 16) & 0xFFFF
            if unix_mode:
                file_type = stat.S_IFMT(unix_mode)
                if file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                    errors.append(f"unsupported archive entry type: {name}")
            if entry.flag_bits & 0x1:
                errors.append(f"encrypted entry is unsupported: {name}")
            if not entry.is_dir():
                regular_entries[normalized_name] = entry
                total_uncompressed += entry.file_size
                if entry.file_size > MAX_FILE_BYTES:
                    errors.append(f"entry exceeds size limit: {name}")
                if (
                    entry.file_size
                    and entry.compress_size == 0
                    or entry.compress_size
                    and entry.file_size / entry.compress_size > MAX_COMPRESSION_RATIO
                ):
                    errors.append(f"entry exceeds compression-ratio limit: {name}")

        if total_uncompressed > MAX_TOTAL_BYTES:
            errors.append("archive exceeds total uncompressed-size limit")
        bad_crc = archive.testzip()
        if bad_crc is not None:
            errors.append(f"archive CRC failure: {bad_crc}")

        roots = {PurePosixPath(name).parts[0] for name in exact if name}
        if len(roots) != 1:
            errors.append("archive must contain exactly one top-level directory")
            release_root = ""
        else:
            release_root = next(iter(roots))
        inventory_name = f"{release_root}/release-files.json"
        if inventory_name not in regular_entries:
            errors.append("archive is missing release-files.json")
        else:
            try:
                inventory = json.loads(archive.read(inventory_name).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                errors.append(f"invalid release-files.json: {error}")
                inventory = {}
            declared = inventory.get("files", []) if isinstance(inventory, dict) else []
            expected_names = {inventory_name}
            for item in declared:
                if not isinstance(item, dict):
                    errors.append("release inventory contains malformed entry")
                    continue
                relative = item.get("path", "")
                if (
                    isinstance(relative, str)
                    and PurePosixPath(relative).name.casefold() == "memory.md"
                ):
                    errors.append(
                        "release inventory includes prohibited private memory file: "
                        f"{relative}"
                    )
                archived_name = f"{release_root}/{relative}"
                expected_names.add(archived_name)
                entry = regular_entries.get(archived_name)
                if entry is None:
                    errors.append(f"archive payload missing: {relative}")
                    continue
                payload = archive.read(entry)
                if (
                    len(payload) != item.get("bytes")
                    or hashlib.sha256(payload).hexdigest() != item.get("sha256")
                ):
                    errors.append(f"archive payload hash mismatch: {relative}")
            unexpected = sorted(set(regular_entries) - expected_names)
            if unexpected:
                errors.append(f"archive contains undeclared files: {unexpected}")
            for required in ("manifest.json", "VERSION", "LICENSE"):
                if f"{release_root}/{required}" not in regular_entries:
                    errors.append(f"archive is missing required file: {required}")

    return {
        "archive": str(path),
        "entries": len(exact),
        "regular_files": len(regular_entries),
        "uncompressed_bytes": total_uncompressed,
        "safe": not errors,
        "errors": errors,
        "files_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    arguments = parser.parse_args()
    try:
        result = validate(arguments.archive.resolve())
    except (OSError, zipfile.BadZipFile) as error:
        result = {
            "archive": str(arguments.archive),
            "safe": False,
            "errors": [str(error)],
            "files_modified": False,
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["safe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
