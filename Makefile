.PHONY: help start security install update lock generate_migrations migrate test lint

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
start:  # Start the virtual env
	poetry shell
build:  # Build the project
	python3 -m pip install --upgrade build && python3 -m build
upload_build:
	python3 -m twine upload --repository pypi dist/*
lint:  ## Run linting checks
	black --line-length 120 .
security: ## Run security checks
	bandit -r . -lll
install: ## Install the project libs
	poetry install
update: ## Update the project libs
	poetry update
lock: ## Lock the project libs
	poetry lock
generate_migrations: ## Generate database migrations
	cd tests/db && ./generate_migrations local
migrate: ## Apply database migrations
	cd tests/db && ./migrate local
test: ## Run the project tests
	poetry run python3 -m unittest discover tests "test_*.py"
tox: ## Run tox
	tox