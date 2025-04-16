"""
Verification API Routes

This module implements the API endpoints for the verification system,
embodying our principles of distributed trust, radical transparency,
and community validation rather than centralized authority.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.database import get_db
from app.models.sqlalchemy_models import (
    VerificationRecord, VerificationAuditLog, VerificationStatus
)
from app.schemas.verification_schemas import (
    VerificationRecordCreate, VerificationRecordResponse,
    VerificationStatusUpdate, VerificationAuditLogResponse
)
from app.services.verification_service import VerificationService
from app.services.user_service import UserService
from app.auth.jwt import get_current_active_user
from app.models.user import UserInDB as PydanticUserInDB  # Pydantic model

router = APIRouter(
    prefix="/api/verification",
    tags=["verification"],
)


@router.post("/records", response_model=VerificationRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_verification_record(
    verification: VerificationRecordCreate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new verification record.
    
    This endpoint embodies our distributed trust system, allowing
    community members to participate in verification processes.
    """
    verification_service = VerificationService(db)
    user_service = UserService(db)
    
    # Check if the current user has verification privileges for this type
    # Implement business logic to determine who can verify what
    if not verification_service.can_user_verify(
        current_user.id, 
        verification.verification_type,
        verification.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to create this type of verification record"
        )
    
    # Log this verification action for transparency
    user_service.log_data_access(
        user_id=verification.user_id,
        accessor_id=current_user.id,
        data_type="verification_record",
        access_type="create",
        access_reason="user initiated verification process",
        data_fields=["verification_type", "status", "evidence"]
    )
    
    # Create the verification record
    return verification_service.create_verification_record(
        verification,
        verifier_id=current_user.id
    )


@router.get("/records", response_model=List[VerificationRecordResponse])
async def get_verification_records(
    user_id: Optional[UUID] = None,
    verification_type: Optional[str] = None,
    status: Optional[VerificationStatus] = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get verification records with optional filtering.
    
    This endpoint embodies radical transparency by making verification
    processes visible and auditable.
    """
    verification_service = VerificationService(db)
    user_service = UserService(db)
    
    # If a specific user_id is provided that is not the current user,
    # ensure the current user has permission to view those records
    if user_id and user_id != current_user.id:
        if not verification_service.can_view_user_verifications(current_user.id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view these verification records"
            )
    
    # Default to current user if no user_id specified
    target_user_id = user_id or current_user.id
    
    # Log this data access for transparency
    user_service.log_data_access(
        user_id=target_user_id,
        accessor_id=current_user.id,
        data_type="verification_records",
        access_type="read",
        access_reason="user requested verification records",
        data_fields=["id", "verification_type", "status", "evidence", "created_at"]
    )
    
    return verification_service.get_verification_records(
        user_id=target_user_id,
        verification_type=verification_type,
        status=status,
        limit=limit,
        offset=offset
    )


@router.get("/records/{record_id}", response_model=VerificationRecordResponse)
async def get_verification_record(
    record_id: UUID,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific verification record by ID.
    
    This endpoint implements transparent data access by checking permissions
    and logging all access attempts.
    """
    verification_service = VerificationService(db)
    user_service = UserService(db)
    
    # Get the verification record
    record = verification_service.get_verification_record(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification record not found"
        )
    
    # Check permissions
    if record.user_id != current_user.id and not verification_service.can_view_verification(current_user.id, record_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this verification record"
        )
    
    # Log this data access for transparency
    user_service.log_data_access(
        user_id=record.user_id,
        accessor_id=current_user.id,
        data_type="verification_record",
        access_type="read",
        access_reason="user requested verification record details",
        data_fields=["id", "verification_type", "status", "evidence", "notes", "created_at"]
    )
    
    return record


@router.put("/records/{record_id}/status", response_model=VerificationRecordResponse)
async def update_verification_status(
    record_id: UUID,
    status_update: VerificationStatusUpdate,
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update the status of a verification record.
    
    This endpoint embodies our distributed trust system, allowing
    authorized community members to participate in verification processes.
    """
    verification_service = VerificationService(db)
    user_service = UserService(db)
    
    # Get the verification record
    record = verification_service.get_verification_record(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification record not found"
        )
    
    # Check if the current user can update this verification record
    if not verification_service.can_update_verification_status(
        current_user.id, 
        record_id, 
        status_update.new_status
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this verification record's status"
        )
    
    # Log this verification action for transparency
    user_service.log_data_access(
        user_id=record.user_id,
        accessor_id=current_user.id,
        data_type="verification_status",
        access_type="update",
        access_reason="user updated verification status",
        data_fields=["status", "reason"]
    )
    
    # Update the verification status
    return verification_service.update_verification_status(
        record_id,
        status_update.new_status,
        status_update.reason,
        actor_id=current_user.id
    )


@router.get("/records/{record_id}/audit-logs", response_model=List[VerificationAuditLogResponse])
async def get_verification_audit_logs(
    record_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: PydanticUserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific verification record.
    
    This endpoint embodies radical transparency by making the entire
    verification process visible and auditable.
    """
    verification_service = VerificationService(db)
    user_service = UserService(db)
    
    # Get the verification record
    record = verification_service.get_verification_record(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification record not found"
        )
    
    # Check permissions
    if record.user_id != current_user.id and not verification_service.can_view_verification(current_user.id, record_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view audit logs for this verification record"
        )
    
    # Log this data access for transparency
    user_service.log_data_access(
        user_id=record.user_id,
        accessor_id=current_user.id,
        data_type="verification_audit_logs",
        access_type="read",
        access_reason="user requested verification audit trail",
        data_fields=["action", "previous_status", "new_status", "reason", "created_at"]
    )
    
    return verification_service.get_verification_audit_logs(record_id, limit, offset)