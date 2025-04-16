"""
ThinkAlike FastAPI Application

This module defines the main FastAPI application for ThinkAlike,
implementing our principles of user sovereignty, radical transparency,
and data minimization.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from .core.config import settings
from .api.api_v1.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ThinkAlike")

# Create FastAPI app
app = FastAPI(
    title="ThinkAlike API",
    description="API for ThinkAlike - A platform for digital liberation",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint for the ThinkAlike API.
    
    This endpoint embodies our principle of radical transparency
    by providing clear information about the API and its purpose.
    """
    return {
        "message": "Welcome to the ThinkAlike API",
        "documentation": "/docs",
        "version": "0.1.0",
        "status": "operational",
        "principles": {
            "user_sovereignty": "All data belongs to users, with explicit consent for every use",
            "radical_transparency": "All operations are explainable and auditable",
            "data_minimization": "We collect only what's necessary, with clear purpose"
        }
    }

# Health check endpoint
@app.get("/health")
async def health():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}

@app.get("/api/v1/graph")
async def get_graph_data():
    return {
        "nodes": [
            {"id": "node1", "label": "User Input", "group": 1, "value": "User data input"},
            {"id": "node2", "label": "AI Agent", "group": 4, "isAI": True, "value": "AI processing node"},
            {"id": "node3", "label": "Database", "group": 3, "value": "Persistent data storage"},
            {"id": "node4", "label": "Response", "group": 2, "value": "Response to the user"}
        ],
        "edges": [
            {"from": "node1", "to": "node2", "value": "User data"},
            {"from": "node2", "to": "node3", "value": "AI processed data"},
            {"from": "node3", "to": "node4", "value": "Data for response"}
        ]
    }

@app.post("/api/v1/connection/status")
async def set_connection_status(status: str):
    if status not in ["disconnected", "connecting", "connected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    return {"status": status}

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Startup event for the FastAPI application.
    """
    logger.info("ThinkAlike API starting up")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event for the FastAPI application.
    """
    logger.info("ThinkAlike API shutting down")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=True)
