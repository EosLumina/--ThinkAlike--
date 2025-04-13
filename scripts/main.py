from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn
from app.routes import agents, users
from app.database import engine
from app import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ThinkAlike API",
    description="API for ThinkAlike platform - Architecting Connection for Enlightenment 2.0",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with appropriate prefixes
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

# Custom OpenAPI schema to include ethical guidelines and data transparency information
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description + "\n\n**Ethical Commitment**: This API adheres to ThinkAlike's Ethical Guidelines, prioritizing data transparency, user sovereignty, and ethical AI.",
        routes=app.routes,
    )

    # Add custom documentation components
    openapi_schema["info"]["x-data-transparency"] = {
        "description": "All endpoints implement data traceability",
        "version": "1.0"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to ThinkAlike API",
        "status": "operational",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
