from __future__ import annotations

from pathlib import Path

from pipeline.config import PipelinePolicy


class SecurityError(Exception):
    pass


def run_security_checks(mod_path: Path, policy: PipelinePolicy) -> list[str]:
    warnings: list[str] = []
    total_size = 0

    for path in sorted(mod_path.rglob("*")):
        if path.is_dir():
            continue

        suffix = path.suffix.lower()
        if suffix in policy.blocked_extensions:
            raise SecurityError(
                f"blocked file type detected: {path.relative_to(mod_path)}"
            )

        size = path.stat().st_size
        total_size += size

        if size > policy.max_file_size_bytes:
            raise SecurityError(
                f"file exceeds {policy.max_file_size_mb} MB limit: "
                f"{path.relative_to(mod_path)} ({size / 1_048_576:.1f} MB)"
            )

    if total_size > policy.max_total_size_bytes:
        raise SecurityError(
            f"mod total size exceeds {policy.max_total_size_mb} MB limit "
            f"({total_size / 1_048_576:.1f} MB)"
        )

    return warnings