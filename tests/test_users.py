def test_create_user(client):
    response = client.post("/users", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data
    assert "password" not in data      # response schema must not leak password


def test_login_returns_token(client):
    # first create the user
    client.post("/users", json={"username": "bob", "password": "bobpass"})
    # then log in — note: login uses FORM data, not json
    response = client.post("/login", data={"username": "bob", "password": "bobpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/users", json={"username": "bob", "password": "bobpass"})

    response = client.post("/login", data={"username": "bob", "password":"wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"