from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.auth.auth_handler import get_current_user
from backend.database.database import get_db
from backend.database.models import User

router = APIRouter()

class UserBasicInfo(BaseModel):
    user_id: str
    username: str

    class Config:
        orm_mode = True

@router.get("/api/v1/match", response_model=List[UserBasicInfo])
async def get_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.user_id != current_user.user_id).all()
    return users
