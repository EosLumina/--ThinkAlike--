from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, JSON, Table, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

Base = declarative_base()

# Enum types
class AccessControlLevel(enum.Enum):
    PUBLIC = "public"
    REGISTERED = "registered"
    PRIVATE = "private"

# Models
class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    communities = relationship("UserCommunity", back_populates="user")
    initiated_shares = relationship("LiveLocationShare",
                                   foreign_keys="LiveLocationShare.user_id",
                                   back_populates="user")
    location_preference = relationship("LocationPreference", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"

    profile_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), unique=True, nullable=False)
    bio = Column(Text)
    birthdate = Column(DateTime)
    location = Column(String)
    profile_picture_url = Column(String)
    static_location_city = Column(String)
    static_location_country = Column(String)

    # Relationships
    user = relationship("User", back_populates="profile")

class Community(Base):
    __tablename__ = "communities"

    community_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    community_name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    users = relationship("UserCommunity", back_populates="community")
    events = relationship("Event", back_populates="community")

class UserCommunity(Base):
    __tablename__ = "user_communities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    community_id = Column(String, ForeignKey("communities.community_id"), nullable=False)
    join_date = Column(DateTime, default=datetime.now)

    # Unique constraint to prevent duplicate memberships
    __table_args__ = (UniqueConstraint("user_id", "community_id", name="uq_user_community"),)

    # Relationships
    user = relationship("User", back_populates="communities")
    community = relationship("Community", back_populates="users")

class Match(Base):
    __tablename__ = "matches"

    match_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id_1 = Column(String, ForeignKey("users.user_id"), nullable=False)
    user_id_2 = Column(String, ForeignKey("users.user_id"), nullable=False)
    match_data = Column(JSON)
    compatibility_score = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

    # Unique constraint to prevent duplicate matches
    __table_args__ = (UniqueConstraint("user_id_1", "user_id_2", name="uq_user_match"),)

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    community_id = Column(String, ForeignKey("communities.community_id"), nullable=False)
    event_name = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    geofence_parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    community = relationship("Community", back_populates="events")
    proximity_opt_ins = relationship("EventProximityOptIn", back_populates="event")

class LiveLocationShare(Base):
    __tablename__ = "live_location_shares"

    share_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    recipient_id = Column(String, nullable=False)  # Could be user_id or community_id
    start_time = Column(DateTime, default=datetime.now, nullable=False)
    end_time = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="initiated_shares")

class EventProximityOptIn(Base):
    __tablename__ = "event_proximity_opt_ins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, ForeignKey("events.event_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    opt_in_time = Column(DateTime, default=datetime.now, nullable=False)
    opt_out_time = Column(DateTime)

    # Unique constraint to prevent duplicate opt-ins
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_user_opt_in"),)

    # Relationships
    event = relationship("Event", back_populates="proximity_opt_ins")

class LocationPreference(Base):
    __tablename__ = "location_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), unique=True)
    share_location = Column(Boolean, default=False)
    location_precision = Column(String, default="neighborhood")  # precise, neighborhood, city
    visible_to = Column(String, default="matches")  # none, matches, all
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="location_preference")
