from typing import Any

from fastapi import APIRouter, Request

router = APIRouter(tags=["Main"])


@router.get("/")
def index(_: Request) -> dict[Any, Any]:
    return {"message": "Hello there! Welcome to cats API"}
