# app/models.py

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # --- GAMIFICATION FIELDS ---
    xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    # When the user signed up — used to calculate the daily challenge
    signup_date = Column(DateTime, default=datetime.utcnow)
    
    # This relationship now correctly points to the UserChallenge association table
    challenges_completed = relationship("UserChallenge", back_populates="user")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    # MODIFIED: Changed 'description' to 'question' to match schemas.py
    question = Column(String)
    category = Column(String)
    answer = Column(String)

    # NEW: Added the missing relationship back to the UserChallenge table
    users_completed = relationship("UserChallenge", back_populates="challenge")

# --- ASSOCIATION TABLE ---
# This table links users to the challenges they have completed.

# --- SUBMISSION TABLE ---
# This table tracks each user's answer attempt, correctness, and timestamp.
from sqlalchemy import DateTime
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    answer = Column(String)
    is_correct = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    challenge = relationship("Challenge")

class UserChallenge(Base):
    __tablename__ = "user_challenges"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), primary_key=True)
    user = relationship("User", back_populates="challenges_completed")
    challenge = relationship("Challenge", back_populates="users_completed")