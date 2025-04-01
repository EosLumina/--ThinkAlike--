from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.agent import router as agent_router
from api.feedback import router as feedback_router
from api.api_v1_graph import router as graph_router
from api.api_v1_connection_status import router as connection_status_router
from api.index import router as index_router

app = FastAPI()

# CORS configuration - TEMPORARILY ALLOW ALL ORIGINS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers WITH PREFIXES
app.include_router(index_router) # No prefix for the root
app.include_router(agent_router, prefix="/agent")  # Prefix for agent routes
app.include_router(feedback_router, prefix="/feedback")  # Prefix for feedback routes
app.include_router(graph_router, prefix="/api/v1/graph") #Prefix for graph
app.include_router(connection_status_router, prefix="/api/v1/connection") #Prefix for status