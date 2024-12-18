from typing import TypeGuard

from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import Cat


def validate_cat(cat: Cat | None, id: int) -> TypeGuard[Cat]:
    if cat is None:
        raise CatNotFoundError(id)
    return True
