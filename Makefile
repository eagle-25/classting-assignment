# Makefile

COMPOSE_FILE = docker-compose.yml

clean-pycache:
	find . -name *.pyc -type f -delete

build:
	docker-compose -f $(COMPOSE_FILE) build

up:
	docker-compose -f $(COMPOSE_FILE) up --build app --remove-orphans

shell:
	docker-compose -f $(COMPOSE_FILE) run --build --rm app bash

test:
	docker-compose -f $(COMPOSE_FILE) run --build --rm test bash -c "pytest -s"

test-shell:
	docker-compose -f $(COMPOSE_FILE) run --build --rm test bash

test-watch:
	docker-compose -f $(COMPOSE_FILE) run --build --rm test bash -c "ptw --poll"

mypy:
	poetry run mypy .

black:
	poetry run black .

flake8:
	poetry run flake8 .

isort:
	poetry run isort .