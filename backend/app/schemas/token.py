from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for the authentication token response."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: Optional[str] = None  # Subject (user_id as string)
    exp: Optional[int] = None  # Expiration time
