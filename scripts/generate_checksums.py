from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


def sha256_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate_checksums(input_dir: Path) -> int:
    print(f"\n{'='*60}")
    print(f"  Generating checksums in: {input_dir}")
    print(f"{'='*60}\n")

    zip_files = sorted(input_dir.glob("*.zip"))
    if not zip_files:
        print("[WARN]  No .zip files found in the input directory.")
        return 0

    written = 0
    for file_path in zip_files:
        checksum = sha256_file(file_path)
        checksum_path = file_path.with_suffix(file_path.suffix + ".sha256")
        checksum_path.write_text(f"{checksum}  {file_path.name}\n", encoding="utf-8")
        print(f"[OK]    {checksum_path.name}")
        print(f"        sha256: {checksum}")
        written += 1

    # Write a combined checksums manifest
    combined_path = input_dir / "checksums.sha256"
    lines = []
    for file_path in zip_files:
        checksum = sha256_file(file_path)
        lines.append(f"{checksum}  {file_path.name}")
    combined_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[OK]    Combined manifest → {combined_path.name}")
    print(f"\n[INFO]  {written} checksum file(s) written.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SHA256 checksums for packaged mod archives")
    parser.add_argument("--input", required=True, help="Directory containing .zip files")
    args = parser.parse_args()
    sys.exit(generate_checksums(Path(args.input)))
