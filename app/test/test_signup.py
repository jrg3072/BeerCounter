from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    payload = {
        "username": "test",
        "password": "test123",
        "name": "test",
        "surname": "test", 
    }
    request = client.post("/signup", data= payload)
    assert request.status_code == 303 or request.status_code == 200