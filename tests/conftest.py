import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cats.api import breeds, cats, index


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    app = FastAPI()
    app.include_router(index.index_router)
    app.include_router(cats.cats_router)
    app.include_router(breeds.breeds_router)

    return TestClient(app)
