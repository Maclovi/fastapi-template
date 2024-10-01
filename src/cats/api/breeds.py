from fastapi import APIRouter

from cats.domain.models import Breed

breeds_router = APIRouter(prefix="/breeds")


@breeds_router.get("/all", response_model=list[Breed])
async def get_all_breeds() -> list[Breed]:
    return [Breed(title="muy"), Breed(title="muy2"), Breed(title="muy3")]
