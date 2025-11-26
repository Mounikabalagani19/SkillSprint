from app.database import SessionLocal, engine
from app.models import Challenge, UserChallenge, Submission, Base

# Create tables if they don't exist (safety)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    all_challenges = db.query(Challenge).all()
    to_delete = [c for c in all_challenges if not c.title.strip().lower().startswith('day ')]
    print(f"Found {len(all_challenges)} total challenges, deleting {len(to_delete)} non-Day entries...")
    if not to_delete:
        print("No non-Day challenges found.")
    else:
        ids = [c.id for c in to_delete]
        # Delete dependent rows first to satisfy FK constraints
        deleted_submissions = db.query(Submission).filter(Submission.challenge_id.in_(ids)).delete(synchronize_session=False)
        deleted_userch = db.query(UserChallenge).filter(UserChallenge.challenge_id.in_(ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_submissions} submission(s) and {deleted_userch} user_challenge(s) related to non-Day challenges.")

        # Now delete the challenge rows
        for c in to_delete:
            print(f"Deleting: {c.id} - {c.title}")
            db.delete(c)

        db.commit()
        print("Deleted non-Day challenges.")
except Exception as e:
    print(f"Error during cleanup: {e}")
    db.rollback()
finally:
    db.close()
