"""
ThinkAlike Quest System

This module defines the data models for the quest-based contribution system
that transforms technical development into an accessible journey of
digital liberation.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class QuestDifficulty(str, Enum):
    """Difficulty levels for quests to accommodate various skill levels."""
    NEWCOMER = "newcomer"       # No technical background needed
    EASY = "easy"               # Basic technical skills
    MEDIUM = "medium"           # Intermediate skills required
    CHALLENGING = "challenging" # Advanced technical knowledge needed
    MULTI_LEVEL = "multi_level" # Contains tasks for various skill levels


class ContributorRole(str, Enum):
    """Roles contributors can take in completing quests."""
    PHILOSOPHER = "philosopher" # Conceptual and ethical thinking
    DESIGNER = "designer"       # User experience and interface design
    DEVELOPER = "developer"     # Code implementation
    TESTER = "tester"           # Testing and validation
    DOCUMENTER = "documenter"   # Documentation and explanation
    COMMUNITY = "community"     # Community building and support


class QuestPath(BaseModel):
    """A specific path within a quest for a particular contributor role."""
    role: ContributorRole
    task: str
    requirements: List[str] = Field(default_factory=list)
    resources: List[Dict[str, str]] = Field(default_factory=list)


class QuestReward(BaseModel):
    """Rewards for completing a quest, supporting gamification."""
    name: str
    description: str
    badge_image_url: Optional[str] = None


class Quest(BaseModel):
    """
    A quest representing a contribution opportunity within ThinkAlike.
    
    Quests embody our revolutionary approach to development by making
    contribution accessible to all, regardless of technical background.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    difficulty: QuestDifficulty
    paths: List[QuestPath] = Field(default_factory=list)
    rewards: List[QuestReward] = Field(default_factory=list)
    prerequisites: List[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True


class QuestProgress(BaseModel):
    """Tracks a contributor's progress on a specific quest."""
    contributor_id: UUID
    quest_id: UUID
    selected_path: Optional[ContributorRole] = None
    progress_percentage: float = 0.0
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    notes: str = ""
    
    class Config:
        from_attributes = True
