PYTHON ?= python
TEST_MODULES = $(shell find tests -name 'test_*.py' | sed 's|.py$$||; s|/|.|g')

install-deps:
	pip install -r dev_requirements.txt

test:
	PYTHONPATH=. $(PYTHON) -m unittest $(TEST_MODULES)
