from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def package_mod(mod_path: Path, output_dir: Path) -> int:
    print(f"\n{'='*60}")
    print(f"  Packaging mod: {mod_path}")
    print(f"{'='*60}\n")

    manifest_path = mod_path / "manifest.json"
    if not manifest_path.exists():
        print("[ERROR] manifest.json not found. Run validation first.")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    name = manifest["name"]
    version = manifest["version"]

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_base = output_dir / f"{name}-{version}"

    # Count files being packaged
    all_files = [f for f in mod_path.rglob("*") if f.is_file()]
    print(f"[INFO]  Bundling {len(all_files)} file(s) from {mod_path.name}/")
    for f in sorted(all_files):
        rel = f.relative_to(mod_path)
        size_kb = f.stat().st_size / 1024
        print(f"        + {rel}  ({size_kb:.1f} KB)")

    shutil.make_archive(str(archive_base), "zip", root_dir=mod_path.parent, base_dir=mod_path.name)

    zip_path = Path(str(archive_base) + ".zip")
    zip_size_kb = zip_path.stat().st_size / 1024
    print(f"\n[OK]    Packaged → {zip_path}  ({zip_size_kb:.1f} KB)")

    # Write a build-info sidecar
    build_info = {
        "name": name,
        "version": version,
        "game": manifest.get("game"),
        "author": manifest.get("author"),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "archive": zip_path.name,
        "file_count": len(all_files),
        "size_bytes": zip_path.stat().st_size,
    }
    build_info_path = output_dir / f"{name}-{version}.build-info.json"
    build_info_path.write_text(json.dumps(build_info, indent=2), encoding="utf-8")
    print(f"[OK]    Build info → {build_info_path}")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package a game mod into a versioned zip archive")
    parser.add_argument("--mod-path", required=True, help="Path to the mod directory")
    parser.add_argument("--output", required=True, help="Output directory for the zip")
    args = parser.parse_args()
    sys.exit(package_mod(Path(args.mod_path), Path(args.output)))
