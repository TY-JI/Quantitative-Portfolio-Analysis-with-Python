import yfinance as yf
import numpy as np

class MarketDataLoader:

    def __init__(self, args):
        self.args = args

    def download(self):
        return yf.download(
            tickers=self.args.tickers,
            start=self.args.start,
            end=self.args.end,
            period=self.args.period,
            interval=self.args.interval,
            auto_adjust=True,
            progress=True,
        )
 
    def market_caps(self):
        market_caps = []

        for ticker in self.args.tickers:
            info = yf.Ticker(ticker).fast_info
            market_caps.append(info['market_cap'])

        market_caps = np.asarray(market_caps, dtype=float)
        self.validate_market_caps(market_caps, self.args.tickers)

        return market_caps


    def get_close_prices(self, data):
        return validate(data['Close'])


    def validate_market_caps(self, market_caps, tickers):
        missing = np.isnan(market_caps)

        if missing.any():
            missing_tickers = [
                ticker for ticker, is_missing in zip(tickers, missing)
                if is_missing
            ]

            raise ValueError(
                f'Missing market capitalization data for: {missing_tickers}'
            )

def validate(data):
    if data.empty:
        raise ValueError('No market data was returned.')

    check_duplicate_indexes(data)
    check_duplicate_tickers(data)
    check_missing_values(data)
    check_non_positive_prices(data)

    return data

def check_missing_values(data):
    missing = data.isna().sum()
    # .isna will check for missing values
    # .sum will collapse all columns summing values of 1 where missing values were

    if missing.any():
        raise ValueError(
            f'Missing values detected:\n{missing[missing > 0]}.'
        )

def check_duplicate_indexes(data):
    if data.index.duplicated().any():
        duplicates = data.index[data.index.duplicated()]
        # Returns list of dates (indexes) at positions where data.index.duplicated() is True
        raise ValueError(
            f'Duplicate index values detected:\n{duplicates}.'
        )

def check_non_positive_prices(data):
    if (data <= 0).any().any():
        invalid_prices = data[data <= 0].stack()
        # Keeps all values that satisfy the (data <= 0) condition in the data dataframe
        # collapses columns vertically with .stack()
        raise ValueError(
            f'Detection of invalid prices:\n{invalid_prices}.'
        )

def check_duplicate_tickers(data):
    duplicates = data.columns[data.columns.duplicated()]
    # Similar logic to the duplicate check in check_duplicate_indexes

    if len(duplicates) > 0:
        raise ValueError(
            f'Duplicate tickers detected:\n{duplicates}.'
        )