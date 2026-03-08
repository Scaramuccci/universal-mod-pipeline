from __future__ import annotations

import json
from pathlib import Path

from pipeline.manifest import ModManifest


def write_reports(
    artifact_path: Path,
    checksum_paths: list[Path],
    manifest: ModManifest,
    reports_dir: Path,
) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_report = reports_dir / "build-report.json"
    md_report   = reports_dir / "build-report.md"

    payload = {
        "name": manifest.name,
        "version": manifest.version,
        "game": manifest.game,
        "engine": manifest.engine,
        "author": manifest.author,
        "description": manifest.description,
        "artifact": artifact_path.name,
        "size_bytes": artifact_path.stat().st_size,
        "checksums": [p.name for p in checksum_paths],
    }

    json_report.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    size_kb = artifact_path.stat().st_size / 1024
    md_lines = [
        "# Build Report", "",
        "| Field    | Value |",
        "|----------|-------|",
        f"| Name     | {manifest.name} |",
        f"| Version  | {manifest.version} |",
        f"| Game     | {manifest.game} |",
        f"| Engine   | {manifest.engine} |",
        f"| Author   | {manifest.author} |",
        f"| Artifact | {artifact_path.name} ({size_kb:.1f} KB) |",
        "", "## Checksums", "",
    ]
    for p in checksum_paths:
        md_lines.append(f"- `{p.name}`")
    md_lines.append("")

    md_report.write_text("\n".join(md_lines), encoding="utf-8")
    return json_report, md_report