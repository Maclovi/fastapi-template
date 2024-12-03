#!/bin/bash

export POSTGRES_URI=postgresql+psycopg://postgres:postgres@localhost:5432/defaultdb   
alembic upgrade head
uvicorn --factory cats.web:create_app --host 0.0.0.0 --port 8000
