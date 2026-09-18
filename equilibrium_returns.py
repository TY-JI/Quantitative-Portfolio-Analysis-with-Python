import numpy as np

class EquilibriumReturns():
    def pi(
            self, 
            market_caps, 
            covariance, 
            market_return=0.08,
            risk_free_rate=0.04
    ):
        
        market_weights = self.market_weights(market_caps)
        risk_aversion = self.risk_aversion(
            market_weights,
            covariance,
            market_return,
            risk_free_rate
        ) 

        return risk_aversion * covariance @ market_weights

    def market_weights(self, market_caps):
        market_caps = np.asarray(market_caps, dtype=float)
        return market_caps / market_caps.sum()

    def risk_aversion(self, market_weights, covariance, market_return=0.08, risk_free_rate=0.04):
        market_variance = market_weights.T @ covariance @ market_weights
        excess_return = market_return - risk_free_rate

        return excess_return / market_variance