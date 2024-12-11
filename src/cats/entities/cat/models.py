from dataclasses import dataclass
from typing import NewType

from cats.domain.models.breed import BreedId
from cats.entities.cat.value_objects import Age, Color
from cats.entities.common.base_entity import BaseEntity

CatId = NewType("CatId", int)


@dataclass(kw_only=True)
class Cat(BaseEntity[CatId]):
    id: CatId | None
    breed_id: BreedId | None
    age: Age
    color: Color
    description: str
