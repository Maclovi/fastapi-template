from logging import getLogger

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from cats.application.queries.breed.get_breeds import (
    GetBreedsQuery,
    GetBreedsQueryHandler,
)
from cats.entities.breed.models import Breed

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"], route_class=DishkaRoute)


@router.get("/")
async def get_all_breeds(
    query_data: GetBreedsQuery,
    interactor: FromDishka[GetBreedsQueryHandler],
) -> list[Breed]:
    return await interactor.run(query_data)
