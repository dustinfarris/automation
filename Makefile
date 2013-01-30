VERSION = 0.1

test: lint

develop:
	pip install "flake8>=1.7" --use-mirrors

lint: lint-python

lint-python:
	@echo "Linting Python files"
	flake8 --ignore=E121,W404 --exclude=.git . || exit 1
	@echo ""
