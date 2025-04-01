from pydantic import BaseModel

class Task(BaseModel):
    task_id: str
    description: str
    # Add other Task model fields here as needed (e.g., agent_id, status, created_at, etc.)
