from pipelines.pdf_to_text_pipeline import PDFToTextPipeline

pipeline = PDFToTextPipeline()

result = pipeline.run("data/pdfs/sample.pdf")

print("\n====================")
print("TOTAL SECTIONS:", result["total_sections"])
print("====================\n")

for sec in result["sections"]:
    print("HEADING:", sec["heading"])
    print("TEXT:", sec["text"][:200], "...\n")
