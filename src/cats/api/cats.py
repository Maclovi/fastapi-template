from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status

from cats.di import CatServiceProvider
from cats.domain.models import Cat
from cats.domain.services import CatService

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"])


@router.get("/all", response_model=list[Cat], summary="Get all cats")
async def get_all(
    service: CatService = Depends(CatServiceProvider),
) -> list[Cat]:
    logger.info("Getting all cats")
    results: list[Cat] = await service.get_all()
    return results


@router.get(
    "/breed/{breed}", response_model=list[Cat], summary="Get cats by breed"
)
async def get_by_breed(
    breed: str, service: CatService = Depends(CatServiceProvider)
) -> list[Cat]:
    logger.info(f"Getting cats with breed: {breed}")

    results: list[Cat] = await service.get_by_breed(breed)
    return results


@router.get("/{id}", response_model=Cat, summary="Get cat by id")
async def get_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> Cat:
    logger.info(f"Getting cat with id: {id}")

    result = await service.get_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="cat not found")
    return result


@router.post("/add", status_code=status.HTTP_201_CREATED, summary="Add cat")
async def add(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Adding cat: {cat}")

    await service.add(cat)
    return {"message": "cat added"}


@router.put("/update", summary="Update cat")
async def update(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")

    await service.update(cat)
    return {"message": "cat updated"}


@router.delete("/{id}/delete", summary="Delete cat by id")
async def delete_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")

    await service.delete_by_id(id)
    return {"message": "cat deleted"}
