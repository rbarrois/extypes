PYTHON ?= python
TEST_MODULES = $(shell find tests -name 'test_*.py' | sed 's|.py$$||; s|/|.|g')

test:
	PYTHONPATH=. $(PYTHON) -m unittest $(TEST_MODULES)
