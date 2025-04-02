from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db

router = APIRouter()

@router.get("")
async def get_graph(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve graph data.

    Returns:
        dict: A dictionary containing graph data.
    """
    try:
        nodes = db.query(Node).all()
        edges = db.query(Edge).all()
        graph_data = {
            "nodes": [{"id": node.id, "label": node.label, "group": node.group, "value": node.value} for node in nodes],
            "edges": [{"from": edge.from_node, "to": edge.to_node, "value": edge.value} for edge in edges]
        }
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()
app.include_router(router)
