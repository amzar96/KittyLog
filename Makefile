.PHONY: install run migrate migration test lint build

install:
	uv sync

run:
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	uv run alembic upgrade head

migration:
	uv run alembic revision --autogenerate -m "$(msg)"

test:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	uv run ruff check src/ tests/

build:
	docker build -t kittylog:latest .
