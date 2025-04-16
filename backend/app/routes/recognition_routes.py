"""
Recognition Routes

This module defines the API endpoints for the badge and rank system,
embodying our revolutionary approach to contributor recognition.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.recognition import BadgeAward, Badge, ContributorRecognition, RankAdvancement
from app.schemas.recognition import (
    BadgeAwardCreate, 
    BadgeAwardResponse, 
    BadgeResponse, 
    ContributorRecognitionResponse
)
from app.services.recognition_service import RecognitionService
from app.auth.jwt import get_current_active_user
from app.models.user import UserInDB

router = APIRouter(
    prefix="/api/recognition",
    tags=["recognition"],
)


@router.get("/badges", response_model=List[BadgeResponse])
async def get_badges(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all available badges, optionally filtered by category.
    
    This endpoint embodies our principle of radical transparency by
    making the complete recognition system visible to all.
    """
    recognition_service = RecognitionService(db)
    return recognition_service.get_badges(category)


@router.get("/badges/{badge_id}", response_model=BadgeResponse)
async def get_badge(
    badge_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get details for a specific badge.
    """
    recognition_service = RecognitionService(db)
    badge = recognition_service.get_badge(badge_id)
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    return badge


@router.post("/award-badge", response_model=BadgeAwardResponse)
async def award_badge(
    award: BadgeAwardCreate,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Award a badge to a contributor.
    
    This endpoint implements our revolutionary recognition system by
    celebrating diverse forms of contribution beyond just code.
    """
    # Only administrators or automated systems can award badges
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to award badges"
        )
    
    recognition_service = RecognitionService(db)
    return recognition_service.award_badge(
        badge_id=award.badge_id,
        contributor_id=award.contributor_id,
        quest_id=award.quest_id,
        contribution_description=award.contribution_description,
        awarded_by=current_user.id
    )


@router.get("/contributor/{contributor_id}", response_model=ContributorRecognitionResponse)
async def get_contributor_recognition(
    contributor_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a contributor's recognition profile, including badges and rank.
    
    This endpoint supports our principle of celebrating diverse contributions
    by making a contributor's achievements visible.
    """
    recognition_service = RecognitionService(db)
    recognition = recognition_service.get_contributor_recognition(contributor_id)
    if not recognition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contributor recognition profile not found"
        )
    return recognition