
def register_and_login(client, username="testuser", email="test@example.com"):
    # Register user
    register_response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    # Login user
    login_response = client.post(
        "/login",
        json={
            "email": email,
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.get_json()["access_token"]

    return token


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
    token = register_and_login(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Study Flask",
            "description": "Complete Flask assignment",
            "status": "pending",
            "priority": "medium"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Task created successfully"
    assert data["task"]["title"] == "Study Flask"


def test_get_tasks(client):
    token = register_and_login(client)

    # Create a task first
    client.post(
        "/tasks",
        json={
            "title": "Study Flask",
            "description": "Complete Flask assignment"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # Get tasks
    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "tasks" in data
    assert len(data["tasks"]) == 1


def test_update_task(client):
    token = register_and_login(client)

    # Create task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "Original description"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.get_json()["task"]["id"]

    # Update task
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "status": "completed"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Task updated successfully"


def test_delete_task(client):
    token = register_and_login(client)

    # Create task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": "This task will be deleted"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.get_json()["task"]["id"]

    # Delete task
    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Task deleted successfully"


def test_user_cannot_access_another_users_task(client):
    # Create User A
    token_a = register_and_login(
        client,
        username="amina",
        email="amina@example.com"
    )

    # User A creates a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Amina's private task",
            "description": "Private task"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.get_json()["task"]["id"]

    # Create User B
    token_b = register_and_login(
        client,
        username="brian",
        email="brian@example.com"
    )

    # User B attempts to access User A's task
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert "access denied" in data["message"].lower()

