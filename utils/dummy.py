import numpy as np
import pandas as pd


def generate_stock_prices(stock_list, start_date, end_date):
    dates = pd.date_range(start_date, end_date, freq="B")  # Business days
    prices = {}
    for ticker in stock_list:
        init_price = np.random.uniform(10, 1000)
        # Simulate log-normal random walk
        returns = np.random.normal(0, 0.01, len(dates))
        price_series = init_price * np.exp(np.cumsum(returns))
        prices[ticker] = pd.Series(price_series, index=dates)
    return prices


def get_quarterly_constituents(stock_list, start_date, end_date):
    quarter_starts = pd.date_range(start_date, end_date, freq="QS")
    constituents = {}
    for q in quarter_starts:
        # Dummy: use full list, or select a random subset
        # Here: full list
        constituents[q] = stock_list.copy()
    return constituents


def sort_basket(basket):
    signals = {ticker: np.random.random() for ticker in basket}
    sorted_basket = sorted(basket, key=lambda x: signals[x], reverse=True)
    return sorted_basket, signals


def get_signals(stock_list, start_date, end_date):
    constituents = get_quarterly_constituents(stock_list, start_date, end_date)
    signal_series = {}
    for q, basket in constituents.items():
        sorted_basket, signals = sort_basket(basket)
        signal_series[q] = {"signals": signals, "sorted_basket": sorted_basket}
    return signal_series
