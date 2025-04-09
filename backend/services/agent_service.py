from backend.app.models.agent import Agent, Task, Document
from backend.app.db.database import get_db
from typing import List, Optional, Dict, Any

class AgentService:
    """Service for managing AI agents and their tasks"""

    def __init__(self, db_session):
        self.db = db_session

    def get_agent(self, agent_id: int) -> Optional[Agent]:
        """Get an agent by ID"""
        return self.db.query(Agent).filter(Agent.agent_id == agent_id).first()

    def get_all_agents(self) -> List[Agent]:
        """Get all active agents"""
        return self.db.query(Agent).filter(Agent.is_active == True).all()

    def create_task(self, agent_id: int, task_name: str, task_description: str) -> Task:
        """Create a new task for an agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        task = Task(
            agent_id=agent_id,
            name=task_name,
            description=task_description,
            status="pending"
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def process_document(self, document: Document, agent_id: int) -> Dict[str, Any]:
        """Process a document with a specific agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # This is where agent logic would run to process the document
        # For now, we'll just return a mock result
        return {
            "document_id": document.document_id,
            "agent_id": agent_id,
            "analysis": f"Document '{document.title}' processed by agent '{agent.name}'",
            "summary": "This is a sample document summary.",
            "status": "completed"
        }
