from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test 1
def test_signup_successful():
    payload = {"name": "Alice Example", "email": "alice@example.com"}
    response = client.post("/signup", data=payload)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Thanks for subscribing, Alice Example!"}

# Test 2
def test_signup_blank_name():
    payload = {"name": "", "email": "blank@name.com"}
    response = client.post("/signup", data=payload)
    assert response.status_code == 422

# Test 3
def test_signup_missing_email():
    payload = {"name": "Missing Email"}
    response = client.post("/signup", data=payload)
    assert response.status_code == 422
