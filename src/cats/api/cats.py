from logging import getLogger

from fastapi import APIRouter, Depends, status

from cats.di import CatServiceProvider
from cats.domain.models import Breed, Cat
from cats.domain.services import CatService

logger = getLogger(__name__)
cats_router = APIRouter(prefix="/cats", tags=["Cats"])


@cats_router.get("/all", response_model=list[Cat])
async def get_all(
    service: CatService = Depends(CatServiceProvider),
) -> list[Cat]:
    logger.info("Getting all cats")

    return [Cat(id=1, color="red", age=5, description="cat1", breed=None)]


@cats_router.get("/breed/{breed}", response_model=list[Cat])
async def get_by_breed(breed: str) -> list[Cat]:
    logger.info(f"Getting cats with breed: {breed}")

    return [
        Cat(id=1, color="red", age=5, description="cat1", breed=None),
        Cat(
            id=2,
            color="blue",
            age=10,
            description="cat2",
            breed=Breed(id=1, title="muy"),
        ),
    ]


@cats_router.get("/id/{id}", response_model=Cat)
async def get_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> Cat:
    logger.info(f"Getting cat with id: {id}")

    return Cat(id=1, color="red", age=5, description="cat1", breed=None)


@cats_router.post(
    "/add", response_model=Cat, status_code=status.HTTP_201_CREATED
)
async def add(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> None:
    logger.info(f"Adding cat: {cat}")


@cats_router.put("/update")
async def update(
    cat: Cat, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")

    return {"message": "cat updated"}


@cats_router.delete("/delete/{id}")
async def delete_by_id(
    id: int, service: CatService = Depends(CatServiceProvider)
) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")

    return {"message": "cat deleted"}
