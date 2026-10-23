.PHONY: setup test lint audit docs ci

setup:
	@echo "No setup required for hardware documentation baseline."

test:
	python3 scripts/verify_repo.py
	python3 -m unittest discover -s tests

lint:
	python3 scripts/verify_repo.py
	python3 -m compileall -q scripts tests

audit:
	python3 scripts/verify_repo.py
	python3 scripts/validate_hardware.py

docs:
	python3 scripts/verify_repo.py
	python3 scripts/validate_hardware.py

ci: setup test lint audit docs

# New compile-only regression; the original documentation CI above is unchanged.
S3_BOD_WORK_DIR ?= $(CURDIR)/.worktrees/s3-bod-run
S3_BOD_CACHE_DIR ?= $(CURDIR)/.worktrees/s3-bod-assets

.PHONY: s3-bod-test s3-bod-compile
s3-bod-test:
	python3 -m unittest discover -s diagnostics/s3-bod-selector/tools -p test_gate.py -v

s3-bod-compile: s3-bod-test
	python3 diagnostics/s3-bod-selector/tools/build_gate.py --mode full --work-dir "$(S3_BOD_WORK_DIR)" --cache-dir "$(S3_BOD_CACHE_DIR)"
