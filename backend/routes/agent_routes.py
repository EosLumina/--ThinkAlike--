from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Optional
from sqlalchemy.orm import Session

# Fix missing imports
from backend.app.models.agent import Agent, Task, Document
from backend.services.agent_service import AgentService
from backend.app.db.database import get_db

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("/", response_model=List[dict])
async def get_agents(db: Session = Depends(get_db)):
    """Get all available agents"""
    agent_svc = AgentService(db)
    return agent_svc.get_all_agents()  # Use the method we defined in agent_service.py

@router.get("/{agent_id}/tasks", response_model=List[dict])
async def get_tasks(agent_id: int = Path(...), db: Session = Depends(get_db)):
    """Get tasks for a specific agent"""
    agent_svc = AgentService(db)
    agent = agent_svc.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.tasks

@router.get("/{agent_id}/documents", response_model=List[dict])
async def get_documents(agent_id: int = Path(...), db: Session = Depends(get_db)):
    """Get documents processed by a specific agent"""
    agent_svc = AgentService(db)
    agent = agent_svc.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    # Return mock documents for now
    return [{"id": 1, "title": "Sample Document", "processed_by": agent.name}]

@router.get("/documents/{document_id}", response_model=dict)
async def get_document(document_id: int = Path(...), db: Session = Depends(get_db)):
    """Get a specific document"""
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": document.document_id, "title": document.title, "content": document.content}
