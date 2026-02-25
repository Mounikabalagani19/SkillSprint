from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import io
from pypdf import PdfReader
import re

from app import models, schemas, crud
from app.database import get_db
from app.security import get_current_user

router = APIRouter()

# --- HELPER: ROLE CHECK ---
def check_mentor_or_admin(user: models.User):
    if user.role not in ["mentor", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")

# --- MENTOR: GET STUDENTS ---
@router.get("/mentor/students", response_model=List[schemas.User])
def get_mentor_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "mentor":
        raise HTTPException(status_code=403, detail="Mentor access required")
    
    return db.query(models.User).filter(models.User.mentor_id == current_user.id).all()

# --- ADMIN: GET STATS ---
@router.get("/admin/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get all mentors under this admin
    mentors = db.query(models.User).filter(models.User.admin_id == current_user.id).all()
    mentor_map = {m.id: m.username for m in mentors}
    mentor_ids = list(mentor_map.keys())
    
    # Get all students under these mentors
    students = db.query(models.User).filter(models.User.mentor_id.in_(mentor_ids)).all()
    
    student_details = []
    for s in students:
        student_details.append({
            "id": s.id,
            "username": s.username,
            "email": s.email,
            "xp": s.xp,
            "streak": s.streak,
            "mentor_name": mentor_map.get(s.mentor_id, "Unknown")
        })
    
    return {
        "mentor_count": len(mentors),
        "student_count": len(students),
        "total_xp": sum(s.xp for s in students),
        "average_streak": sum(s.streak for s in students) / len(students) if students else 0,
        "students": student_details
    }

# --- MENTOR: BATCH UPLOAD CHALLENGES ---
@router.post("/mentor/challenges")
def batch_upload_challenges(
    challenges: List[schemas.ChallengeCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "mentor":
        raise HTTPException(status_code=403, detail="Mentor access required")
    
    new_challenges = []
    for c in challenges:
        db_challenge = models.Challenge(**c.dict())
        db.add(db_challenge)
        new_challenges.append(db_challenge)
    
    db.commit()
    return {"status": "success", "count": len(new_challenges)}

# --- MENTOR: PDF TO MODULE ---
@router.post("/mentor/modules/pdf")
async def create_module_from_pdf(
    file: UploadFile = File(...),
    level: str = Form(...),
    module_name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "mentor":
        raise HTTPException(status_code=403, detail="Mentor access required")
    
    content = await file.read()
    pdf = PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    
    # Simple logic to find questions and answers (Demo only)
    # Expected format: Q: <question> A: <answer>
    qa_pairs = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=Q:|$)", text, re.DOTALL)
    
    questions = []
    for q, a in qa_pairs[:20]: # Limit to 20 for module compatibility
        questions.append({
            "question": q.strip(),
            "answer": a.strip(),
            "explanation": "Extracted from PDF"
        })
    
    if not questions:
        raise HTTPException(status_code=400, detail="No Q: and A: pairs found in PDF")

    # In a real app, we would save this to a new module table or questions files
    return {
        "module": module_name,
        "level": level,
        "questions_parsed": len(questions),
        "preview": questions[:3]
    }
