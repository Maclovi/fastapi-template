import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cats.api import breeds, cats, index


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    app = FastAPI()
    app.include_router(index.router)
    app.include_router(cats.router)
    app.include_router(breeds.router)

    return TestClient(app)
