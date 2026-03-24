from pathlib import Path
from typing import List, Union
from uuid import uuid4

from pypdf import PdfReader

from app.schemas.document import RawDocument, RawPageDocument


class DocumentLoaderService:
    @staticmethod
    def load_txt(file_path: str) -> RawDocument:
        path = Path(file_path)
        text = path.read_text(encoding="utf-8")

        return RawDocument(
            document_id=str(uuid4()),
            source=str(path),
            text=text,
        )

    @staticmethod
    def load_pdf(file_path: str) -> List[RawPageDocument]:
        path = Path(file_path)
        reader = PdfReader(str(path))
        document_id = str(uuid4())

        pages: List[RawPageDocument] = []

        for index, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            pages.append(
                RawPageDocument(
                    document_id=document_id,
                    source=str(path),
                    page_number=index,
                    text=page_text,
                )
            )

        return pages

    @staticmethod
    def load_document(file_path: str) -> Union[RawDocument, List[RawPageDocument]]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return DocumentLoaderService.load_txt(file_path)

        if suffix == ".pdf":
            return DocumentLoaderService.load_pdf(file_path)

        raise ValueError(f"Unsupported file type: {suffix}")