"""
Aurora⚛ - The Frontend Development Guide

This guide assists contributors with frontend tasks, focusing on
creating interfaces that embody radical transparency and enhance
user sovereignty through meaningful control and understanding.
"""
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class FrontendDomain(str, Enum):
    """Specialized areas within frontend development."""
    COMPONENT_DESIGN = "component_design"
    STATE_MANAGEMENT = "state_management"
    ACCESSIBILITY = "accessibility"
    DATA_VISUALIZATION = "data_visualization"
    USER_FLOW = "user_flow"

class TransparencyPattern(str, Enum):
    """UI patterns that enhance transparency and user understanding."""
    DATA_TRACEABILITY = "data_traceability"
    DECISION_EXPLANATION = "decision_explanation"
    CONTROL_AFFORDANCE = "control_affordance"
    INFORMATION_HIERARCHY = "information_hierarchy"
    CONSENT_CLARITY = "consent_clarity"

# Implementation details to follow based on the guide system framework