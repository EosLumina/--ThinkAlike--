from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_agent_status():
    return {"status": "active"}
