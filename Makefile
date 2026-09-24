.PHONY: dev test lint format setup-hooks docker-up docker-down docker-logs

dev:
	python3 run.py dev

test:
	python3 run.py test

lint:
	python3 run.py lint

format:
	python3 run.py format

setup-hooks:
	python3 run.py setup-hooks

docker-up:
	python3 run.py docker-up

docker-down:
	python3 run.py docker-down

docker-logs:
	python3 run.py docker-logs
