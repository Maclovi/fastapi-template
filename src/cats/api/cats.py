from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status

from cats.di import CatServiceProvider
from cats.domain.models import Cat
from cats.domain.services import CatService

logger = getLogger(__name__)
cats_router = APIRouter(prefix="/cats", tags=["Cats"])


@cats_router.get("/all", response_model=list[Cat])
async def get_all(
    service: CatService = Depends(CatServiceProvider),
) -> list[Cat]:
    logger.info("Getting all cats")
    results: list[Cat] = await service.get_all()
    return results


@cats_router.get("/breed/{breed}", response_model=list[Cat])
async def get_by_breed(
    breed: str, service: CatService = Depends(CatServiceProvider)
) -> list[Cat]:
    logger.info(f"Getting cats with breed: {breed}")

    results: list[Cat] = await service.get_by_breed(breed)
    return results


@cats_router.get("/id/{id}", response_model=Cat)
async def get_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> Cat:
    logger.info(f"Getting cat with id: {id}")

    result = await service.get_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="cat not found")
    return result


@cats_router.post(
    "/add", response_model=Cat, status_code=status.HTTP_201_CREATED
)
async def add(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Adding cat: {cat}")

    await service.add(cat)
    return {"message": "cat added"}


@cats_router.put("/update")
async def update(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")

    await service.update(cat)
    return {"message": "cat updated"}


@cats_router.delete("/delete/{id}")
async def delete_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")

    await service.delete_by_id(id)
    return {"message": "cat deleted"}
