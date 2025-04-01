from pydantic import BaseModel

class Agent(BaseModel):
    agent_id: str
    name: str
    # Add other Agent model fields here as needed (e.g., description, capabilities, etc.)
