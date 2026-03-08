
# UniversalModLoader

![CI](https://github.com/Scaramuccci/universal-mod-pipeline/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/Scaramuccci/universal-mod-pipeline)
![Downloads](https://img.shields.io/github/downloads/Scaramuccci/universal-mod-pipeline/total)
![License](https://img.shields.io/github/license/Scaramuccci/universal-mod-pipeline)

A DevOps‑driven pipeline for validating, packaging, and releasing game mods automatically.

UniversalModLoader demonstrates how CI/CD principles can be applied to game mod development.  
It provides automated validation, reproducible builds, artifact checksums, and release management using GitHub Actions.

---

# Pipeline Overview

```
Push to main / open PR
        │
        ▼
┌──────────────────────────┐
│       Validate Mod       │
│ structure + manifest     │
│ schema + entry script    │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│       Package Mod        │
│ versioned archive (.zip) │
│ + build-info.json        │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Generate Checksums   │
│ per-file .sha256         │
│ + combined manifest      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│      Upload Artifacts    │
│ stored in GitHub Actions │
│ for 30 days              │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│      GitHub Release      │
│ .zip + checksums + build │
│ metadata attached        │
└──────────────────────────┘
```

---

# Why I built it

Most modding workflows are still very manual. Usually you zip the files locally, upload them somewhere, and hope nothing was missed.

UniversalModLoader treats a mod more like a normal software artifact.  
The pipeline validates the structure, packages it in a consistent way, generates checksums, and publishes the release automatically.

The goal is to bring a bit of DevOps workflow thinking into modding projects.

---

# Repository Structure

```
universal-mod-pipeline/
│
├─ .github/workflows/
│  └─ release.yml
│
├─ docker/
│  └─ Dockerfile
│
├─ mods/
│  └─ UniversalModLoader/
│     ├─ manifest.json
│     ├─ assets/
│     └─ scripts/
│        └─ init.lua
│
├─ scripts/
│  ├─ validate_mod.py
│  ├─ package_mod.py
│  └─ generate_checksums.py
│
├─ Makefile
├─ requirements.txt
└─ .gitignore
```

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
```

| Field | Required | Notes |
|------|------|------|
| name | Yes | Used when generating the archive |
| version | Yes | Must follow MAJOR.MINOR.PATCH |
| game | Yes | Target game identifier |
| author | Yes | Display name |
| entry_script | Yes | Relative path to entry script |
| description | Optional | Recommended |
| tags | Optional | Metadata |
| homepage | Optional | Project link |

The validator checks that required fields exist and that the entry script referenced in the manifest actually exists.

---

# Local Usage

Install dependencies

```
pip install -r requirements.txt
```

Validate the mod

```
python scripts/validate_mod.py --mod-path mods/UniversalModLoader
```

Package the mod

```
python scripts/package_mod.py --mod-path mods/UniversalModLoader --output dist
```

Generate checksums

```
python scripts/generate_checksums.py --input dist
```

Run the full pipeline locally

```
make all
```

---

# Docker

A Docker environment is included so the pipeline can run in a reproducible build environment.

```
make docker-build
make docker-run
```

Manual run

```
docker run --rm -v $(pwd):/app game-mod-ci python scripts/validate_mod.py --mod-path mods/UniversalModLoader
```

---

# VR Modding Use Cases

This project isn't tied to any specific engine, but the workflow can be useful for VR modding communities where mods are usually distributed manually as zip files.

For example, in games like Pavlov VR or other Unreal Engine based titles, maps and gameplay mods usually contain scripts, assets, and configuration files.

A pipeline like this helps by:

• validating that required assets and scripts exist before release  
• packaging mods into consistent versioned archives  
• generating checksums so communities can verify downloads  
• automatically publishing releases when a version tag is pushed  

This does not replace engine‑specific mod kits, but it provides a structured way to build and distribute mod releases.

---

# Releasing

Push a version tag and the pipeline publishes a GitHub release automatically.

```
git tag v1.2.0
git push origin v1.2.0
```

The release will include

• UniversalModLoader-1.2.0.zip  
• UniversalModLoader-1.2.0.zip.sha256  
• UniversalModLoader-1.2.0.build-info.json  
• auto-generated release notes  

---

# Ideas for v2
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 30c340f (rewrite README with clean pipeline documentation)

• Multi‑mod repository support  
• Asset validation (images, audio, scripts)  
• Mod size comparison between releases  
• Discord webhook notifications on release  
• Simple dashboard for pipeline history  
<<<<<<< HEAD
=======

---

# License

MIT
>>>>>>> 30c340f (rewrite README with clean pipeline documentation)
