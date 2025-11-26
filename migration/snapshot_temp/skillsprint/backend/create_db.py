# create_db.py
from app.database import engine, Base
from app.models import User, Challenge, UserChallenge
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")