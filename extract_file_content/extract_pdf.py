import pdfplumber
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    text = ""

    # Try extracting text using pdfplumber (for normal PDFs)
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # If no text is found, use OCR (for scanned PDFs)
    if not text.strip():
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return text

if __name__ == "__main__":
    # Example usage
    pdf_file = "D:\\test\\u2-c1.pdf"
    extracted_text = extract_text_from_pdf(pdf_file)
    print(extracted_text)
