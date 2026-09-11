
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Secure Task API is running"


def test_signup(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code in [200, 201]


def test_login(client):
    client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200


def test_invalid_login(client):
    client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [400, 401]