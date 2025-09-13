# app/api/v1/api.py

from fastapi import APIRouter
from .endpoints import users, challenges, leaderboard

api_router = APIRouter()
from fastapi import Depends
from datetime import date
router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
