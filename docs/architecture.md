\# Architecture



\## Module responsibilities



\- `config.py` — all rules in one place (blocked extensions, size limits, required dirs)

\- `manifest.py` — parses and validates manifest.json using stdlib only

\- `security.py` — blocks dangerous file types and enforces size limits

\- `checks.py` — top-level validation orchestrator

\- `packaging.py` — creates ZIP, writes build-info sidecar and checksums

\- `reporting.py` — writes JSON and Markdown build reports

\- `cli.py` — exposes validate / package / report subcommands



\## CI/CD flow

```

push / PR  →  ci.yml    →  validate + package + report + pytest

tag v\*     →  release.yml  →  same steps + GitHub Release upload

```

