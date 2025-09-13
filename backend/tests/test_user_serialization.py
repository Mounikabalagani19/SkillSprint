import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app import crud, models, security


client = TestClient(app)


def test_user_serialization_and_me_endpoint():
    db = SessionLocal()
    # Create a unique test user
    username = "test_serial_user"
    email = "test_serial@example.com"
    # Clean up any existing user with that username
    existing = crud.get_user_by_username(db, username=username)
    if existing:
        db.delete(existing)
        db.commit()

    user_in = models.User(username=username, email=email, hashed_password=security.get_password_hash("pass"))
    db.add(user_in)
    db.commit()
    db.refresh(user_in)

    # Create token
    token = security.create_access_token({"sub": username})

    # Call /users/me with the token
    headers = {"Authorization": f"Bearer {token}", "Origin": "http://localhost:5173"}
    resp = client.get("/api/v1/users/me", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["username"] == username
    assert body["email"] == email

    # Cleanup
    db.delete(user_in)
    db.commit()
    db.close()
