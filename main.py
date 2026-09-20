import time

from data import MarketDataLoader
from black_litterman import BlackLitterman
from optimizer import Optimizer
import market as m

from returns import pct_returns
from covariance import ledoit_wolf
from views import construct_views
from parser import parse_args

def main():
    args = parse_args()

    if args.benchmark:
        start_time = time.perf_counter()
        
    # Load market data and extract close prices
    loader = MarketDataLoader(args)
    data = loader.download()
    close_prices = loader.get_close_prices(data)

    # Computing % returns and remove missing data
    returns = pct_returns(close_prices)

    # Constructing Ledoit-Wolf covariance matrix
    ledoit_wolf_matrix = ledoit_wolf(returns)

    # Computing market weights
    market_caps = loader.market_caps()
    market_weights = m.market_weights(market_caps)

    # Constructing view matrix
    P, q = construct_views(args.view, args.tickers)

    # Computing expected returns using black litterman framework 
    bl = BlackLitterman(
        covariance=ledoit_wolf_matrix,
        pi = m.equilibrium_returns(market_caps, ledoit_wolf_matrix),
        P = P,
        q = q
    )
    expected_returns = bl.expected_returns()

    # Computing optimized portfolio weights
    risk_aversion = m.risk_aversion(market_weights, ledoit_wolf_matrix)
    opt = Optimizer(expected_returns,ledoit_wolf_matrix,risk_aversion)
    optimized_weights = opt.optimize_pga()

    if args.benchmark:
        print(f'\nTotal runtime: {time.perf_counter() - start_time:.4f} seconds.\n')

    print(f'Market weights: {market_weights}')
    print(f'Expected returns: {expected_returns}')
    print(f'Optimized weights: {optimized_weights}')

if __name__=='__main__':
    main()