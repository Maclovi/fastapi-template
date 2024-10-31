from dataclasses import dataclass, field
from typing import NewType

BreedId = NewType("BreedId", int)


@dataclass
class Breed:
    title: str
    id: BreedId | None = field(default=None)
