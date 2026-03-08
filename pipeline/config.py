from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PipelinePolicy:
    required_directories: tuple[str, ...] = ("assets", "scripts")
    blocked_extensions: tuple[str, ...] = (
        ".exe", ".dll", ".bat", ".cmd", ".ps1", ".sh", ".msi",
    )
    optional_manifest_fields: tuple[str, ...] = ("description", "homepage", "tags")
    max_file_size_mb: int = 50
    max_total_size_mb: int = 500
    reports_dir: str = "reports"
    dist_dir: str = "dist"

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def max_total_size_bytes(self) -> int:
        return self.max_total_size_mb * 1024 * 1024


DEFAULT_POLICY = PipelinePolicy()