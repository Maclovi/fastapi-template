from dataclasses import dataclass
from typing import NewType

from cats.entities.breed.value_objects import BreedName
from cats.entities.common.base_entity import BaseEntity

BreedID = NewType("BreedID", int)


@dataclass
class Breed(BaseEntity[BreedID]):
    name: BreedName
