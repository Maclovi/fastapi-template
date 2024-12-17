from typing import TypeGuard

from cats.application.common.errors.breed import BreedNotFoundWithTitleError
from cats.application.common.errors.cat import (
    CatIDNotFoundError,
    CatNotFoundError,
)
from cats.entities.breed.models import Breed
from cats.entities.cat.models import Cat, CatID


def validate_cat(cat: Cat | None, id: int) -> TypeGuard[Cat]:
    if cat is None:
        raise CatNotFoundError(id)
    return True


def validate_cat_id(id: CatID | None) -> TypeGuard[CatID]:
    if id is None:
        raise CatIDNotFoundError
    return True


def validate_breed_with_title(
    breed: Breed | None, title: str = ""
) -> TypeGuard[Breed]:
    if breed is None:
        raise BreedNotFoundWithTitleError(title)
    return True
