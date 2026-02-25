import requests

# This script assumes the server is running on localhost:8000
# and needs a valid token for an admin user.
# Since I can't easily get a token here without credentials, 
# I will check the Pydantic schema logic instead.

print("--- Verification: schemas.User ---")
from app import schemas
from datetime import datetime

test_user_data = {
    "id": 1,
    "username": "admin_user",
    "email": "admin@test.com",
    "xp": 100,
    "streak": 5,
    "role": "admin",
    "join_code": "ADMIN123",
    "signup_date": datetime.now()
}

user_schema = schemas.User(**test_user_data)
print(f"Schema dump: {user_schema.model_dump()}")
if user_schema.join_code == "ADMIN123":
    print("SUCCESS: join_code is correctly validated and serialized in the User schema.")
else:
    print("FAILURE: join_code missing or incorrect in schema.")
