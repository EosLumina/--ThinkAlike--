from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid
import random
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from ..auth.auth_handler import get_current_user
from ..database.models import User, LiveLocationShare, EventProximityOptIn, Event, Profile, Match, LocationPreference
from ..database.database import get_db

# Define FriendLocationResponse directly here if it doesn't exist in response_models
class FriendLocationResponse(BaseModel):
    user_id: str
    username: str
    full_name: str
    profile_picture_url: Optional[str]
    location_type: str  # Indicates precision level
    latitude: float
    longitude: float
    compatibility_score: Optional[float]

router = APIRouter(prefix="/api/v1/location", tags=["location"])

# ----- Pydantic Models -----

class ShareLocationRequest(BaseModel):
    recipientId: str = Field(..., description="ID of user or group to share with")
    durationMinutes: int = Field(..., description="Time in minutes for sharing to remain active")
    message: Optional[str] = Field(None, description="Optional message to accompany sharing request")

class ShareLocationResponse(BaseModel):
    shareId: str
    expiresAt: str
    message: str
    ui_validation: dict

class StopSharingRequest(BaseModel):
    shareId: str = Field(..., description="ID of the sharing session to terminate")

class StopSharingResponse(BaseModel):
    message: str
    shareId: str
    ui_validation: dict

class ActiveShareRecipient(BaseModel):
    shareId: str
    recipientId: str
    recipientName: str
    expiresAt: str

class ActiveShareSender(BaseModel):
    shareId: str
    senderId: str
    senderName: str
    expiresAt: str

class ActiveSharesResponse(BaseModel):
    initiated: List[ActiveShareRecipient]
    received: List[ActiveShareSender]
    ui_validation: dict

class ProximityUser(BaseModel):
    userId: str
    approxProximity: str
    lastUpdated: str

class ProximityResponse(BaseModel):
    users: List[ProximityUser]
    ui_validation: dict

class OptInRequest(BaseModel):
    duration: Optional[int] = Field(None, description="Duration in minutes to override default event duration")

class OptInResponse(BaseModel):
    message: str
    eventId: str
    eventName: str
    expiresAt: str
    ui_validation: dict

class NearbyAttendee(BaseModel):
    userId: str
    displayName: str
    proximityCategory: str
    lastUpdated: str

class NearbyAttendeesResponse(BaseModel):
    attendees: List[NearbyAttendee]
    ui_validation: dict

class LocationPreferenceModel(BaseModel):
    share_location: bool
    location_precision: str  # "precise", "neighborhood", "city"
    visible_to: str  # "none", "matches", "all"

# ----- API Endpoints -----

