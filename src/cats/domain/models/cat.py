from dataclasses import dataclass, field

from cats.domain.models.breed import Breed


@dataclass
class Cat:
    id: int
    color: str
    age: int
    description: str
    breed: Breed | None = field(default=None)
