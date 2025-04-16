"""
ThinkAlike Recognition System

This module defines the badge and rank systems that recognize contributor
achievements while embodying our revolutionary principles of inclusion,
diversity of contribution, and rejection of traditional hierarchies.

Unlike conventional achievement systems that reinforce power structures,
ThinkAlike's recognition constellation creates multiple valid paths
of advancement and celebrates diverse forms of revolutionary work.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ContributionType(str, Enum):
    """Types of valuable contributions to the liberation movement."""
    CODE = "code"                 # Technical implementation
    DOCUMENTATION = "documentation"  # Knowledge sharing and explanation
    DESIGN = "design"             # User interface and experience design
    REVIEW = "review"             # Code and documentation review
    COMMUNITY = "community"       # Community building and support
    PHILOSOPHICAL = "philosophical"  # Ethical and conceptual development
    TESTING = "testing"           # Quality assurance and validation
    ACCESSIBILITY = "accessibility"  # Making the project more accessible


class RevolutionaryRank(str, Enum):
    """
    Ranks representing depth of contribution to the liberation movement.
    
    These ranks deliberately avoid traditional hierarchical language,
    instead using astronomical metaphors that emphasize different types
    of contribution rather than "higher" and "lower" positions.
    """
    NOVA = "nova"                 # New contributors (bright, energetic)
    PULSAR = "pulsar"             # Regular contributors (consistent impact)
    QUASAR = "quasar"             # Major contributors (far-reaching influence)
    SUPERNOVA = "supernova"       # Transformative contributors (expansive impact)
    NEBULA = "nebula"             # Community-building contributors (nurturing)
    GALAXY = "galaxy"             # Holistic contributors (integrating many aspects)


class BadgeCategory(str, Enum):
    """Categories of badges representing different contribution areas."""
    TECHNICAL = "technical"       # Technical implementation achievements
    PHILOSOPHICAL = "philosophical"  # Ethical and conceptual contributions
    COMMUNITY = "community"       # Community building and support
    EDUCATIONAL = "educational"   # Learning and knowledge sharing
    REVOLUTIONARY = "revolutionary"  # Special achievements aligned with core principles


class Badge(BaseModel):
    """
    A badge representing a specific achievement or contribution.
    
    Badges embody our principle of recognizing diverse forms of
    contribution beyond just code, celebrating the many ways
    people can participate in digital liberation.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    category: BadgeCategory
    image_url: str
    contribution_types: List[ContributionType]
    requirements: Dict[str, str]  # Key-value pairs of requirement descriptions
    points_value: int = 1         # Contribution points for rank advancement
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True


class ContributorRecognition(BaseModel):
    """
    Recognition profile for a contributor, tracking badges and rank.
    
    This model embodies our revolutionary approach to recognition,
    celebrating diverse contributions and providing multiple paths
    for advancement without creating traditional hierarchies.
    """
    contributor_id: UUID
    badges: List[UUID] = Field(default_factory=list)
    total_points: int = 0
    rank: RevolutionaryRank = RevolutionaryRank.NOVA
    contribution_types: Set[ContributionType] = Field(default_factory=set)
    first_contribution_at: Optional[datetime] = None
    latest_contribution_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BadgeAward(BaseModel):
    """
    Record of a badge being awarded to a contributor.
    
    This model provides transparent tracking of recognition,
    embodying our principle of radical transparency.
    """
    id: UUID = Field(default_factory=uuid4)
    badge_id: UUID
    contributor_id: UUID
    quest_id: Optional[UUID] = None
    contribution_description: str
    awarded_at: datetime = Field(default_factory=datetime.now)
    awarded_by: Optional[UUID] = None  # Administrator or automated system
    
    class Config:
        from_attributes = True


class RankAdvancement(BaseModel):
    """
    Record of a contributor advancing to a new rank.
    
    This model tracks the revolutionary journey of contributors
    as they deepen their participation in digital liberation.
    """
    id: UUID = Field(default_factory=uuid4)
    contributor_id: UUID
    previous_rank: Optional[RevolutionaryRank] = None
    new_rank: RevolutionaryRank
    advancement_reason: str
    badges_count: int
    total_points: int
    advanced_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True