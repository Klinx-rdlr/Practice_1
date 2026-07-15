def test_create_task(auth_client, project):
    response = auth_client.post("/tasks", json={"title":"test_title", "completed":False, "project_id": project})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test_title"
    assert data["completed"] == False
    assert "project_id" in data       # owner assigned from the token

def test_create_task_no_token(client):
    response = client.post("/tasks", json={"title": "should fail", "project_id": 1})
    assert response.status_code == 401

def test_cannot_access_others_task(auth_client, project):
    response_a = auth_client.post("/tasks", json={"title": "test_title_1", "project_id": project})
    assert response_a.status_code == 200
    task_a = response_a.json()["id"]

    auth_client.post("/users", json={"username":"test_user_2", "password": "test_password_2"})
    login_b = auth_client.post("/login", data={"username" : "test_user_2", "password" :"test_password_2"})

    token_b = login_b.json()["access_token"]

    auth_client.headers.update({"Authorization": f"Bearer {token_b}"})

    response_b = auth_client.get(f"/tasks/{task_a}")
    assert response_b.status_code == 403
