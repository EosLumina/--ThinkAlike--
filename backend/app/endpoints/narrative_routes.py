from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any, List, Optional
from backend.app.models.narrative_model import UserNarratives
from backend.app.db.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User

router = APIRouter()

class NarrativeCreate(BaseModel):
    content: str

class NarrativeResponse(BaseModel):
    id: int
    user_id: int
    content: str

@router.post("/api/v1/narratives", response_model=NarrativeResponse)
def create_narrative(
    narrative: NarrativeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    db_narrative = UserNarratives(
        user_id=current_user.id,
        content=narrative.content
    )
    db.add(db_narrative)
    db.commit()
    db.refresh(db_narrative)
    return db_narrative
