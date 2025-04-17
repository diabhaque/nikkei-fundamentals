import json

from utils.datapath import nikkei_225_path

with open(nikkei_225_path) as f:
    nikkei_225 = json.load(f)
