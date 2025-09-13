from sqlalchemy.orm import Session
from . import models, schemas, security

# --- User Functions ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
    hashed_password=hashed_password,
    # allow optional signup_date if present in user payload
    **({"signup_date": user.signup_date} if getattr(user, "signup_date", None) else {})
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

# --- Challenge Functions ---

def get_challenges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Challenge).offset(skip).limit(limit).all()

def handle_submission(db: Session, user: models.User, challenge_id: int, submitted_answer: str):
    # 1. Check if challenge exists
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        return {"success": False, "message": "Challenge not found."}

    # 2. Check if user already completed this challenge
    completion_record = db.query(models.UserChallenge).filter(
        models.UserChallenge.user_id == user.id,
        models.UserChallenge.challenge_id == challenge_id
    ).first()
    if completion_record:
        return {"success": False, "message": "You have already completed this challenge."}

    # 3. Check if the answer is correct
    is_correct = str(challenge.answer).strip().lower() == str(submitted_answer).strip().lower()

    # Record the submission attempt
    try:
        submission_record = models.Submission(
            user_id=user.id,
            challenge_id=challenge_id,
            answer=str(submitted_answer),
            is_correct=is_correct
        )
        db.add(submission_record)
    except Exception:
        # If Submission model/table is not present or any other DB error occurs,
        # continue with the main logic but report via rollback later if needed.
        db.rollback()

    if is_correct:
        # Award XP
        user.xp += 10
        # TODO: Implement more complex streak logic (e.g., based on timestamps)
        user.streak += 1

        # Mark challenge as completed
        new_completion = models.UserChallenge(user_id=user.id, challenge_id=challenge_id)
        db.add(new_completion)
        db.commit()
        db.refresh(user)
        return {"success": True, "message": "Correct! You've earned 10 XP."}
    else:
        # Incorrect answer - reset streak
        user.streak = 0
        db.commit()
        return {"success": False, "message": "Incorrect answer. Try again!"}

# --- Leaderboard Function ---

def get_leaderboard_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).order_by(models.User.xp.desc()).offset(skip).limit(limit).all()

