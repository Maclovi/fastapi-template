from dataclasses import dataclass, field
from typing import NewType

from cats.domain.models.breed import BreedId

CatId = NewType("CatId", int)


@dataclass
class Cat:
    id: CatId
    color: str
    age: int
    description: str
    breed_id: BreedId | None = field(default=None)
