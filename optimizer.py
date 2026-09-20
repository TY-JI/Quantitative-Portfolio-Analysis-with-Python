import numpy as np

class Optimizer:
    def __init__(self, expected_returns, covariance, risk_aversion):
        self.expected_returns = expected_returns
        self.covariance = covariance
        self.risk_aversion = risk_aversion

    def optimize_pga(self, iterations=1000, step=0.01, tolerance=1e-8):
        weights = self.project(
            self.optimize_unconstrained()
        )

        for _ in range(iterations):
            previous_weights = weights.copy()

            gradient = self.expected_returns - self.risk_aversion * np.dot(
                self.covariance , weights
            )

            weights = self.project(weights + step * gradient)
            if np.linalg.norm(weights - previous_weights) < tolerance:
                break

        return weights

    def project(self, weights):
        n = len(weights)
        sorted_weights = np.sort(weights)[::-1]
        summed_weights = np.cumsum(sorted_weights)

        rho = np.nonzero(sorted_weights * np.arange(1, n + 1) > (summed_weights - 1))[0][-1]
        theta = (summed_weights[rho] - 1) / (rho + 1)

        return np.maximum(weights - theta, 0)

    def optimize_unconstrained(self):
        return np.linalg.solve(
            self.risk_aversion * self.covariance,
            self.expected_returns
        )