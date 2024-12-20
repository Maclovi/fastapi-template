from logging import getLogger

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from cats.application.common.persistence.filters import Pagination
from cats.application.queries.breed.get_breeds import (
    GetBreedsQuery,
    GetBreedsQueryHandler,
)
from cats.entities.breed.models import Breed

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"], route_class=DishkaRoute)


@router.get("/")
async def get_all_breeds(
    interactor: FromDishka[GetBreedsQueryHandler],
    offset: int | None = None,
    limit: int | None = None,
) -> list[Breed]:
    return await interactor.run(GetBreedsQuery(Pagination(offset, limit)))
