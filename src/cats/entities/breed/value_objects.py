from dataclasses import dataclass
from typing import Final

from cats.entities.breed.errors import BreedNamelengthError

BREED_MIN_LENGTH: Final = 2
BREED_MAX_LENGTH: Final = 50


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedName:
    value: str

    def __post_init__(self) -> None:
        if not (BREED_MIN_LENGTH <= len(self.value) <= BREED_MAX_LENGTH):
            raise BreedNamelengthError(BREED_MAX_LENGTH)

    def __str__(self) -> str:
        return self.value
