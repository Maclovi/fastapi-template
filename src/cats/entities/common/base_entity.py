from typing import Generic, TypeVar

from cats.entities.common.errors import EntityError

OIDType = TypeVar("OIDType")


class BaseEntity(Generic[OIDType]):
    id: OIDType | None

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)) or self.id is None:
            raise EntityError

        return self.id == other.id
