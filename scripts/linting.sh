#!/bin/bash

ruff check src
mypy src
bandit -c pyproject.toml -r cats
semgrep scan --config auto --error
codespell
