from fastapi import APIRouter, UploadFile, File
from app.services.pdf_processor import PDFProcessor
from app.models.pdf_models import PDFUploadResponse
import os

router = APIRouter()   # No prefix here

DATA_DIR = "data/pdfs/"
TEXT_DIR = "data/extracted_text/"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)


@router.post("/pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    save_path = os.path.join(DATA_DIR, file.filename)

    # Save uploaded PDF
    PDFProcessor.save_pdf(file, save_path)

    # Extract text
    result = PDFProcessor.extract_text(save_path)

    # Save extracted text
    text_path = os.path.join(TEXT_DIR, file.filename + ".txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    return PDFUploadResponse(
        filename=file.filename,
        pages=result["pages"],
        extracted_text=result["text"]
    )
