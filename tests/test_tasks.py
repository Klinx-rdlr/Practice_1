def test_create_task(auth_client):
    response = auth_client.post("/tasks", json={"title": "my first task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "my first task"
    assert data["completed"] == False
    assert "user_id" in data       # owner assigned from the token

def test_create_task_no_token(client):
    response = client.post("/tasks", json={"title": "should fail"})
    assert response.status_code == 401

def test_cannot_access_others_task(auth_client):
    # user A (testuser, already authenticated via the fixture) creates a task
    response_a = auth_client.post("/tasks", json={"title": "test_title_1"})
    assert response_a.status_code == 200
    task_id = response_a.json()["id"]

    # create user B and log in
    auth_client.post("/users", json={"username": "test_user_2", "password": "test_password_2"})
    login_b = auth_client.post("/login", data={"username": "test_user_2", "password": "test_password_2"})
    token_b = login_b.json()["access_token"]

    # swap the client's identity to user B
    auth_client.headers.update({"Authorization": f"Bearer {token_b}"})

    # user B tries to read user A's task
    response_b = auth_client.get(f"/tasks/{task_id}")
    assert response_b.status_code == 403
