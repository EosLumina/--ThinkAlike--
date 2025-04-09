from typing import Optional, List, Union, Pattern
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, Field

# For Pydantic v1
try:
    from pydantic import constr
except ImportError:
    # For Pydantic v2
    from pydantic import StringConstraints as constr

class UserBase(BaseModel):
    """Base Pydantic schema for common user fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for user creation with password."""
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength (basic check for MVP)."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user as stored in database (internal use)."""
    user_id: int
    password_hash: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    roles: str  # For MVP, we'll use a string instead of a list

    class Config:
        orm_mode = True


class UserPublic(BaseModel):
    """Schema for user data exposed to the public API."""
    user_id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserWithProfile(UserPublic):
    """Schema for user data with profile information."""
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        orm_mode = True
