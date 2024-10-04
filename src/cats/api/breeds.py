from logging import getLogger

from fastapi import APIRouter, Depends

from cats.di import BreedServiceProvider
from cats.domain.models import Breed
from cats.domain.services import BreedService

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"])


@router.get("/all", response_model=list[Breed])
async def get_all_breeds(
    service: BreedService = Depends(BreedServiceProvider),
) -> list[Breed]:
    logger.info("Getting all breeds")

    results: list[Breed] = await service.get_all()
    return results
