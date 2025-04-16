"""
SQLAlchemy Data Models

This module defines the database models for ThinkAlike, implementingystem,
our principles of user sovereignty, radical transparency, and ethical data handling.
"""
"""
from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuidm uuid import UUID
from datetime import datetimeimport datetime

from app.db.database import Base
e,
   NarrativeDerivedValue, Narrative, AlgorithmExecution
class User(Base):
    """
    User model representing a ThinkAlike user.ode, DataFlowEdge,
    se, AlgorithmExecutionDetail
    This model embodies user sovereignty by:
    1. Using a unique ID that doesn't expose personal information
    2. Storing only necessary user attributes
    3. Explicitly tracking user activity stateclass TraceabilityService:
    4. Supporting verifiable creation and update timestamps
    """    Service for data traceability and transparency functionality.
    __tablename__ = "users"
dical transparency principle by making
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)a flows and algorithm operations visible and understandable.
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True) self.db = db
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # Relationshipsal[str] = None,
    value_profile = relationship("ValueProfile", back_populates="user", uselist=False)        time_period: Optional[int] = 30,
    narratives = relationship("Narrative", back_populates="user")        detail_level: Optional[str] = "medium"
    verification_logs = relationship(
        "VerificationAuditLog", back_populates="user")
    data_accesses = relationship("DataAccessAudit", foreign_keys="DataAccessAudit.user_id", back_populates="user") """
    data_accessed = relationship("DataAccessAudit", foreign_keys="DataAccessAudit.accessor_id", back_populates="accessor") for a user.


class ValueProfile(Base): their data moves through the system.
    """
    Value profile for a user, representing their core values and preferences.
    f the user
    This is central to the ThinkAlike matching system, allowing users totional filter for specific data type
    connect based on genuine value alignment rather than superficial traits.Time period in days to include
    """l: Level of detail to include(low, medium, high)
    __tablename__ = "value_profiles"
        Returns:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)raceabilityResponse: Visualization data for the frontend
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True) """
    explicit_values = Column(JSON, nullable=False, default=list)
    narrative_derived_values = Column(JSON, nullable=False, default=dict)        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=time_period)
    interests = Column(JSON, nullable=False, default=list)
    skills = Column(JSON, nullable=False, default=list)od
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # Relationships )
    user = relationship("User", back_populates="value_profile")
    # Apply data type filter if provided
    derived_values = relationship(
        "NarrativeDerivedValue", back_populates="value_profile")

ata_type)
class Narrative(Base):
    """
    User narrative representing a personal story that reveals values.udit.access_time).all()

    Narratives are the primary method for derived value discovery in ThinkAlike, alization
    allowing values to emerge naturally rather than through direct questioning.
    """
    __tablename__ = "narratives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)        user = self.db.query(User).filter(User.id == user_id).first()
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)d(
    content = Column(Text, nullable=False)
    prompt_used = Column(String, nullable=False)
    is_analyzed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="narratives")
    derived_values = relationship("NarrativeDerivedValue", back_populates="narrative")        )

e've already added to avoid duplicates
class NarrativeDerivedValue(Base):
    """        added_edges = set()
    Value derived from narrative analysis.
    ta access to build the graph
    These values represent the system's understanding of a user's values for access in data_accesses:
    based on their narratives, forming part of their value profile.es, interests, and preferences.
    """            accessor_id = str(
    __tablename__ = "narrative_derived_values"ess.data_type}"tem, allowing users to
s
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)ccess.data_type)
    narrative_id = Column(UUID(as_uuid=True), ForeignKey("narratives.id"), nullable=False)     accessor_type = "user" if access.accessor_id else "system"    """
    value_profile_id = Column(UUID(as_uuid=True), ForeignKey("value_profiles.id"), nullable=False)
    value_name= Column(String, nullable=False) if accessor_id not in added_nodes:
    value_score = Column(Integer, nullable=False)
    evidence_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)id,
    es
    # Relationshipsr_type,ives
    narrative = relationship("Narrative", back_populates="derived_values")
    value_profile= relationship("ValueProfile", back_populates="derived_values")r" else "  # 4caf50"n(JSONB, default=dict)  # Areas of interest
tise

class Connection(Base):
    """
    Connection between users based on value alignment.ady added                        onupdate=datetime.utcnow)
                data_node_id = f"data_{access.data_type}"
    This represents the core output of ThinkAlike's matching system,d not in added_nodes:etails
    connecting users with aligned values for meaningful interaction.lumn(DateTime, nullable=True)
    """
    __tablename__ = "connections"
                        label= f"Data: {access.data_type}",
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)     type = "data", # Relationships
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) back_populates = "value_profile")
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)                        color = "#673ab7"
    match_score = Column(Integer, nullable=False)
    connection_status = Column(String, nullable=False, default="pending")  # pending, accepted, rejecteduser_id}>"
    shared_values = Column(JSON, nullable=False)                added_nodes.add(data_node_id)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)s
         # User -> Data
    # Relationshipser's narrative - a story or experience they've shared.
    user1= relationship("User", foreign_keys=[user1_id]) if user_data_edge not in added_edges:
    user2 = relationship("User", foreign_keys=[user2_id])

