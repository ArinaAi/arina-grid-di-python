#!/usr/bin/env python3
"""Import a generated SDK zip into this repo.

    python scripts/import_sdk.py path/to/<sdk>.zip

Generated paths are replaced; ours are untouched; preserved files (pyproject.toml,
README.md, LICENSE, SECURITY.md) are created once, then only diffed. The version in
pyproject.toml is written back into the generated _version.py; environment variable names
are rewritten to the ARINA_GRID_* family and the distribution name in shipped docs to the
one in pyproject.toml (the generator derives both from the API title and offers no setting);
and the placeholder default base URL the generator emits when no environment is configured
is replaced by an error (a client must never fall back to a host we do not own).
See CONTRIBUTING.md.
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
PACKAGE = REPO / "src" / "arina_grid_di"
PYPROJECT = REPO / "pyproject.toml"

# Zip-owned paths, replaced wholesale (minus OURS_INSIDE_GENERATED).
GENERATED = [
    "src/arina_grid_di",
    "api.md",
    "SKILL.md",
    ".claude",
    "scalar-sdk.manifest.json",
    "tests/smoke-test.py",
    ".gitignore",
]

# Hand-written code living under a generated directory.
OURS_INSIDE_GENERATED = [
    "src/arina_grid_di/lib",
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
    if not (root / "src" / "arina_grid_di" / "_client.py").exists():
        fail("zip does not contain src/arina_grid_di/_client.py")
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


# Generated env var name -> ours. A key that is absent is treated as already renamed, so this
# step retires itself if the generator adopts the names.
ENV_RENAMES = {
    "API_KEY": "ARINA_GRID_API_KEY",
    "ARINA_BASE_URL": "ARINA_GRID_BASE_URL",
    "ARINA_LOG": "ARINA_GRID_LOG",
    "ARINA_CUSTOM_HEADERS": "ARINA_GRID_CUSTOM_HEADERS",
}
RENAME_FILES = ["src/arina_grid_di/**/*.py", "api.md", "SKILL.md", ".claude/**/*.md", "tests/smoke-test.py"]
PROJECT_NAME_RE = re.compile(r'^name\s*=\s*"([^"]+)"', re.MULTILINE)

PLACEHOLDER_BASE_URL = re.compile(
    r'(if base_url is None:\n(?P<indent>\s+)base_url = os\.environ\.get\("(?P<env>[A-Z0-9_]+)"\)\n'
    r'\s+if base_url is None:\n\s+)base_url = "https://example\.com"'
)


def _generated_text_files():
    for pattern in RENAME_FILES:
        for path in REPO.glob(pattern):
            if path.is_file() and "lib" not in path.relative_to(REPO).parts:
                yield path


def rename_package(source: Path) -> str:
    """Make shipped docs name our distribution, whatever name the generator was configured with."""
    theirs = PROJECT_NAME_RE.search((source / "pyproject.toml").read_text(encoding="utf-8"))
    ours = PROJECT_NAME_RE.search(PYPROJECT.read_text(encoding="utf-8"))
    if not theirs or not ours or theirs.group(1) == ours.group(1):
        return f"generated docs already name {ours.group(1) if ours else '?'}"
    count = 0
    for path in _generated_text_files():
        text = path.read_text(encoding="utf-8")
        if theirs.group(1) in text:
            count += text.count(theirs.group(1))
            path.write_text(text.replace(theirs.group(1), ours.group(1)), encoding="utf-8")
    return f"generated docs renamed {theirs.group(1)} -> {ours.group(1)} ({count} mentions)"


def rename_env_vars() -> str:
    """Rewrite generated environment variable names to the ARINA_GRID_* family."""
    counts = dict.fromkeys(ENV_RENAMES, 0)
    for path in _generated_text_files():
        text = original = path.read_text(encoding="utf-8")
        for old, new in ENV_RENAMES.items():
            text, n = re.subn(rf"(?<![A-Za-z0-9_]){old}(?![A-Za-z0-9_])", new, text)
            counts[old] += n
        if text != original:
            path.write_text(text, encoding="utf-8")
    if not counts["API_KEY"] and not counts["ARINA_BASE_URL"]:
        return "generated code already uses ARINA_GRID_* names; nothing renamed"
    return "env vars renamed: " + ", ".join(f"{k}->{v} ({counts[k]})" for k, v in ENV_RENAMES.items())


def patch_placeholder_base_url() -> str:
    """Make base_url required when the generator emitted its placeholder default.

    With no environment configured, generated clients fall back to https://example.com and
    would send the API key there. Replace that fallback with the SDK's own error. Once a
    production environment is configured the placeholder is gone and this is a no-op.
    """
    client_py = PACKAGE / "_client.py"
    text = client_py.read_text(encoding="utf-8")
    error = re.search(r"raise (\w+Error)\(", text)
    if not error:
        fail("_client.py: could not find the SDK error class")

    def replacement(match: re.Match) -> str:
        indent, env = match["indent"], match["env"]
        return (
            f"{match.group(1)}raise {error.group(1)}(\n"
            f'{indent}    "The base_url client option must be set either by passing base_url to the client '
            f'or by setting the {env} environment variable"\n'
            f"{indent})"
        )

    text, count = PLACEHOLDER_BASE_URL.subn(replacement, text)
    if count == 0:
        return "generated client has a real default base URL; no patch needed"
    if count != 2:
        fail(f"_client.py: expected the placeholder in both sync and async clients, patched {count}")
    client_py.write_text(text, encoding="utf-8")
    return "placeholder default base URL replaced with a required-option error (sync + async)"


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
        package = rename_package(source)

    version = restore_version()
    renamed = rename_env_vars()
    patched = patch_placeholder_base_url()

    print("\nimport complete")
    print(f"  replaced (generated): {', '.join(replaced)}")
    if created:
        print(f"  created (preserved, first import): {', '.join(created)}")
    if differing:
        print(f"  review (preserved, zip differs): {', '.join(differing)}")
    print(f"  version restored to {version} in _version.py")
    print(f"  package:  {package}")
    print(f"  env vars: {renamed}")
    print(f"  base url: {patched}")
    print("\nnext: pytest, then commit as feat:/fix: describing the API change.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
