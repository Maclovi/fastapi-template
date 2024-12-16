#!/bin/bash

export $(grep -v '^#' .env | xargs)
alembic upgrade head
uvicorn --factory cats.web:create_app --host $UVICORN_HOST --port $UVICORN_PORT
