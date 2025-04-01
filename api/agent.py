from fastapi import APIRouter, FastAPI

router = APIRouter()

@router.get("")
async def get_agent():
    return {"message": "This is the agent endpoint. Replace with your agent logic."}

app = FastAPI()
app.include_router(router)