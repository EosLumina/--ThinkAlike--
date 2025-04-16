"""
Narrative API Routes

This module implements the API endpoints for user narratives, embodying
our principles of digital storytelling, contextual understanding, and
user sovereignty over personal experiences and stories.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.sqlalchemy_models import Narrative, NarrativeDerivedValue, ConsentPurpose
from app.schemas.narrative_schemas import (
    NarrativeCreate, NarrativeResponse, NarrativeUpdate,
    NarrativeDerivedValueResponse
)
from app.services.narrative_service import NarrativeService
from app.services.user_service import UserService
from app.auth.jwt import get_current_active_user
from app.models.user import UserInDB as PydanticUserInDB  # Pydantic model

router = APIRouter(
    prefix="/api/narratives",
    tags=["narratives"],
)


@router.post("/", response_model=NarrativeResponse, status_code=status.HTTP_201_CREATED)
async def create_narrative(
    narrative: NarrativeCreate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new narrative.

    Narratives are core to ThinkAlike's approach of understanding users
    through their self-expressed stories rather than extracting data from
    behavior patterns.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Log this data creation for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="narrative",
        access_type="create",
        access_reason="user created new narrative",
        data_fields=["title", "content", "topics",
                     "visibility", "is_core_narrative"]
    )

    # Create the narrative
    new_narrative = narrative_service.create_narrative(
        current_user.id, narrative)

    # If the user has consented to narrative analysis, analyze this narrative
    # to extract values (only if it's a core narrative)
    if narrative.is_core_narrative:
        user_consent = user_service.get_consent_for_purpose(
            current_user.id,
            ConsentPurpose.NARRATIVE_ANALYSIS
        )
        if user_consent and user_consent.is_granted:
            narrative_service.analyze_narrative(new_narrative.id)

    return new_narrative


@router.get("/", response_model=List[NarrativeResponse])
async def get_user_narratives(
    visibility: Optional[str] = None,
    is_core: Optional[bool] = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's narratives.

    This endpoint embodies user sovereignty by giving users access to
    all their own narrative content.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="narratives",
        access_type="read",
        access_reason="user requested own narratives",
        data_fields=["id", "title", "content",
                     "topics", "visibility", "is_core_narrative"]
    )

    return narrative_service.get_user_narratives(
        current_user.id, visibility, is_core, limit, offset
    )


@router.get("/{narrative_id}", response_model=NarrativeResponse)
async def get_narrative(
    narrative_id: UUID,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific narrative by ID.

    This endpoint implements transparent data access by checking permissions
    and logging all access attempts.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Get the narrative first to check ownership
    narrative = narrative_service.get_narrative(narrative_id)
    if not narrative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narrative not found"
        )

    # If the narrative belongs to the current user, allow access
    if narrative.user_id == current_user.id:
        # Log this data access for transparency
        user_service.log_data_access(
            user_id=current_user.id,
            accessor_id=current_user.id,
            data_type="narrative",
            access_type="read",
            access_reason="user requested own narrative",
            data_fields=["id", "title", "content",
                         "topics", "visibility", "is_core_narrative"]
        )
        return narrative

    # If the narrative belongs to another user, check visibility and connection
    if narrative.visibility == "private":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this narrative"
        )

    if narrative.visibility == "connections":
        # Check if the users are connected
        if not user_service.are_users_connected(current_user.id, narrative.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be connected to this user to view this narrative"
            )

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=narrative.user_id,
        accessor_id=current_user.id,
        data_type="narrative",
        access_type="read",
        access_reason="user requested another user's narrative",
        data_fields=["id", "title", "content", "topics", "visibility"]
    )

    return narrative


@router.put("/{narrative_id}", response_model=NarrativeResponse)
async def update_narrative(
    narrative_id: UUID,
    narrative_update: NarrativeUpdate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific narrative.

    This endpoint embodies user sovereignty by giving users control
    over their own narrative content.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Ensure the narrative belongs to the current user
    narrative = narrative_service.get_narrative(narrative_id)
    if not narrative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narrative not found"
        )

    if narrative.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this narrative"
        )

    # Log this data update for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="narrative",
        access_type="update",
        access_reason="user updated narrative",
        data_fields=list(narrative_update.dict(exclude_unset=True).keys())
    )

    # Update the narrative
    updated_narrative = narrative_service.update_narrative(
        narrative_id, narrative_update)

    # If the narrative is a core narrative and has changed, re-analyze it
    # (only if the user has consented to narrative analysis)
    if narrative.is_core_narrative and "content" in narrative_update.dict(exclude_unset=True):
        user_consent = user_service.get_consent_for_purpose(
            current_user.id,
            ConsentPurpose.NARRATIVE_ANALYSIS
        )
        if user_consent and user_consent.is_granted:
            narrative_service.analyze_narrative(narrative_id)

    return updated_narrative


@router.delete("/{narrative_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_narrative(
    narrative_id: UUID,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific narrative.

    This endpoint embodies our principle of user data sovereignty by
    allowing users to completely remove their content.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Ensure the narrative belongs to the current user
    narrative = narrative_service.get_narrative(narrative_id)
    if not narrative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narrative not found"
        )

    if narrative.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this narrative"
        )

    # Log this data deletion for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="narrative",
        access_type="delete",
        access_reason="user deleted narrative",
        data_fields=["id", "title", "content"]
    )

    # Delete the narrative
    narrative_service.delete_narrative(narrative_id)


@router.get("/{narrative_id}/derived-values", response_model=List[NarrativeDerivedValueResponse])
async def get_narrative_derived_values(
    narrative_id: UUID,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get values derived from a specific narrative.

    This endpoint embodies radical transparency by showing users exactly
    what values have been derived from their narratives and how.
    """
    narrative_service = NarrativeService(db)
    user_service = UserService(db)

    # Ensure the narrative exists
    narrative = narrative_service.get_narrative(narrative_id)
    if not narrative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narrative not found"
        )

    # Check ownership and permissions
    if narrative.user_id != current_user.id:
        # Check if the user has permission to view this narrative
        if narrative.visibility == "private":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access derived values for this narrative"
            )

        if narrative.visibility == "connections":
            # Check if the users are connected
            if not user_service.are_users_connected(current_user.id, narrative.user_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You must be connected to this user to view derived values"
                )

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=narrative.user_id,
        accessor_id=current_user.id,
        data_type="narrative_derived_values",
        access_type="read",
        access_reason="user requested narrative derived values",
        data_fields=["value_name", "confidence_score",
                     "extraction_method", "evidence_text"]
    )

    return narrative_service.get_narrative_derived_values(narrative_id)
