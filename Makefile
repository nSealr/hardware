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
