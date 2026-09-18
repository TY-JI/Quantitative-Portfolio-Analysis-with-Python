from data import MarketDataLoader
from validation import DataValidator
from returns import Returns
from covariance import Covariance
from black_litterman import BlackLitterman
from equilibrium_returns import EquilibriumReturns
from optimizer import Optimizer
from views import construct_views
from parser import parse_args

def main():
    args = parse_args()
    # Load market data and extract close prices
    loader = MarketDataLoader(args)
    data = loader.download()
    close_prices = loader.get_close_prices(data)

    # Validating close prices
    validator = DataValidator()
    validator.validate(close_prices)

    # Computing % returns and remove missing data
    r = Returns()
    returns = r.pct_returns(close_prices)
    returns = r.remove_missing_returns(returns)

    # Constructing Ledoit-Wolf covariance matrix
    covariance = Covariance()
    ledoit_wolf_matrix = covariance.ledoit_wolf(returns)

    # Computing market weights
    eq = EquilibriumReturns()
    market_caps = loader.market_caps()
    market_weights = eq.market_weights(market_caps)

    # Constructing view matrix
    P, q = construct_views(args.view, args.tickers)

    # Computing expected returns using black litterman framework 
    bl = BlackLitterman(
        covariance=ledoit_wolf_matrix,
        pi=eq.pi(market_caps, ledoit_wolf_matrix),
        P=P,
        q=q
    )
    expected_returns = bl.expected_returns()

    # Computing optimized portfolio weights
    risk_aversion = eq.risk_aversion(market_weights, ledoit_wolf_matrix)
    opt = Optimizer(expected_returns,ledoit_wolf_matrix,risk_aversion)
    optimized_weights = opt.optimize()

    print(f'Market weights: {market_weights}')
    print(f'Expected returns: {expected_returns}')
    print(f'Optimized weights: {optimized_weights}')

if __name__=='__main__':
    main()