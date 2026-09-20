import numpy as np

def equilibrium_returns(
        market_caps, 
        covariance, 
        market_return=0.08,
        risk_free_rate=0.04
):
    
    mw = market_weights(market_caps)
    ra = risk_aversion(
        mw,
        covariance,
        market_return,
        risk_free_rate
    ) 

    return ra * covariance @ mw

def market_weights(market_caps):
    market_caps = np.asarray(market_caps, dtype=float)
    return market_caps / market_caps.sum()

def risk_aversion(market_weights, covariance, market_return=0.08, risk_free_rate=0.04):
    market_variance = market_weights.T @ covariance @ market_weights
    excess_return = market_return - risk_free_rate

    return excess_return / market_variance