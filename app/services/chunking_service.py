from typing import Any, Dict, List, Optional


class TextChunkingService:
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> List[str]:
        if not text:
            return []

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end == text_length:
                break

            start += chunk_size - chunk_overlap

        return chunks

    @staticmethod
    def build_chunk_records(
        document_id: str,
        source: str,
        text: str,
        chunk_size: int,
        chunk_overlap: int,
        page_number: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        chunks = TextChunkingService.chunk_text(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        records = []
        for index, chunk in enumerate(chunks):
            records.append(
                {
                    "document_id": document_id,
                    "source": source,
                    "page_number": page_number,
                    "chunk_index": index,
                    "text": chunk,
                }
            )

        return records