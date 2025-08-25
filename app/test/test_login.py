from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    payload = {
        "username": "test",
        "password": "test123"
    }
    request = client.post("/login", data= payload)
    assert request.status_code == 303 or request.status_code == 200