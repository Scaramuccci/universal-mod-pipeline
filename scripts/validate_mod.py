from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ERRORS: list[str] = []
WARNINGS: list[str] = []

# ── Lightweight manifest schema (stdlib only, no external deps) ─────────────
REQUIRED_FIELDS: dict[str, type] = {
    "name": str,
    "version": str,
    "game": str,
    "author": str,
    "entry_script": str,
}
OPTIONAL_FIELDS = ("description", "tags", "homepage")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def err(msg: str) -> None:
    ERRORS.append(msg)
    print(f"[ERROR] {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"[WARN]  {msg}")


def ok(msg: str) -> None:
    print(f"[OK]    {msg}")


def _validate_schema(manifest: dict) -> bool:
    passed = True
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in manifest:
            err(f"Manifest missing required field: '{field}'")
            passed = False
        elif not isinstance(manifest[field], expected_type):
            err(f"Manifest field '{field}' must be {expected_type.__name__}")
            passed = False
        elif isinstance(manifest[field], str) and not manifest[field].strip():
            err(f"Manifest field '{field}' must not be empty")
            passed = False

    version = manifest.get("version", "")
    if isinstance(version, str) and version and not SEMVER_RE.match(version):
        err(f"'version' must be MAJOR.MINOR.PATCH — got: '{version}'")
        passed = False

    return passed


def validate_mod(mod_path: Path) -> int:
    print(f"\n{'='*60}")
    print(f"  Validating mod: {mod_path}")
    print(f"{'='*60}\n")

    if not mod_path.exists() or not mod_path.is_dir():
        err(f"Mod path does not exist: {mod_path}")
        _print_summary()
        return 1

    manifest_path = mod_path / "manifest.json"
    assets_path = mod_path / "assets"
    scripts_path = mod_path / "scripts"

    for required_dir in (assets_path, scripts_path):
        if not required_dir.exists():
            err(f"Required directory missing: {required_dir.name}/")
        else:
            ok(f"Directory exists: {required_dir.name}/")

    if not manifest_path.exists():
        err("manifest.json is missing")
        _print_summary()
        return 1

    ok("manifest.json found")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"Invalid JSON in manifest.json: {exc}")
        _print_summary()
        return 1

    ok("manifest.json is valid JSON")

    if _validate_schema(manifest):
        ok("Manifest schema is valid")

    entry_script = mod_path / manifest.get("entry_script", "")
    if not entry_script.exists():
        err(f"Entry script not found: {manifest.get('entry_script')}")
    else:
        ok(f"Entry script found: {manifest.get('entry_script')}")

    if assets_path.exists():
        asset_files = [f for f in assets_path.rglob("*") if f.is_file()]
        if not asset_files:
            warn("assets/ directory is empty — no game assets found")
        else:
            ok(f"Assets found: {len(asset_files)} file(s)")

    for optional in OPTIONAL_FIELDS:
        if optional not in manifest:
            warn(f"Optional field '{optional}' not in manifest.json")

    print(f"\n  Mod     : {manifest.get('name', 'unknown')}")
    print(f"  Version : {manifest.get('version', 'unknown')}")
    print(f"  Game    : {manifest.get('game', 'unknown')}")
    print(f"  Author  : {manifest.get('author', 'unknown')}")
    if "description" in manifest:
        print(f"  Desc    : {manifest['description']}")

    _print_summary()
    return 1 if ERRORS else 0


def _print_summary() -> None:
    print(f"\n{'─'*60}")
    status = "✓ PASSED" if not ERRORS else "✗ FAILED"
    print(f"  {status} — {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
    print(f"{'─'*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a game mod structure and manifest")
    parser.add_argument("--mod-path", required=True, help="Path to the mod directory")
    args = parser.parse_args()
    sys.exit(validate_mod(Path(args.mod_path)))
