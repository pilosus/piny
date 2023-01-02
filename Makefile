.DEFAULT_GOAL := check
isort = isort src tests
black = black src tests


.PHONY: install
install:
	@echo "Install package and its dependencies"
	pip install -U -r requirements.txt
	pip install -e .


.PHONY: format
format:
	@echo "Run code formatters"
	$(isort)
	$(black)


.PHONY: lint
lint:
	@echo "Run linters"
	$(isort) --check-only
	$(black) --check


.PHONY: test
test:
	@echo "Run tests"
	pytest -vvs --cov=src.piny tests

.PHONY: testcov
testcov: test
	@echo "Build coverage html"
	@coverage html

.PHONY: mypy
mypy:
	@echo "Run mypy static analysis"
	mypy --install-types --non-interactive piny

.PHONY: safety
safety:
	@echo "Run safety checker"
	safety check --full-report


.PHONY: check
check: lint test mypy safety


.PHONY: build
build:
	@echo "Build Python package"
	python -m build --sdist --wheel
	python -m twine check dist/*

.PHONY: push-test
push-test:
	@echo "Push package to test.pypi.org"
	python -m twine upload --verbose --repository testpypi dist/*


.PHONY: push
push:
	@echo "Run package to PyPI"
	python -m twine upload --verbose dist/*


.PHONY: clean
clean:
	@echo "Clean up files"
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist

.PHONY: docs
docs:
	make -C docs html
