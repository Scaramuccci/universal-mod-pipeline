# Game Mod CI Pipeline

A DevOps project that brings proper CI/CD practices to game modding — automated validation, reproducible packaging, checksum generation, and GitHub Release publishing.

## What it does

```
Push to main / open PR
        │
        ▼
┌───────────────────┐
│  Validate mod     │  ← structure, manifest schema, entry script
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Package mod      │  ← versioned .zip + build-info.json
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Generate         │  ← per-file .sha256 + combined checksums.sha256
│  checksums        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Upload artifacts │  ← stored in GitHub Actions for 30 days
└────────┬──────────┘
         │ (tag push only)
         ▼
┌───────────────────┐
│  GitHub Release   │  ← .zip, .sha256, .build-info.json attached
└───────────────────┘
```

## Why I built it

Most modding workflows are entirely manual — zip it up yourself, upload by hand, hope you didn't forget anything. This project treats a game mod like any other software artifact: validated, versioned, checksummed, and released through a repeatable automated pipeline.

## Repo structure

```
game-mod-ci-pipeline/
├── .github/workflows/
│   └── release.yml          # Full CI/CD pipeline
├── docker/
│   └── Dockerfile           # Reproducible build environment
├── mods/
│   └── UniversalModLoader/
│       ├── manifest.json    # Mod metadata (validated by schema)
│       ├── assets/
│       └── scripts/
│           └── init.lua
├── scripts/
│   ├── validate_mod.py      # Structure + schema validation
│   ├── package_mod.py       # Zip packaging + build-info sidecar
│   └── generate_checksums.py# SHA256 per file + combined manifest
├── Makefile
├── requirements.txt
└── .gitignore
```

## Manifest format

```json
{
  "name": "your_mod",
  "version": "1.0.0",
  "game": "target-game",
  "author": "Your Name",
  "entry_script": "scripts/init.lua",
  "description": "Optional but recommended.",
  "tags": ["optional"],
  "homepage": "https://optional.link"
}
```

| Field          | Required | Notes                              |
|----------------|----------|------------------------------------|
| `name`         | ✅       | Alphanumeric, used in archive name |
| `version`      | ✅       | Must be `MAJOR.MINOR.PATCH`        |
| `game`         | ✅       | Target game identifier             |
| `author`       | ✅       | Display name                       |
| `entry_script` | ✅       | Relative path; must exist on disk  |
| `description`  | ⚠️       | Optional, warned if missing        |
| `tags`         | ⚠️       | Optional, warned if missing        |
| `homepage`     | ⚠️       | Optional, warned if missing        |

## Local usage

```bash
# Install dependencies
pip install -r requirements.txt

# Validate
python scripts/validate_mod.py --mod-path mods/UniversalModLoader

# Package
python scripts/package_mod.py --mod-path mods/UniversalModLoader --output dist

# Checksums
python scripts/generate_checksums.py --input dist

# Or run everything at once
make all
```

## Docker

```bash
make docker-build
make docker-run
# or manually:
docker run --rm -v $(pwd):/app game-mod-ci \
  python scripts/validate_mod.py --mod-path mods/UniversalModLoader
```

## Releasing

Push a version tag and the pipeline publishes a GitHub Release automatically:

```bash
git tag v1.2.0
git push origin v1.2.0
```

The release will include:
- `UniversalModLoader-1.2.0.zip` — the packaged mod
- `UniversalModLoader-1.2.0.zip.sha256` — SHA256 checksum
- `UniversalModLoader-1.2.0.build-info.json` — build metadata (timestamp, file count, size)
- Auto-generated release notes from commit history

## Ideas for v2

- Multi-mod monorepo support (validate/package each mod independently)
- Asset type validation (image dimensions, audio format, script syntax)
- Mod size diff reports between releases
- Discord webhook notifications on release
- Web dashboard for pipeline history

## License

MIT
