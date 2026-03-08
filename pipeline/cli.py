from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pipeline.checks import ValidationError, validate_mod
from pipeline.config import DEFAULT_POLICY
from pipeline.packaging import package_mod, write_checksums
from pipeline.reporting import write_reports


def _ok(msg):   print(f"[OK]    {msg}")
def _warn(msg): print(f"[WARN]  {msg}")
def _err(msg):  print(f"[ERROR] {msg}")
def _info(msg): print(f"[INFO]  {msg}")

def _header(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}\n")

def _summary(errors, warnings):
    print(f"\n{'─'*60}")
    print(f"  {'✓ PASSED' if errors == 0 else '✗ FAILED'} — {errors} error(s), {warnings} warning(s)")
    print(f"{'─'*60}\n")


def cmd_validate(mod_path: Path) -> int:
    _header(f"Validate  →  {mod_path}")
    try:
        manifest, warnings = validate_mod(mod_path, DEFAULT_POLICY)
    except Exception as exc:
        _err(str(exc))
        _summary(1, 0)
        return 1

    _ok("manifest.json found and valid")
    _ok(f"Required directories present: {', '.join(DEFAULT_POLICY.required_directories)}")
    _ok(f"Entry script found: {manifest.entry_script}")
    _ok("Security checks passed")
    for w in warnings:
        _warn(w)

    print(f"\n  Mod     : {manifest.name}")
    print(f"  Version : {manifest.version}")
    print(f"  Game    : {manifest.game}")
    print(f"  Engine  : {manifest.engine}")
    print(f"  Author  : {manifest.author}")
    if manifest.description:
        print(f"  Desc    : {manifest.description}")

    _summary(0, len(warnings))
    return 0


def cmd_package(mod_path: Path, output_dir: Path) -> int:
    _header(f"Package  →  {mod_path}  →  {output_dir}")
    try:
        manifest, warnings = validate_mod(mod_path, DEFAULT_POLICY)
    except Exception as exc:
        _err(str(exc))
        return 1

    for w in warnings:
        _warn(w)

    try:
        archive_path, bundled_files = package_mod(mod_path, output_dir, manifest)
    except Exception as exc:
        _err(f"Packaging failed: {exc}")
        return 1

    _info(f"Bundling {len(bundled_files)} file(s):")
    for f in bundled_files:
        print(f"        + {f.relative_to(mod_path)}  ({f.stat().st_size/1024:.1f} KB)")

    _ok(f"Packaged → {archive_path}  ({archive_path.stat().st_size/1024:.1f} KB)")

    checksum_paths = write_checksums(output_dir)
    for cp in checksum_paths:
        _ok(f"Checksum → {cp.name}")

    _summary(0, len(warnings))
    return 0


def cmd_report(mod_path: Path, artifacts_dir: Path) -> int:
    _header(f"Report  →  {artifacts_dir}")
    try:
        manifest, _ = validate_mod(mod_path, DEFAULT_POLICY)
    except Exception as exc:
        _err(f"Could not load manifest: {exc}")
        return 1

    zip_files = list(artifacts_dir.glob("*.zip"))
    sha_files = [p for p in artifacts_dir.glob("*.sha256") if p.name != "checksums.sha256"]

    if not zip_files:
        _err("No .zip artifacts found. Run 'package' first.")
        return 1

    json_report, md_report = write_reports(
        sorted(zip_files)[0], sha_files, manifest,
        Path(DEFAULT_POLICY.reports_dir),
    )
    _ok(f"JSON report → {json_report}")
    _ok(f"Markdown report → {md_report}")
    print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Universal Mod Pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="Validate a mod")
    v.add_argument("--mod-path", required=True)

    p = sub.add_parser("package", help="Package a mod into a versioned ZIP")
    p.add_argument("--mod-path", required=True)
    p.add_argument("--output", required=True)

    r = sub.add_parser("report", help="Write build reports")
    r.add_argument("--mod-path", required=True)
    r.add_argument("--artifacts", required=True)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate":
        return cmd_validate(Path(args.mod_path))
    if args.command == "package":
        return cmd_package(Path(args.mod_path), Path(args.output))
    if args.command == "report":
        return cmd_report(Path(args.mod_path), Path(args.artifacts))
    return 1


if __name__ == "__main__":
    sys.exit(main())