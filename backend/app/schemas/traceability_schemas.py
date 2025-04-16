"""
Traceability Schemas

This module defines the Pydantic models for the data traceability system,
which is central to ThinkAlike's principle of radical transparency.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Any
from uuid import UUID


class DataFlowNode(BaseModel):
    """
    A node in the data flow visualization graph.
    
    Nodes represent entities like users, data types, and system components
    that participate in data flows.
    """
    id: str
    label: str
    type: str  # user, data, system, algorithm
    size: int
    color: str
    
    class Config:
        from_attributes = True


class DataFlowEdge(BaseModel):
    """
    An edge in the data flow visualization graph.
    
    Edges represent data flows between nodes, including the purpose
    and timestamp of the flow.
    """
    id: str
    source: str
    target: str
    label: str
    thickness: int
    timestamp: Optional[str] = None
    
    class Config:
        from_attributes = True


class DataTraceabilityResponse(BaseModel):
    """
    Response model for data traceability visualization.
    
    This contains all the data needed for frontend visualization
    of data flows.
    """
    user_id: str
    nodes: List[DataFlowNode]
    edges: List[DataFlowEdge]
    time_period: int
    detail_level: str
    
    class Config:
        from_attributes = True


class AlgorithmExecutionDetail(BaseModel):
    """
    Details of a single algorithm execution.
    
    This provides transparency into how an algorithm processed data,
    including inputs, outputs, and ethical constraints.
    """
    execution_id: str
    execution_time: str
    user_id: Optional[str] = None
    purpose: str
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None
    status: str
    duration_ms: Optional[int] = None
    ethical_constraints: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class AlgorithmTraceabilityResponse(BaseModel):
    """
    Response model for algorithm traceability.
    
    This contains detailed information about algorithm executions,
    providing transparency into how algorithms operate.
    """
    algorithm_id: str
    algorithm_name: str
    algorithm_description: str
    user_id: Optional[str] = None
    time_period: int
    execution_count: int
    executions: List[AlgorithmExecutionDetail]
    
    class Config:
        from_attributes = True


class DataAccessAuditCreate(BaseModel):
    """
    Model for creating a data access audit record.
    
    This is used when recording a new data access event.
    """
    user_id: UUID
    data_type: str
    purpose: str
    accessor_id: Optional[UUID] = None
    algorithm_id: Optional[str] = None
    algorithm_name: Optional[str] = None
    access_details: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class DataAccessAuditResponse(BaseModel):
    """
    Response model for a data access audit record.
    
    This is used when returning audit records to the frontend.
    """
    id: UUID
    user_id: UUID
    accessor_id: Optional[UUID] = None
    data_type: str
    purpose: str
    algorithm_id: Optional[str] = None
    algorithm_name: Optional[str] = None
    access_details: Optional[Dict[str, Any]] = None
    access_time: datetime
    
    class Config:
        from_attributes = True