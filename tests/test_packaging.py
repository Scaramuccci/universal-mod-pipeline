from pathlib import Path
from pipeline.manifest import load_manifest
from pipeline.packaging import package_mod, sha256_file, write_checksums


def test_package_creates_zip(tmp_path):
    mod_path = Path("examples/sample_mod")
    manifest = load_manifest(mod_path)
    archive_path, bundled_files = package_mod(mod_path, tmp_path, manifest)
    assert archive_path.exists()
    assert archive_path.suffix == ".zip"
    assert len(bundled_files) > 0


def test_build_info_sidecar(tmp_path):
    mod_path = Path("examples/sample_mod")
    manifest = load_manifest(mod_path)
    _, _ = package_mod(mod_path, tmp_path, manifest)
    build_info = tmp_path / f"{manifest.name}-{manifest.version}.build-info.json"
    assert build_info.exists()


def test_checksums_written(tmp_path):
    mod_path = Path("examples/sample_mod")
    manifest = load_manifest(mod_path)
    package_mod(mod_path, tmp_path, manifest)
    paths = write_checksums(tmp_path)
    names = [p.name for p in paths]
    assert any(n.endswith(".zip.sha256") for n in names)
    assert "checksums.sha256" in names


def test_sha256_deterministic(tmp_path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"hello world")
    assert sha256_file(f) == sha256_file(f)
    assert len(sha256_file(f)) == 64