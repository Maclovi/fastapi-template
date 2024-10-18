from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from cats.domain.protocols import UoWProtocol

if TYPE_CHECKING:
    from dishka import AsyncContainer


@pytest.mark.container
@pytest.mark.asyncio
async def test_container(container: "AsyncContainer") -> None:
    async with container() as c_request:
        assert await c_request.get(AsyncEngine) is not None
        assert await c_request.get(UoWProtocol) is await c_request.get(
            AsyncSession
        ), "AsyncSession and UoWProtocol should be same instances"
