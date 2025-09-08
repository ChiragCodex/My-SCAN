"""
option_ltp_and_greeks_calculator.py
-----------------------------------
Purpose:
    Calculates option Greeks (Delta, Gamma, Vega, Theta) using the Black-Scholes model.

Functions:
    - calculate_greeks(S, K, T, r, sigma, option_type):
      - S: Spot price of the underlying.
      - K: Strike price of the option.
      - T: Time to expiry in years.
      - r: Risk-free interest rate.
      - sigma: Volatility (standard deviation).
      - option_type: 'call' or 'put'.
      -> Returns a dictionary of calculated Greeks.

Notes:
    - This model assumes European options, no dividends, and constant volatility/risk-free rate.
    - Volatility (sigma) is a critical input and must be estimated or derived (e.g., from VIX).
    - The formulas provided are for a non-dividend-paying stock, a common simplification of the Black-Scholes model.
"""
import math
from scipy.stats import norm

# Standard Normal Probability Density Function
def normal_pdf(x):
    return (1.0 / (math.sqrt(2 * math.pi))) * math.exp(-x * x / 2.0)

# Main Greek calculation function
def calculate_greeks(S, K, T, r, sigma, option_type):
    """
    Calculates the Greeks (Delta, Gamma, Vega, Theta) for a European option.

    Args:
        S (float): Current price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to expiration in years.
        r (float): Annualized risk-free interest rate.
        sigma (float): Annualized volatility.
        option_type (str): "call" or "put".

    Returns:
        dict: A dictionary containing the calculated Greeks.
    """
    if T <= 0:
        return {"delta": None, "gamma": None, "vega": None, "theta": None}
    
    # Calculate d1 and d2, the core components of the Black-Scholes model
    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    # N(d1) and N(d2) are the cumulative probability functions for a standard normal distribution
    # N'(d1) is the standard normal probability density function
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    N_prime_d1 = normal_pdf(d1)

    # Initialize Greeks dictionary
    greeks = {}

    if option_type == 'call':
        # Delta: Measures the rate of change of the option price with respect to a change in the underlying asset's price.
        # Formula: N(d1)
        greeks["delta"] = Nd1
        
        # Theta: Measures the rate of decline in the value of an option over time (time decay).
        # Formula: -((S * N'(d1) * sigma) / (2 * sqrt(T))) - (r * K * exp(-r * T) * N(d2))
        greeks["theta"] = -((S * N_prime_d1 * sigma) / (2 * math.sqrt(T))) - (r * K * math.exp(-r * T) * Nd2)
        
    elif option_type == 'put':
        # Delta: Measures the rate of change of the option price with respect to a change in the underlying asset's price.
        # Formula: N(d1) - 1
        greeks["delta"] = Nd1 - 1
        
        # Theta: Measures the rate of decline in the value of an option over time (time decay).
        # Formula: -((S * N'(d1) * sigma) / (2 * sqrt(T))) + (r * K * exp(-r * T) * (1 - N(d2)))
        greeks["theta"] = -((S * N_prime_d1 * sigma) / (2 * math.sqrt(T))) + (r * K * math.exp(-r * T) * (1 - Nd2))
    
    # Gamma: Measures the rate of change of Delta. Gamma is the same for both calls and puts.
    # Formula: N'(d1) / (S * sigma * sqrt(T))
    greeks["gamma"] = N_prime_d1 / (S * sigma * math.sqrt(T))
    
    # Vega: Measures the sensitivity to volatility. Vega is the same for both calls and puts.
    # Formula: S * N'(d1) * sqrt(T)
    greeks["vega"] = S * N_prime_d1 * math.sqrt(T)

    return greeks