\# Universal Mod Pipeline



A general-purpose DevOps pipeline for validating, packaging, and releasing game mods. Engine-agnostic — works for Unreal, Unity, Lua-based mods, asset packs, and more.



\## Quick start

```bash

pip install -r requirements.txt

python -m pipeline.cli validate --mod-path examples/sample\_mod

python -m pipeline.cli package --mod-path examples/sample\_mod --output dist

python -m pipeline.cli report  --mod-path examples/sample\_mod --artifacts dist

pytest

```



\## Releasing

```bash

git tag v1.0.0

git push origin v1.0.0

```



See \[docs/architecture.md](docs/architecture.md) for how it's built.

