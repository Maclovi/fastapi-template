from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status

from cats.adapters.schemes.catinput import CatInput
from cats.di import CatServiceProvider
from cats.domain.models import Cat
from cats.domain.services import CatService

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"])


@router.get("/", response_model=list[Cat], summary="Get all cats")
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
    if not results:
        raise HTTPException(status_code=404, detail="cats not found")
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
    cat: CatInput, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Adding cat: {cat}")

    try:
        await service.add(cat.to_model())
        return {"message": "cat added"}
    except Exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_409_CONFLICT, detail="cat already exists"
        )


@router.put("/update", summary="Update cat")
async def update(
    cat: CatInput, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")

    await service.update(cat.to_model())
    return {"message": "cat updated"}


@router.delete("/delete/{id}", summary="Delete cat by id")
async def delete_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")

    await service.delete_by_id(id)
    return {"message": "cat deleted"}
