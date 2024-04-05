# Makefile

COMPOSE_FILE = docker-compose.yml

clean-pycache:
	find . -name *.pyc -type f -delete

build:
	docker-compose -f $(COMPOSE_FILE) build

run:
	docker-compose -f $(COMPOSE_FILE) up --build

test:
	docker-compose -f $(COMPOSE_FILE) run --build --rm dev bash -c "pytest -s"

test-shell:
	docker-compose -f $(COMPOSE_FILE) run --build --rm dev bash

test-watch:
	docker-compose -f $(COMPOSE_FILE) run --build --rm dev bash -c "ptw --poll"

mypy:
	poetry run mypy .

lint:
	poetry run flake8 .

format:
	poetry run black .
	poetry run isort .