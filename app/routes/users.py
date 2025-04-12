from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel

router = APIRouter()

class UserBase(BaseModel):
    username: str = Field(..., description="Unique username for the user")
    email: EmailStr = Field(..., description="Valid email address")
    display_name: Optional[str] = Field(None, description="Display name (optional)")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password, min 8 characters")

class User(UserBase):
    id: int
    has_ethical_profile: bool = Field(default=False, description="Whether the user has completed ethical profiling")
    data_transparency_level: str = Field(default="full", description="User's chosen data transparency level")

    class Config:
        # Fixed Pydantic v2 warning (schema_extra → json_schema_extra)
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com",
                "display_name": "Enlightened User",
                "has_ethical_profile": True,
                "data_transparency_level": "full"
            }
        }
        # Fixed Pydantic v2 warning (orm_mode → from_attributes)
        from_attributes = True

@router.get("/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """
    Retrieve all users with data transparency controls.

    This endpoint adheres to ThinkAlike's radical transparency principle
    by clearly documenting what user data is accessible and why.
    """
    # In a real implementation, fetch from database
    users = db.query(UserModel).all()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID with transparency indicators.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"X-Error-Type": "EntityNotFound"}
        )

    return user
