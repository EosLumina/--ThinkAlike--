from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....core.config import settings
from ....core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from ....db.database import get_db
from ....db.models.user import User
from ....db.models.profile import Profile
from ....schemas.token import Token
from ....schemas.user import UserCreate, UserPublic

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Register a new user.

    Args:
        user_in: User registration data
        db: Database session

    Returns:
        UserPublic: Public user data

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if user with this username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_in.username) |
        (User.email == user_in.email)
    ).first()

    # Fix SQLAlchemy Column comparison
    if existing_user is not None:
        if existing_user.username.is_(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow()
    )

    # Add user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create associated profile
    db_profile = Profile(
        user_id=db_user.user_id,
        full_name=user_in.full_name,
        created_at=datetime.utcnow(),
        last_updated=datetime.utcnow()
    )

    # Add profile to database
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests.

    Args:
        db: Database session
        form_data: OAuth2 form containing username and password

    Returns:
        Token: JWT access token

    Raises:
        HTTPException: If authentication fails
    """
    # Find user by username (OAuth2PasswordRequestForm uses username field even for email login)
    user = db.query(User).filter(User.username == form_data.username).first()

    # Check user exists and password is correct - fix for Column type issue
    if not user or not verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login timestamp - fix for SQL Column assignment
    current_time = datetime.utcnow()
    setattr(user, 'last_login_at', current_time)
    db.commit()

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.user_id, expires_delta=access_token_expires
    )

    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user.

    Args:
        current_user: Current authenticated user

    Returns:
        UserPublic: Public user data
    """
    return current_user
