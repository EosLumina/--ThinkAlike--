from datetime import datetime, timedelta
from typing import Any, Optional, Union, Dict, List  # Add List to imports

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Fix import and type issues by using direct imports without assignment
import jose.jwt
import jose.exceptions
from passlib.context import CryptContext

# Define our own classes for type safety
class JWTHelper:
    """JWT helper functions that wrap jose.jwt module"""

    @staticmethod
    def encode(payload: Dict[str, Any], key: str, algorithm: str) -> str:
        """Encode JWT token"""
        return jose.jwt.encode(payload, key, algorithm)

    @staticmethod
    def decode(token: str, key: str, algorithms: List[str]) -> Dict[str, Any]:
        """Decode JWT token"""
        return jose.jwt.decode(token, key, algorithms)

# Use our wrapper class instead of direct assignment
jwt = JWTHelper()
# Use the original exception class
JWTError = jose.exceptions.JWTError

from sqlalchemy.orm import Session
from sqlalchemy import Boolean

from ..db.database import get_db
from ..db.models.user import User
from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash from a password."""
    return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Args:
        subject: Subject identifier (typically user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create JWT payload - ensuring subject is a string (works for int or UUID)
    to_encode = {"exp": expire, "sub": str(subject)}

    # Encode JWT with secret key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt if encoded_jwt is not None else ""


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """FastAPI dependency to get the current authenticated user.

    Args:
        db: Database session
        token: JWT token from Authorization header

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If authentication fails
    """
    # Define the error to raise for authentication failures
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Check for None payload
        if payload is None:
            raise credentials_exception

        # Extract user ID from payload
        user_id = payload.get("sub")
        if not isinstance(user_id, str):
            raise credentials_exception
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Find user in database - convert string user_id from payload to int
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    # Check if user is active - fix for SQLAlchemy Column comparison
    if user.is_active is False:  # Fixed conditional check
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user
