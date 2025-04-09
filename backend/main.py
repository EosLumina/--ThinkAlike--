import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.routes import agent_routes

# Create FastAPI app
app = FastAPI(
    title="ThinkAlike API",
    description="Backend API for the ThinkAlike platform",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_routes.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to ThinkAlike API"}
