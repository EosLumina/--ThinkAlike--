from pydantic import BaseModel

class Document(BaseModel):
    document_id: str
    filename: str
    content: str
    # Add other Document model fields here as needed (e.g., task_id, created_at, document_type, etc.)
