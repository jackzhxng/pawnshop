# Makefile for Python project with Docker

# Variables
PYTHON := python3
PIP := pip
DOCKER_IMAGE := "pawnshop"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

venv:
	echo "Run source `.venv/bin/activate` to activate the virtual environment."

docker-build:
	$(DOCKER) build -t $(DOCKER_IMAGE) .

docker-run:
	$(DOCKER) run -dit -p 8080:8080 $(DOCKER_IMAGE)

