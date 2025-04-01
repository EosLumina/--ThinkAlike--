from fastapi import APIRouter, FastAPI

router = APIRouter()

@router.get("")
async def get_status():
    return {"message": "Connection status check successful."}

app = FastAPI()
app.include_router(router)