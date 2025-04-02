from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..auth.auth_handler import get_current_user
from ..database.models import User, Community, Event, EventProximityOptIn
from ..database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/events", tags=["events"])

# ----- Pydantic Models -----

class EventBase(BaseModel):
    event_name: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    geofence_parameters: Optional[dict] = None

class EventCreate(EventBase):
    community_id: str

class EventResponse(EventBase):
    event_id: str
    community_id: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class EventList(BaseModel):
    events: List[EventResponse]

# ----- API Endpoints -----

@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new event for a community.
    """
    # Verify community exists
    community = db.query(Community).filter(Community.community_id == event.community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if user is part of the community
    # This would depend on your community membership model
    # For simplicity, we'll assume users can add events to any community
    
    # Create event
    new_event = Event(
        event_id=str(uuid.uuid4()),
        community_id=event.community_id,
        event_name=event.event_name,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        geofence_parameters=event.geofence_parameters
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event

@router.get("", response_model=EventList)
async def list_events(
    community_id: Optional[str] = None,
    upcoming_only: bool = Query(True, description="Only show upcoming events"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List events, optionally filtered by community.
    """
    query = db.query(Event)
    
    if community_id:
        query = query.filter(Event.community_id == community_id)
    
    if upcoming_only:
        query = query.filter(Event.end_time >= datetime.now())
    
    events = query.order_by(Event.start_time).all()
    
    return {"events": events}

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str = Path(..., description="The ID of the event to retrieve"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details for a specific event.
    """
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event

@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: str = Path(..., description="The ID of the event to delete"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an event.
    """
    event = db.query(Event).filter(Event.event_id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check authorization (this is simplified)
    # In a real app, check if current_user is event creator or community admin
    
    # Delete all proximity opt-ins first
    db.query(EventProximityOptIn).filter(EventProximityOptIn.event_id == event_id).delete()
    
    # Delete the event
    db.delete(event)
    db.commit()
    
    return None