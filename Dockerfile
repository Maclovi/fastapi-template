FROM python:3.12.6-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install --no-cache --system .

COPY src/ .

RUN pip install uv && uv pip install --no-cache --system -e .
