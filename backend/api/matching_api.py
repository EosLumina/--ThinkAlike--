from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import random

# Fix imports using relative paths for consistency
from ..auth.auth_handler import get_current_user
from ..database.models import User, Profile, Match
from ..database.database import get_db

# Import matcher class - could also use ValueBasedMatcher as an alternative name
from ..services.value_based_matcher import ValueBasedMatcher

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])

# Models
class MatchResponse(BaseModel):
    match_id: int
    user_id: str
    username: str
    full_name: str
    profile_picture_url: str
    compatibility_score: float
    common_values: List[str]
    match_description: str

    class Config:
        orm_mode = True

class MatchDetailResponse(BaseModel):
    match_id: int
    user_id: str
    username: str
    full_name: str
    profile_picture_url: str
    bio: Optional[str]
    location: Optional[str]
    compatibility_score: float
    compatibility_breakdown: dict
    shared_interests: List[str]
    shared_values: List[str]
    complementary_traits: List[dict]
    match_created_at: str

    class Config:
        orm_mode = True

# API Endpoints
@router.get("/discover", response_model=List[MatchResponse])
async def discover_matches(
    value_focus: Optional[str] = Query(None, description="Focus on specific value area"),
    min_score: Optional[float] = Query(0.0, description="Minimum compatibility score"),
    max_results: int = Query(20, description="Maximum number of results to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Discover potential matches based on value compatibility.
    Returns a list of users who share values and interests.
    """
    # Get current user profile
    user_profile = db.query(Profile).filter(Profile.user_id == current_user.user_id).first()
    if user_profile is None:
        raise HTTPException(status_code=404, detail="Your profile is not complete")

    # Get existing matches to exclude them
    existing_match_user_ids = []
    # Fix: Use SQLAlchemy's or_ function explicitly for boolean expressions
    existing_matches = db.query(Match).filter(
        or_(
            Match.user_id_1 == current_user.user_id,
            Match.user_id_2 == current_user.user_id
        )
    ).all()

    for match in existing_matches:
        if match.user_id_1.scalar() == current_user.user_id:
            existing_match_user_ids.append(match.user_id_2)
        else:
            existing_match_user_ids.append(match.user_id_1)

    # Fix: Use SQLAlchemy operators correctly for boolean expressions
    potential_matches = db.query(User, Profile).join(Profile).filter(
        User.user_id != current_user.user_id,
        User.is_active.is_(True),  # Correct SQLAlchemy boolean comparison
        ~User.user_id.in_(existing_match_user_ids)
    ).all()

    # Create matcher instance with db session
    matcher = ValueBasedMatcher(db_session=db)

    # Calculate compatibility for each potential match
    match_results = []
    for user, profile in potential_matches:
        # Fix: Remove unknown parameter 'value_focus'
        compatibility = matcher.calculate_compatibility(
            user_profile,
            profile
            # Remove the value_focus parameter as it doesn't exist in the method signature
        )

        # Handle case where compatibility might be a float or dict
        compatibility_dict = {}
        if isinstance(compatibility, dict):
            compatibility_dict = compatibility
        else:
            # If it's a float or another simple value, create a dictionary
            compatibility_dict = {
                "score": float(compatibility),
                "shared_values": [],
                "description": "Match based on compatibility score"
            }

        # Now we can safely use dictionary access
        if compatibility_dict.get("score", 0.0) >= min_score:
            match_results.append({
                "match_id": 0,
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "profile_picture_url": profile.profile_picture_url or "",
                "compatibility_score": compatibility_dict.get("score", 0.0),
                "common_values": compatibility_dict.get("shared_values", []),
                "match_description": compatibility_dict.get("description", "")
            })

    # Sort by compatibility score and limit results
    match_results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return match_results[:max_results]

@router.post("/{user_id}", response_model=MatchResponse)
async def create_match(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new match with another user"""
    # Check if user exists
    match_user = db.query(User).filter(User.user_id == user_id).first()
    if match_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if match already exists
    existing_match = db.query(Match).filter(
        or_(
            and_(Match.user_id_1 == current_user.user_id, Match.user_id_2 == user_id),
            and_(Match.user_id_1 == user_id, Match.user_id_2 == current_user.user_id)
        )
    ).first()

    if existing_match is not None:
        raise HTTPException(status_code=400, detail="Match already exists")

    # Get profiles
    current_profile = db.query(Profile).filter(Profile.user_id == current_user.user_id).first()
    match_profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    # Calculate compatibility - Fix: ensure both arguments are passed
    matcher = ValueBasedMatcher(db_session=db)
    compatibility_result = matcher.calculate_compatibility(current_profile, match_profile)

    # Fix: Handle both dictionary and non-dictionary return types
    compatibility_dict = {}
    if isinstance(compatibility_result, dict):
        compatibility_dict = compatibility_result
    else:
        # If it's a float or another simple value, create a dictionary
        compatibility_dict = {
            "score": float(compatibility_result),
            "shared_values": [],
            "shared_interests": [],
            "complementary_traits": [],
            "description": "Match based on compatibility score"
        }

    # Create match record with safe dictionary access
    new_match = Match(
        user_id_1=current_user.user_id,
        user_id_2=user_id,
        match_data={
            "shared_values": compatibility_dict.get("shared_values", []),
            "shared_interests": compatibility_dict.get("shared_interests", []),
            "complementary_traits": compatibility_dict.get("complementary_traits", [])
        },
        compatibility_score=compatibility_dict.get("score", 0.0)
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    # Fix: Use safe dictionary access with proper handling for None
    return {
        "match_id": new_match.match_id,
        "user_id": match_user.user_id,
        "username": match_user.username,
        "full_name": match_user.full_name,
        "profile_picture_url": match_profile.profile_picture_url if match_profile else "",
        "compatibility_score": compatibility_dict.get("score", 0.0),
        "common_values": compatibility_dict.get("shared_values", []),
        "match_description": compatibility_dict.get("description", "")
    }

@router.get("/{match_id}", response_model=MatchDetailResponse)
async def get_match_details(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific match"""
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    # Fix: Use proper boolean comparison for SQLAlchemy columns
    # Instead of direct comparison, get the actual values
    is_user1 = match.user_id_1 == current_user.user_id
    is_user2 = match.user_id_2 == current_user.user_id

    # Now we can safely use these in a boolean expression
    if not (is_user1.scalar() or is_user2.scalar()):
        raise HTTPException(status_code=403, detail="Not authorized to view this match")

    # Determine which user to show details for
    if is_user1.scalar():
        match_user_id = match.user_id_2
    else:
        match_user_id = match.user_id_1

    # Get user and profile
    match_user = db.query(User).filter(User.user_id == match_user_id).first()
    match_profile = db.query(Profile).filter(Profile.user_id == match_user_id).first()

    # Fix: Add null checks for match_user
    if match_user is None:
        raise HTTPException(status_code=404, detail="Match user not found")

    # Extract match data
    match_data = match.match_data or {}

    # Fix optional member access issues with proper null checks
    return {
        "match_id": match.match_id,
        "user_id": match_user.user_id,
        "username": match_user.username,
        "full_name": match_user.full_name,
        "profile_picture_url": getattr(match_profile, "profile_picture_url", None) or "",
        "bio": getattr(match_profile, "bio", None),
        "location": getattr(match_profile, "location", None),
        "compatibility_score": match.compatibility_score,
        "compatibility_breakdown": match_data.get("compatibility_breakdown", {}),
        "shared_interests": match_data.get("shared_interests", []),
        "shared_values": match_data.get("shared_values", []),
        "complementary_traits": match_data.get("complementary_traits", []),
        "match_created_at": match.created_at.isoformat()
    }

# Helper functions for safety

def check_user_eligibility(user_query, db: Session):
    """Check if user meets matching criteria"""
    # Fix: Don't use ColumnElement in boolean contexts
    if user_query is None:
        return False

    # Using scalar() to get the actual boolean value
    active_query = db.query(user_query.is_active.is_(True)).scalar()
    if active_query:
        # ...proceed with active user
        pass

    # Fix for matched_before check
    if user_query is None:
        return False
    else:
        # Get actual boolean value from query
        not_matched_query = db.query(user_query.matched_before.is_(False)).scalar()
        if not_matched_query:
            # ...handle non-matched users
            pass

# Fix the ValueBasedMatcher interface for type safety
def get_user_profile_data(profile):
    """Safe handling of profile data with proper null checks"""
    if profile is None:
        return {
            "user_id": None,
            "username": None,
            "full_name": None,
            "profile_picture_url": None,
            "bio": None,
            "location": None
        }

    # Use getattr for safe attribute access
    return {
        "user_id": getattr(profile, "user_id", None),
        "username": getattr(profile, "username", None),
        "full_name": getattr(profile, "full_name", None),
        "profile_picture_url": getattr(profile, "profile_picture_url", None),
        "bio": getattr(profile, "bio", None),
        "location": getattr(profile, "location", None)
    }
