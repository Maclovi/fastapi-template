from fastapi.testclient import TestClient


def test_add_cat(client: TestClient) -> None:
    payload = {
        "id": 24,
        "color": "black",
        "age": 2,
        "description": "test",
        "breed": "Abyssinian",
    }
    response = client.post("/cats/add", json=payload)
    assert response.status_code == 201


def test_add_cat_conflict(client: TestClient) -> None:
    payload = {
        "id": 24,
        "color": "black",
        "age": 2,
        "description": "test",
        "breed": "Abyssinian",
    }
    response = client.post("/cats/add", json=payload)
    assert response.status_code == 409


def test_all_cats(client: TestClient) -> None:
    response = client.get("/cats")
    assert response.status_code == 200


def test_cat_by_id(client: TestClient) -> None:
    response = client.get("/cats/24")
    assert response.status_code == 200


def test_cat_by_id_not_found(client: TestClient) -> None:
    response = client.get("/cats/100")
    assert response.status_code == 404


def test_cat_by_breed(client: TestClient) -> None:
    response = client.get("/cats/breed/Abyssinian")
    assert response.status_code == 200


def test_cat_by_breed_not_found(client: TestClient) -> None:
    response = client.get("/cats/breed/Unknown")
    assert response.status_code == 404


def test_update_cat(client: TestClient) -> None:
    payload = {
        "id": 24,
        "color": "white",
        "age": 3,
        "description": "test",
        "breed": "Abyssinian",
    }
    response = client.put("/cats/update", json=payload)
    assert response.status_code == 200


def test_update_get_cat(client: TestClient) -> None:
    response = client.get("/cats/24")
    cat = response.json()
    assert response.status_code == 200
    assert cat["color"] == "white"


def test_delete_cat(client: TestClient) -> None:
    response = client.delete("/cats/delete/24")
    assert response.status_code == 200
