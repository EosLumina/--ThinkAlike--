"""
User API Routes

This module implements the API endpoints for user management, embodying
our principles of user sovereignty, explicit consent, and radical transparency.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.sqlalchemy_models import User, ValueProfile, UserConsent, DataAccessAudit, ConsentPurpose
from app.schemas.user_schemas import (
    UserCreate, UserResponse, ValueProfileCreate, ValueProfileResponse,
    UserConsentCreate, UserConsentResponse, UserConsentUpdate
)
from app.services.user_service import UserService
from app.auth.jwt import get_current_active_user
from app.models.user import UserInDB as PydanticUserInDB  # Pydantic model

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    
    This endpoint embodies our principle of user sovereignty by
    allowing users to establish their identity in the system with
    explicit consent and minimal required data.
    """
    user_service = UserService(db)
    try:
        return user_service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's profile.

    This endpoint implements our principle of data self-determination,
    allowing users to access their own data without restrictions.
    """
    user_service = UserService(db)

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="user_profile",
        access_type="read",
        access_reason="user requested own profile",
        data_fields=["id", "username", "email",
                     "full_name", "is_active", "is_verified"]
    )

    return user_service.get_user_by_id(current_user.id)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a user's profile by ID.

    This endpoint implements radical transparency by logging all access
    to user data and requiring explicit consent for access to other users' data.
    """
    user_service = UserService(db)

    # If user is requesting their own profile, allow access
    if current_user.id == user_id:
        return await get_current_user_profile(current_user, db)

    # If user is requesting another user's profile, check consent and connection
    user_service.verify_data_access_permission(
        accessing_user_id=current_user.id,
        target_user_id=user_id,
        data_type="user_profile",
        required_consent_purpose=ConsentPurpose.MATCHING
    )

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=user_id,
        accessor_id=current_user.id,
        data_type="user_profile",
        access_type="read",
        access_reason="user requested another user's public profile",
        data_fields=["id", "username", "is_active",
                     "is_verified"]  # Note: limited fields
    )

    # Return only the public profile (limited fields)
    return user_service.get_user_public_profile(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserCreate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user details.
    
    This endpoint embodies user sovereignty by allowing users to
    update their own information at any time.
    """
    # Check if user is updating their own data or has admin privileges
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's data"
        )
    
    user_service = UserService(db)
    try:
        return user_service.update_user(user_id, user_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/me/value-profile", response_model=ValueProfileResponse)
async def create_value_profile(
    profile: ValueProfileCreate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create or update the current user's value profile.

    This endpoint is central to ThinkAlike's value-based matching system,
    allowing users to define their core values explicitly.
    """
    user_service = UserService(db)

    # Log this data update for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="value_profile",
        access_type="create",
        access_reason="user created value profile",
        data_fields=["explicit_values", "interests", "skills", "preferences"]
    )

    return user_service.create_or_update_value_profile(current_user.id, profile)


@router.get("/me/value-profile", response_model=ValueProfileResponse)
async def get_current_user_value_profile(
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's value profile.

    This endpoint implements our principle of data self-determination,
    giving users access to their own value profile data.
    """
    user_service = UserService(db)

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="value_profile",
        access_type="read",
        access_reason="user requested own value profile",
        data_fields=["explicit_values", "narrative_derived_values",
                     "interests", "skills", "preferences"]
    )

    return user_service.get_value_profile(current_user.id)


@router.post("/me/consents", response_model=UserConsentResponse)
async def update_user_consent(
    consent: UserConsentCreate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create or update user consent for a specific purpose.

    This endpoint is fundamental to our user sovereignty principle,
    allowing users to explicitly control how their data is used.
    """
    user_service = UserService(db)

    # Log this data update for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="user_consent",
        access_type="update",
        access_reason="user updated consent settings",
        data_fields=["purpose", "is_granted", "data_categories"]
    )

    return user_service.update_consent(current_user.id, consent)


@router.get("/me/consents", response_model=List[UserConsentResponse])
async def get_user_consents(
    purpose: Optional[ConsentPurpose] = None,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's consent settings.

    This endpoint implements radical transparency by allowing users
    to see all their current consent settings.
    """
    user_service = UserService(db)

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="user_consent",
        access_type="read",
        access_reason="user requested consent settings",
        data_fields=["purpose", "is_granted",
                     "granted_at", "expires_at", "data_categories"]
    )

    return user_service.get_user_consents(current_user.id, purpose)


@router.get("/me/data-accesses", response_model=List[dict])
async def get_data_access_logs(
    data_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get logs of all accesses to the current user's data.

    This endpoint embodies our radical transparency principle by giving
    users visibility into every access to their data.
    """
    user_service = UserService(db)

    # Log this meta-access for transparency (yes, we even log access to the logs!)
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="data_access_logs",
        access_type="read",
        access_reason="user requested data access logs",
        data_fields=["all"]
    )

    return user_service.get_data_access_logs(current_user.id, data_type, limit, offset)
