from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DocumentChunk
from app.db.session import SessionLocal
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    @staticmethod
    def retrieve(query: str, top_k: int = 3) -> list[dict]:
        query_embedding = EmbeddingService.embed_text(query)

        db: Session = SessionLocal()

        try:
            stmt = (
                select(DocumentChunk)
                .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
                .limit(top_k)
            )

            results = db.execute(stmt).scalars().all()

            return [
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
                for chunk in results
            ]
        finally:
            db.close()