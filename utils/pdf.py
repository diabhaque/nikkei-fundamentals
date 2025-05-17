import pdfplumber
import pymupdf
import logging


logging.getLogger("pdfminer").setLevel(logging.WARNING)


def extract_pdf_text(pdf_path):
    logger = logging.getLogger("pdfminer")
    logger.setLevel(logging.CRITICAL + 1)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


def extract_pdf_text_mu(pdf_path):
    doc = pymupdf.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])
