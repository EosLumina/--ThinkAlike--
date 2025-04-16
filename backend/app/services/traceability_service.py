"""
Traceability Service

This module implements the business logic for the data traceability system,
making visible how data flows through the ThinkAlike platform and how
algorithms operate on that data.
"""

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Union
from uuid import UUID
import datetime

from app.models.sqlalchemy_models import (
    DataAccessAudit, Connection, User, ValueProfile,
    NarrativeDerivedValue, Narrative
)
from app.schemas.traceability_schemas import (
    DataTraceabilityResponse, DataFlowNode, DataFlowEdge,
    AlgorithmTraceabilityResponse
)


class TraceabilityService:
    """
    Service for data traceability and transparency functionality.

    This service embodies our radical transparency principle by making
    data flows and algorithm operations visible and understandable.
    """

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def get_data_flow_visualization(
        self,
        user_id: UUID,
        data_type: Optional[str] = None,
        time_period: Optional[int] = 30,
        detail_level: Optional[str] = "medium"
    ) -> DataTraceabilityResponse:
        """
        Generate a visualization of data flows for a user.

        This method implements our radical transparency principle by
        showing users exactly how their data moves through the system.

        Args:
            user_id: ID of the user
            data_type: Optional filter for specific data type
            time_period: Time period in days to include
            detail_level: Level of detail to include (low, medium, high)

        Returns:
            DataTraceabilityResponse: Visualization data for the frontend
        """
        # Set the time cutoff based on the time period
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=time_period)

        # Get all data access records for this user within the time period
        query = self.db.query(DataAccessAudit).filter(
            DataAccessAudit.user_id == user_id,
            DataAccessAudit.access_time >= cutoff_date
        )

        # Apply data type filter if provided
        if data_type:
            query = query.filter(DataAccessAudit.data_type == data_type)

        # Execute query
        data_accesses = query.order_by(DataAccessAudit.access_time).all()

        # Build the nodes and edges for the visualization
        nodes = []
        edges = []

        # Add the user as the central node
        user = self.db.query(User).filter(User.id == user_id).first()
        nodes.append(
            DataFlowNode(
                id=str(user_id),
                label=f"User: {user.username}",
                type="user",
                size=30,
                color="#2596be"
            )
        )

        # Track nodes we've already added to avoid duplicates
        added_nodes = {str(user_id)}

        # Process each data access to build the graph
        for access in data_accesses:
            # Add the accessor as a node if not already added
            accessor_id = str(
                access.accessor_id) if access.accessor_id else f"system_{access.data_type}"
            accessor_label = self._get_accessor_label(
                access.accessor_id, access.data_type)
            accessor_type = "user" if access.accessor_id else "system"

            if accessor_id not in added_nodes:
                nodes.append(
                    DataFlowNode(
                        id=accessor_id,
                        label=accessor_label,
                        type=accessor_type,
                        size=15,
                        color="#ff7043" if accessor_type == "user" else "#4caf50"
                    )
                )
                # filepath: /workspaces/--ThinkAlike--/backend/app/services/traceability_service.py
                added_nodes.add(accessor_id)


"""
Traceability Service

This module implements the business logic for the data traceability system,
making visible how data flows through the ThinkAlike platform and how
algorithms operate on that data.
"""


class TraceabilityService:
    """
    Service for data traceability and transparency functionality.

    This service embodies our radical transparency principle by making
    data flows and algorithm operations visible and understandable.
    """

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def get_data_flow_visualization(
        self,
        user_id: UUID,
        data_type: Optional[str] = None,
        time_period: Optional[int] = 30,
        detail_level: Optional[str] = "medium"
    ) -> DataTraceabilityResponse:
        """
        Generate a visualization of data flows for a user.

        This method implements our radical transparency principle by
        showing users exactly how their data moves through the system.

        Args:
            user_id: ID of the user
            data_type: Optional filter for specific data type
            time_period: Time period in days to include
            detail_level: Level of detail to include (low, medium, high)

        Returns:
            DataTraceabilityResponse: Visualization data for the frontend
        """
        # Set the time cutoff based on the time period
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=time_period)

        # Get all data access records for this user within the time period
        query = self.db.query(DataAccessAudit).filter(
            DataAccessAudit.user_id == user_id,
            DataAccessAudit.access_time >= cutoff_date
        )

        # Apply data type filter if provided
        if data_type:
            query = query.filter(DataAccessAudit.data_type == data_type)

        # Execute query
        data_accesses = query.order_by(DataAccessAudit.access_time).all()

        # Build the nodes and edges for the visualization
        nodes = []
        edges = []

        # Add the user as the central node
        user = self.db.query(User).filter(User.id == user_id).first()
        nodes.append(
            DataFlowNode(
                id=str(user_id),
                label=f"User: {user.username}",
                type="user",
                size=30,
                color="#2596be"
            )
        )

        # Track nodes we've already added to avoid duplicates
        added_nodes = {str(user_id)}

        # Process each data access to build the graph
        for access in data_accesses:
            # Add the accessor as a node if not already added
            accessor_id = str(
                access.accessor_id) if access.accessor_id else f"system_{access.data_type}"
            accessor_label = self._get_accessor_label(
                access.accessor_id, access.data_type)
            accessor_type = "user" if access.accessor_id else "system"

            if accessor_id not in added_nodes:
                nodes.append(
                    DataFlowNode(
                        id=accessor_id,
                        label=accessor_label,
                        type=accessor_type,
                        size=15,
                        color="#ff7043" if accessor_type == "user" else "#4caf50"
                    )
                )
                added_nodes.add(accessor_id)
