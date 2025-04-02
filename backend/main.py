# Add this import and include the router in your FastAPI app

from api.location_api import router as location_router

app.include_router(location_router)