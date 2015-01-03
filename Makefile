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

