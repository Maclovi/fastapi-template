from dataclasses import dataclass
from typing import Final

from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatColorLengthError,
    CatDescriptionLengthError,
)

MAX_AGE: Final = 99
COLOR_MIN_LENGTH: Final = 3
COLOR_MAX_LENGTH: Final = 50
DESCRIPTION_MAX_LENGTH: Final = 1000


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatAge:
    value: int

    def __post_init__(self) -> None:
        if self.value > MAX_AGE:
            raise CatAgeMaxError(self.value)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatColor:
    value: str

    def __post_init__(self) -> None:
        if not (COLOR_MIN_LENGTH <= len(self.value) <= COLOR_MAX_LENGTH):
            raise CatColorLengthError(COLOR_MAX_LENGTH)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatDescription:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) > DESCRIPTION_MAX_LENGTH:
            raise CatDescriptionLengthError(DESCRIPTION_MAX_LENGTH)

    def __str__(self) -> str:
        return self.value
