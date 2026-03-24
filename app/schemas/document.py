from typing import Optional
from pydantic import BaseModel


class RawDocument(BaseModel):
    document_id: str
    source: str
    text: str


class RawPageDocument(BaseModel):
    document_id: str
    source: str
    page_number: Optional[int] = None
    text: str