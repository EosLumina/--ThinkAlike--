from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models.agent_model import Agent
from ..auth.auth_handler import get_current_user
from ..database.models import User

router = APIRouter()

@router.get("/agents", response_model=List[Agent], tags=["agents"])
async def list_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lists all available agents.
    """
    agents = db.query(Agent).all()
    return agents

@router.post("/agents", response_model=Agent, tags=["agents"])
async def create_agent(agent: Agent, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a new agent.
    """
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.put("/agents/{agent_id}", response_model=Agent, tags=["agents"])
async def update_agent(agent_id: str, agent: Agent, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Updates an existing agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    for key, value in agent.dict().items():
        setattr(db_agent, key, value)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.delete("/agents/{agent_id}", response_model=Agent, tags=["agents"])
async def delete_agent(agent_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes an existing agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    db.delete(db_agent)
    db.commit()
    return db_agent

@router.get("/agents/{agent_id}", response_model=Agent, tags=["agents"])
async def get_agent(agent_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves detailed information about a specific agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return db_agent

@router.get("/agents/{agent_id}/status", tags=["agents"])
async def get_agent_status(agent_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the status of a specific agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return {"status": "active"}

@router.get("/agents/{agent_id}/tasks", response_model=List[Task], tags=["agents"])
async def get_agent_tasks(agent_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves tasks associated with a specific agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent_service.get_agent_tasks(agent_id)

@router.get("/agents/{agent_id}/tasks/{task_id}/documents", response_model=List[Document], tags=["agents"])
async def get_agent_task_documents(agent_id: str, task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves documents associated with a specific task for an agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent_service.get_agent_task_documents(agent_id, task_id)

@router.get("/agents/{agent_id}/tasks/{task_id}/documents/{document_id}", response_model=Document, tags=["agents"])
async def get_document(agent_id: str, task_id: str, document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves a specific document associated with a task for an agent.
    """
    db_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent_service.get_document(agent_id, task_id, document_id)
