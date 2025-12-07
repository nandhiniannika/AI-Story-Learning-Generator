import os
from backend.app.services.pdf_processor import PDFProcessor
from backend.app.models.pdf_models import PDFExtractedData, PDFSection

class PDFToTextPipeline:

    def __init__(self):
        self.processor = PDFProcessor()

    def run(self, pdf_path: str, save_folder="data/extracted_text/"):
        """
        Runs full PDF → text → cleaned JSON pipeline.
        """
        print("Extracting text...")
        text = self.processor.extract_text(pdf_path)

        json_data = self.processor.extract_json(text)

        # Save text output
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, "extracted_text.txt")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Text saved to {save_path}")

        return json_data
