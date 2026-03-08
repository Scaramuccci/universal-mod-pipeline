from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from pipeline.manifest import ModManifest


def sha256_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_mod(
    mod_path: Path, output_dir: Path, manifest: ModManifest
) -> tuple[Path, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_base = output_dir / f"{manifest.name}-{manifest.version}"

    all_files = sorted(f for f in mod_path.rglob("*") if f.is_file())

    archive_path = Path(
        shutil.make_archive(
            str(archive_base), "zip",
            root_dir=mod_path.parent,
            base_dir=mod_path.name,
        )
    )

    build_info = {
        "name": manifest.name,
        "version": manifest.version,
        "game": manifest.game,
        "engine": manifest.engine,
        "author": manifest.author,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "archive": archive_path.name,
        "file_count": len(all_files),
        "size_bytes": archive_path.stat().st_size,
    }
    build_info_path = output_dir / f"{manifest.name}-{manifest.version}.build-info.json"
    build_info_path.write_text(json.dumps(build_info, indent=2), encoding="utf-8")

    return archive_path, all_files


def write_checksums(output_dir: Path) -> list[Path]:
    zip_files = sorted(output_dir.glob("*.zip"))
    written: list[Path] = []
    combined_lines: list[str] = []

    for file_path in zip_files:
        checksum = sha256_file(file_path)
        checksum_path = file_path.with_suffix(file_path.suffix + ".sha256")
        checksum_path.write_text(
            f"{checksum}  {file_path.name}\n", encoding="utf-8"
        )
        written.append(checksum_path)
        combined_lines.append(f"{checksum}  {file_path.name}")

    if combined_lines:
        combined_path = output_dir / "checksums.sha256"
        combined_path.write_text("\n".join(combined_lines) + "\n", encoding="utf-8")
        written.append(combined_path)

    return written