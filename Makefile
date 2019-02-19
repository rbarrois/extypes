PACKAGE := extypes
TESTS_DIR := tests

PYTHON ?= python
TEST_MODULES = $(shell find $(TESTS_DIR) -name 'test_*.py' | sed 's|.py$$||; s|/|.|g')

default:

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	find . -type d -empty -delete

update:
	pip install --upgrade pip setuptools
	pip install -r requirements_dev.txt
	pip freeze

release:
	fullrelease

.PHONY: default clean update release

test:
	PYTHONPATH=. $(PYTHON) -m unittest $(TEST_MODULES)

.PHONY: test

lint: flake8 isort check-manifest

flake8:
	flake8 --config .flake8 $(PACKAGE) $(TESTS_DIR)

isort:
	isort $(PACKAGE) $(TESTS_DIR) --recursive --check-only --diff --project $(PACKAGE) --project $(TESTS_DIR)

check-manifest:
	check-manifest

.PHONY: isort lint flake8 checl-manifest
