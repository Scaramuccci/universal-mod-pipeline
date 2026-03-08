PYTHON    := python
MOD_PATH  := mods/example_mod
DIST      := dist

.PHONY: install validate package checksums all clean docker-build docker-run

install:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_mod.py --mod-path $(MOD_PATH)

package:
	$(PYTHON) scripts/package_mod.py --mod-path $(MOD_PATH) --output $(DIST)

checksums:
	$(PYTHON) scripts/generate_checksums.py --input $(DIST)

all: validate package checksums

clean:
	rm -rf $(DIST) __pycache__ **/__pycache__ *.pyc **/*.pyc

docker-build:
	docker build -t game-mod-ci -f docker/Dockerfile .

docker-run:
	docker run --rm -v $$(pwd):/app game-mod-ci python scripts/validate_mod.py --mod-path mods/example_mod
