from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    ethical_rating: float
    transparency_score: float

class Agent(AgentBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "ValueExplorer",
                "description": "Helps users explore their values and ethical principles",
                "type": "exploration",
                "ethical_rating": 95.5,
                "transparency_score": 98.2
            }
        }

@router.get("/", response_model=List[Agent], summary="Get all agents")
async def get_agents(
    type_filter: Optional[str] = Query(None, description="Filter agents by type"),
    min_ethical_rating: Optional[float] = Query(None, ge=0, le=100, description="Minimum ethical rating threshold")
):
    """
    Retrieve all available agents with optional filtering.

    - **type_filter**: Optional filter by agent type (e.g., 'exploration', 'connection')
    - **min_ethical_rating**: Only show agents with ethical rating above this threshold

    All agent data includes transparency scores to ensure alignment with ThinkAlike's
    ethical guidelines and radical transparency principles.
    """
    # Sample data - in a real implementation, this would come from a database
    agents = [
        {
            "id": 1,
            "name": "ValueExplorer",
            "description": "Helps users explore their values and ethical principles",
            "type": "exploration",
            "ethical_rating": 95.5,
            "transparency_score": 98.2
        },
        {
            "id": 2,
            "name": "ConnectBuilder",
            "description": "Facilitates authentic connections based on shared values",
            "type": "connection",
            "ethical_rating": 92.8,
            "transparency_score": 97.5
        },
        {
            "id": 3,
            "name": "CommunityFormer",
            "description": "Helps form decentralized, self-governing communities",
            "type": "community",
            "ethical_rating": 96.1,
            "transparency_score": 99.0
        }
    ]

    # Apply filters if provided
    if type_filter:
        agents = [a for a in agents if a["type"] == type_filter]

    if min_ethical_rating is not None:
        agents = [a for a in agents if a["ethical_rating"] >= min_ethical_rating]

    return agents

@router.get("/{agent_id}", response_model=Agent, summary="Get a specific agent")
async def get_agent(agent_id: int):
    """
    Retrieve a specific agent by ID.

    This endpoint provides detailed information about a specific agent, including:
    - Basic information (name, description)
    - Agent type
    - Ethical rating
    - Transparency score

    These metrics ensure alignment with ThinkAlike's commitment to ethical technology.
    """
    # Sample data dictionary - in a real implementation, this would be a database lookup
    agents = {
        1: {
            "id": 1,
            "name": "ValueExplorer",
            "description": "Helps users explore their values and ethical principles",
            "type": "exploration",
            "ethical_rating": 95.5,
            "transparency_score": 98.2
        },
        2: {
            "id": 2,
            "name": "ConnectBuilder",
            "description": "Facilitates authentic connections based on shared values",
            "type": "connection",
            "ethical_rating": 92.8,
            "transparency_score": 97.5
        },
        3: {
            "id": 3,
            "name": "CommunityFormer",
            "description": "Helps form decentralized, self-governing communities",
            "type": "community",
            "ethical_rating": 96.1,
            "transparency_score": 99.0
        }
    }

    if agent_id not in agents:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agents[agent_id]
