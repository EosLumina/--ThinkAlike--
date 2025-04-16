"""
Quest Service

This module provides services for managing quests and tracking progress,
including integration with the badge and rank system.
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from uuid import UUID

from app.models.quest import Quest, QuestProgress, ContributorRole
from app.models.recognition import Badge, BadgeAward
from app.services.recognition_service import RecognitionService


class QuestService:
    """
    Service for managing quests and tracking progress,
    including integration with the badge and rank system.
    """

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.recognition_service = RecognitionService(db)

    def complete_quest_path(
        self,
        contributor_id: UUID,
        quest_id: UUID,
        selected_path: ContributorRole,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Mark a quest path as completed and award appropriate badges.

        This method embodies our revolutionary recognition system by
        awarding badges for diverse types of contributions, not just code.
        """
        # Get the quest details
        quest = self.db.query(Quest).filter(Quest.id == quest_id).first()
        if not quest:
            raise ValueError(f"Quest with ID {quest_id} not found")

        # Get or create progress record
        progress = self.db.query(QuestProgress).filter(
            QuestProgress.contributor_id == contributor_id,
            QuestProgress.quest_id == quest_id
        ).first()

        if not progress:
            progress = QuestProgress(
                contributor_id=contributor_id,
                quest_id=quest_id,
                selected_path=selected_path,
                progress_percentage=100.0,
                notes=notes or ""
            )
            self.db.add(progress)
        else:
            progress.selected_path = selected_path
            progress.progress_percentage = 100.0
            progress.notes = notes or progress.notes

        # Award badges associated with this quest and path
        awarded_badges = self._award_quest_badges(
            contributor_id=contributor_id,
            quest=quest,
            selected_path=selected_path
        )

        # Check for rank advancement
        rank_advancement = self.recognition_service.check_rank_advancement(
            contributor_id)

        self.db.commit()

        return {
            "quest_completed": True,
            "selected_path": selected_path,
            "awarded_badges": awarded_badges,
            "rank_advancement": rank_advancement
        }

    def _award_quest_badges(
        self,
        contributor_id: UUID,
        quest: Quest,
        selected_path: ContributorRole
    ) -> List[Dict]:
        """
        Award badges associated with completing a quest path.

        Returns information about awarded badges.
        """
        # This would normally look up badges associated with this quest and path
        # For simplicity, we'll just create a placeholder implementation

        # Find badges for this quest and path (in a real implementation, this would
        # be determined by the quest and path configuration)
        badges_to_award = []

        # Award each badge
        awarded_badges = []
        for badge_id in badges_to_award:
            badge_award = self.recognition_service.award_badge(
                badge_id=badge_id,
                contributor_id=contributor_id,
                quest_id=quest.id,
                contribution_description=f"Completed the {selected_path.value} path in quest '{quest.name}'",
                awarded_by=None  # Automated award
            )
            awarded_badges.append({
                "badge_id": badge_award.badge_id,
                "badge_name": badge_award.badge.name,
                "badge_category": badge_award.badge.category,
                "awarded_at": badge_award.awarded_at
            })

        return awarded_badges
