from cats.domain.models import Breed
from cats.domain.protocols import BreedRepositoryProtocol, UoWProtocol


class BreedService:
    """
    Breed service. The service layer is responsible for the business logic.
    """

    def __init__(
        self, repository: BreedRepositoryProtocol, uow: UoWProtocol,
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def get_all(self) -> list[Breed]:
        return await self._repository.get_all()
