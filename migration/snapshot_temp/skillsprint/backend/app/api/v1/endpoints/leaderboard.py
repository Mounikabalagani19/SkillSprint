from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_leaderboard(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve the top users for the leaderboard.
    """
    users = crud.get_leaderboard_users(db, skip=skip, limit=limit)
    return users

