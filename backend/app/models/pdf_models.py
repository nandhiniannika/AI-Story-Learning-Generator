from pydantic import BaseModel

class PDFUploadResponse(BaseModel):
    filename: str
    pages: int
    extracted_text: str
