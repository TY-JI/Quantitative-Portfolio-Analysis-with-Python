import numpy as np

def ledoit_wolf(returns):
    returns = returns.to_numpy()

    T, N = returns.shape
    demeaned_returns = demean(returns)
    S = sample_covariance(demeaned_returns, T)
    F, r_bar = target_matrix(S, N)

    pi_matrix = pi_hat_matrix(demeaned_returns, S, T)
    pi = pi_matrix.sum()
    rho = rho_hat(demeaned_returns,S,T,r_bar, pi_matrix)
    gamma = gamma_hat(S,F)

    k = (pi-rho)/gamma
    delta = max(0,min(1,k/T))

    return (delta*F) + (1-delta)*S



def pi_hat_matrix(demeaned_returns, S, T):
    squared_deviation = covariance_deviations(S,demeaned_returns) ** 2
    pi_hat_matrix = squared_deviation.sum(axis=0) / T
    return pi_hat_matrix



def rho_hat(demeaned_returns, S, T, r_bar, pi_matrix):
    rho_diag = np.diag(pi_matrix).sum()

    # Covariance between the estimation error of asset i's variance
    # and the estimation error of covariance (i, j).
    v_ii_ij = np.einsum(
        'ti,tij->ij',
        demeaned_returns**2 - np.diag(S),
        covariance_deviations(S,demeaned_returns)
    )/T
    
    v_jj_ij = v_ii_ij.T

    standard_deviations = np.sqrt(np.diag(S))

    standard_deviation_ratio = np.outer(
        standard_deviations,
        1/standard_deviations
    )

    theta = (r_bar/2) * ((1/standard_deviation_ratio) * v_ii_ij + standard_deviation_ratio * v_jj_ij)

    np.fill_diagonal(theta,0)
    rho_off_diag = theta.sum()

    return rho_diag + rho_off_diag



def gamma_hat(S, F):
    return np.sum((S - F)**2)



def target_matrix(S, N):
    variances = np.diag(S)
    # Extract sample variances of all securities from the diagonal of sample cov matrix

    standard_deviations = np.sqrt(variances)
    # Calculate standard deviations of securities

    standard_deviations_outer = np.outer(
        standard_deviations,
        standard_deviations
    )
    # Constructing matrix of products of standard deviations sigma_i * sigma_j

    correlation_matrix = S / standard_deviations_outer
    # Recovering correlation matrix

    r_bar = (np.sum(correlation_matrix) - N) / (N*(N - 1))
    # - N eliminates 1s along the diagonal and since there are N - 1 other asses for every asset we have N(N - 1) in the denominator
    
    F = r_bar * standard_deviations_outer
    np.fill_diagonal(F, variances)

    return F, r_bar



def demean(returns):
    return returns - returns.mean()

def sample_covariance(demeaned_returns, T):
    return (demeaned_returns.T @ demeaned_returns) / T

def period_covariances(demeaned_returns):
    covariances = np.einsum(
        'ti,tj->tij',
        demeaned_returns,
        demeaned_returns
    )
    return covariances

def covariance_deviations(S, demeaned_returns):
    deviation = period_covariances(demeaned_returns) - S
    return deviation