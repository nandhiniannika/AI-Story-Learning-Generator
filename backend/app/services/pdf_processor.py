import pdfplumber
import re

class PDFProcessor:

    def extract_text(self, pdf_path: str) -> str:
        """
        Extracts clean text from PDF using pdfplumber.
        """
        text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                cleaned = self.clean_text(page_text)
                text += cleaned + "\n"

        return text.strip()

    def clean_text(self, text: str) -> str:
        """
        Basic cleaning: remove extra spaces, line breaks.
        """
        text = text.replace("\n", " ")
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def split_into_sections(self, text: str):
        """
        Splits PDF text into sections by detecting UPPERCASE HEADINGS.
        """
        lines = text.split(". ")
        sections = []
        current = {"heading": "Introduction", "text": ""}

        for line in lines:
            if line.strip().isupper() and len(line) < 70:
                # new heading found
                sections.append(current)
                current = {"heading": line.strip(), "text": ""}
            else:
                current["text"] += line + ". "

        sections.append(current)

        return sections

    def extract_json(self, text: str):
        """
        Converts extracted text → json sections.
        """
        sections = self.split_into_sections(text)

        return {
            "total_sections": len(sections),
            "sections": sections
        }
