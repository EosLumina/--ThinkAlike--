from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Define feedback data model
class FeedbackModel(BaseModel):
    user_id: str
    message: str
    category: Optional[str] = "general"
    rating: Optional[int] = None

router = APIRouter()

@router.post("/")
async def submit_feedback(feedback: FeedbackModel):
    """
    Submit user feedback
    """
    # Add validation for rating
    if feedback.rating is not None and not (1 <= feedback.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    return {
        "status": "success",
        "message": "Feedback received",
        "feedback": feedback.dict()
    }

@router.get("/categories")
async def get_feedback_categories():
    """
    Get available feedback categories
    """
    return {
        "categories": [
            "general",
            "bug",
            "feature_request",
            "improvement",
            "other"
        ]
    }

# Example feedback data
example_feedback = {
    "user_id": "user123",
    "message": "Great application!",
    "category": "general",
    "rating": 5
}
