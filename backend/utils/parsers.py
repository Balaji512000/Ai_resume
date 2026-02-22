"""Helper functions for extracting text from resume files."""
import pdfplumber
from docx import Document

def extract_text_from_pdf(file_path):
    """Extracts all text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    """Extracts all text from a Word (DOCX) file."""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
