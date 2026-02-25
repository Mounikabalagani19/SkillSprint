from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Announcement)
def create_announcement(
    announcement: schemas.AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "mentor":
        raise HTTPException(status_code=403, detail="Only mentors can create announcements")
    
    db_announcement = models.Announcement(
        content=announcement.content,
        mentor_id=current_user.id
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.get("/", response_model=List[schemas.Announcement])
def get_announcements(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == "mentor":
        # Mentors see their own announcements
        return db.query(models.Announcement).filter(models.Announcement.mentor_id == current_user.id).all()
    
    elif current_user.role == "student":
        # Students see announcements from their mentor
        if not current_user.mentor_id:
            return []
        return db.query(models.Announcement).filter(models.Announcement.mentor_id == current_user.mentor_id).all()
    
    elif current_user.role == "parent":
        # Parents see announcements from their child's mentor
        if not current_user.child_id:
            return []
        # Get child
        child = db.query(models.User).filter(models.User.id == current_user.child_id).first()
        if not child or not child.mentor_id:
            return []
        return db.query(models.Announcement).filter(models.Announcement.mentor_id == child.mentor_id).all()
    
    elif current_user.role == "admin":
        # Admins see all announcements
        return db.query(models.Announcement).all()
    
    return []
