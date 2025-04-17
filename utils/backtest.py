import pandas as pd
import numpy as np


class Portfolio:
    def __init__(self, assets={}, liabilities={}, cash=1000):
        self.assets = assets
        self.liabilities = liabilities
        self.cash = cash

    def nav(self):
        return sum(self.assets.values()) - sum(self.liabilities.values()) + self.cash


class Timeline:
    def __init__(self, initial_date: pd.Timestamp, initial_portfolio: Portfolio):
        # curve maps date -> Portfolio
        self.curve = {initial_date: initial_portfolio}
        self.current_date = initial_date
        self.rebalancing_dates = []

    def get_portfolio(self, date: pd.Timestamp) -> Portfolio:
        # TODO: Update to get portfolio on or before this date
        return self.curve[date]

    def get_current_portfolio(self) -> Portfolio:
        return self.get_portfolio(self.current_date)

    def get_navs(self):
        return pd.Series({d: p.nav() for d, p in self.curve.items()}).sort_index()

    def add_portfolio(self, date: pd.Timestamp, portfolio: Portfolio):
        self.curve[date] = portfolio
        self.current_date = date

    def remark(self, date: pd.Timestamp, daily_returns: pd.Series):
        portfolio = self.get_current_portfolio()

        assets, liabilities, cash = (
            portfolio.assets,
            portfolio.liabilities,
            portfolio.cash,
        )

        remarked_assets = {
            ticker: value * (1 + daily_returns.get(ticker, 0.0))
            for ticker, value in assets.items()
        }

        remarked_liabilities = {
            ticker: value * (1 + daily_returns.get(ticker, 0.0))
            for ticker, value in liabilities.items()
        }

        remarked_portfolio = Portfolio(remarked_assets, remarked_liabilities, cash)

        self.add_portfolio(date, remarked_portfolio)

    def rebalance(self, date: pd.Timestamp, top_assets: list, bottom_assets: list):
        # Close all positions
        cash = self.get_current_portfolio().nav()

        # Invest
        assets = {ticker: cash * (1 / len(top_assets)) for ticker in top_assets}

        # Short
        liabilities = {
            ticker: cash * (1 / len(bottom_assets)) for ticker in bottom_assets
        }

        # Pay
        cash -= sum(assets.values())
        cash += sum(liabilities.values())

        rebalanced_portfolio = Portfolio(assets, liabilities, cash)
        self.add_portfolio(date, rebalanced_portfolio)
        self.rebalancing_dates.append(date)

    def calculate_annualized_return(self, trading_days_per_year=252):
        dates = sorted(self.curve)
        navs = [self.curve[d].nav() for d in dates]
        total_days = len(dates) - 1

        if total_days <= 0:
            return 0.0

        start_nav, end_nav = navs[0], navs[-1]
        return (end_nav / start_nav) ** (trading_days_per_year / total_days) - 1

    def calculate_sharpe_ratio(self, risk_free_rate=0.0):
        dates = sorted(self.curve)
        navs = [self.curve[d].nav() for d in dates]
        returns = np.diff(navs) / navs[:-1]
        return (np.mean(returns) - risk_free_rate) / np.std(returns)

    def get_cumulative_returns(self):
        navs = self.get_navs()
        return navs / navs.iloc[0]
