"""
Family Tree and Digital Legacy models.

This module defines the data models for the Digital Legacy framework,
including family connections, legacy content, and legacy preferences.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4

from app.models.base import TimestampedModel
from app.models.user import User


class VerificationMethod(str, Enum):
    """Methods for verifying family connections."""
    MUTUAL_CONFIRMATION = "mutual_confirmation"
    DNA = "dna"
    DOCUMENTS = "documents"
    FAMILY_CONSENSUS = "family_consensus"
    HISTORICAL_RECORD = "historical_record"
    ACADEMIC_VERIFICATION = "academic_verification"


class RelationshipType(str, Enum):
    """Types of family relationships."""
    PARENT_CHILD_BIOLOGICAL = "parent_child_biological"
    PARENT_CHILD_ADOPTIVE = "parent_child_adoptive"
    PARENT_CHILD_STEP = "parent_child_step"
    SIBLING_FULL = "sibling_full"
    SIBLING_HALF = "sibling_half"
    SIBLING_STEP = "sibling_step"
    SPOUSE = "spouse"
    PARTNER = "partner"
    GRANDPARENT_GRANDCHILD = "grandparent_grandchild"
    AUNT_UNCLE_NIECE_NEPHEW = "aunt_uncle_niece_nephew"
    COUSIN = "cousin"
    CHOSEN_FAMILY = "chosen_family"
    GUARDIAN = "guardian"
    HISTORICAL_FIGURE = "historical_figure"
    CUSTOM = "custom"


class VerificationStatus(str, Enum):
    """Status of verification for family connections."""
    PENDING = "pending"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    REJECTED = "rejected"


class VisibilityLevel(str, Enum):
    """Visibility settings for family connections and legacy content."""
    PRIVATE = "private"  # Only self
    DIRECT_FAMILY = "direct_family"  # Parents, children, siblings, spouse
    EXTENDED_FAMILY = "extended_family"  # All connected family members
    SELECTED_INDIVIDUALS = "selected_individuals"  # Specific users
    PUBLIC = "public"  # Anyone can see


class ContentType(str, Enum):
    """Types of legacy content."""
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    STRUCTURED_DATA = "structured_data"


class PreservationLevel(str, Enum):
    """Levels of digital legacy preservation."""
    BASIC = "basic"  # Just factual information and direct recordings
    STANDARD = "standard"  # Includes some personality aspects
    COMPREHENSIVE = "comprehensive"  # Full personality preservation


class TimeRestriction(BaseModel):
    """Time-based access restrictions for legacy content."""
    restriction_type: str = Field(..., description="Type of time restriction")
    start_date: Optional[datetime] = Field(None, description="When access becomes available")
    end_date: Optional[datetime] = Field(None, description="When access expires")
    years_after_death: Optional[int] = Field(None, description="Years after death when content becomes available")


class RelationshipAccessRule(BaseModel):
    """Relationship-based access rules for legacy content."""
    relationship_types: List[RelationshipType] = Field(..., description="Types of relationships that can access")
    min_relationship_distance: Optional[int] = Field(None, description="Minimum relationship distance (e.g., 1 for direct)")
    max_relationship_distance: Optional[int] = Field(None, description="Maximum relationship distance")
    requires_verification: bool = Field(False, description="Whether relationship must be verified")


class Attachment(BaseModel):
    """Attachments for family connections."""
    id: UUID = Field(default_factory=uuid4)
    type: str
    url: str
    name: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EmotionalToneAnalysis(BaseModel):
    """Analysis of emotional tone in content."""
    primary_emotion: str
    emotion_scores: Dict[str, float]
    intensity: float
    confidence: float


class AccessControl(BaseModel):
    """Access control rules for legacy content."""
    rule_type: str
    parameters: Dict[str, Any]
    description: str


class FamilyConnection(TimestampedModel):
    """Model representing a connection between family members."""
    id: UUID = Field(default_factory=uuid4)
    source_user_id: UUID
    target_user_id: UUID
    relationship_type: RelationshipType
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verification_methods: List[VerificationMethod] = Field(default_factory=list)
    visibility: VisibilityLevel = VisibilityLevel.DIRECT_FAMILY
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "source_user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "target_user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "relationship_type": RelationshipType.PARENT_CHILD_BIOLOGICAL,
                "verification_status": VerificationStatus.VERIFIED,
                "verification_methods": [VerificationMethod.MUTUAL_CONFIRMATION],
                "visibility": VisibilityLevel.EXTENDED_FAMILY,
                "metadata": {
                    "notes": "Confirmed by both parties",
                    "start_date": "1980-01-01"
                }
            }
        }


class LegacyContent(TimestampedModel):
    """Model representing preserved legacy content."""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    content_type: ContentType
    content: Any  # Type varies based on content_type
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_direct_recording: bool = True
    confidence_score: Optional[float] = None
    source_materials: List[str] = Field(default_factory=list)
    verification_status: str = "verified"
    access_controls: List[AccessControl] = Field(default_factory=list)

    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        """Validate confidence score is between 0 and 1."""
        if v is not None and (v < 0 or v > 1):
            raise ValueError("Confidence score must be between 0 and 1")
        return v

    class Config:
        schema_extra = {
            "example": {
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "content_type": ContentType.TEXT,
                "content": "I grew up in a small town near the coast...",
                "metadata": {
                    "recorded_at": "2024-01-01T12:00:00Z",
                    "context": "Life story interview",
                    "topics": ["childhood", "hometown"]
                },
                "is_direct_recording": True,
                "access_controls": [
                    {
                        "rule_type": "relationship",
                        "parameters": {
                            "relationship_types": ["direct_family"],
                            "min_distance": 1
                        },
                        "description": "Available to direct family members"
                    }
                ]
            }
        }


class LegacyPreferences(BaseModel):
    """User preferences for digital legacy preservation."""
    is_enabled: bool = False
    preservation_level: PreservationLevel = PreservationLevel.BASIC
    access_controls: Dict[str, Any] = Field(
        default_factory=lambda: {
            "time_restrictions": [],
            "relationship_access": [
                {
                    "relationship_types": [RelationshipType.PARENT_CHILD_BIOLOGICAL,
                                         RelationshipType.PARENT_CHILD_ADOPTIVE],
                    "min_relationship_distance": 1,
                    "max_relationship_distance": 1,
                    "requires_verification": True
                }
            ],
            "public_availability": "none"
        }
    )
    ai_representation: Dict[str, Any] = Field(
        default_factory=lambda: {
            "allow_generation": False,
            "confidence_threshold": 0.85,
            "prohibited_topics": [],
            "allowed_data_sources": ["direct_recordings"]
        }
    )
    content_preferences: Dict[str, bool] = Field(
        default_factory=lambda: {
            "use_voice_patterns": False,
            "use_writing_style": False,
            "preserve_facial_expressions": False,
            "include_personal_stories": True
        }
    )
    review_schedule: str = "yearly"
    executors: List[UUID] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "is_enabled": True,
                "preservation_level": PreservationLevel.STANDARD,
                "access_controls": {
                    "time_restrictions": [
                        {
                            "restriction_type": "years_after_death",
                            "years_after_death": 5
                        }
                    ],
                    "relationship_access": [
                        {
                            "relationship_types": [
                                RelationshipType.PARENT_CHILD_BIOLOGICAL,
                                RelationshipType.PARENT_CHILD_ADOPTIVE
                            ],
                            "min_relationship_distance": 1,
                            "max_relationship_distance": 3,
                            "requires_verification": True
                        }
                    ],
                    "public_availability": "none"
                },
                "ai_representation": {
                    "allow_generation": True,
                    "confidence_threshold": 0.9,
                    "prohibited_topics": ["politics", "religion"],
                    "allowed_data_sources": ["direct_recordings", "writing_samples"]
                },
                "content_preferences": {
                    "use_voice_patterns": True,
                    "use_writing_style": True,
                    "preserve_facial_expressions": False,
                    "include_personal_stories": True
                },
                "review_schedule": "quarterly",
                "executors": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
            }
        }


"""
Family Tree Model - Representing interconnection between individuals.

