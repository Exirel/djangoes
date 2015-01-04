# Djangoes project tasks
# ======================

.PHONY: pylint report test all

test:
	coverage run $(VIRTUAL_ENV)/bin/py.test tests

report: pylint
	coverage html

pylint:
	pylint djangoes > pylint.html || exit 0

all: test report


# Documentation
# =============

.PHONY: doc

clean_doc:
	$(MAKE) -C docs clean

build_doc:
	$(MAKE) -C docs html

doc: clean_doc build_doc

