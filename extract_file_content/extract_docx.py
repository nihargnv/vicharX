from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

if __name__ == "__main__":
    # Test
    docx_file = "D:\\test\\demo.docx"
    extracted_text = extract_text_from_docx(docx_file)
    print(extracted_text)
