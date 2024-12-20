from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from cats.application.commands.cat.add_cat import (
    AddCatCommand,
    AddCatCommandHandler,
)
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommand,
    DeleteCatCommandHandler,
)
from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommand,
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.persistence.cat import CatFilters
from cats.application.common.persistence.filters import Pagination
from cats.application.queries.cat.get_cat_by_id import (
    GetCatWithIDQuery,
    GetCatWithIDQueryHandler,
)
from cats.application.queries.cat.get_cats import (
    GetCatsQuery,
    GetCatsQueryHandler,
)
from cats.application.queries.cat.get_cats_by_breed import (
    GetCatsWithBreedQuery,
    GetCatsWithBreedQueryHandler,
)
from cats.entities.cat.models import Cat

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats")
async def get_all(
    interactor: FromDishka[GetCatsQueryHandler],
    filters: Annotated[CatFilters, Query()],
    pagination: Annotated[Pagination, Query()],
) -> list[Cat]:
    return await interactor.run(GetCatsQuery(filters, pagination))


@router.get("/breed/{breed}", summary="Get cats by breed")
async def get_by_breed(
    query_data: GetCatsWithBreedQuery,
    intteractor: FromDishka[GetCatsWithBreedQueryHandler],
) -> list[Cat]:
    return await intteractor.run(query_data)


@router.get("/{id}", summary="Get cat by id")
async def get_by_id(
    query_data: GetCatWithIDQuery,
    interactor: FromDishka[GetCatWithIDQueryHandler],
) -> Cat:
    return await interactor.run(query_data)


@router.post("/add", summary="Add cat")
async def add(
    command_data: AddCatCommand,
    interactor: FromDishka[AddCatCommandHandler],
) -> int:
    return await interactor.run(command_data)


@router.put("/update_description/{cat_id}", summary="Update cat")
async def update_description(
    command_data: UpdateCatDescriptionCommand,
    interactor: FromDishka[UpdateCatDescriptionCommandHandler],
) -> dict[str, str]:
    await interactor.run(command_data)
    return {"message": "cat updated"}


@router.delete("/delete/{id}", summary="Delete cat by id")
async def delete_by_id(
    command_data: DeleteCatCommand,
    interactor: FromDishka[DeleteCatCommandHandler],
) -> dict[str, str]:
    await interactor.run(command_data)
    return {"message": "Cat deleted"}
