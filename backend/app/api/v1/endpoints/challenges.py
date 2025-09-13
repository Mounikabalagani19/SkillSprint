from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from datetime import date
import re

from app import crud, models, schemas
from app.database import get_db
from app.security import get_current_active_user, get_current_user_optional

router = APIRouter()


@router.get("/", response_model=List[schemas.Challenge])
def read_challenges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_current_user_optional),
):
    """
    Retrieve only the challenges for the authenticated user's current nth day.
    nth day is calculated from the user's signup_date and cycles every 30 days.
    """
    # Calculate days since signup (1-based)
    # If no user (anonymous) or missing signup_date, default to day 1
    if not current_user or not getattr(current_user, "signup_date", None):
        nth = 1
    else:
        days_since = (date.today() - current_user.signup_date.date()).days + 1
        nth = ((days_since - 1) % 30) + 1

    all_challenges = crud.get_challenges(db, skip=skip, limit=limit*5)
    filtered = []
    for c in all_challenges:
        m = re.search(r"Day\s*(\d+)", c.title or "", re.IGNORECASE)
        if m:
            try:
                day_num = int(m.group(1))
            except Exception:
                continue
            if day_num == nth:
                filtered.append(c)
    return filtered

@router.post("/{challenge_id}/submit")
def submit_challenge_answer(
    challenge_id: int,
    submission: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Submit an answer for a challenge.
    """
    # MODIFIED: Pass the answer string from the submission object, not the object itself.
    # accept flexible body shapes (frontend may send {answer} or nested payloads)
    answer = None
    if isinstance(submission, dict):
        # try common keys
        answer = submission.get('answer') or submission.get('answer_text') or submission.get('answerValue')

    if answer is None:
        raise HTTPException(status_code=400, detail="Missing 'answer' in request body")

    result = crud.handle_submission(
        db=db,
        user=current_user,
        challenge_id=challenge_id,
        submitted_answer=answer
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
