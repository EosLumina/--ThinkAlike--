import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .api.api_v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS is not None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Development fallback - allow localhost
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
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
    return {
        "message": "Welcome to ThinkAlike API",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=True)
