import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app
import models  # noqa: F401 — ensures models register into Base.metadata

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)   # create all tables in test DB
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # destroy all tables after


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # the db_session fixture handles closing

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear() 


@pytest.fixture
def auth_client(client):
    # create a user
    client.post("/users", json={"username": "testuser", "password": "testpass"})
    # log in to get a token
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    # attach the token to all future requests from this client
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def project(auth_client):
  
    response = auth_client.post("/projects", json={"name":"test_project", "description": "for testing purposes"})

    return response.json()["id"]