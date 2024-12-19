from fastapi import APIRouter, Request

router = APIRouter(tags=["Main"])


@router.get("/")
def index(_: Request) -> dict[str, str]:
    return {"message": "Hello there! Welcome to cats API"}
