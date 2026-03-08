import json
from pathlib import Path
import pytest
from pipeline.checks import ValidationError, validate_mod
from pipeline.config import DEFAULT_POLICY


def test_validates_sample_mod():
    manifest, warnings = validate_mod(Path("examples/sample_mod"), DEFAULT_POLICY)
    assert manifest.name == "sample_mod"
    assert isinstance(warnings, list)


def test_missing_path(tmp_path):
    with pytest.raises(ValidationError, match="does not exist"):
        validate_mod(tmp_path / "nope", DEFAULT_POLICY)


def test_missing_assets_dir(tmp_path):
    (tmp_path / "manifest.json").write_text(json.dumps({
        "name": "m", "version": "1.0.0", "game": "g",
        "engine": "e", "author": "a", "entry_script": "scripts/init.lua",
    }), encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "init.lua").write_text("", encoding="utf-8")
    with pytest.raises(ValidationError, match="assets"):
        validate_mod(tmp_path, DEFAULT_POLICY)


def test_blocked_extension(tmp_path):
    (tmp_path / "manifest.json").write_text(json.dumps({
        "name": "m", "version": "1.0.0", "game": "g",
        "engine": "e", "author": "a", "entry_script": "scripts/init.lua",
    }), encoding="utf-8")
    (tmp_path / "assets").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "init.lua").write_text("", encoding="utf-8")
    (tmp_path / "assets" / "malware.exe").write_bytes(b"")
    with pytest.raises(ValidationError, match="blocked file type"):
        validate_mod(tmp_path, DEFAULT_POLICY)