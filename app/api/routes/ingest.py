import os
import shutil

from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.services.cleaner_service import TextCleanerService
from app.services.chunking_service import TextChunkingService
from app.services.indexing_service import IndexingService
from app.services.loader_service import DocumentLoaderService


router = APIRouter(tags=["Ingestion"])

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    loaded = DocumentLoaderService.load_document(file_path)
    all_chunks = []

    if isinstance(loaded, list):
        for page in loaded:
            cleaned = TextCleanerService.clean_text(page.text)
            chunks = TextChunkingService.build_chunk_records(
                document_id=page.document_id,
                source=page.source,
                text=cleaned,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                page_number=page.page_number,
            )
            all_chunks.extend(chunks)
    else:
        cleaned = TextCleanerService.clean_text(loaded.text)
        chunks = TextChunkingService.build_chunk_records(
            document_id=loaded.document_id,
            source=loaded.source,
            text=cleaned,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        all_chunks.extend(chunks)

    IndexingService.index_chunks(all_chunks)

    return {
        "filename": file.filename,
        "chunks_indexed": len(all_chunks),
        "message": "Document indexed successfully",
    }