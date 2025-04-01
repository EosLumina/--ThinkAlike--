from fastapi import APIRouter, FastAPI

router = APIRouter()

@router.get("")
async def root():
    return {"message": "ThinkAlike API Root.  Go to /docs for documentation."}

app = FastAPI()
app.include_router(router)