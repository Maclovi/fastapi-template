from pydantic import BaseModel

from cats.application.common.persistence.filters import SortOrder


class ExceptionSchema(BaseModel):
    detail: str


class PaginationSchema(BaseModel):
    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


class CatFiltersSchema(BaseModel):
    breed_id: int | None = None
    color: str | None = None


class CatsAllSchema(PaginationSchema, CatFiltersSchema):
    pass


class BreedSchema(BaseModel):
    breed: str


class CatsWithBreedSchema(BreedSchema, PaginationSchema):
    pass
