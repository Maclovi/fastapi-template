from logging import getLogger

from fastapi import APIRouter, status

from cats.domain.models import Breed, Cat

logger = getLogger(__name__)
cats_router = APIRouter(prefix="/cats")


@cats_router.get("/all", response_model=list[Cat])
async def get_all() -> list[Cat]:
    return [
        Cat(color="red", age=5, description="cat1", breed=None),
        Cat(
            color="blue", age=10, description="cat2", breed=Breed(title="muy")
        ),
    ]


@cats_router.get("/breed/{breed}", response_model=list[Cat])
async def get_by_breed(breed: str) -> list[Cat]:
    return [
        Cat(color="red", age=5, description="cat1", breed=None),
        Cat(
            color="blue", age=10, description="cat2", breed=Breed(title="muy")
        ),
    ]


@cats_router.get("/id/{id}", response_model=Cat)
async def get_by_id(id: int) -> Cat:
    logger.info(f"Getting cat with id: {id}")
    return Cat(color="red", age=5, description="cat1", breed=None)


@cats_router.post(
    "/add", response_model=Cat, status_code=status.HTTP_201_CREATED
)
async def add(cat: Cat) -> None:
    logger.info(f"Adding cat: {cat}")


@cats_router.put("/update")
async def update(cat: Cat) -> dict[str, str]:
    logger.info(f"Updating cat: {cat}")
    return {"message": "cat updated"}


@cats_router.delete("/delete/{id}")
async def delete_by_id(id: int) -> dict[str, str]:
    logger.info(f"Deleting cat with id: {id}")
    return {"message": "cat deleted"}
