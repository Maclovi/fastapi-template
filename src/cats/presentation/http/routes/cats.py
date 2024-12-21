from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, status

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
from cats.presentation.http.common.schemes import (
    CatsAllSchema,
    CatsWithBreedSchema,
    ExceptionSchema,
)

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats", status_code=status.HTTP_200_OK)
async def get_all(
    query: Annotated[CatsAllSchema, Query()],
    interactor: FromDishka[GetCatsQueryHandler],
) -> list[Cat]:
    dto = GetCatsQuery(
        CatFilters(query.breed_id, query.color),
        Pagination(query.offset, query.limit, query.order),
    )
    return await interactor.run(dto)


@router.get(
    "/breed/{breed}",
    summary="Get cats by breed",
    status_code=status.HTTP_200_OK,
)
async def get_by_breed(
    query: Annotated[CatsWithBreedSchema, Query()],
    intteractor: FromDishka[GetCatsWithBreedQueryHandler],
) -> list[Cat]:
    dto = GetCatsWithBreedQuery(
        query.breed,
        Pagination(query.offset, query.limit, query.order),
    )
    return await intteractor.run(dto)


@router.get(
    "/{id}",
    summary="Get cat by id",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"detail": ExceptionSchema}},
)
async def get_by_id(
    id: Annotated[int, Path()],
    interactor: FromDishka[GetCatWithIDQueryHandler],
) -> Cat:
    return await interactor.run(GetCatWithIDQuery(id))


@router.post("/add", summary="Add cat", status_code=status.HTTP_201_CREATED)
async def add(
    command_data: AddCatCommand,
    interactor: FromDishka[AddCatCommandHandler],
) -> int:
    return await interactor.run(command_data)


@router.patch(
    "/update_description/{cat_id}",
    summary="Update cat",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def update_description(
    command_data: UpdateCatDescriptionCommand,
    interactor: FromDishka[UpdateCatDescriptionCommandHandler],
) -> dict[str, str]:
    await interactor.run(command_data)
    return {"message": "cat updated"}


@router.delete(
    "/delete/{id}",
    summary="Delete cat by id",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def delete_by_id(
    command_data: DeleteCatCommand,
    interactor: FromDishka[DeleteCatCommandHandler],
) -> dict[str, str]:
    await interactor.run(command_data)
    return {"message": "Cat deleted"}
