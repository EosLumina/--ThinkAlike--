from fastapi import APIRouter

from .endpoints import auth

# Create main v1 API router
api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Additional endpoint routers will be added here as they are implemented
