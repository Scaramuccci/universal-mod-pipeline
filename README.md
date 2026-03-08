# Universal Mod Pipeline

A DevOps pipeline for validating, packaging, and releasing game mods automatically.

Universal Mod Pipeline provides a structured workflow for mod developers to validate mod structure, package assets, generate build artifacts, and publish releases through automated CI/CD pipelines.

The system is **engine-agnostic** and can be used for mods targeting:

- Unreal Engine
- Unity
- Source Engine
- Lua-based games
- VR titles
- Asset packs and map packs

The goal of this project is to bring **modern DevOps practices into game modding workflows**, where most modding projects are still manual.

---

# Features

- Automated mod validation
- Security checks for mod packages
- Manifest schema validation
- Automatic packaging into versioned ZIP archives
- SHA256 checksum generation
- Build metadata generation
- JSON and Markdown build reports
- GitHub Actions CI/CD integration
- Automated GitHub release publishing

---

# Project Structure

universal-mod-pipeline
│
├── .github/workflows
│ ├── ci.yml
│ └── release.yml
│
├── pipeline
│ ├── cli.py
│ ├── config.py
│ ├── manifest.py
│ ├── checks.py
│ ├── security.py
│ ├── packaging.py
│ └── reporting.py
│
├── examples
│ └── sample_mod
│ ├── manifest.json
│ ├── assets
│ └── scripts
│
├── tests
│
├── docs
│ └── architecture.md
│
├── requirements.txt
├── pyproject.toml
├── Makefile
└── README.md


---

# How the Pipeline Works


Push code
│
▼
GitHub Actions CI
│
├── Validate mod structure
├── Run security checks
├── Package mod into ZIP
├── Generate checksums
├── Generate build reports
└── Run tests


When a **release tag** is pushed:


git tag v0.1.0
git push origin v0.1.0


The release pipeline automatically:

- validates the mod
- packages the mod
- generates checksums
- generates build reports
- publishes a GitHub release with artifacts

---

# Requirements

- Python 3.12+
- Git
- GitHub repository (for CI/CD)

Install dependencies:

pip install -r requirements.txt


---

# Quick Start

Validate the example mod:

python -m pipeline.cli validate --mod-path examples/sample_mod


Package the mod:
python -m pipeline.cli package --mod-path examples/sample_mod --output dist


Generate build reports:
python -m pipeline.cli report --mod-path examples/sample_mod --artifacts dist


Run tests:
python -m pytest


---

# Example Mod Layout

Every mod should follow a standard structure:

my_mod/
│
├── manifest.json
├── assets/
└── scripts/


Example manifest:

{
"name": "sample_mod",
"version": "0.1.0",
"game": "generic",
"engine": "generic",
"author": "Your Name",
"entry_script": "scripts/init.lua",
"description": "Example mod package",
"tags": ["example"]
}


---

# CI/CD Integration

This repository includes two GitHub workflows.

## CI Workflow

Runs on every push and pull request.

Pipeline steps:

- validate mod
- package mod
- generate reports
- run tests
- upload build artifacts

## Release Workflow

Runs when a version tag is pushed.

Example:
git tag v0.1.0
git push origin v0.1.0


Artifacts published in the release:
sample_mod-0.1.0.zip
sample_mod-0.1.0.zip.sha256
sample_mod-0.1.0.build-info.json
build-report.json
build-report.md


---

# Security Checks

The pipeline includes safety checks to prevent malicious mod packages.

- blocks dangerous file types (`.exe`, `.dll`, `.bat`, `.ps1`)
- enforces maximum file size limits
- enforces maximum total package size
- validates entry scripts
- validates required mod directories

These checks help ensure safe and consistent mod releases.

---

# Testing

The project includes automated tests for:

- manifest validation
- packaging logic
- security checks
- checksum generation

Run tests locally:
python -m pytest


---

# Documentation

Additional technical documentation is available here:
docs/architecture.md


This document explains the internal pipeline design and module responsibilities.

---

# Roadmap

Future improvements planned:

- support multiple mods in one repository
- mod dependency validation
- mod signing and verification
- mod registry support
- containerized build environments
- plugin system for engine-specific pipelines

---

# License

This project is released under the MIT License.

---

# Author

Ibrahim Rahmani

DevOps engineer with a passion for games, modding, and automation tooling.

This project is a hobby effort to bring modern DevOps practices into the game modding ecosystem.

