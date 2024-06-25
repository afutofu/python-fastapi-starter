from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


# Helper function to create a user and get a token
def create_user_and_get_token(username: str, password: str):
    response = client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


# Test registration and login
def test_register_and_login():
    response = client.post(
        "/auth/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test registration with existing username
def test_register_existing_user():
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/auth/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


# Test todo routes with authentication
def test_todo_routes():

    token = create_user_and_get_token("testuser1", "testpass1")

    headers = {"Authorization": f"Bearer {token}"}

    # Create a new todo
    response = client.post(
        "/todos",
        json={"text": "Buy milk", "completed": False},
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "text": "Buy milk",
        "completed": False,
    }

    # Get all todos
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Get a specific todo by id
    response = client.get("/todos/1", headers=headers)
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
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "Buy bread", "completed": True}

    # Delete a todo
    response = client.delete("/todos/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted"}

    # Check if the todo is deleted
    response = client.get("/todos/1", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


# Test logout
def test_logout():
    token = create_user_and_get_token("testuser2", "testpass2")

    headers = {"Authorization": f"Bearer {token}"}

    # Logout
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}

    # Try to access a protected route with the blacklisted token
    response = client.get("/todos", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
