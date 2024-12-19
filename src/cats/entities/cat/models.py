from dataclasses import dataclass
from typing import NewType

from cats.entities.breed.models import BreedID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.base_entity import BaseEntity

CatID = NewType("CatID", int)


@dataclass
class Cat(BaseEntity[CatID]):
    breed_id: BreedID | None
    age: CatAge
    color: CatColor
    description: CatDescription
