from cats.application.common.committer import Committer
from cats.application.common.interactor import Interactor


class AddCat(Interactor[None, None]):
    def __init__(self, committer: Committer) -> None:
        self._committer = committer
        super().__init__()

    async def run(self, data: None) -> None:
        pass
