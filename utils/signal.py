import json
import random

from utils.data import edinet_to_stock_code_map
from utils.llm_api import call_grok_api, call_grok_mini_api, prepare_prompt_messages
from utils.pdf import extract_pdf_text


def get_winner(client, pdf1_path, pdf2_path):
    return random.choice([0, 1])  # Change name to get_random_winner


def get_winner_grok_mini(client, pdf1_path, pdf2_path):
    pdf1_txt, pdf2_txt = extract_pdf_text(pdf1_path), extract_pdf_text(pdf2_path)
    completion = call_grok_mini_api(client, prepare_prompt_messages(pdf1_txt, pdf2_txt))
    return int(completion.choices[0].message.content)


def get_winner_grok(client, pdf1_path, pdf2_path):
    pdf1_txt, pdf2_txt = extract_pdf_text(pdf1_path), extract_pdf_text(pdf2_path)
    completion = call_grok_api(client, prepare_prompt_messages(pdf1_txt, pdf2_txt))
    return int(completion.choices[0].message.content)


def get_edinet_code_from_path(pdf_path):
    """
    path = f"../../documents/{quarter}/{edinet_code}_{filer}_{doc_type_code}_{doc_id}.{FILE_EXT}"
    """
    return pdf_path.split("/")[-1].split("_")[0]


def get_stock_code_from_path(pdf_path):
    """
    path = f"../../documents/{quarter}/{edinet_code}_{filer}_{doc_type_code}_{doc_id}.{FILE_EXT}"
    """
    return edinet_to_stock_code_map.get(get_edinet_code_from_path(pdf_path))
