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


# Test logout
def test_logout():
    token = create_user_and_get_token("testuser2", "testpass2")

    headers = {"Authorization": f"Bearer {token}"}

    # Logout
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
