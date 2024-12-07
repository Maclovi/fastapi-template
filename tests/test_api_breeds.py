from httpx import AsyncClient
from starlette import status


async def test_all_breeds(client: AsyncClient) -> None:
    response = await client.get("/breeds/")
    assert response.status_code == status.HTTP_200_OK
