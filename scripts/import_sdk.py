#!/usr/bin/env python3
"""Import a generated SDK zip into this repo.

    python scripts/import_sdk.py path/to/<sdk>.zip

Generated paths are replaced; ours are untouched; preserved files (pyproject.toml,
README.md, LICENSE, SECURITY.md) are created once, then only diffed. The version in
pyproject.toml is written back into the generated _version.py. See CONTRIBUTING.md.
"""

from __future__ import annotations

import difflib
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "src" / "arina_document_intelligence"

# Zip-owned paths, replaced wholesale (minus OURS_INSIDE_GENERATED).
GENERATED = [
    "src/arina_document_intelligence",
    "api.md",
    "SKILL.md",
    ".claude",
    "scalar-sdk.manifest.json",
    "tests/smoke-test.py",
    ".gitignore",
]

# Hand-written code living under a generated directory.
OURS_INSIDE_GENERATED = [
    "src/arina_document_intelligence/lib",
]

# Created on first import, then owned here; diffed on later imports.
PRESERVED = [
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "SECURITY.md",
]

VERSION_RE = re.compile(r'^(version\s*=\s*)"([^"]+)"', re.MULTILINE)
# Keeps the trailing `# x-release-please-version` marker: release-please bumps the line by it.
VERSION_PY_RE = re.compile(r'^(__version__\s*=\s*)"([^"]+)"', re.MULTILINE)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def extract(zip_path: Path, into: Path) -> Path:
    """Unzip and return the directory that holds pyproject.toml."""
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(into)
    candidates = [p.parent for p in into.rglob("pyproject.toml")]
    if len(candidates) != 1:
        fail(f"expected exactly one pyproject.toml in the zip, found {len(candidates)}")
    root = candidates[0]
    if not (root / "src" / "arina_document_intelligence" / "_client.py").exists():
        fail("zip does not contain src/arina_document_intelligence/_client.py")
    return root


def replace_generated(source: Path) -> list[str]:
    """Copy generated paths from ``source`` into the repo. Returns what was replaced."""
    replaced: list[str] = []
    keep = [REPO / p for p in OURS_INSIDE_GENERATED]

    for rel in GENERATED:
        src, dst = source / rel, REPO / rel
        if not src.exists():
            print(f"note: zip has no {rel}; leaving ours in place")
            continue
        if src.is_dir():
            if dst.exists():
                for child in dst.iterdir():
                    if any(child == k or k.is_relative_to(child) for k in keep):
                        # Contains (or is) one of ours: descend instead of deleting.
                        _remove_generated_within(child, keep)
                    else:
                        shutil.rmtree(child) if child.is_dir() else child.unlink()
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        replaced.append(rel)
    return replaced


def _remove_generated_within(directory: Path, keep: list[Path]) -> None:
    """Delete everything under ``directory`` except the ``keep`` paths."""
    if directory in keep:
        return
    if directory.is_file():
        directory.unlink()
        return
    for child in directory.iterdir():
        if any(child == k or k.is_relative_to(child) for k in keep):
            _remove_generated_within(child, keep)
        else:
            shutil.rmtree(child) if child.is_dir() else child.unlink()


def handle_preserved(source: Path) -> tuple[list[str], list[str]]:
    """Bootstrap missing preserved files; diff the rest. Returns (created, differing)."""
    created: list[str] = []
    differing: list[str] = []
    for rel in PRESERVED:
        src, dst = source / rel, REPO / rel
        if not src.exists():
            continue
        if not dst.exists():
            shutil.copy2(src, dst)
            created.append(rel)
            continue
        theirs = src.read_text(encoding="utf-8").splitlines(keepends=True)
        ours = dst.read_text(encoding="utf-8").splitlines(keepends=True)
        if theirs != ours:
            differing.append(rel)
            print(f"\n--- {rel}: generated version differs from ours (ours is kept) ---")
            sys.stdout.writelines(difflib.unified_diff(ours, theirs, fromfile=f"ours/{rel}", tofile=f"zip/{rel}", n=1))
    return created, differing


def restore_version() -> str:
    """Write the version from pyproject.toml into the generated _version.py."""
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    match = VERSION_RE.search(pyproject)
    if not match:
        fail("could not find a version line in pyproject.toml")
    version = match.group(2)
    version_py = PACKAGE / "_version.py"
    text = version_py.read_text(encoding="utf-8")
    new_text, count = VERSION_PY_RE.subn(rf'\g<1>"{version}"', text)
    if count != 1:
        fail("could not find __version__ in the generated _version.py")
    version_py.write_text(new_text, encoding="utf-8")
    return version


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    zip_path = Path(argv[1]).expanduser().resolve()
    if not zip_path.is_file():
        fail(f"no such file: {zip_path}")

    with tempfile.TemporaryDirectory() as tmp:
        source = extract(zip_path, Path(tmp))
        replaced = replace_generated(source)
        created, differing = handle_preserved(source)

    version = restore_version()

    print("\nimport complete")
    print(f"  replaced (generated): {', '.join(replaced)}")
    if created:
        print(f"  created (preserved, first import): {', '.join(created)}")
    if differing:
        print(f"  review (preserved, zip differs): {', '.join(differing)}")
    print(f"  version restored to {version} in _version.py")
    print("\nnext: pytest, then commit as feat:/fix: describing the API change.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
