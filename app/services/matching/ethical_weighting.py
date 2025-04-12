from typing import Dict, List, Any
from pydantic import BaseModel
import numpy as np

class EthicalWeight(BaseModel):
    """Core ethical weight configuration"""
    dimension_id: str
    base_weight: float        # Base importance in matching (0.0-1.0)
    justification: str        # Ethical reasoning for this weight
    modifiable_by_user: bool  # Whether users can override this weight

class EthicalWeightingSystem:
    """System for applying ethical considerations to matching"""

    def __init__(self, tracer=None):
        """Initialize with default E2.0 values and optional DataTracer"""
        self.core_weights = self._load_core_weights()
        self.tracer = tracer

    def _load_core_weights(self) -> Dict[str, EthicalWeight]:
        """Load core ethical weights from configuration"""
        # Initial weights based on Enlightenment 2.0 principles
        return {
            "autonomy": EthicalWeight(
                dimension_id="autonomy",
                base_weight=0.9,
                justification="Core to user sovereignty principle",
                modifiable_by_user=True
            ),
            # Additional core values
            # ...
        }

    def get_weighted_dimensions(self, user_preferences: Dict[str, float] = None) -> Dict[str, float]:
        """
        Get final dimension weights combining core ethical weights with user preferences
        Ensures user agency while maintaining ethical minimums
        """
        # Initialize with default weights
        weighted_dimensions = {}

        # Apply core ethical weights
        for dim_id, weight in self.core_weights.items():
            weighted_dimensions[dim_id] = weight.base_weight

        # Apply user preferences if provided
        if user_preferences:
            for dim_id, user_weight in user_preferences.items():
                if dim_id in self.core_weights and self.core_weights[dim_id].modifiable_by_user:
                    # Ensure weights don't go below ethical minimums
                    weighted_dimensions[dim_id] = max(user_weight, self.core_weights[dim_id].base_weight * 0.5)

        # Normalize weights if needed
        if self.tracer:
            self.tracer.log_operation("weight_calculation", {"raw_weights": weighted_dimensions})

        return weighted_dimensions

    def explain_weighting(self, dimension_id: str) -> Dict[str, Any]:
        """Provide human-readable explanation of weight calculation for UI"""
        explanation = {
            "dimension": dimension_id,
            "base_weight": 0.0,
            "final_weight": 0.0,
            "is_modifiable": False,
            "justification": "",
            "user_modification": 0.0
        }

        if dimension_id in self.core_weights:
            weight = self.core_weights[dimension_id]
            explanation["base_weight"] = weight.base_weight
            explanation["is_modifiable"] = weight.modifiable_by_user
            explanation["justification"] = weight.justification

        # Add more explanation details as needed

        return explanation
