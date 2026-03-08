from __future__ import annotations

from pathlib import Path

from pipeline.config import PipelinePolicy
from pipeline.manifest import ManifestError, ModManifest, load_manifest
from pipeline.security import SecurityError, run_security_checks


class ValidationError(Exception):
    pass


def validate_mod(
    mod_path: Path, policy: PipelinePolicy
) -> tuple[ModManifest, list[str]]:
    warnings: list[str] = []

    if not mod_path.exists() or not mod_path.is_dir():
        raise ValidationError(f"mod path does not exist: {mod_path}")

    try:
        manifest = load_manifest(mod_path)
    except ManifestError as exc:
        raise ValidationError(str(exc)) from exc

    for directory in policy.required_directories:
        target = mod_path / directory
        if not target.exists() or not target.is_dir():
            raise ValidationError(f"required directory missing: {directory}/")

    entry_script_path = mod_path / manifest.entry_script
    if not entry_script_path.exists():
        raise ValidationError(f"entry script not found: {manifest.entry_script}")

    assets_dir = mod_path / "assets"
    if assets_dir.exists():
        asset_files = [f for f in assets_dir.rglob("*") if f.is_file()]
        if not asset_files:
            warnings.append("assets/ directory is empty — no game assets found")

    for field in policy.optional_manifest_fields:
        if not getattr(manifest, field, None):
            warnings.append(f"optional manifest field '{field}' is not set")

    try:
        security_warnings = run_security_checks(mod_path, policy)
        warnings.extend(security_warnings)
    except SecurityError as exc:
        raise ValidationError(str(exc)) from exc

    return manifest, warnings