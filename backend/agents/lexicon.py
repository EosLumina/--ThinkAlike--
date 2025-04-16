"""
Lexic𝚺 - The Documentation & Knowledge Management Guide

This guide assists contributors with creating, updating, and
structuring documentation that embodies our commitment to
knowledge sovereignty and collective understanding.
"""
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class DocumentationType(str, Enum):
    """Types of documentation within the ThinkAlike ecosystem."""
    PHILOSOPHICAL = "philosophical"
    ARCHITECTURAL = "architectural"
    TECHNICAL = "technical"
    USER_FACING = "user_facing"
    ONBOARDING = "onboarding"

class DocumentationPrinciple(str, Enum):
    """Principles guiding our documentation practices."""
    ACCESSIBILITY = "accessibility"
    CONTEXTUAL_DEPTH = "contextual_depth"
    TECHNICAL_PRECISION = "technical_precision"
    EVOLUTIONARY_DESIGN = "evolutionary_design"
    REVOLUTIONARY_CONTEXT = "revolutionary_context"

# Implementation details to follow based on the guide system framework