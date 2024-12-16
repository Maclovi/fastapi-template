from dataclasses import dataclass
from typing import NewType

from cats.entities.breed.value_objects import BreedTitle
from cats.entities.common.base_entity import BaseEntity

BreedId = NewType("BreedId", int)


@dataclass
class Breed(BaseEntity[BreedId]):
    id: BreedId | None
    title: BreedTitle
