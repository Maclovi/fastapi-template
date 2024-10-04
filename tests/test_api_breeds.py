from fastapi.testclient import TestClient


def test_all_breeds(client: TestClient) -> None:
    response = client.get("/breeds")
    assert response.status_code == 200
