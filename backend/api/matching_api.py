from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random
from ..auth.auth_handler import get_current_user
from ..database.models import User, Profile, Match
from ..database.database import get_db
from ..services.matching_service import ValueBasedMatcher

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
    if not user_profile:
        raise HTTPException(status_code=404, detail="Your profile is not complete")
    
    # Get existing matches to exclude them
    existing_match_user_ids = []
    existing_matches = db.query(Match).filter(
        (Match.user_id_1 == current_user.user_id) | 
        (Match.user_id_2 == current_user.user_id)
    ).all()
    
    for match in existing_matches:
        if match.user_id_1 == current_user.user_id:
            existing_match_user_ids.append(match.user_id_2)
        else:
            existing_match_user_ids.append(match.user_id_1)
    
    # Get potential matches (users with profiles)
    potential_matches = db.query(User, Profile).join(Profile).filter(
        User.user_id != current_user.user_id,
        User.is_active == True,
        ~User.user_id.in_(existing_match_user_ids)
    ).all()
    
    # Create matcher instance
    matcher = ValueBasedMatcher()
    
    # Calculate compatibility for each potential match
    match_results = []
    for user, profile in potential_matches:
        # In a real implementation, this would use actual user values from profiles
        # For now, we'll use a simplified scoring with random shared values
        
        compatibility = matcher.calculate_compatibility(user_profile, profile, value_focus)
        
        if compatibility["score"] >= min_score:
            match_results.append({
                "match_id": 0,  # No match record exists yet
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "profile_picture_url": profile.profile_picture_url or "",
                "compatibility_score": compatibility["score"],
                "common_values": compatibility["shared_values"],
                "match_description": compatibility["description"]
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
    """
    Create a new match with another user
    """
    # Check if user exists
    match_user = db.query(User).filter(User.user_id == user_id).first()
    if not match_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if match already exists
    existing_match = db.query(Match).filter(
        ((Match.user_id_1 == current_user.user_id) & (Match.user_id_2 == user_id)) |
        ((Match.user_id_1 == user_id) & (Match.user_id_2 == current_user.user_id))
    ).first()
    
    if existing_match:
        raise HTTPException(status_code=400, detail="Match already exists")
    
    # Get profiles
    current_profile = db.query(Profile).filter(Profile.user_id == current_user.user_id).first()
    match_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    
    # Calculate compatibility
    matcher = ValueBasedMatcher()
    compatibility = matcher.calculate_compatibility(current_profile, match_profile)
    
    # Create match record
    new_match = Match(
        user_id_1=current_user.user_id,
        user_id_2=user_id,
        match_data={
            "shared_values": compatibility["shared_values"],
            "shared_interests": compatibility["shared_interests"],
            "complementary_traits": compatibility["complementary_traits"]
        },
        compatibility_score=compatibility["score"]
    )
    
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    
    return {
        "match_id": new_match.match_id,
        "user_id": match_user.user_id,
        "username": match_user.username,
        "full_name": match_user.full_name,
        "profile_picture_url": match_profile.profile_picture_url or "",
        "compatibility_score": compatibility["score"],
        "common_values": compatibility["shared_values"],
        "match_description": compatibility["description"]
    }

@router.get("/{match_id}", response_model=MatchDetailResponse)
async def get_match_details(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific match
    """
    match = db.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Verify current user is part of this match
    if match.user_id_1 != current_user.user_id and match.user_id_2 != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this match")
    
    # Determine which user to show details for (the one that's not the current user)
    if match.user_id_1 == current_user.user_id:
        match_user_id = match.user_id_2
    else:
        match_user_id = match.user_id_1
    
    # Get user and profile
    match_user = db.query(User).filter(User.user_id == match_user_id).first()
    match_profile = db.query(Profile).filter(Profile.user_id == match_user_id).first()
    
    # Extract match data
    match_data = match.match_data or {}
    
    return {
        "match_id": match.match_id,
        "user_id": match_user.user_id,
        "username": match_user.username,
        "full_name": match_user.full_name,
        "profile_picture_url": match_profile.profile_picture_url or "",
        "bio": match_profile.bio,
        "location": match_profile.location,
        "compatibility_score": match.compatibility_score,
        "compatibility_breakdown": match_data.get("compatibility_breakdown", {}),
        "shared_interests": match_data.get("shared_interests", []),
        "shared_values": match_data.get("shared_values", []),
        "complementary_traits": match_data.get("complementary_traits", []),
        "match_created_at": match.created_at.isoformat()
    }