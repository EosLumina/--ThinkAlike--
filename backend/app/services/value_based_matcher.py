"""
Value-based matcher service for ThinkAlike.

This service matches users, content, or other entities based on value alignment
and ethical principles rather than traditional recommendation algorithms that
optimize for engagement metrics.
"""
from typing import Dict, List, Optional, Set, Tuple, Union
import logging
from datetime import datetime


class ValueBasedMatcher:
    """
    Matches entities based on value alignment instead of engagement metrics.

    The ValueBasedMatcher implements an ethical recommendation system that
    prioritizes authentic connections based on shared values, philosophical
    alignment, and user-defined preferences without exploiting attention
    or manipulating behavior.
    """

    def __init__(self,
                 ethical_weight: float = 0.6,
                 preference_weight: float = 0.3,
                 diversity_weight: float = 0.1):
        """
        Initialize the matcher with configurable weighting parameters.

        Args:
            ethical_weight: Weight given to ethical alignment (0-1)
            preference_weight: Weight given to user preferences (0-1)
            diversity_weight: Weight given to introducing diversity (0-1)
        """
        # Validate weights sum to 1.0
        total_weight = ethical_weight + preference_weight + diversity_weight
        if not 0.99 <= total_weight <= 1.01:  # Allow for small floating point errors
            raise ValueError("Weights must sum to 1.0")

        self.ethical_weight = ethical_weight
        self.preference_weight = preference_weight
        self.diversity_weight = diversity_weight
        self.logger = logging.getLogger(__name__)

    def calculate_value_compatibility(self,
                                      user_values: Dict[str, float],
                                      entity_values: Dict[str, float]) -> float:
        """
        Calculate compatibility score based on value alignment.

        Args:
            user_values: Dictionary of user values and their weights
            entity_values: Dictionary of entity values and their weights

        Returns:
            float: Compatibility score between 0 and 1
        """
        if not user_values or not entity_values:
            return 0.0

        # Find common values
        common_values = set(user_values.keys()) & set(entity_values.keys())
        if not common_values:
            return 0.0

        # Calculate weighted compatibility
        compatibility_sum = 0.0
        weight_sum = 0.0

        for value in common_values:
            user_weight = user_values[value]
            entity_weight = entity_values[value]
            # Compatibility is higher when both weights are similar and high
            score = 1.0 - abs(user_weight - entity_weight)
            weighted_score = score * (user_weight + entity_weight) / 2

            compatibility_sum += weighted_score
            weight_sum += (user_weight + entity_weight) / 2

        # Normalize by weight sum
        if weight_sum > 0:
            return compatibility_sum / weight_sum
        return 0.0

    def match(self,
              user_profile: Dict,
              candidates: List[Dict],
              top_n: int = 5) -> List[Tuple[Dict, float]]:
        """
        Find the best matches for a user from candidate entities.

        Args:
            user_profile: User profile with values, preferences
            candidates: List of candidate entities to match against
            top_n: Number of top matches to return

        Returns:
            List of (entity, score) tuples for the best matches
        """
        matches = []

        for candidate in candidates:
            # Calculate ethical alignment score
            ethical_score = self.calculate_value_compatibility(
                user_profile.get("values", {}),
                candidate.get("values", {})
            )

            # Calculate preference alignment score
            preference_score = self.calculate_value_compatibility(
                user_profile.get("preferences", {}),
                candidate.get("attributes", {})
            )

            # Calculate diversity score (inverse of similarity to already seen)
            diversity_score = self.calculate_diversity_score(
                user_profile.get("history", []),
                candidate
            )

            # Combine scores with weights
            total_score = (
                self.ethical_weight * ethical_score +
                self.preference_weight * preference_score +
                self.diversity_weight * diversity_score
            )

            matches.append((candidate, total_score))

        # Sort by score in descending order and take top_n
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]

    def calculate_diversity_score(self,
                                 history: List[Dict],
                                 candidate: Dict) -> float:
        """
        Calculate how diverse a candidate is compared to user history.

        Args:
            history: User's history of interactions
            candidate: Candidate entity

        Returns:
            float: Diversity score between 0 and 1
        """
        if not history:
            return 1.0  # Maximum diversity when no history

        # Extract relevant attributes for comparison
        candidate_attrs = set(candidate.get("categories", []))
        if not candidate_attrs:
            return 0.5  # Neutral score when no attributes

        # Calculate average similarity to history
        similarity_sum = 0.0
        for item in history:
            item_attrs = set(item.get("categories", []))
            if item_attrs:
                # Jaccard similarity
                intersection = len(candidate_attrs & item_attrs)
                union = len(candidate_attrs | item_attrs)
                similarity = intersection / union if union > 0 else 0
                similarity_sum += similarity

        avg_similarity = similarity_sum / len(history) if history else 0
        # Return diversity (inverse of similarity)
        return 1.0 - avg_similarity

    def explain_match(self,
                      user_profile: Dict,
                      entity: Dict,
                      score: float) -> Dict:
        """
        Provide a human-readable explanation for why a match was made.

        Args:
            user_profile: User's profile
            entity: The matched entity
            score: The match score

        Returns:
            Dict: Explanation with factors and their contributions
        """
        # Calculate individual component scores
        ethical_score = self.calculate_value_compatibility(
            user_profile.get("values", {}),
            entity.get("values", {})
        )

        preference_score = self.calculate_value_compatibility(
            user_profile.get("preferences", {}),
            entity.get("attributes", {})
        )

        diversity_score = self.calculate_diversity_score(
            user_profile.get("history", []),
            entity
        )

        # Calculate contributions to final score
        ethical_contribution = ethical_score * self.ethical_weight
        preference_contribution = preference_score * self.preference_weight
        diversity_contribution = diversity_score * self.diversity_weight

        # Find shared values
        shared_values = set(user_profile.get("values", {}).keys()) & set(entity.get("values", {}).keys())

        explanation = {
            "score": score,
            "factors": {
                "ethical_alignment": {
                    "score": ethical_score,
                    "weight": self.ethical_weight,
                    "contribution": ethical_contribution,
                    "shared_values": list(shared_values)
                },
                "preference_match": {
                    "score": preference_score,
                    "weight": self.preference_weight,
                    "contribution": preference_contribution
                },
                "diversity_factor": {
                    "score": diversity_score,
                    "weight": self.diversity_weight,
                    "contribution": diversity_contribution
                }
            },
            "timestamp": datetime.now().isoformat()
        }

        return explanation
