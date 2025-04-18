import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

from jose import jwt, JWTError  # type: ignore
from passlib.context import CryptContext  # type: ignore
from pydantic import ValidationError

from backend.app.core.config import settings
from backend.app.models.user import UserInDB  # Assuming UserInDB is in models.user
from backend.app.schemas.token import TokenPayload

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings from environment or defaults
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token.

    Args:
        subject: The subject of the token (e.g., user ID or email).
        expires_delta: Optional timedelta for token expiration. Defaults to
                       ACCESS_TOKEN_EXPIRE_MINUTES from settings.

    Returns:
        The encoded JWT access token.

    Raises:
        ValueError: If SECRET_KEY or ALGORITHM is not configured.
    """
    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("JWT SECRET_KEY and ALGORITHM must be configured.")

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenPayload]:
    """
    Decodes a JWT access token and validates its payload.

    Args:
        token: The JWT token string.

    Returns:
        A TokenPayload object if the token is valid and not expired, otherwise None.

    Raises:
        ValueError: If SECRET_KEY or ALGORITHM is not configured.
    """
    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("JWT SECRET_KEY and ALGORITHM must be configured.")

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        # Optional: Check if token is expired (though jwt.decode usually handles this)
        # if token_data.exp < datetime.now(timezone.utc):
        #     return None
        return token_data
    except (JWTError, ValidationError):
        # Log the error appropriately in a real application
        # print(f"Token validation error: {e}")
        return None


# Example usage (optional, for testing or demonstration)
if __name__ == "__main__":
    # Ensure settings are loaded if running directly
    # This might require adjusting paths depending on how settings are loaded
    # from backend.app.core.config import settings

    if not SECRET_KEY or not ALGORITHM:
        print("Error: JWT SECRET_KEY and ALGORITHM must be set in your environment or .env file.")
    else:
        # Example: Create a token
        user_id = "user123"
        token = create_access_token(subject=user_id)
        print(f"Generated Token: {token}")

        # Example: Decode a token
        decoded_payload = decode_access_token(token)
        if decoded_payload:
            print(f"Decoded Payload: {decoded_payload}")
            print(f"Subject (User ID): {decoded_payload.sub}")
            print(f"Expires at: {decoded_payload.exp}")
        else:
            print("Token is invalid or expired.")

        # Example: Password hashing
        password = "mysecretpassword"
        hashed_pw = get_password_hash(password)
        print(f"Original Password: {password}")
        print(f"Hashed Password: {hashed_pw}")
        print(f"Verification (correct): {verify_password(password, hashed_pw)}")
        print(f"Verification (incorrect): {verify_password('wrongpassword', hashed_pw)}")
