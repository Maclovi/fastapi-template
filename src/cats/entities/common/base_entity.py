from dataclasses import dataclass
from typing import Generic, TypeVar

from cats.entities.common.errors import EntityError

OIDType = TypeVar("OIDType")


@dataclass
class BaseEntity(Generic[OIDType]):
    oid: OIDType | None

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)) or self.oid is None:
            raise EntityError

        return self.oid == other.oid
