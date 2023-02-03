.DEFAULT_GOAL := check
isort = isort src tests
black = black src tests
mypy = mypy --install-types --non-interactive src

.PHONY: install-pip
install-pip:
	@echo "Install pip"
	pip install -U pip


.PHONY: install-deps
install-deps:
	@echo "Install dependencies"
	pip install -U -r requirements.txt

.PHONY: install-package
install-package:
	@echo "Install package"
	pip install -e .

.PHONY: install-package-with-extra
install-package-with-extra:
	@echo "Install package with extra dependencies"
	pip install -e .[pydantic,marshmallow,trafaret]

.PHONY: install
install: install-pip install-deps install-package-with-extra

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
	pytest -vvs --cov=piny tests

.PHONY: testcov
testcov: test
	@echo "Build coverage html"
	@coverage html

.PHONY: mypy
mypy:
	@echo "Run mypy static analysis"
	$(mypy)


.PHONY: check
check: lint test mypy


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
	pip install -U -r docs/requirements.txt
	make -C docs html
