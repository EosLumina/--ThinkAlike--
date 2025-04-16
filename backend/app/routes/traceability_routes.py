"""
Traceability Routes

This module defines the API endpoints for the data traceability system,
implementing our principle of radical transparency.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.sqlalchemy_models import DataAccessAudit
from app.models.user import UserInDB
from app.schemas.traceability_schemas import (
    DataTraceabilityResponse, AlgorithmTraceabilityResponse,
    DataAccessAuditCreate, DataAccessAuditResponse
)
from app.services.traceability_service import TraceabilityService
from app.services.user_service import UserService
from app.auth.jwt import get_current_active_user

router = APIRouter(
    prefix="/api/traceability",
    tags=["traceability"],
)


@router.get("/data-flow/{user_id}", response_model=DataTraceabilityResponse)
async def get_data_flow(
    user_id: UUID,
    data_type: Optional[str] = None,
    time_period: Optional[int] = 30,
    detail_level: Optional[str] = "medium",
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get a visualization of data flows for a user.

    This endpoint implements our radical transparency principle by
    showing users exactly how their data moves through the system.
    """
    # Only allow users to see their own data flow or administrators
    if str(user_id) != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other users' data flows"
        )

    traceability_service = TraceabilityService(db)
    return traceability_service.get_data_flow_visualization(
        user_id=user_id,
        data_type=data_type,
        time_period=time_period,
        detail_level=detail_level
    )


@router.get("/algorithm/{algorithm_id}", response_model=AlgorithmTraceabilityResponse)
async def get_algorithm_traceability(
    algorithm_id: str,
    user_id: Optional[UUID] = None,
    time_period: Optional[int] = 30,
    include_inputs: Optional[bool] = True,
    include_outputs: Optional[bool] = True,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get traceability information for algorithm executions.

    This endpoint implements our radical transparency principle by
    revealing how algorithms operate on user data.
    """
    # If user_id is specified, only allow users to see their own algorithm
    # traceability or administrators
    if user_id and str(user_id) != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view algorithm traceability for other users"
        )

    traceability_service = TraceabilityService(db)
    return traceability_service.get_algorithm_traceability(
        algorithm_id=algorithm_id,
        user_id=user_id,
        time_period=time_period,
        include_inputs=include_inputs,
        include_outputs=include_outputs
    )


@router.post("/record-access", response_model=DataAccessAuditResponse)
async def record_data_access(
    audit: DataAccessAuditCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Record a data access event for transparency.

    This endpoint supports radical transparency by ensuring all
    data access is recorded and traceable.
    """
    # Only allow system components (via admin tokens) or users accessing their own data
    if not current_user.is_admin and (
        audit.accessor_id is None or  # System components must use admin tokens
        # Users can only record their own access
        str(audit.accessor_id) != str(current_user.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to record this data access"
        )

    traceability_service = TraceabilityService(db)
    audit_id = traceability_service.record_data_access(
        user_id=audit.user_id,
        data_type=audit.data_type,
        purpose=audit.purpose,
        accessor_id=audit.accessor_id,
        algorithm_id=audit.algorithm_id,
        algorithm_name=audit.algorithm_name,
        access_details=audit.access_details
    )

    # Retrieve the created audit record
    audit_record = db.query(DataAccessAudit).filter(
        DataAccessAudit.id == audit_id).first()
    return audit_record


@router.get("/data-access", response_model=List[Dict])
async def get_data_access_visualization(
    time_period: Optional[int] = Query(30, description="Time period in days"),
    data_type: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a visualization of who has accessed the user's data.

    This endpoint embodies radical transparency by showing users exactly
    who has accessed their data, when, and for what purpose.
    """
    traceability_service = TraceabilityService(db)
    user_service = UserService(db)

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=current_user.id,
        accessor_id=current_user.id,
        data_type="data_access_visualization",
        access_type="read",
        access_reason="user requested data access visualization",
        data_fields=["access_records"]
    )

    # Get the data access visualization
    return traceability_service.get_data_access_visualization(
        user_id=current_user.id,
        time_period=time_period,
        data_type=data_type
    )


@router.get("/matching-explanation/{connection_id}", response_model=Dict)
async def get_matching_explanation(
    connection_id: UUID,
    detail_level: Optional[str] = Query(
        "medium", description="Level of detail: low, medium, high"),
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get an explanation of why a specific match was recommended.

    This endpoint embodies our commitment to explainable AI by making
    the matching algorithm's decisions transparent and understandable.
    """
    traceability_service = TraceabilityService(db)
    user_service = UserService(db)

    # Get the connection details
    connection = traceability_service.get_connection(connection_id)
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )

    # Ensure the current user is part of this connection
    if connection.user_id_a != current_user.id and connection.user_id_b != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this connection explanation"
        )

    # Determine the other user in the connection
    other_user_id = connection.user_id_b if connection.user_id_a == current_user.id else connection.user_id_a

    # Log this data access for transparency
    user_service.log_data_access(
        user_id=other_user_id,
        accessor_id=current_user.id,
        data_type="matching_explanation",
        access_type="read",
        access_reason="user requested match explanation",
        data_fields=["connection_id",
                     "alignment_dimensions", "alignment_score"]
    )

    # Get the matching explanation
    return traceability_service.get_matching_explanation(
        connection_id=connection_id,
        user_id=current_user.id,
        detail_level=detail_level
    )
