import os
import random

refdata_path = os.path.join("..", "refdata")

edinet_codes_path = os.path.join(refdata_path, "edinet_codes.xlsx")
nikkei_225_path = os.path.join(refdata_path, "nikkei_225.json")
all_securities_path = os.path.join(refdata_path, "all_securities.json")
docs_metadata_path = os.path.join(refdata_path, "docs_metadata.json")
basket_all_path = os.path.join(refdata_path, "basket_all.json")
basket_500_path = os.path.join(refdata_path, "basket_500.json")

documents_path = os.path.join("..", "documents")

signals_path = os.path.join("..", "signals")
wins_signals_path = os.path.join(signals_path, "wins.json")
elo_signals_path = os.path.join(signals_path, "elo.json")

market_data_path = os.path.join("..", "market_data")
adj_share_counts_path = os.path.join(market_data_path, "avg_share_counts_adj.csv")
daily_prices_path = os.path.join(market_data_path, "daily_prices.csv")
quarterly_prices_path = os.path.join(market_data_path, "quarterly_prices.csv")


def get_all_pdfs_for_quarter(quarter):
    quarter_documents_path = os.path.join(documents_path, quarter)
    return [f for f in os.listdir(quarter_documents_path) if f.lower().endswith(".pdf")]


def get_all_pdfs():
    quarters = [q for q in os.listdir(documents_path)]
    return [pdf for quarter in quarters for pdf in get_all_pdfs_for_quarter(quarter)]


def get_random_pdf_pair():
    # Get list of all PDF files in the directory
    quarters = [q for q in os.listdir(documents_path)]
    random_quarter = random.choice(quarters)
    pdf_files = get_all_pdfs_for_quarter(random_quarter)

    # Select 2 random PDFs
    selected_pdfs = random.sample(pdf_files, 2)

    # Return full paths to the PDFs
    quarter_documents_path = os.path.join(documents_path, random_quarter)
    return (
        os.path.join(quarter_documents_path, selected_pdfs[0]),
        os.path.join(quarter_documents_path, selected_pdfs[1]),
    )
