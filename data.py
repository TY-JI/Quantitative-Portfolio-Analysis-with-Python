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

# TODO -Calculate market capitalizations using a broader market universe 
#       rather than only the securities selected for the portfolio.
#      -allow retrival of historical market caps
 
    def market_caps(self):
        market_caps = []

        for ticker in self.args.tickers:
            info = yf.Ticker(ticker).fast_info
            market_caps.append(info['market_cap'])

        return np.asarray(market_caps, dtype=float)
        
    def get_close_prices(self, data):
        return data['Close']