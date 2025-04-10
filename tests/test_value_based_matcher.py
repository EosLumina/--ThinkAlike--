import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.value_based_matcher import ValueBasedMatcher

# Mock profile class for testing
class MockProfile:
    def __init__(self, ethical_values=None, political_values=None,
                spiritual_values=None, lifestyle_values=None,
                practical_values=None, interests=None):
        self.ethical_values = ethical_values or []
        self.political_values = political_values or []
        self.spiritual_values = spiritual_values or []
        self.lifestyle_values = lifestyle_values or []
        self.practical_values = practical_values or []
        self.interests = interests or []

class TestValueBasedMatcher:
    """Test suite for the ValueBasedMatcher class"""

    @pytest.fixture
    def db_session(self):
        """Create a mock database session"""
        return MagicMock()

    @pytest.fixture
    def matcher(self, db_session):
        """Create a ValueBasedMatcher instance with mock db session"""
        return ValueBasedMatcher(db_session)

    def test_empty_profiles_return_zero_compatibility(self, matcher):
        """Test that empty profiles return zero compatibility"""
        profile1 = MockProfile()
        profile2 = MockProfile()

        result = matcher.calculate_compatibility(profile1, profile2)

        assert result["score"] == 0.0
        assert len(result["shared_values"]) == 0
        assert "Insufficient" in result["description"]

    def test_identical_profiles_return_high_compatibility(self, matcher):
        """Test that identical profiles return high compatibility"""
        ethical_values = ["honesty", "compassion", "integrity"]
        political_values = ["equality", "freedom", "justice"]
        interests = ["reading", "hiking", "philosophy"]

        profile1 = MockProfile(
            ethical_values=ethical_values,
            political_values=political_values,
            interests=interests
        )
        profile2 = MockProfile(
            ethical_values=ethical_values,
            political_values=political_values,
            interests=interests
        )

        result = matcher.calculate_compatibility(profile1, profile2)

        assert result["score"] == 1.0
        assert set(result["shared_values"]) == set(ethical_values + political_values)
        assert set(result["shared_interests"]) == set(interests)
        assert "Exceptional" in result["description"]

    def test_partially_overlapping_profiles(self, matcher):
        """Test profiles with partial value overlap"""
        profile1 = MockProfile(
            ethical_values=["honesty", "compassion"],
            political_values=["equality", "freedom"],
            interests=["reading", "hiking"]
        )
        profile2 = MockProfile(
            ethical_values=["honesty", "integrity"],
            political_values=["freedom", "justice"],
            interests=["hiking", "philosophy"]
        )

        result = matcher.calculate_compatibility(profile1, profile2)

        assert 0.3 < result["score"] < 0.7  # Should be moderate compatibility
        assert "honesty" in result["shared_values"]
        assert "freedom" in result["shared_values"]
        assert "hiking" in result["shared_interests"]

    def test_different_value_weights(self, matcher):
        """Test that different value categories have different weights"""
        # Only ethical values in common (highest weight)
        profile1 = MockProfile(ethical_values=["honesty", "compassion"])
        profile2 = MockProfile(ethical_values=["honesty", "compassion"])

        ethical_result = matcher.calculate_compatibility(profile1, profile2)

        # Only practical values in common (lowest weight)
        profile3 = MockProfile(practical_values=["organization", "punctuality"])
        profile4 = MockProfile(practical_values=["organization", "punctuality"])

        practical_result = matcher.calculate_compatibility(profile3, profile4)

        # Ethical values should have a stronger impact
        assert ethical_result["score"] > practical_result["score"]
