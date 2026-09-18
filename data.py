import yfinance as yf
import numpy as np

# TODO
# add proper error handling for detected correctly formatted date inputs
# add option to select desired time frame

class MarketDataLoader:

    def __init__(self, args):
        self.args = args

    def download(self):
        data = yf.download(
            tickers=self.args.tickers,
            start=self.args.start,
            end=self.args.end,
            period=self.args.period,
            interval=self.args.interval,
            auto_adjust=True,
            progress=True,
        )

        return data

    def market_caps(self):
        market_caps = []

        for ticker in self.args.tickers:
            info = yf.Ticker(ticker).fast_info
            market_caps.append(info['market_cap'])

        return np.asarray(market_caps, dtype=float)
        
    def get_close_prices(self, data):
        return data['Close']