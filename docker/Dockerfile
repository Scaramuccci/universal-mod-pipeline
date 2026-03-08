FROM python:3.12-slim

LABEL org.opencontainers.image.title="game-mod-ci" \
      org.opencontainers.image.description="CI build environment for game mod validation and packaging" \
      org.opencontainers.image.source="https://github.com/yourusername/game-mod-ci-pipeline"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: validate the example mod
CMD ["python", "scripts/validate_mod.py", "--mod-path", "mods/example_mod"]
