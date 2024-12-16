from dataclasses import dataclass
from typing import NewType

from cats.domain.models.breed import BreedId
from cats.entities.cat.value_objects import CatAge, CatColor
from cats.entities.common.base_entity import BaseEntity

CatId = NewType("CatId", int)


@dataclass(kw_only=True)
class Cat(BaseEntity[CatId]):
    id: CatId | None
    breed_id: BreedId | None
    age: CatAge
    color: CatColor
    description: str
