import os
import random

refdata_path = os.path.join("..", "refdata")

edinet_codes_path = os.path.join(refdata_path, "edinet_codes.xlsx")
nikkei_225_path = os.path.join(refdata_path, "nikkei_225.json")
docs_metadata_path = os.path.join(refdata_path, "docs_metadata.json")

documents_path = os.path.join("..", "documents")


def get_all_pdfs():
    return [f for f in os.listdir(documents_path) if f.lower().endswith(".pdf")]


def get_random_pdf_pair():
    # Get list of all PDF files in the directory
    pdf_files = [f for f in os.listdir(documents_path) if f.lower().endswith(".pdf")]

    # Select 2 random PDFs
    selected_pdfs = random.sample(pdf_files, 2)

    # Return full paths to the PDFs
    return (
        os.path.join(documents_path, selected_pdfs[0]),
        os.path.join(documents_path, selected_pdfs[1]),
    )
