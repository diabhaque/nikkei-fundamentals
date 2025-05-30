import json

from utils.datapath import (
    nikkei_225_path,
    all_securities_path,
    basket_all_path,
    basket_500_path,
)

with open(nikkei_225_path) as f:
    nikkei_225 = json.load(f)

with open(all_securities_path) as f:
    all_securities = json.load(f)

with open(basket_all_path) as f:
    jp_all = json.load(f)

with open(basket_500_path) as f:
    jp_500 = json.load(f)

edinet_to_stock_code_map = {
    security["edinet_code"]: security["code"] for security in all_securities
}

stock_to_edinet_code_map = {
    security["code"]: security["edinet_code"] for security in all_securities
}
