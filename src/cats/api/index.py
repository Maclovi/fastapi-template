from typing import Any

from fastapi import APIRouter, Request

index_router = APIRouter(tags=["Main"])


@index_router.get("/")
def index(_: Request) -> dict[Any, Any]:
    return {"message": "Hello there! Welcome to cats API"}
