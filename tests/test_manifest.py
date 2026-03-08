from pathlib import Path
import pytest
from pipeline.manifest import ManifestError, ModManifest, load_manifest


def test_manifest_loads_valid():
    manifest = load_manifest(Path("examples/sample_mod"))
    assert manifest.name == "sample_mod"
    assert manifest.version == "0.1.0"
    assert isinstance(manifest, ModManifest)


def test_manifest_missing_dir(tmp_path):
    with pytest.raises(ManifestError, match="manifest.json is missing"):
        load_manifest(tmp_path)


def test_manifest_bad_json(tmp_path):
    (tmp_path / "manifest.json").write_text("{invalid json", encoding="utf-8")
    with pytest.raises(ManifestError, match="not valid JSON"):
        load_manifest(tmp_path)


def test_manifest_missing_field(tmp_path):
    import json
    (tmp_path / "manifest.json").write_text(
        json.dumps({"name": "x", "version": "1.0.0", "game": "g"}),
        encoding="utf-8"
    )
    with pytest.raises(ManifestError, match="required field missing"):
        load_manifest(tmp_path)


def test_manifest_bad_semver(tmp_path):
    import json
    (tmp_path / "manifest.json").write_text(json.dumps({
        "name": "x", "version": "1.0", "game": "g",
        "engine": "e", "author": "a", "entry_script": "scripts/init.lua",
    }), encoding="utf-8")
    with pytest.raises(ManifestError, match="MAJOR.MINOR.PATCH"):
        load_manifest(tmp_path)