import yfinance as yf
import pandas as pd


def get_stock_prices(stock_list, start_date, end_date):
    # TODO: Can probably simplify using df["Close"].to_dict()
    prices = {}
    ticker_codes = [f"{ticker_code}.T" for ticker_code in stock_list]
    df = yf.download(ticker_codes, start=start_date, end=end_date)

    for ticker in stock_list:
        ticker_code = f"{ticker}.T"
        prices[ticker] = pd.Series(df["Close"][ticker_code])
    return prices
