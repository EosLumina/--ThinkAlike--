from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
import random

from ..auth.auth_handler import get_current_user
from ..database.models import User, Profile, Match, LocationPreference
from ..database.database import get_db

class LocationPreferenceModel(BaseModel):
    share_location: bool
    location_precision: str  # "precise", "neighborhood", "city"
    visible_to: str  # "none", "matches", "all"

class FriendLocationResponse(BaseModel):
    user_id: str
    username: str
    full_name: str
    profile_picture_url: Optional[str]
    location_type: str  # Indicates precision level
    latitude: float
    longitude: float
    compatibility_score: Optional[float]

router = APIRouter(prefix="/api/v1/friend-maps", tags=["friend-maps"])

@router.put("/preferences", response_model=LocationPreferenceModel)
async def update_user_location_preferences(
    preferences: LocationPreferenceModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's location sharing preferences"""
    # Get or create location preference
    location_pref = db.query(LocationPreference).filter(
        LocationPreference.user_id == current_user.user_id
    ).first()

    if not location_pref:
        location_pref = LocationPreference(
            user_id=current_user.user_id,
            share_location=preferences.share_location,
            location_precision=preferences.location_precision,
            visible_to=preferences.visible_to if preferences.visible_to is not None else "friends"
        )
        db.add(location_pref)
    else:
        # Use setattr for SQLAlchemy model updates
        setattr(location_pref, "share_location", preferences.share_location)
        setattr(location_pref, "location_precision", preferences.location_precision)
        setattr(location_pref, "visible_to", preferences.visible_to if preferences.visible_to is not None else "friends")

    db.commit()
    db.refresh(location_pref)

    return LocationPreferenceModel(
        share_location=bool(db.scalar(select(location_pref.share_location))),
        location_precision=str(db.scalar(select(location_pref.location_precision))),
        visible_to=str(db.scalar(select(location_pref.visible_to)))
    )

@router.get("/map", response_model=List[FriendLocationResponse])
async def get_friends_map(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get locations of connections who have opted in to location sharing"""
    # Check if current user has enabled location viewing
    user_pref = db.query(LocationPreference).filter(
        LocationPreference.user_id == current_user.user_id
    ).first()

    if not user_pref or not db.scalar(select(user_pref.share_location)):
        raise HTTPException(
            status_code=400,
            detail="You must enable location sharing to see others' locations"
        )

    # Get all matches for current user
    matches = db.query(Match).filter(
        or_(
            Match.user_id_1 == current_user.user_id,
            Match.user_id_2 == current_user.user_id
        )
    ).all()

    match_user_ids = []
    for match in matches:
        if match.user_id_1.is_(current_user.user_id):
            match_user_ids.append(match.user_id_2)
        else:
            match_user_ids.append(match.user_id_1)

    friend_locations = []
    for match_id in match_user_ids:
        profile = db.query(Profile).filter(Profile.user_id == match_id).first()
        user = db.query(User).filter(User.user_id == match_id).first()

        if not profile or not user:
            continue

        if profile.latitude is None or profile.longitude is None:
            continue

        # Extract scalar values and convert to proper types
        latitude = float(db.scalar(select(profile.latitude)) or 0.0)
        longitude_value = db.scalar(select(profile.longitude))
        longitude = float(longitude_value) if longitude_value is not None else 0.0

        # Apply location precision
        location_precision = db.scalar(select(profile.location_precision)) or "city"
        lat, lng = apply_location_precision(latitude, longitude, location_precision)

        # Find compatibility score
        match_record = next(
            (m for m in matches if m.user_id_1 == match_id or m.user_id_2 == match_id),
            None
        )
        compatibility_score = (
            float(db.scalar(select(match_record.compatibility_score)) or 0.0)
            if match_record and match_record.compatibility_score is not None
            else None
        )

        # Construct response object
        friend_locations.append(
            FriendLocationResponse(
                user_id=str(user.user_id),
                username=str(user.username),
                full_name=str(user.full_name),
                profile_picture_url=str(db.scalar(select(profile.profile_picture_url))) if db.scalar(select(profile.profile_picture_url)) else None,
                location_type=location_precision,
                latitude=lat,
                longitude=lng,
                compatibility_score=compatibility_score
            )
        )

    return friend_locations

@router.get("/preferences", response_model=LocationPreferenceModel)
async def get_location_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's location sharing preferences"""
    location_pref = db.query(LocationPreference).filter(
        LocationPreference.user_id == current_user.user_id
    ).first()

    if not location_pref:
        return LocationPreferenceModel(
            share_location=False,
            location_precision="city",
            visible_to="friends"
        )

    # Extract scalar values from SQLAlchemy columns
    share_location = db.scalar(select(location_pref.share_location))
    location_precision = db.scalar(select(location_pref.location_precision))
    visible_to = db.scalar(select(location_pref.visible_to))

    return LocationPreferenceModel(
        share_location=bool(share_location if share_location is not None else False),
        location_precision=str(location_precision if location_precision is not None else "city"),
        visible_to=str(visible_to if visible_to is not None else "friends")
    )

def apply_location_precision(lat: float, lng: float, precision: str) -> tuple:
    """Apply fuzzing to coordinates based on precision level"""
    if precision == "precise":
        return lat, lng
    elif precision == "neighborhood":
        lat_offset = random.uniform(-0.009, 0.009)
        lng_offset = random.uniform(-0.009, 0.009)
        return lat + lat_offset, lng + lng_offset
    elif precision == "city":
        lat_offset = random.uniform(-0.045, 0.045)
        lng_offset = random.uniform(-0.045, 0.045)
        return lat + lat_offset, lng + lng_offset
    return lat, lng
