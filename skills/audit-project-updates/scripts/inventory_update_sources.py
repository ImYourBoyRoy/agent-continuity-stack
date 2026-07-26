#!/usr/bin/env python3
"""Inventory likely update surfaces without network access or file mutation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_update_check import ConfigError, load_document, validate_config


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "target",
    "dist",
    "build",
    "vendor",
    "__pycache__",
    ".cache",
}

SURFACES = {
    "Cargo.toml": "rust-manifest",
    "Cargo.lock": "rust-lockfile",
    "rust-toolchain": "rust-toolchain",
    "rust-toolchain.toml": "rust-toolchain",
    "package.json": "javascript-manifest",
    "package-lock.json": "npm-lockfile",
    "npm-shrinkwrap.json": "npm-lockfile",
    "pnpm-lock.yaml": "pnpm-lockfile",
    "yarn.lock": "yarn-lockfile",
    "bun.lock": "bun-lockfile",
    "bun.lockb": "bun-lockfile",
    "pyproject.toml": "python-manifest",
    "uv.lock": "uv-lockfile",
    "poetry.lock": "poetry-lockfile",
    "Pipfile": "pipenv-manifest",
    "Pipfile.lock": "pipenv-lockfile",
    "go.mod": "go-manifest",
    "go.sum": "go-lockfile",
    "go.work": "go-workspace",
    "go.work.sum": "go-workspace-lockfile",
    "pom.xml": "maven-manifest",
    "build.gradle": "gradle-build",
    "build.gradle.kts": "gradle-build",
    "settings.gradle": "gradle-settings",
    "settings.gradle.kts": "gradle-settings",
    "gradle-wrapper.properties": "gradle-wrapper",
    "libs.versions.toml": "gradle-version-catalog",
    "Gemfile": "ruby-manifest",
    "Gemfile.lock": "ruby-lockfile",
    "composer.json": "composer-manifest",
    "composer.lock": "composer-lockfile",
    "mix.exs": "elixir-manifest",
    "mix.lock": "elixir-lockfile",
    "pubspec.yaml": "dart-manifest",
    "pubspec.lock": "dart-lockfile",
    "Package.swift": "swift-manifest",
    "Package.resolved": "swift-lockfile",
    "Podfile": "cocoapods-manifest",
    "Podfile.lock": "cocoapods-lockfile",
    "Cartfile": "carthage-manifest",
    "Cartfile.resolved": "carthage-lockfile",
    "flake.nix": "nix-flake",
    "flake.lock": "nix-lockfile",
    "Dockerfile": "container-build",
    "compose.yml": "container-compose",
    "compose.yaml": "container-compose",
    "docker-compose.yml": "container-compose",
    "docker-compose.yaml": "container-compose",
    ".terraform.lock.hcl": "terraform-lockfile",
    "Chart.yaml": "helm-chart",
    "Chart.lock": "helm-lockfile",
    "wrangler.toml": "cloudflare-config",
    "wrangler.json": "cloudflare-config",
    "wrangler.jsonc": "cloudflare-config",
    ".node-version": "node-runtime",
    ".python-version": "python-runtime",
    ".tool-versions": "runtime-toolchain",
    "renovate.json": "renovate-config",
    "renovate.json5": "renovate-config",
    "dependabot.yml": "dependabot-config",
    "dependabot.yaml": "dependabot-config",
    ".gitmodules": "git-submodules",
    ".update-check.yml": "explicit-update-sources",
    ".update-check.yaml": "explicit-update-sources",
    ".update-check.json": "explicit-update-sources",
}

TEXT_SOURCE_NAMES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "DEVELOPMENT.md",
    "Makefile",
    "justfile",
    ".update-check.yml",
    ".update-check.yaml",
    ".update-check.json",
    ".gitmodules",
}

REPOSITORY_RES = [
    re.compile(
        r"https://(?:github\.com|gitlab\.com|codeberg\.org)/"
        r"[A-Za-z0-9_.~/-]+/[A-Za-z0-9_.~/-]+(?:\.git)?",
        re.IGNORECASE,
    ),
    re.compile(
        r"https://git\.sr\.ht/~[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:ssh://git@|git@)[A-Za-z0-9_.-]+(?::|/)"
        r"[A-Za-z0-9_.~/-]+/[A-Za-z0-9_.~/-]+(?:\.git)?",
        re.IGNORECASE,
    ),
    re.compile(
        r"https://[A-Za-z0-9_.-]+/[A-Za-z0-9_.~/-]+/"
        r"[A-Za-z0-9_.~/-]+\.git",
        re.IGNORECASE,
    ),
]
CONTAINER_RE = re.compile(r"^\s*FROM\s+(?:--platform=\S+\s+)?(\S+)", re.MULTILINE)
ACTION_RE = re.compile(
    r"^\s*uses:\s*[\"']?([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[^\s\"'#]+)",
    re.MULTILINE,
)


def walk_files(root: Path):
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            continue
        try:
            path.resolve().relative_to(root)
        except (OSError, ValueError):
            continue
        if path.is_file():
            yield path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def surface_kind(path: Path, root: Path) -> str | None:
    if path.name in SURFACES:
        return SURFACES[path.name]
    name = path.name.lower()
    parts = path.relative_to(root).parts
    if re.fullmatch(r"requirements(?:-[a-z0-9_.-]+)?\.txt", name):
        return "python-requirements"
    if path.suffix == ".tf":
        return "terraform-config"
    if len(parts) >= 3 and parts[-3:-1] == (".github", "workflows"):
        return "github-workflow"
    if ".github" in parts and "actions" in parts and name in {"action.yml", "action.yaml"}:
        return "github-local-action"
    if ".devcontainer" in parts and name in {
        "devcontainer.json",
        "docker-compose.yml",
        "docker-compose.yaml",
    }:
        return "devcontainer-config"
    return None


def should_scan_text(path: Path, root: Path, kind: str | None) -> bool:
    if path.name in TEXT_SOURCE_NAMES:
        return True
    if path.suffix.lower() in {".sh", ".ps1", ".bat", ".cmd"}:
        return True
    return kind in {
        "javascript-manifest",
        "python-manifest",
        "rust-manifest",
        "container-build",
        "github-workflow",
        "github-local-action",
        "explicit-update-sources",
    }


def clean_repository(value: str) -> str:
    return value.rstrip(".,;:)]}\"'").removesuffix(".git")


def add_candidate(
    candidates: dict[tuple[str, str], set[str]],
    kind: str,
    value: str,
    source_path: str,
) -> None:
    candidates.setdefault((kind, value), set()).add(source_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository or workspace root")
    parser.add_argument(
        "--show-absolute-root",
        action="store_true",
        help="Include the resolved root path in output; may disclose local identity",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    surfaces: list[dict[str, str]] = []
    candidates: dict[tuple[str, str], set[str]] = {}
    explicit_sources: list[dict[str, object]] = []
    config_errors: list[dict[str, str]] = []

    for path in walk_files(root):
        kind = surface_kind(path, root)
        path_text = relative(path, root)
        if kind:
            surfaces.append({"kind": kind, "path": path_text})

        if kind == "explicit-update-sources":
            try:
                config = validate_config(load_document(path))
                for source in config["sources"]:
                    explicit_sources.append(
                        {
                            "id": source["id"],
                            "kind": source["kind"],
                            "locator": source.get("locator"),
                            "purpose": source["purpose"],
                            "defined_by": path_text,
                        }
                    )
            except (OSError, json.JSONDecodeError, ConfigError) as error:
                config_errors.append({"path": path_text, "error": str(error)})

        if not should_scan_text(path, root, kind):
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for repository_re in REPOSITORY_RES:
            for match in repository_re.findall(text):
                add_candidate(
                    candidates, "repository", clean_repository(match), path_text
                )
        if kind == "container-build":
            for image in CONTAINER_RE.findall(text):
                add_candidate(candidates, "container-image", image, path_text)
        if kind == "github-workflow":
            for action in ACTION_RE.findall(text):
                add_candidate(candidates, "github-action", action, path_text)

    result = {
        "schema": 2,
        "root": str(root) if args.show_absolute_root else ".",
        "absolute_root_disclosed": args.show_absolute_root,
        "network_used": False,
        "files_modified": False,
        "surfaces": sorted(surfaces, key=lambda item: (item["kind"], item["path"])),
        "declared_candidates": [
            {"kind": kind, "value": value, "referenced_by": sorted(paths)}
            for (kind, value), paths in sorted(candidates.items())
        ],
        "explicit_sources": sorted(
            explicit_sources, key=lambda item: (str(item["id"]), str(item["defined_by"]))
        ),
        "configuration_errors": config_errors,
        "caution": (
            "Candidates require agent review; a manifest or textual reference does "
            "not prove active use, public visibility, or compatibility."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if config_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
