from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.db.database import Base

class Agent(Base):
    """Model representing an AI agent in the system"""
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="agent")

    def __repr__(self):
        return f"Agent(agent_id={self.agent_id}, name='{self.name}')"

class Task(Base):
    """Model representing tasks assigned to agents"""
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    agent = relationship("Agent", back_populates="tasks")

    def __repr__(self):
        return f"Task(task_id={self.task_id}, name='{self.name}')"

class Document(Base):
    """Model representing documents that can be analyzed by agents"""
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    document_type = Column(String, default="text")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"Document(document_id={self.document_id}, title='{self.title}')"
