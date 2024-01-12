.DEFAULT_GOAL := all
DIRS = src/
pdm = pdm run
isort = isort
black = black
mypy = mypy
flake8  = flake8
pyupgrade = pyupgrade --py311-plus


.PHONY: install-linting
install-linting:
	pdm add ruff -G dev

.PHONY: format
format:
	ruff $(DIRS)
	mypy $(DIRS)

.PHONY: export-dependencies
export-dependencies:
	pdm export -f requirements -o requirements.txt
	pdm export -f requirements -o requirements-dev.txt -G dev

.PHONY: database
database:
	docker compose up database -d

.PHONY: test
test:
	pdm run pytest --cov=app --cov-report=html

.PHONY: migrate
migrate:
	@read -p "Enter migration message: " message; \
	pdm run alembic revision --autogenerate -m "$$message"

.PHONY: downgrade
downgrade:
	alembic downgrade -1

.PHONY: upgrade
upgrade:
	alembic upgrade +1

.PHONY: upgrade-offline
upgrade-offline:
	alembic upgrade head --sql

.PHONY: all
all: format export-dependencies
