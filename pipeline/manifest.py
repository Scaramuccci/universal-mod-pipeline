from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

REQUIRED_FIELDS: dict[str, type] = {
    "name": str,
    "version": str,
    "game": str,
    "engine": str,
    "author": str,
    "entry_script": str,
}


class ManifestError(Exception):
    pass


@dataclass(slots=True)
class ModManifest:
    name: str
    version: str
    game: str
    engine: str
    author: str
    entry_script: str
    description: str = ""
    homepage: str = ""
    tags: list = None

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


def _validate_schema(data: dict) -> None:
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            raise ManifestError(f"required field missing: '{field}'")
        if not isinstance(data[field], expected_type):
            raise ManifestError(
                f"field '{field}' must be {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )
        if isinstance(data[field], str) and not data[field].strip():
            raise ManifestError(f"field '{field}' must not be empty")

    version = data.get("version", "")
    if not SEMVER_RE.match(version):
        raise ManifestError(
            f"'version' must follow MAJOR.MINOR.PATCH — got: '{version}'"
        )


def load_manifest(mod_path: Path) -> ModManifest:
    manifest_path = mod_path / "manifest.json"

    if not manifest_path.exists():
        raise ManifestError("manifest.json is missing")

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestError(f"manifest.json is not valid JSON: {exc}") from exc

    _validate_schema(data)

    return ModManifest(
        name=data["name"],
        version=data["version"],
        game=data["game"],
        engine=data["engine"],
        author=data["author"],
        entry_script=data["entry_script"],
        description=data.get("description", ""),
        homepage=data.get("homepage", ""),
        tags=data.get("tags", []),
    )