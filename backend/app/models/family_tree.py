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


class FamilyTreeVisualization(BaseModel):
    """Configuration for family tree visualization."""
    layout_type: str = "hierarchical"
    center_user_id: UUID
    display_generations_up: int = 3
    display_generations_down: int = 3
    include_extended_family: bool = True
    include_spouses: bool = True
    display_preferences: Dict[str, Any] = Field(default_factory=dict)
