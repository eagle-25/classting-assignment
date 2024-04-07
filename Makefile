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

shell:
	docker-compose -f $(COMPOSE_FILE) run --build --rm dev bash

test-watch:
	docker-compose -f $(COMPOSE_FILE) run --build --rm dev bash -c "ptw --poll"

mypy:
	poetry run mypy .

black:
	poetry run black .

flake8:
	poetry run flake8 .

isort:
	poetry run isort .