from logging import getLogger

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from cats.domain.exceptions.cat_exc import CatAlreadyExistError
from cats.domain.models import Cat
from cats.domain.services import CatService
from cats.domain.services.cat import CatInputData

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats")
async def get_all(service: FromDishka[CatService]) -> list[Cat]:
    logger.info("Getting all cats")
    return await service.get_all()


@router.get("/breed/{breed}", summary="Get cats by breed")
async def get_by_breed(
    breed: str,
    service: FromDishka[CatService],
) -> list[Cat]:
    results = await service.get_by_breed(breed)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cats not found by breed {breed}",
        )
    return results


@router.get("/{id}", summary="Get cat by id")
async def get_by_id(id: int, service: FromDishka[CatService]) -> Cat:
    result = await service.get_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return result


@router.post("/add", status_code=status.HTTP_201_CREATED, summary="Add cat")
async def add(
    data: CatInputData,
    service: FromDishka[CatService],
) -> dict[str, str]:
    try:
        cat_id = await service.add(data)
    except CatAlreadyExistError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cat already exists",
        ) from exc
    else:
        return {"message": f"cat added, {cat_id=}"}


@router.put("/update", summary="Update cat")
async def update(
    cat: CatInputData,
    service: FromDishka[CatService],
) -> dict[str, str]:
    await service.update(cat)
    return {"message": "cat updated"}


@router.delete("/delete/{id}", summary="Delete cat by id")
async def delete_by_id(
    id: int,
    service: FromDishka[CatService],
) -> dict[str, str]:
    await service.delete_by_id(id)
    return {"message": "Cat deleted"}
