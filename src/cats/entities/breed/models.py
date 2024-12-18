from dataclasses import dataclass
from typing import NewType

from cats.entities.breed.value_objects import BreedName
from cats.entities.common.base_entity import BaseEntity

BreedID = NewType("BreedID", int)


@dataclass(kw_only=True)
class Breed(BaseEntity[BreedID]):
    id: BreedID | None
    name: BreedName
