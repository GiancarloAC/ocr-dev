from pydantic import BaseModel
from typing import List, Optional

class OCRItem(BaseModel):
    text: str
    confidence: float
    box: List[List[float]]

class OCRPageResult(BaseModel):
    page_number: int
    raw_text: str
    structured_data: List[OCRItem]

class OCRResponse(BaseModel):
    filename: str
    content_type: str
    raw_text: str
    structured_data: Optional[List[OCRItem]] = None
    pages: Optional[List[OCRPageResult]] = None
