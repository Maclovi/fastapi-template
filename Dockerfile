FROM python:3.12.6-slim

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
RUN pip install uv && uv pip install --no-cache --system -r pyproject.toml

COPY alembic.ini ./src ./
