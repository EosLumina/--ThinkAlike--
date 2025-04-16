"""
Match Routes

This module defines API endpoints for the matching functionality,
implementing our principles of transparent algorithms and user control.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.user import UserInDB
from app.schemas.match import MatchResponse, ConnectionRequest, ConnectionResponse
from app.services.match_service import MatchService
from app.auth.jwt import get_current_active_user

router = APIRouter(
    prefix="/api/match",
    tags=["match"],
)


@router.get("/potential-matches", response_model=List[MatchResponse])
async def get_potential_matches(
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get potential matches for the current user.

    This endpoint implements our principle of transparent algorithms by
    providing matches with clear explanations of why users are matched.
    """
    match_service = MatchService(db)
    return match_service.get_potential_matches(current_user.id, limit, skip)


@router.get("/user-profile/{user_id}", response_model=MatchResponse)
async def get_user_profile(
    user_id: UUID,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed profile information for a potential match.

    This endpoint embodies radical transparency by providing clear
    information about why users are matched and what values they share.
    """
    match_service = MatchService(db)
    profile = match_service.get_match_profile(current_user.id, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return profile


@router.post("/connections", response_model=ConnectionResponse)
async def create_connection_request(
    connection_request: ConnectionRequest,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a connection request to another user.

    This endpoint implements user sovereignty by requiring explicit
    consent through connection requests before establishing connections.
    """
    match_service = MatchService(db)
    try:
        return match_service.create_connection_request(
            sender_id=current_user.id,
            recipient_id=connection_request.recipient_id,
            message=connection_request.message
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/connections/{request_id}/accept", response_model=ConnectionResponse)
async def accept_connection_request(
    request_id: UUID,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Accept a connection request.

    This endpoint implements user control by allowing users to
    explicitly accept connection requests.
    """
    match_service = MatchService(db)
    try:
        return match_service.accept_connection_request(request_id, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
