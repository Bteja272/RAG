from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import RAGService


router = APIRouter(tags=["Query"])


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_rag(request: QueryRequest):
    return RAGService.query(request.query)