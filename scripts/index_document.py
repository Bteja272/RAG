import sys

from app.core.config import settings
from app.services.cleaner_service import TextCleanerService
from app.services.chunking_service import TextChunkingService
from app.services.indexing_service import IndexingService
from app.services.loader_service import DocumentLoaderService


def process_file(file_path: str) -> list[dict]:
    loaded = DocumentLoaderService.load_document(file_path)
    all_chunk_records = []

    if isinstance(loaded, list):
        for page in loaded:
            cleaned_text = TextCleanerService.clean_text(page.text)
            chunk_records = TextChunkingService.build_chunk_records(
                document_id=page.document_id,
                source=page.source,
                text=cleaned_text,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                page_number=page.page_number,
            )
            all_chunk_records.extend(chunk_records)
    else:
        cleaned_text = TextCleanerService.clean_text(loaded.text)
        chunk_records = TextChunkingService.build_chunk_records(
            document_id=loaded.document_id,
            source=loaded.source,
            text=cleaned_text,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        all_chunk_records.extend(chunk_records)

    return all_chunk_records


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.index_document <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    chunk_records = process_file(file_path)
    IndexingService.index_chunks(chunk_records)

    print(f"Indexed {len(chunk_records)} chunks successfully.")


if __name__ == "__main__":
    main()