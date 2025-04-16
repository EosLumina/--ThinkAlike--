from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
import logging
import os

from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

# Import from our user model
from app.models.user import UserInDB

# Load environment variables
load_dotenv()

# Retrieve secrets from environment (or use defaults only in development)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security check for production environments - This ensures we never have a None key
if not SECRET_KEY or SECRET_KEY == "thisisasecretkey":
    logging.warning(
        "WARNING: Using default or missing JWT_SECRET_KEY. This is insecure for production environments!")
    # In development, use a default key if not provided
    if os.getenv("ENVIRONMENT", "development") == "development":
        SECRET_KEY = "thisisasecretkey"  # Now guaranteed to be set
    else:
        raise ValueError(
            "Production environment detected but no secure JWT_SECRET_KEY provided!")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the provided data payload.

    This function supports user sovereignty by enabling users to receive a 
    transparent authentication token containing only necessary claims, with
    a clearly defined expiration. The token gives users control over their 
    authenticated sessions without excessive tracking or hidden data collection.

    Args:
        data: Dictionary containing the claims to encode in the token
        expires_delta: Optional custom expiration time, defaults to ACCESS_TOKEN_EXPIRE_MINUTES

    Returns:
        str: JWT token as a string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Include token metadata for transparency
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),  # Issued at time
        "token_type": "access"
    })

    # SECRET_KEY is guaranteed to be str by this point
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifies a JWT token and returns its payload if valid.

    Implements radical transparency by raising specific, informative exceptions
    when tokens fail validation for any reason.

    Args:
        token: The JWT token to verify

    Returns:
        dict: The decoded payload if the token is valid

    Raises:
        HTTPException: If the token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Get the current user based on the provided JWT token.

    This function ensures user sovereignty by validating the user's
    authentication token and providing access to their own data.

    Args:
        token: JWT token from the Authorization header

    Returns:
        UserInDB: The authenticated user's data

    Raises:
        HTTPException: If authentication fails or user not found
    """
    payload = verify_token(token)

    # Extract user_id from the payload
    user_id: Union[str, None] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: user ID missing from token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Here you would typically retrieve the user from your database
    # For example:
    # user = await get_user_by_id(user_id)
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return user

    # Placeholder until you implement your database retrieval:
    return UserInDB(id=user_id, username="current_user")


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """
    Verify that the current user is active.

    This function adds an additional layer of security by ensuring
    that deactivated accounts cannot access protected resources.

    Args:
        current_user: The authenticated user

    Returns:
        UserInDB: The authenticated and active user

    Raises:
        HTTPException: If the user's account is inactive
    """
    if hasattr(current_user, 'is_active') and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user
