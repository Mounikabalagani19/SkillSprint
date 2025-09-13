"""
Small script to load the test user from the DB and serialize with Pydantic
to reproduce the Internal Server Error seen when calling /users/me.
"""
from app.database import SessionLocal
from app import crud, schemas

if __name__ == '__main__':
    db = SessionLocal()
    user = crud.get_user_by_username(db, username='devtests')
    print('Loaded user from DB:', user)
    try:
        u = schemas.User.model_validate(user)
        print('Pydantic serialized:', u)
    except Exception as e:
        print('Serialization error:', type(e), e)
    finally:
        db.close()
