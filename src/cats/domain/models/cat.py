from dataclasses import dataclass

from . import Breed


@dataclass
class Cat:
    id: int
    color: str
    age: int
    description: str
    breed: Breed | None
