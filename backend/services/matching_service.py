import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..models import User, Profile, Match

class MatchingService:
    """
    Service that handles the core matching algorithm for ThinkAlike.
    Uses a combination of explicit user preferences and implicit behavioral data.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        
    def generate_user_vector(self, user_id):
        """Convert user data into a numerical vector for similarity computation"""
        # Fetch user profile, interests, community memberships
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            return None
            
        # Generate vector from user data (simplified version)
        # In production, this would use more sophisticated embedding techniques
        vector = []
        
        # Add interests (converted to numerical values)
        if profile.interests:
            for interest in profile.interests:
                # Convert interest to numerical representation
                vector.append(hash(interest) % 100 / 100)
        
        # Add community affiliations
        communities = self.db.query(UserCommunity).filter(
            UserCommunity.user_id == user_id
        ).all()
        
        for community in communities:
            vector.append(hash(community.community_id) % 100 / 100)
            
        return np.array(vector).reshape(1, -1)
    
    def find_matches(self, user_id, limit=10, min_score=0.6):
        """Find potential matches for a user"""
        user_vector = self.generate_user_vector(user_id)
        if user_vector is None:
            return []
        
        # Get all users except the target user
        other_users = self.db.query(User).filter(User.user_id != user_id).all()
        matches = []
        
        for other_user in other_users:
            other_vector = self.generate_user_vector(other_user.user_id)
            if other_vector is None:
                continue
                
            # Calculate similarity score
            similarity = cosine_similarity(user_vector, other_vector)[0][0]
            
            if similarity >= min_score:
                matches.append({
                    "user_id": other_user.user_id,
                    "username": other_user.username,
                    "compatibility_score": float(similarity),
                    "matched_interests": self._get_matched_interests(user_id, other_user.user_id)
                })
        
        # Sort by compatibility score
        matches.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return matches[:limit]
    
    def _get_matched_interests(self, user_id1, user_id2):
        """Find common interests between two users"""
        profile1 = self.db.query(Profile).filter(Profile.user_id == user_id1).first()
        profile2 = self.db.query(Profile).filter(Profile.user_id == user_id2).first()
        
        if not profile1 or not profile2 or not profile1.interests or not profile2.interests:
            return []
            
        return list(set(profile1.interests).intersection(set(profile2.interests)))