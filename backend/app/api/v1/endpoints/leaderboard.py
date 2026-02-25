from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_leaderboard(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve the top users for the leaderboard.
    """
    users = crud.get_leaderboard_users(db, skip=skip, limit=limit, current_user=current_user)
    return users

