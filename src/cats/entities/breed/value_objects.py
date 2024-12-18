from dataclasses import dataclass, field

from cats.entities.breed.errors import TitlelengthError


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedName:
    value: str

    MIN_LENGTH: int = field(init=False, default=2)
    MAX_LENGTH: int = field(init=False, default=50)

    def __post_init__(self) -> None:
        if not (self.MIN_LENGTH <= len(self.value) <= self.MAX_LENGTH):
            raise TitlelengthError(self.MAX_LENGTH)
