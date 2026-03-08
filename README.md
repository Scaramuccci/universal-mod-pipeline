# UniversalModLoader

![CI](https://github.com/Scaramuccci/universal-mod-pipeline/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/Scaramuccci/universal-mod-pipeline)
![Downloads](https://img.shields.io/github/downloads/Scaramuccci/universal-mod-pipeline/total)
![License](https://img.shields.io/github/license/Scaramuccci/universal-mod-pipeline)

A DevOps-driven pipeline for validating, packaging, and releasing game mods automatically.

UniversalModLoader demonstrates how CI/CD principles can be applied to game mod development.  
It provides automated validation, reproducible builds, artifact checksums, and release management using GitHub Actions.

---

# Pipeline Overview


Push to main / open PR
│
▼
┌───────────────────┐
│ Validate mod │ ← structure, manifest schema, entry script
└────────┬──────────┘
│
▼
┌───────────────────┐
│ Package mod │ ← versioned .zip + build-info.json
└────────┬──────────┘
│
▼
┌───────────────────┐
│ Generate │ ← per-file .sha256 + combined checksums.sha256
│ checksums │
└────────┬──────────┘
│
▼
┌───────────────────┐
│ Upload artifacts │ ← stored in GitHub Actions for 30 days
└────────┬──────────┘
│ (tag push only)
▼
┌───────────────────┐
│ GitHub Release │ ← .zip, .sha256, .build-info.json attached
└───────────────────┘


---

# Why I built it

Most modding workflows are still very manual. Usually you zip the files locally, upload them somewhere, and hope nothing was missed.

UniversalModLoader treats a mod more like a normal software artifact.  
The pipeline validates the structure, packages it in a consistent way, generates checksums, and publishes the release automatically.

The goal is to bring a bit of DevOps workflow thinking into modding projects.

---

# Repo structure


universal-mod-pipeline/
├── .github/workflows/
│ └── release.yml # CI/CD pipeline
├── docker/
│ └── Dockerfile # Reproducible build environment
├── mods/
│ └── UniversalModLoader/
│ ├── manifest.json # Mod metadata (validated by schema)
│ ├── assets/
│ └── scripts/
│ └── init.lua
├── scripts/
│ ├── validate_mod.py # Structure + schema validation
│ ├── package_mod.py # Zip packaging + build-info sidecar
│ └── generate_checksums.py# SHA256 per file + combined manifest
├── Makefile
├── requirements.txt
└── .gitignore


---

# Manifest format

Each mod includes a `manifest.json` file describing the mod metadata.

Example:

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
Field	Required	Notes
name	✅	Used when generating the archive
version	✅	Must follow MAJOR.MINOR.PATCH
game	✅	Target game identifier
author	✅	Display name
entry_script	✅	Relative path to entry script
description	⚠️	Optional but recommended
tags	⚠️	Optional
homepage	⚠️	Optional

The validator checks that required fields exist and that the entry script referenced in the manifest actually exists.

Local usage

Install dependencies:

pip install -r requirements.txt

Validate the mod:

python scripts/validate_mod.py --mod-path mods/UniversalModLoader

Package the mod:

python scripts/package_mod.py --mod-path mods/UniversalModLoader --output dist

Generate checksums:

python scripts/generate_checksums.py --input dist

Run everything at once:

make all
Docker

A Docker environment is included so the pipeline can run in a reproducible build environment.

make docker-build
make docker-run

Or manually:

docker run --rm -v $(pwd):/app game-mod-ci \
  python scripts/validate_mod.py --mod-path mods/UniversalModLoader
VR Modding Use Cases

While this project isn't tied to a specific game engine, the workflow is useful for VR modding communities where mods are usually distributed as zip archives.

For example, in games like Pavlov VR or other Unreal Engine based titles, maps and gameplay mods typically consist of a mixture of scripts, assets, and configuration files.

A pipeline like this can help by:

validating that a mod contains required files before release

packaging maps or mods into consistent versioned builds

generating checksums so communities can verify downloads

automatically publishing releases when a version tag is pushed

This doesn't replace engine-specific tooling like Unreal Engine mod kits, but it provides a structured way to build and distribute mod releases.

Releasing

Push a version tag and the pipeline publishes a GitHub Release automatically.

git tag v1.2.0
git push origin v1.2.0

The release will include:

UniversalModLoader-1.2.0.zip

UniversalModLoader-1.2.0.zip.sha256

UniversalModLoader-1.2.0.build-info.json

automatically generated release notes

Ideas for v2

Some things I may experiment with later:

Multi-mod monorepo support (build every mod automatically)

Asset validation (images, audio formats, scripts)

Mod size comparison between releases

Discord webhook notifications on releases

Simple dashboard for pipeline history
