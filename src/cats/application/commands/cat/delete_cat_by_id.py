from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatGateway
from cats.application.common.transaction import Transaction
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID
from cats.entities.cat.services import CatService


@dataclass(frozen=True, slots=True)
class DeleteCatCommand:
    id: int


class DeleteCatCommandHandler(Interactor[DeleteCatCommand, None]):
    def __init__(
        self,
        transaction: Transaction,
        cat_gateway: CatGateway,
        cat_service: CatService,
    ) -> None:
        self._transaction = transaction
        self._cat_gateway = cat_gateway
        self._cat_service = cat_service

    async def run(self, data: DeleteCatCommand) -> None:
        cat = await self._cat_gateway.with_id(CatID(data.id))
        assert validate_cat(cat, data.id)
        await self._transaction.commit()