The model implements the philosophical concept that we are all connected,
simultaneously "one" and "many" - a unified whole composed of sovereign individuals.
"""
from typing import List, Dict, Any, Optional, Set, Tuple
from enum import Enum
import logging
from datetime import datetime

from pydantic import BaseModel, Field
from neo4j import GraphDatabase

from backend.app.config import settings
from backend.app.models.base import BaseDBModel

logger = logging.getLogger(__name__)

class ConnectionType(str, Enum):
    """Types of connections that can exist between entities in the family tree."""
    BIOLOGICAL = "biological"
    CHOSEN_FAMILY = "chosen_family"
    MENTORSHIP = "mentorship"
    COLLABORATION = "collaboration"
    INSPIRATION = "inspiration"
    COMMUNITY = "community"

    @property
    def description(self) -> str:
        """Human-readable description of the connection type."""
        descriptions = {
            "biological": "Genetic or legal family relationships",
            "chosen_family": "Deeply bonded relationships chosen as family",
            "mentorship": "Teaching and learning relationships",
            "collaboration": "Working together on shared projects",
            "inspiration": "Philosophical or creative influence",
            "community": "Shared values, spaces, and collective action"
        }
        return descriptions.get(self.value, "Connection between individuals")

class ConnectionStrength(BaseModel):
    """
    Represents the strength of a connection as perceived by each participant.

    This dual-perspective approach honors the subjective nature of relationships
    while still enabling collective pattern recognition.
    """
    source_perception: float = Field(0.0, ge=0.0, le=1.0)
    target_perception: float = Field(0.0, ge=0.0, le=1.0)

    @property
    def is_mutual(self) -> bool:
        """Whether the connection is mutually acknowledged."""
        return self.source_perception > 0 and self.target_perception > 0

    @property
    def average(self) -> float:
        """Average strength, meaningful only for mutual connections."""
        if not self.is_mutual:
            return 0.0
        return (self.source_perception + self.target_perception) / 2

class FamilyTreeConnection(BaseDBModel):
    """
    Represents a connection between two individuals in the family tree.

    Connections are bidirectional by default but can have different meanings
    and strengths from each perspective. This honors both the interconnected
    nature of relationships and the subjective experience of each participant.
    """
    source_id: str
    target_id: str
    connection_type: ConnectionType
    strength: ConnectionStrength
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "source_id": "user123",
                "target_id": "user456",
                "connection_type": "mentorship",
                "strength": {
                    "source_perception": 0.8,
                    "target_perception": 0.7
                },
                "metadata": {
                    "years_connected": 5,
                    "shared_experiences": ["project_alpha", "conference_beta"],
                    "privacy_level": "community_visible"
                }
            }
        }

    @classmethod
    async def get_network(
        cls,
        user_id: str,
        depth: int = 2,
        connection_types: Optional[List[ConnectionType]] = None
    ) -> Dict[str, Any]:
        """
        Get a network of connections centered around a user.

        This method retrieves both the individual connections and the
        emergent collective patterns they form together.
        """
        # Implementation using graph database to retrieve network
        # ...existing code...

        # Calculate emergent properties that show how individual
        # connections contribute to collective patterns
        network = calculate_network_properties(nodes, connections)

        # Add both individual-focused and collective-focused metrics
        network["metrics"] = {
            "individual": {
                "connection_count": len(connections),
                "diversity_score": calculate_diversity_score(connections),
                "centrality": calculate_node_centrality(user_id, network)
            },
            "collective": {
                "network_density": calculate_network_density(network),
                "community_clusters": identify_community_clusters(network),
                "bridging_connections": identify_bridging_connections(network)
            }
        }

        return network

    def get_network_impact(self) -> Dict[str, float]:
        """
        Calculate how this single connection contributes to the emergent
        properties of the whole network.

        Returns a measure of how this connection strengthens the overall
        resilience and connectedness of the community.
        """
        # Calculate metrics that show how this connection contributes
        # to the collective pattern while respecting individual agency
        impact_metrics = {
            "bridging_score": 0.0,  # How much this connects otherwise separate groups
            "reinforcement_score": 0.0,  # How much this strengthens existing communities
            "diversity_contribution": 0.0,  # How this adds new perspectives
            "resilience_contribution": 0.0  # How this improves overall network resilience
        }

        # Implementation of graph algorithm calculations
        # ...existing code...

        return impact_metrics

# Visualization helpers for the "One and Many" concept
class FamilyTreeVisualization:
    """
    Generate visualizations that reveal both unity and diversity.

    These visualizations show how we are simultaneously one interconnected
    community and many sovereign individuals.
    """

    @staticmethod
    def generate_unity_view(network: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a visualization that emphasizes the emergent collective pattern.

        This view shows how individual connections form a greater whole,
        like cells forming an organism or stars forming a galaxy.
        """
        # Implementation that emphasizes collective patterns
        # ...existing code...
        pass

    @staticmethod
    def generate_diversity_view(network: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a visualization that emphasizes individual uniqueness.

        This view highlights the distinct qualities of each node while still
        showing how they participate in the greater system.
        """
        # Implementation that emphasizes individual attributes
        # ...existing code...
        pass

    @staticmethod
    def generate_balanced_view(network: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a visualization that balances unity and diversity.

        This view reveals how we are simultaneously one collective and
        many individuals - the default visualization that shows both aspects.
        """
        # Implementation that balances collective and individual focus
        # ...existing code...
        pass

    @staticmethod
    def generate_fractal_view(network: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a visualization showing self-similar patterns at different scales.

        This view reveals how individual connections, family units, and communities
        all follow similar organizational principles at different scales.
        """
        # Implementation that shows self-similarity across scales
        # ...existing code...
        pass

# Additional helper functions and classes
# ...existing code...
