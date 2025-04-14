from fastapi import FastAPI

app = FastAPI(
    title="ThinkAlike API",
    description="API for ThinkAlike platform - Architecting Connection for Enlightenment 2.0",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to ThinkAlike API",
        "status": "operational",
        "docs_url": "/docs"
    }
