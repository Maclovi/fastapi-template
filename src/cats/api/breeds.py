from logging import getLogger

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from cats.domain.models import Breed
from cats.domain.services import BreedService

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"], route_class=DishkaRoute)


@router.get("/")
async def get_all_breeds(service: FromDishka[BreedService]) -> list[Breed]:
    logger.info("Getting all breeds")

    results: list[Breed] = await service.get_all()
    return results
