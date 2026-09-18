def pct_returns(prices):
    return prices.pct_change().iloc[1:]
    # Calculates the percentage change between consecutive rows within each column