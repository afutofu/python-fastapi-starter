from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


# Test todo routes with authentication
def test_todo_routes():

    # Create a new todo
    response = client.post(
        "/todos",
        json={"text": "Buy milk", "completed": False},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "text": "Buy milk",
        "completed": False,
    }

    # Get all todos
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get a specific todo by id
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "text": "Buy milk",
        "completed": False,
    }

    # Update a todo
    response = client.put(
        "/todos/1",
        json={"id": 1, "text": "Buy bread", "completed": True},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "Buy bread", "completed": True}

    # Delete a todo
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted"}

    # Check if the todo is deleted
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
