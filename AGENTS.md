# Repository Guidelines

## Project Structure & Module Organization

This repository contains a small FastAPI todo service. Application code lives in `app/`, tests in `tests/`, browser assets in `static/`, and deployment files in `.github/workflows/`, `k8s/`, and `argocd/`. Put cross-platform task entry points in `run.py`; keep equivalent Unix shortcuts in `Makefile`.

## Build, Test, and Development Commands

Create and activate a virtual environment before installing dependencies:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python run.py test
python run.py dev
```

`python run.py test` runs the complete automated suite. `python run.py dev` starts the API at `http://localhost:8000`, with OpenAPI docs at `/docs`. On macOS, Linux, and WSL2, `make test` and `make dev` are equivalent aliases.

## Coding Style & Naming Conventions

Use four spaces for Python indentation, type annotations for public functions, and short docstrings where behavior is not obvious. Name modules and functions with `snake_case`, classes with `PascalCase`, and constants with `UPPER_SNAKE_CASE`. Keep route handlers thin; place reusable validation and business logic in separate modules. Run the formatter and linter configured in the eventual development dependencies before submitting changes.

## Testing Guidelines

Use `pytest` conventions: files named `test_*.py`, test functions named `test_<behavior>`, and shared fixtures in `tests/conftest.py`. Cover success, validation, and failure paths for each endpoint. Every bug fix should include a regression test. Avoid tests that depend on network access or execution order.

## Commit & Pull Request Guidelines

No Git history is available yet, so use concise, imperative commit subjects such as `Add todo completion endpoint`. Keep commits scoped to one logical change. Pull requests should explain the motivation and behavior change, list verification commands, link relevant issues, and call out configuration or deployment impacts. Include screenshots for visible UI changes and example requests/responses for API changes.

## Security & Configuration

Never commit secrets, tokens, local virtual environments, or generated credentials. Read configuration from environment variables, provide safe example values in an `.env.example`, and keep real `.env` files ignored.
