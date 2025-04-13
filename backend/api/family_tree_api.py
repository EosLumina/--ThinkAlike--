"""
Family Tree API - Supporting the philosophical concept of "One and Many"
through data structures and endpoints that honor both collective connection
and individual sovereignty.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from backend.auth.auth_handler import get_current_user
from backend.app.models.family_tree import FamilyTree, FamilyTreeConnection, ConnectionType
from backend.app.services.connection_discovery import ConnectionDiscoveryService

router = APIRouter(prefix="/api/family-tree", tags=["family-tree"])

class ConnectionFilterParams(BaseModel):
    """Parameters for filtering connection views to balance unity and diversity."""
    depth: int = Field(3, description="How many degrees of connection to include")
    connection_types: List[ConnectionType] = Field(
        default_factory=lambda: list(ConnectionType),
        description="Types of connections to include in the view"
    )
    unity_emphasis: float = Field(
        0.5,
        ge=0.0,
        le=1.0,
        description="Balance between collective pattern (1.0) and individual focus (0.0)"
    )
    include_metadata: bool = Field(
        True,
        description="Include rich metadata about connections and permissions"
    )

@router.get("/view")
async def get_family_tree_view(
    filters: ConnectionFilterParams = Depends(),
    current_user = Depends(get_current_user)
):
    """
    Get a view of the family tree that balances unity (collective patterns)
    and diversity (individual uniqueness).

    This is the central endpoint embodying our "one and many" philosophy,
    where the data structure preserves both collective interconnection and
    individual sovereignty.
    """
    try:
        # Get connections based on filter parameters
        connections = await FamilyTreeConnection.get_network(
            user_id=current_user.id,
            depth=filters.depth,
            connection_types=filters.connection_types
        )

        # Balance the representation based on unity emphasis parameter
        if filters.unity_emphasis > 0.7:
            # Emphasize pattern emergence, community clusters
            view = FamilyTree.generate_unity_view(connections)
        elif filters.unity_emphasis < 0.3:
            # Emphasize individual nodes and their unique attributes
            view = FamilyTree.generate_diversity_view(connections)
        else:
            # Balanced view showing both individual uniqueness and collective patterns
            view = FamilyTree.generate_balanced_view(connections)

        # Add metadata when requested
        if filters.include_metadata:
            view["metadata"] = {
                "perspectives": FamilyTree.get_perspective_options(),
                "connection_types": [
                    {"id": ct.value, "name": ct.name, "description": ct.description}
                    for ct in ConnectionType
                ],
                "data_sovereignty": {
                    "user_controlled_nodes": [
                        node["id"] for node in view["nodes"]
                        if node["user_id"] == current_user.id
                    ],
                    "permission_settings": FamilyTree.get_user_permissions(current_user.id)
                }
            }

        return view

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving family tree view: {str(e)}"
        )

@router.get("/discover")
async def discover_potential_connections(
    current_user = Depends(get_current_user),
    connection_type: Optional[ConnectionType] = None,
    max_results: int = Query(10, ge=1, le=50)
):
    """
    Discover potential new connections that would enhance both personal relationships
    and collective understanding.

    This endpoint suggests connections that strengthen both individual growth and
    community resilience, embodying the "one and many" duality.
    """
    discovery_service = ConnectionDiscoveryService()
    suggestions = await discovery_service.find_meaningful_connections(
        user_id=current_user.id,
        connection_type=connection_type,
        max_results=max_results
    )

    # For each suggestion, include both:
    # 1. Personal relevance - how it benefits the individual
    # 2. Collective impact - how it strengthens the community pattern
    for suggestion in suggestions:
        suggestion["personal_relevance"] = discovery_service.calculate_personal_relevance(
            user_id=current_user.id,
            connection=suggestion
        )
        suggestion["collective_impact"] = discovery_service.calculate_collective_impact(
            connection=suggestion,
            existing_network=await FamilyTreeConnection.get_network(
                user_id=current_user.id,
                depth=2
            )
        )

    return {
        "suggestions": suggestions,
        "explanation": {
            "methodology": "These suggestions balance personal growth and collective resilience",
            "consent_required": True,
            "data_sources": discovery_service.get_transparent_data_sources()
        }
    }

# Additional endpoints for connection management, view customization, etc.
# ...existing code...
