from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import CatReader
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import Cat, CatID


class GetCatWithIDCommandHandler(Interactor[int, Cat]):
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader = cat_reader

    async def run(self, data: int) -> Cat:
        cat = await self._cat_reader.with_id(CatID(data))
        assert validate_cat(cat, data)
        return cat
