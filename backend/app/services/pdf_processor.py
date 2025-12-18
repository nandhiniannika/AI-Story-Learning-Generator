import fitz  # PyMuPDF

class PDFProcessor:

    @staticmethod
    def save_pdf(file, save_path):
        with open(save_path, "wb") as f:
            f.write(file.file.read())

    @staticmethod
    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return {"pages": len(doc), "text": text}
