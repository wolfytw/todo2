.PHONY: dev test lint format

dev:
	python3 run.py dev

test:
	python3 run.py test

lint:
	python3 run.py lint

format:
	python3 run.py format

