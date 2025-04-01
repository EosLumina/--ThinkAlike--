from fastapi import APIRouter, FastAPI

router = APIRouter()

@router.get("")
async def get_graph():
    return {"message": "Graph endpoint. Replace with graph data."}

app = FastAPI()
app.include_router(router)