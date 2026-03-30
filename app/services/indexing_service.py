from app.db.models import Document, DocumentChunk
from app.db.session import SessionLocal
from app.services.embedding_service import EmbeddingService
from app.core.logger import logger


class IndexingService:
    @staticmethod
    def index_chunks(chunk_records: list[dict]) -> None:
        if not chunk_records:
            return

        db = SessionLocal()

        try:
            first_record = chunk_records[0]

            existing_document = (
                db.query(Document)
                .filter(Document.document_id == first_record["document_id"])
                .first()
            )

            if not existing_document:
                document = Document(
                    document_id=first_record["document_id"],
                    source=first_record["source"],
                )
                db.add(document)
                db.flush()

            texts = [record["text"] for record in chunk_records]
            embeddings = EmbeddingService.embed_texts(texts)

            for record, embedding in zip(chunk_records, embeddings):
                chunk = DocumentChunk(
                    chunk_id=record.get(
                        "chunk_id",
                        f"{record['document_id']}_{record.get('page_number', 0)}_{record['chunk_index']}"
                    ),
                    document_id=record["document_id"],
                    page_number=record.get("page_number"),
                    chunk_index=record["chunk_index"],
                    text=record["text"],
                    embedding=embedding,
                )
                db.add(chunk)

            db.commit()

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()