from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from ..auth.auth_handler import get_current_user
from ..database.models import User, Community, Event, user_communities
from ..database.database import get_db

router = APIRouter(prefix="/api/v1/communities", tags=["communities"])

# Models
class CommunityCreate(BaseModel):
    community_name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10)

class CommunityResponse(BaseModel):
    community_id: str
    community_name: str
    description: str
    member_count: int
    is_member: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class CommunityDetailResponse(BaseModel):
    community_id: str
    community_name: str
    description: str
    member_count: int
    is_member: bool
    created_at: datetime
    upcoming_events: List[dict]
    
    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    event_name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    location: str = Field(..., min_length=3)
    start_time: datetime
    end_time: datetime
    geofence_parameters: Optional[dict] = None

class EventResponse(BaseModel):
    event_id: str
    event_name: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime
    community_name: str
    attendee_count: int
    is_attending: bool
    
    class Config:
        orm_mode = True

# API Endpoints
@router.post("/", response_model=CommunityResponse, status_code=201)
async def create_community(
    community: CommunityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new community"""
    # Check if name is taken
    existing = db.query(Community).filter(Community.community_name == community.community_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Community name is already taken")
    
    # Create community
    new_community = Community(
        community_name=community.community_name,
        description=community.description
    )
    
    db.add(new_community)
    db.commit()
    db.refresh(new_community)
    
    # Add creator as member
    new_community.members.append(current_user)
    db.commit()
    
    return {
        "community_id": new_community.community_id,
        "community_name": new_community.community_name,
        "description": new_community.description,
        "member_count": 1,
        "is_member": True,
        "created_at": new_community.created_at
    }

@router.get("/", response_model=List[CommunityResponse])
async def list_communities(
    search: Optional[str] = Query(None, description="Search term for community name or description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all communities with optional search"""
    query = db.query(Community)
    
    # Apply search if provided
    if search:
        query = query.filter(
            (Community.community_name.ilike(f"%{search}%")) | 
            (Community.description.ilike(f"%{search}%"))
        )
    
    communities = query.all()
    
    # Get current user's memberships for is_member flag
    user_community_ids = [c.community_id for c in current_user.communities]
    
    # Format response
    results = []
    for community in communities:
        member_count = len(community.members)
        results.append({
            "community_id": community.community_id,
            "community_name": community.community_name,
            "description": community.description,
            "member_count": member_count,
            "is_member": community.community_id in user_community_ids,
            "created_at": community.created_at
        })
    
    return results

@router.get("/{community_id}", response_model=CommunityDetailResponse)
async def get_community(
    community_id: str = Path(..., description="ID of the community to retrieve"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a community"""
    community = db.query(Community).filter(Community.community_id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if user is a member
    is_member = current_user in community.members
    
    # Get upcoming events for this community
    upcoming_events = db.query(Event).filter(
        Event.community_id == community_id,
        Event.end_time > datetime.utcnow()
    ).order_by(Event.start_time.asc()).all()
    
    # Format events
    event_list = []
    for event in upcoming_events:
        event_list.append({
            "event_id": event.event_id,
            "event_name": event.event_name,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "location": event.location
        })
    
    return {
        "community_id": community.community_id,
        "community_name": community.community_name,
        "description": community.description,
        "member_count": len(community.members),
        "is_member": is_member,
        "created_at": community.created_at,
        "upcoming_events": event_list
    }

@router.post("/{community_id}/join")
async def join_community(
    community_id: str = Path(..., description="ID of the community to join"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a community"""
    community = db.query(Community).filter(Community.community_id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if already a member
    if current_user in community.members:
        raise HTTPException(status_code=400, detail="You are already a member of this community")
    
    # Add user to community
    community.members.append(current_user)
    db.commit()
    
    return {"message": f"Successfully joined {community.community_name}"}

@router.post("/{community_id}/leave")
async def leave_community(
    community_id: str = Path(..., description="ID of the community to leave"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Leave a community"""
    community = db.query(Community).filter(Community.community_id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if a member
    if current_user not in community.members:
        raise HTTPException(status_code=400, detail="You are not a member of this community")
    
    # Remove user from community
    community.members.remove(current_user)
    db.commit()
    
    return {"message": f"Successfully left {community.community_name}"}

@router.post("/{community_id}/events", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    community_id: str = Path(..., description="ID of the community to create the event for"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new event for a community"""
    # Check if community exists
    community = db.query(Community).filter(Community.community_id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if user is a member
    if current_user not in community.members:
        raise HTTPException(status_code=403, detail="Only community members can create events")
    
    # Validate times
    if event.start_time >= event.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    if event.start_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Start time cannot be in the past")
    
    # Create event
    new_event = Event(
        community_id=community_id,
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
    
    return {
        "event_id": new_event.event_id,
        "event_name": new_event.event_name,
        "description": new_event.description,
        "location": new_event.location,
        "start_time": new_event.start_time,
        "end_time": new_event.end_time,
        "community_name": community.community_name,
        "attendee_count": 0,  # No attendees yet
        "is_attending": False  # Creator isn't automatically attending
    }