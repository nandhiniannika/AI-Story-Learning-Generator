from pydantic import BaseModel
from typing import List

class PDFSection(BaseModel):
    heading: str
    text: str

class PDFExtractedData(BaseModel):
    total_sections: int
    sections: List[PDFSection]
