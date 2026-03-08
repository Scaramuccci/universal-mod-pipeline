PYTHON   = python
MOD_PATH = examplessample_mod
DIST     = dist

.PHONY install validate package report test all clean

install
	$(PYTHON) -m pip install -r requirements.txt

validate
	$(PYTHON) -m pipeline.cli validate --mod-path $(MOD_PATH)

package
	$(PYTHON) -m pipeline.cli package --mod-path $(MOD_PATH) --output $(DIST)

report
	$(PYTHON) -m pipeline.cli report --mod-path $(MOD_PATH) --artifacts $(DIST)

test
	pytest

all validate package report

clean
	rm -rf $(DIST) reports __pycache__ .pytest_cache