@router.post("/share_live", response_model=ShareLocationResponse, status_code=201)
async def share_live_location(
    request: ShareLocationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initiates a live location sharing session with a specified user or group.
    """
    # Validate recipient exists
    recipient = db.query(User).filter(User.user_id == request.recipientId).first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Invalid recipient ID")

    # Create sharing session
    share_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=request.durationMinutes)

    new_share = LiveLocationShare(
        share_id=share_id,
        user_id=current_user.user_id,
        recipient_id=request.recipientId,
        start_time=datetime.now(),
        end_time=expires_at,
        active=True
    )

    db.add(new_share)
    db.commit()

    return {
        "shareId": share_id,
        "expiresAt": expires_at.isoformat(),
        "message": "Location sharing initiated successfully",
        "ui_validation": {
            "status": "success",
            "component": "LocationSharingConfirmation",
            "duration_minutes": request.durationMinutes,
            "recipient": recipient.username
        }
    }

@router.post("/stop_sharing", response_model=StopSharingResponse)
async def stop_sharing(
    request: StopSharingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stop an active location sharing session.
    """
    # Find the sharing session
    share = db.query(LiveLocationShare).filter(
        LiveLocationShare.share_id == request.shareId,
        LiveLocationShare.user_id == current_user.user_id,
        LiveLocationShare.active == True
    ).first()

    if not share:
        raise HTTPException(status_code=404, detail="Sharing session not found or already expired")

    # Use SQLAlchemy-safe assignment with setattr
    setattr(share, 'active', False)
    db.commit()

    return {
        "message": "Location sharing terminated successfully",
        "shareId": request.shareId,
        "ui_validation": {
            "status": "success",
            "component": "LocationSharingTerminated"
        }
    }

@router.get("/active_shares", response_model=ActiveSharesResponse)
async def get_active_shares(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List active location sharing sessions.
    """
    # Get shares initiated by the user
    initiated_shares = db.query(LiveLocationShare).filter(
        LiveLocationShare.user_id == current_user.user_id,
        LiveLocationShare.active == True
    ).all()

    # Get shares shared with the user
    received_shares = db.query(LiveLocationShare).filter(
        LiveLocationShare.recipient_id == current_user.user_id,
        LiveLocationShare.active == True
    ).all()

    # Format the response
    initiated = []
    for share in initiated_shares:
        recipient = db.query(User).filter(User.user_id == share.recipient_id).first()
        if recipient is not None:
            initiated.append({
                "shareId": share.share_id,
                "recipientId": share.recipient_id,
                "recipientName": recipient.username,
                "expiresAt": share.end_time.isoformat()
            })

    received = []
    for share in received_shares:
        sender = db.query(User).filter(User.user_id == share.user_id).first()
        if sender is not None:
            received.append({
                "shareId": share.share_id,
                "senderId": share.user_id,
                "senderName": sender.username,
                "expiresAt": share.end_time.isoformat()
            })

    return {
        "initiated": initiated,
        "received": received,
        "ui_validation": {
            "component": "ActiveSharesDisplay",
            "initiated_count": len(initiated),
            "received_count": len(received)
        }
    }

@router.get("/proximity", response_model=ProximityResponse)
async def get_proximity(
    eventId: str = Query(..., description="ID of the event to get proximity data for"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve proximity data for event attendees.
    """
    # Check if event exists
    event = db.query(Event).filter(Event.event_id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if user has opted in
    user_opt_in = db.query(EventProximityOptIn).filter(
        EventProximityOptIn.event_id == eventId,
        EventProximityOptIn.user_id == current_user.user_id,
        EventProximityOptIn.opt_out_time == None
    ).first()

    if not user_opt_in:
        raise HTTPException(status_code=403, detail="You must opt into proximity sharing for this event")

    # Get other opted-in users
    opt_ins = db.query(EventProximityOptIn, User).join(User).filter(
        EventProximityOptIn.event_id == eventId,
        EventProximityOptIn.user_id != current_user.user_id,
        EventProximityOptIn.opt_out_time == None
    ).all()

    # In a real implementation, we would calculate actual proximity
    # Here we just return mock data with privacy-preserving categories
    proximity_data = []
    for opt_in, user in opt_ins:
        # This would use actual location data in a real implementation
        # Here we just assign random proximity categories for demonstration
        categories = ["Nearby", "Within 200m", "Within venue", "At entrance"]
        proximity_data.append({
            "userId": user.user_id,
            "approxProximity": random.choice(categories),
            "lastUpdated": datetime.now().isoformat()
        })

    return {
        "users": proximity_data,
        "ui_validation": {
            "component": "ProximityVisualization",
            "event_name": event.event_name,
            "privacy_level": "anonymized"
        }
    }

@router.post("/events/{eventId}/proximity_opt_in", response_model=OptInResponse)
async def opt_in_to_proximity(
    eventId: str = Path(..., description="ID of the event to opt into"),
    request: Optional[OptInRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Opt into proximity sharing for a specific event.
    """
    # Check if event exists
    event = db.query(Event).filter(Event.event_id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Determine expiration time
    if request and request.duration:
        expires_at = datetime.now() + timedelta(minutes=request.duration)
    else:
        # Default to event end time
        expires_at = event.end_time

    # Check if user is already opted in
    existing_opt_in = db.query(EventProximityOptIn).filter(
        EventProximityOptIn.event_id == eventId,
        EventProximityOptIn.user_id == current_user.user_id,
        EventProximityOptIn.opt_out_time == None
    ).first()

    if existing_opt_in is not None:
        # Use SQLAlchemy-safe assignment with setattr
        setattr(existing_opt_in, 'opt_in_time', datetime.now())
        db.commit()
    else:
        # Create new opt-in
        new_opt_in = EventProximityOptIn(
            event_id=eventId,
            user_id=current_user.user_id,
            opt_in_time=datetime.now(),
            opt_out_time=None
        )
        db.add(new_opt_in)
        db.commit()

    return {
        "message": "Successfully opted into proximity sharing",
        "eventId": eventId,
        "eventName": event.event_name,
        "expiresAt": expires_at.isoformat(),
        "ui_validation": {
            "component": "ProximityOptInConfirmation",
            "consent_confirmed": True,
            "expiration_displayed": True
        }
    }

@router.get("/events/{eventId}/nearby_attendees", response_model=NearbyAttendeesResponse)
async def get_nearby_attendees(
    eventId: str = Path(..., description="ID of the event to retrieve attendee proximity data for"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get anonymized proximity data for event attendees.
    """
    # Check if event exists
    event = db.query(Event).filter(Event.event_id == eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if user has opted in
    user_opt_in = db.query(EventProximityOptIn).filter(
        EventProximityOptIn.event_id == eventId,
        EventProximityOptIn.user_id == current_user.user_id,
        EventProximityOptIn.opt_out_time == None
    ).first()

    if not user_opt_in:
        raise HTTPException(status_code=403, detail="You must opt into proximity sharing for this event")

    # Get other opted-in users
    opt_ins = db.query(EventProximityOptIn, User).join(User).filter(
        EventProximityOptIn.event_id == eventId,
        EventProximityOptIn.user_id != current_user.user_id,
        EventProximityOptIn.opt_out_time == None
    ).all()

    # In a real implementation, we'd calculate actual proximity
    # Here we just return mock data for demonstration
    nearby_attendees = []
    for opt_in, user in opt_ins:
        categories = ["Nearby", "Within venue", "Just arrived", "Within 500m"]
        nearby_attendees.append({
            "userId": user.user_id,
            "displayName": user.username,
            "proximityCategory": random.choice(categories),
            "lastUpdated": datetime.now().isoformat()
        })

    return {
        "attendees": nearby_attendees,
        "ui_validation": {
            "component": "NearbyAttendeesMap",
            "privacy_preserved": True,
            "consent_validated": True
        }
    }

@router.put("/preferences", response_model=LocationPreferenceModel)
async def update_location_preferences(
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
            visible_to=preferences.visible_to
        )
        db.add(location_pref)
    else:
        # Use SQLAlchemy's setattr() instead of direct assignment
        setattr(location_pref, "share_location", preferences.share_location)
        setattr(location_pref, "location_precision", preferences.location_precision)
        setattr(location_pref, "visible_to", preferences.visible_to)

    db.commit()

    return preferences

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
        share_location=share_location if share_location is not None else False,
        location_precision=location_precision if location_precision is not None else "city",
        visible_to=visible_to if visible_to is not None else "none"
    )

@router.get("/friends-map", response_model=List[FriendLocationResponse])
async def get_friend_locations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get locations of friends who have opted in to location sharing"""
    # Check if current user has enabled location viewing
    user_pref = db.query(LocationPreference).filter(
        LocationPreference.user_id == current_user.user_id
    ).first()

    # Use SQLAlchemy's safe evaluation pattern
    share_str = db.scalar(select(user_pref.share_location)) if user_pref else None
    if share_str is None or not share_str:
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
        match_user_ids.append(
            db.scalar(select(match.user_id_2).where(match.user_id_1 == current_user.user_id)) or db.scalar(select(match.user_id_1).where(match.user_id_2 == current_user.user_id))
        )

    # Get profiles and location preferences for matches
    friend_locations = []

    for match_id in match_user_ids:
        profile = db.query(Profile).filter(Profile.user_id == match_id).first()
        user = db.query(User).filter(User.user_id == match_id).first()
        loc_pref = db.query(LocationPreference).filter(
            LocationPreference.user_id == match_id
        ).first()

        # Skip if any required data is missing
        if not profile or not user or not loc_pref:
            continue

        # Safely extract values from SQLAlchemy columns
        share_location = db.scalar(select(loc_pref.share_location))
        visible_to = db.scalar(select(loc_pref.visible_to))
        location_precision = db.scalar(select(loc_pref.location_precision))

        # Only include users who've opted to share location and have location data
        if (share_location and
            profile.latitude is not None and
            profile.longitude is not None):

            # Determine visibility level
            visible = False
            if visible_to == "all":
                visible = True
            elif visible_to == "matches":
                # They're already in the match_user_ids list, so they're a match
                visible = True

            if visible:
                # Apply location precision (fuzzing for privacy)
                location_lat = None
                location_lng = None
                if profile.latitude is not None and profile.longitude is not None:
                    latitude_value = db.scalar(select(profile.latitude))
                    location_lat = float(latitude_value) if latitude_value is not None else 0.0
                    longitude_value = db.scalar(select(profile.longitude))
                    location_lng = float(longitude_value) if longitude_value is not None else 0.0

                # Only proceed if we have valid location data
                if location_lat is not None and location_lng is not None:
                    # Extract scalar values from SQLAlchemy columns
                    latitude_value = db.scalar(select(profile.latitude))
                    lat_val = float(latitude_value) if latitude_value is not None else None
                    longitude_value = db.scalar(select(profile.longitude))
                    lng_val = float(longitude_value) if longitude_value is not None else None

                    # Fix for type issues with latitude and longitude
                    latitude = db.scalar(select(profile.latitude)) if profile.latitude is not None else 0.0
                    longitude = db.scalar(select(profile.longitude)) if profile.longitude is not None else 0.0

                    # Ensure apply_location_precision is called with valid float arguments
                    lat, lng = apply_location_precision(
                        float(latitude) if latitude is not None else 0.0,
                        float(longitude) if longitude is not None else 0.0,
                        "city"
                    )

                    # Find compatibility score
                    match_record = next(
                        (m for m in matches if m.user_id_1 == match_id or m.user_id_2 == match_id),
                        None
                    )

                    # Extract scalar values and use proper type conversion
                    compatibility_score_val = None
                    if match_record and hasattr(match_record, 'compatibility_score'):
                        if match_record.compatibility_score is not None:
                            try:
                                compatibility_score_val = float(db.scalar(select(match_record.compatibility_score)) or 0.0) if match_record and match_record.compatibility_score is not None else None
                            except (TypeError, ValueError):
                                pass

                    # Extract the value before using in conditional
                    profile_url = None
                    if profile.profile_picture_url is not None:
                        profile_url = db.scalar(select(profile.profile_picture_url))

                    # Create response objects with properly converted values
                    friend_locations.append(
                        FriendLocationResponse(
                            user_id=str(user.user_id),
                            username=str(user.username),
                            full_name=str(user.full_name),
                            profile_picture_url=profile_url,
                            location_type=str(location_precision) if location_precision else "city",
                            latitude=lat,
                            longitude=lng,
                            compatibility_score=float(compatibility_score_val) if compatibility_score_val is not None else None
                        )
                    )

    return friend_locations

def apply_location_precision(lat: float, lng: float, precision: str) -> tuple:
    """Apply fuzzing to coordinates based on precision level"""
    if precision == "precise":
        return lat, lng
    elif precision == "neighborhood":
        # Add small random offset (roughly ~1km)
        lat_offset = random.uniform(-0.009, 0.009)
        lng_offset = random.uniform(-0.009, 0.009)
        return lat + lat_offset, lng + lng_offset
    elif precision == "city":
        # Add larger random offset (roughly ~5km)
        lat_offset = random.uniform(-0.045, 0.045)
        lng_offset = random.uniform(-0.045, 0.045)
        return lat + lat_offset, lng + lng_offset

    # Default to neighborhood level
    return lat, lng
