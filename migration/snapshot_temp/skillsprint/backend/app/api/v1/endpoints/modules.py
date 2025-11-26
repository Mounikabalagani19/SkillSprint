from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Literal, Optional

from app.database import get_db
from app import models
from app.security import get_current_active_user
from app.modules.questions import get_questions as get_py_questions, ModuleLevel
from app.modules import java_questions

router = APIRouter()


def normalize_level(level: str) -> ModuleLevel:
    try:
        return ModuleLevel(level.lower())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid level. Use beginner|intermediate|expert")


@router.get("/levels", tags=["modules"]) 
def list_levels() -> List[str]:
    return [l.value for l in ModuleLevel]


def _get_items(module: str, level: str, db: Session, current_user: Optional[models.User]):
    lvl = normalize_level(level)
    mod = (module or "python").lower()
    if mod == "python":
        items = get_py_questions(lvl)
    elif mod == "java":
        items = java_questions.get_questions(lvl)
    else:
        raise HTTPException(status_code=404, detail="Unknown module. Try 'python' or 'java'")

    # Determine completed items for this user and level
    completed_ids = set()
    if current_user is not None:
        rows = (
            db.query(models.ModuleProgress.qa_id)
            .filter(
                models.ModuleProgress.user_id == current_user.id,
                models.ModuleProgress.level == lvl.value,
            )
            .all()
        )
        completed_ids = {qa_id for (qa_id,) in rows}
    return [
        {
            "id": qa.id,
            "level": qa.level.value,
            "question": qa.question,
            "explanation": qa.explanation,
            "completed": qa.id in completed_ids,
        }
        for qa in items
    ]


@router.get("/{level}", tags=["modules"])  # Back-compat: defaults to python
def get_module_items_default(
    level: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_active_user),
):
    return _get_items("python", level, db, current_user)


@router.get("/{module}/{level}", tags=["modules"])  
def get_module_items_module(
    module: str,
    level: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_active_user),
):
    return _get_items(module, level, db, current_user)


def _submit_answer_for(module: str, level: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Check an answer for a module item and update XP/streak.
    Rules:
      - Correct: +5 XP and +1 streak, and record completion (no double award for same item)
      - Wrong: apply same rules as daily quiz -> reset streak to 0

    Request body shape:
      { "id": <int>, "answer": <str> }
    """
    lvl = normalize_level(level)
    qa_id = payload.get("id")
    submitted = payload.get("answer")
    if not isinstance(qa_id, int) or submitted is None:
        raise HTTPException(status_code=400, detail="Body must include integer 'id' and 'answer'")

    # Find the referenced QA
    mod = (module or "python").lower()
    if mod == "python":
        source_items = get_py_questions(lvl)
    elif mod == "java":
        source_items = java_questions.get_questions(lvl)
    else:
        raise HTTPException(status_code=404, detail="Unknown module. Try 'python' or 'java'")

    items = {qa.id: qa for qa in source_items}
    qa = items.get(qa_id)
    if qa is None:
        raise HTTPException(status_code=404, detail="Question not found")

    def _norm(s: str) -> str:
        s = (s or "").strip()
        # normalize surrounding quotes if present
        if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
            s = s[1:-1].strip()
        return s.lower()

    submitted_n = _norm(str(submitted))
    candidates = [_norm(str(qa.answer))] + [_norm(v) for v in getattr(qa, "variants", [])]
    is_correct = submitted_n in candidates

    if is_correct:
        # Check if already completed
        existing = (
            db.query(models.ModuleProgress)
            .filter(
                models.ModuleProgress.user_id == current_user.id,
                models.ModuleProgress.level == lvl.value,
                models.ModuleProgress.qa_id == qa_id,
            )
            .first()
        )
        if existing:
            return {"success": True, "message": "Already completed. No additional XP awarded."}

        # Award 5 XP and +1 streak
        current_user.xp += 5
        current_user.streak += 1

        db.add(
            models.ModuleProgress(
                user_id=current_user.id, level=lvl.value, qa_id=qa_id
            )
        )
        db.commit()
        return {"success": True, "message": "Correct! You've earned 5 XP."}
    else:
        # Wrong answer rule same as daily quiz: reset streak
        current_user.streak = 0
        db.commit()
        return {"success": False, "message": "Incorrect answer. Try again!"}


@router.post("/{level}/submit", tags=["modules"])  # Back-compat: python default
def submit_module_answer_default(
    level: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return _submit_answer_for("python", level, payload, db, current_user)


@router.post("/{module}/{level}/submit", tags=["modules"]) 
def submit_module_answer_module(
    module: str,
    level: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return _submit_answer_for(module, level, payload, db, current_user)
