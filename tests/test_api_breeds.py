from httpx import AsyncClient


async def test_all_breeds(client: AsyncClient) -> None:
    response = await client.get("/breeds/")
    assert response.status_code == 200
