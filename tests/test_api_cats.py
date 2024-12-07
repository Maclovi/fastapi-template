from httpx import AsyncClient
from starlette import status


def _create_cat_payload(
    *,
    id: int = 24,
    color: str = "black",
    age: int = 2,
    description: str = "test",
    breed_title: str | None = "Abyssinian",
) -> dict[str, str | int | None]:
    return {
        "id": id,
        "color": color,
        "age": age,
        "description": description,
        "breed_title": breed_title,
    }


async def test_add_cat(client: AsyncClient) -> None:
    payload = _create_cat_payload()
    response = await client.post("/cats/add", json=payload)
    assert response.status_code == status.HTTP_201_CREATED


async def test_add_cat_conflict(client: AsyncClient) -> None:
    payload = _create_cat_payload()
    response = await client.post("/cats/add", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_all_cats(client: AsyncClient) -> None:
    response = await client.get("/cats/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["id"] == _create_cat_payload()["id"]


async def test_cat_by_id(client: AsyncClient) -> None:
    response = await client.get("/cats/24")
    assert response.status_code == status.HTTP_200_OK


async def test_cat_by_id_not_found(client: AsyncClient) -> None:
    response = await client.get("/cats/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_cat_by_breed(client: AsyncClient) -> None:
    response = await client.get("/cats/breed/Abyssinian")
    assert response.status_code == status.HTTP_200_OK


async def test_cat_by_breed_not_found(client: AsyncClient) -> None:
    response = await client.get("/cats/breed/Unknown")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_cat(client: AsyncClient) -> None:
    payload = _create_cat_payload(age=3, color="white")
    response = await client.put("/cats/update", json=payload)
    assert response.status_code == status.HTTP_200_OK


async def test_update_get_cat(client: AsyncClient) -> None:
    response = await client.get("/cats/24")
    cat = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert cat["color"] == "white"


async def test_delete_cat(client: AsyncClient) -> None:
    response = await client.delete("/cats/delete/24")
    assert response.status_code == status.HTTP_200_OK
