from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_todo_lifecycle_and_stats(client: TestClient) -> None:
    created = client.post("/api/todos", json={"title": "Write tests"})
    assert created.status_code == 201
    todo_id = created.json()["id"]

    assert client.get("/stats").json() == {
        "total": 1,
        "completed": 0,
        "pending": 1,
    }

    updated = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True
    assert updated.json()["completed_at"] is not None
    assert client.get("/stats").json()["completed"] == 1

    assert client.delete(f"/api/todos/{todo_id}").status_code == 204
    assert client.get("/api/todos").json() == []


def test_missing_todo_returns_404(client: TestClient) -> None:
    assert client.get("/api/todos/999").status_code == 404
    assert client.patch("/api/todos/999", json={"completed": True}).status_code == 404
    assert client.delete("/api/todos/999").status_code == 404


def test_rejects_blank_title(client: TestClient) -> None:
    assert client.post("/api/todos", json={"title": ""}).status_code == 422
    assert client.post("/api/todos", json={"title": "   "}).status_code == 422


def test_normalizes_title(client: TestClient) -> None:
    response = client.post("/api/todos", json={"title": "  Buy milk  "})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy milk"


def test_clears_completion_date_when_reopened(client: TestClient) -> None:
    todo_id = client.post("/api/todos", json={"title": "Ship app"}).json()["id"]

    completed = client.patch(f"/api/todos/{todo_id}", json={"completed": True}).json()
    assert completed["completed_at"] is not None

    reopened = client.patch(f"/api/todos/{todo_id}", json={"completed": False}).json()
    assert reopened["completed"] is False
    assert reopened["completed_at"] is None
