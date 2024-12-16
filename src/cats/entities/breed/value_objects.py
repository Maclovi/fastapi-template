from dataclasses import dataclass, field

from cats.entities.breed.errors import TitlelengthError


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedTitle:
    value: str

    MAX_LENGTH: int = field(init=False, default=50)

    def __post_init__(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise TitlelengthError(self.MAX_LENGTH)
