from logging import getLogger

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from cats.adapters.schemes.catinput import CatInput
from cats.domain.models import Cat
from cats.domain.services import CatService

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats")
async def get_all(service: FromDishka[CatService]) -> list[Cat]:
    logger.info("Getting all cats")
    results: list[Cat] = await service.get_all()
    return results


@router.get("/breed/{breed}", summary="Get cats by breed")
async def get_by_breed(
    breed: str, service: FromDishka[CatService]
) -> list[Cat]:
    logger.info(f"Getting cats with breed: {breed}")

    results: list[Cat] = await service.get_by_breed(breed)
    if not results:
        raise HTTPException(status_code=404, detail="cats not found")
    return results


@router.get("/{id}", summary="Get cat by id")
async def get_by_id(id: int, service: FromDishka[CatService]) -> Cat:
    logger.info(f"Getting cat with id: {id}")

    result = await service.get_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="cat not found")
    return result


@router.post("/add", status_code=status.HTTP_201_CREATED, summary="Add cat")
async def add(
    cat: CatInput, service: FromDishka[CatService]
) -> dict[str, str]:
    logger.info(f"Adding cat: {cat}")

    try:
        await service.add(cat.to_model())
        return {"message": "cat added"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="cat already exists"
        ) from e


@router.put("/update", summary="Update cat")
async def update(
    cat: CatInput, service: FromDishka[CatService]
) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")

    await service.update(cat.to_model())
    return {"message": "cat updated"}


@router.delete("/delete/{id}", summary="Delete cat by id")
async def delete_by_id(
    id: int, service: FromDishka[CatService]
) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")

    await service.delete_by_id(id)
    return {"message": "cat deleted"}
