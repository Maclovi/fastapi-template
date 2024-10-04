FROM python:3.12.6-slim

WORKDIR /app

COPY . .

RUN pip install uv && uv pip install --no-cache --system -e .
