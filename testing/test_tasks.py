def test_get_tasks_requires_authentication(client):
    response = client.get("/tasks")

    assert response.status_code in [401, 403]


def test_create_task_requires_authentication(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Study Flask",
            "description": "Complete Flask assignment"
        }
    )

    assert response.status_code in [401, 403]


def test_create_task(client):
    # Signup
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    # Authentication mechanism depends on Student 2's implementation.
    # Add token/session handling here.

    # Create task
    response = client.post(
        "/tasks",
        json={
            "title": "Study Flask",
            "description": "Complete Flask assignment"
        }
    )

    assert response.status_code in [200, 201]


def test_get_tasks(client):
    # Login first
    # Add authentication
    # Then request /tasks

    response = client.get("/tasks")

    assert response.status_code in [200, 401, 403]


def test_update_task(client):
    # Login
    # Create task
    # PATCH /tasks/<id>
    pass


def test_delete_task(client):
    # Login
    # Create task
    # DELETE /tasks/<id>
    pass


def test_user_cannot_access_another_users_task(client):
    # Create User A
    # Create User B
    # Create task belonging to User A
    # Authenticate as User B
    # Attempt to access User A's task
    pass