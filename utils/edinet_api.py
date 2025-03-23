import os
import datetime
import json
import urllib.parse
import urllib.request
from dotenv import load_dotenv

from typing import List, Dict, Union
from tqdm import tqdm

# Load variables from the .env file and retrieve api key
load_dotenv()
EDINET_API_KEY = os.getenv("EDINET_API_KEY")


file_config = {
    "PDF": {"type": 2, "extension": "pdf"},
    "CSV": {"type": 5, "extension": "zip"},
}

FILE_TYPE = "PDF"
FILE_TYPE_CODE = file_config[FILE_TYPE]["type"]
FILE_EXT = file_config[FILE_TYPE]["extension"]


def filter_by_codes(
    docs: List[Dict],
    edinet_codes: Union[List[str], str] = [],
    doc_type_codes: Union[List[str], str] = [],
) -> List[Dict]:
    """Filter documents by EDINET codes and document type codes."""

    if len(edinet_codes) == 0:
        edinet_codes = [doc["edinetCode"] for doc in docs]
    elif isinstance(edinet_codes, str):
        edinet_codes = [edinet_codes]

    if len(doc_type_codes) == 0:
        doc_type_codes = [doc["docTypeCode"] for doc in docs]
    elif isinstance(doc_type_codes, str):
        doc_type_codes = [doc_type_codes]

    return [
        doc
        for doc in docs
        if doc["edinetCode"] in edinet_codes and doc["docTypeCode"] in doc_type_codes
    ]


def disclosure_documents(date: Union[str, datetime.date], type: int = 2) -> Dict:
    """Retrieve disclosure documents from EDINET API for a specified date."""

    if isinstance(date, str):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date string. Use format 'YYYY-MM-DD'")
        date_str = date
    elif isinstance(date, datetime.date):
        date_str = date.strftime("%Y-%m-%d")
    else:
        raise TypeError("Date must be a string ('YYYY-MM-DD') or datetime.date")

    url = "https://disclosure.edinet-fsa.go.jp/api/v2/documents.json"
    params = {
        "date": date_str,
        "type": type,  # '1' is metadata only, '2' is metadata and results
        "Subscription-Key": EDINET_API_KEY,
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    with urllib.request.urlopen(full_url) as response:
        return json.loads(response.read().decode("utf-8"))


def get_document(doc_id: str) -> urllib.request.urlopen:
    """Retrieve a specific document from EDINET API."""
    url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc_id}"
    params = {
        "type": FILE_TYPE_CODE,  # '2' for PDF, '5' for CSV
        "Subscription-Key": EDINET_API_KEY,
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    return urllib.request.urlopen(full_url)


def save_document(doc_res: urllib.request.urlopen, output_path: str) -> None:
    """Save the document content to file."""
    with open(output_path, "wb") as file_out:
        file_out.write(doc_res.read())


def get_documents_for_date_range(
    start_date: datetime.date,
    end_date: datetime.date,
    edinet_codes: List[str] = [],
    doc_type_codes: List[str] = [],
) -> List[Dict]:
    """Retrieve and filter documents for a date range."""
    matching_docs = []

    total_days = (end_date - start_date).days + 1

    for single_date in tqdm(
        (start_date + datetime.timedelta(days=n) for n in range(total_days)),
        total=total_days,
        desc="Retrieving documents",
    ):
        docs_res = disclosure_documents(date=single_date)
        if docs_res["results"]:
            filtered_docs = filter_by_codes(
                docs_res["results"], edinet_codes, doc_type_codes
            )
            matching_docs.extend(filtered_docs)

    return matching_docs
