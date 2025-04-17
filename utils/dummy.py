import numpy as np
import pandas as pd

from utils.constants import DATE_FORMAT


def generate_stock_prices(stock_list, start_date, end_date):
    dates = pd.date_range(start_date, end_date, freq="B")  # Business days
    dates = [d.strftime(DATE_FORMAT) for d in dates]
    prices = {}
    for ticker in stock_list:
        init_price = np.random.uniform(10, 1000)
        # Simulate log-normal random walk
        returns = np.random.normal(0, 0.01, len(dates))
        price_series = init_price * np.exp(np.cumsum(returns))
        prices[ticker] = pd.Series(price_series, index=dates)
    return prices


def get_quarterly_constituents(stock_list, start_date, end_date):
    quarter_starts = pd.date_range(start_date, end_date, freq="BQS")
    constituents = {q.strftime(DATE_FORMAT): stock_list.copy() for q in quarter_starts}
    return constituents


def sort_basket(signals):
    sorted_basket = sorted(signals.keys(), key=lambda x: signals[x], reverse=True)
    return sorted_basket


def generate_signals(constituents):
    signal_series = {}
    for q, basket in constituents.items():
        signals = {ticker: np.random.random() for ticker in basket}
        signal_series[q] = signals
    return signal_series