tractable data points.
class DataAccessAudit(Base):                 source = str(user_id),    """
    """ata_node_id,
    Audit record for data access.                        label = "provides",
    t = uuid.uuid4)
    This model implements our radical transparency principle by
    recording every data access event for user visibility.
    """)
    __tablename__ = "data_access_audit"
elevant topics/tags
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)"{data_node_id}_{accessor_id}_{access.access_time.isoformat()}"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)g(50), default="private")
    accessor_id = Column(UUID(as_uuid=True),
                         ForeignKey("users.id"), nullable=True)
    data_type = Column(String, nullable=False)
    purpose = Column(String, nullable=False)olumn(DateTime, default=datetime.utcnow)
    algorithm_id = Column(String, nullable=True), default=datetime.utcnow,
    algorithm_name = Column(String, nullable=True)ime.utcnow)
    access_details = Column(JSON, nullable=True)                    thickness=1,
    access_time = Column(DateTime, default=datetime.utcnow, nullable=False) timestamp=access.access_time.isoformat()

    # Relationshipsrelationship(
    user = relationship("User", foreign_keys=[
                        user_id], back_populates="data_accesses")
    accessor = relationship("User", foreign_keys=[accessor_id], back_populates="data_accessed")lgorithm, add algorithm node
access.algorithm_id:rificationRecord", back_populates="narrative")
                algorithm_node_id = f"algorithm_{access.algorithm_id}"
class AlgorithmExecution(Base):rithm_node_id not in added_nodes:
    """itle} by user_id= {self.user_id} >"
    Record of an algorithm execution.                        DataFlowNode(
                                id=algorithm_node_id,
    This model implements our radical transparency principle byf"Algorithm: {access.algorithm_name or 'Unknown'}",
    making algorithm operations visible and auditable.                     type="algorithm",
    """narrative through analysis.
    __tablename__ = "algorithm_executions"                            color="#e91e63"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    algorithm_id = Column(String, nullable=False)dd(algorithm_node_id)
    algorithm_name = Column(String, nullable=False)             """
    algorithm_description=Column(Text, nullable=True)_derived_values"
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)                accessor_algorithm_edge=f"{accessor_id}_{algorithm_node_id}"
    purpose=Column(String, nullable=False)lumn(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_parameters=Column(JSON, nullable=True)
    output_result=Column(JSON, nullable=True)"), nullable = False)
    ethical_constraints= Column(JSON, nullable=True)ge, olumn(String(100), nullable=False)
    status = Column(String, nullable=False)onfidence_score = Column(Float, nullable=False)
    duration_ms = Column(Integer, nullable=True)rget = algorithm_node_id,
    execution_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    =1algorithm/method
    # Relationships
    user = relationship("User")
    role = Column(String(100), default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="active")  # active, inactive, banned

    # Relationships
    community = relationship("Community", back_populates="members")

    # Prevent duplicate memberships
    __table_args__ = (
        UniqueConstraint('community_id', 'user_id',
                         name='uq_community_membership'),
    )

    def __repr__(self):
        return f"<CommunityMembership user_id={self.user_id} in community_id={self.community_id}>"


class VerificationRecord(Base):
    """
    Record of a verification action on user content or profile.

    This model implements our radical transparency principle by making
    verification processes explicit and auditable, rather than hidden
    behind opaque algorithms.
    """
    __tablename__ = "verification_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=False)  # User being verified
    verifier_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=True)  # User performing verification
    # identity, narrative, claim, etc.
    verification_type = Column(String(100), nullable=False)
    status = Column(Enum(VerificationStatus),
                    default=VerificationStatus.PENDING)
    evidence = Column(JSONB, default=dict)  # Evidence used for verification
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration date

    # Optional references to specific content
    narrative_id = Column(UUID(as_uuid=True), ForeignKey(
        "narratives.id"), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[
                        user_id], back_populates="verification_records")
    verifier = relationship("User", foreign_keys=[verifier_id])
    narrative = relationship(
        "Narrative", back_populates="verification_records")
    audit_logs = relationship("VerificationAuditLog",
                              back_populates="verification_record")

    def __repr__(self):
        return f"<VerificationRecord type={self.verification_type}, status={self.status.value}>"


class VerificationAuditLog(Base):
    """
    Audit log for verification actions.

    This model implements our commitment to transparent processes by
    tracking all changes to verification status, creating an immutable
    record of decision-making.
    """
    __tablename__ = "verification_audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verification_record_id = Column(UUID(as_uuid=True), ForeignKey(
        "verification_records.id"), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=True)  # User who made the change
    # created, updated, disputed, etc.
    action = Column(String(100), nullable=False)
    previous_status = Column(Enum(VerificationStatus), nullable=True)
    new_status = Column(Enum(VerificationStatus), nullable=True)
    reason = Column(Text, nullable=True)
    metadata = Column(JSONB, default=dict)  # Additional context/data
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    verification_record = relationship(
        "VerificationRecord", back_populates="audit_logs")
    actor = relationship("User")

    def __repr__(self):
        return f"<VerificationAuditLog action={self.action} on record_id={self.verification_record_id}>"


class DataAccessAudit(Base):
    """
    Audit log for all data access events.

    This model embodies our commitment to radical transparency by
    tracking every access to user data, ensuring that users can see
    who accessed their data, when, and for what purpose.
    """
    __tablename__ = "data_access_audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                     nullable=False)  # User whose data was accessed
    accessor_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id"), nullable=True)  # User who accessed the data
    # profile, narrative, values, etc.
    data_type = Column(String(100), nullable=False)
    access_type = Column(String(50), nullable=False)  # read, update, delete
    access_reason = Column(String(255), nullable=False)  # Purpose of access
    data_fields = Column(JSONB, default=list)  # Specific fields accessed
    consent_id = Column(UUID(as_uuid=True), ForeignKey(
        "user_consents.id"), nullable=True)  # Associated consent
    access_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[
                        user_id], back_populates="audit_logs")
    accessor = relationship("User", foreign_keys=[accessor_id])

    def __repr__(self):
        return f"<DataAccessAudit type={self.access_type} on {self.data_type} for user_id={self.user_id}>"
