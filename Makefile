# Makefile for dev workflow

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	flake8 .

format:
	black . && isort .

type-check:
	mypy agents.py app.py

test:
	pytest

run:
	streamlit run app.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache .coverage

all: install-dev lint format type-check test
