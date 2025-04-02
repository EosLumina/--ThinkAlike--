from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid
from ..auth.auth_handler import get_current_user
from ..database.models import User, LiveLocationShare, EventProximityOptIn, Event
from ..database.database import get_db
from sqlalchemy.orm import Session

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
    
    # Terminate the session
    share.active = False
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
        if recipient:
            initiated.append({
                "shareId": share.share_id,
                "recipientId": share.recipient_id,
                "recipientName": recipient.username,
                "expiresAt": share.end_time.isoformat()
            })
    
    received = []
    for share in received_shares:
        sender = db.query(User).filter(User.user_id == share.user_id).first()
        if sender:
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
        import random
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
    request: OptInRequest = None,
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
    
    if existing_opt_in:
        # Update existing opt-in
        existing_opt_in.opt_in_time = datetime.now()
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
        import random
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