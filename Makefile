# Environment variables
ENV_FILE = .env

# Python environment
VENV = venv
PYTHON = $(VENV)/bin/python

.PHONY: setup
setup: # Setup virtual environment
	python -m venv $(VENV)
	$(MAKE) install


.PHONY: install
install: # Install dependencies
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt


.PHONY: upgrade
upgrade: # Run the migrations
	flask db upgrade


.PHONY: generate-migration
generate-migration: ## Generate a new migration
	read -p "Enter migration message: " msg; \
	flask db migrate -m "$$msg"


.PHONY: rollback
rollback: ## Rollback migrations one level
	flask db downgrade


.PHONY: lint
lint: # Lint with ruff
	ruff check .


.PHONY: format 
format: # Format code with ruff
	ruff check . --fix


.PHONY: run 
run: # Run the app
	python3 main.py
