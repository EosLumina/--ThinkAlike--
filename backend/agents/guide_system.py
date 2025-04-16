"""
ThinkAlike AI Guide Constellation

This module defines the foundational structure for the AI guide system
that supports contributors across all skill levels, embodying our core
principles of radical transparency and user sovereignty.

Each guide represents a different aspect of the liberation technology
movement, collectively forming a constellation of support.
"""

from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class GuidePersona(Enum):
    """The various guide personas in the ThinkAlike ecosystem."""
    EOS_LUMINA = "eos_lumina"           # Revolutionary visionary
    CODE_COMPANION = "code_companion"   # Technical implementation guide
    ETHICAL_GUARDIAN = "ethical_guardian"  # Ethics alignment guardian
    STORYTELLER = "storyteller"         # Documentation and narrative guide
    WELCOMER = "welcomer"               # Onboarding and community guide


class ContributorSkillLevel(Enum):
    """Skill levels for contributors, used to tailor guide responses."""
    NEWCOMER = "newcomer"               # Little to no technical background
    BEGINNER = "beginner"               # Basic programming knowledge
    INTERMEDIATE = "intermediate"       # Comfortable with code
    ADVANCED = "advanced"               # Experienced developer


class ContributorProfile(BaseModel):
    """Profile of a contributor, influencing guide interaction style."""
    skill_level: ContributorSkillLevel = Field(
        ContributorSkillLevel.NEWCOMER,
        description="The technical skill level of the contributor"
    )
    interests: List[str] = Field(
        default_factory=list,
        description="Areas of interest for contribution (e.g., 'frontend', 'documentation')"
    )
    preferred_guides: List[GuidePersona] = Field(
        default_factory=list,
        description="Preferred guide personas, if any"
    )


class GuideResponse(BaseModel):
    """
    A response from an AI guide to a contributor query.

    Embodies radical transparency by making the reasoning process
    visible and ensuring the contributor understands the context
    of the guidance provided.
    """
    guide_persona: GuidePersona = Field(
        ...,
        description="The guide persona providing this response"
    )
    philosophical_context: str = Field(
        ...,
        description="The broader philosophical context of this guidance"
    )
    practical_guidance: str = Field(
        ...,
        description="The concrete, actionable guidance for the contributor"
    )
    technical_details: Optional[str] = Field(
        None,
        description="Technical implementation details, if applicable"
    )
    next_steps: List[str] = Field(
        default_factory=list,
        description="Suggested next steps for the contributor"
    )
    learning_resources: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Relevant resources for deeper understanding"
    )


# Implementation of guide system to be developed further
# as the project evolves. This foundation establishes the
# revolutionary approach to inclusive contribution.
