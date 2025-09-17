"""
options_config.py
---------------------
Purpose:
    A centralized location for configuration variables that are subject to frequent changes.
    This file separates hard-coded values from the application logic for easier
    management and updates.

Editable:
    - NEAREST_EXPIRY_STR: The target options expiry date.
    - SPOT_PRICE_INCREASE_PERCENTAGE: The percentage to calculate the "new" spot price.
    - THREAD_WORKERS: Number of threads for parallel data fetching.
"""

# --- Options Data Configuration ---
NEAREST_EXPIRY_STR = "30SEP2025"

# --- Analysis & Performance Configuration ---
# Percentage increase to calculate the hypothetical "new" spot price for OTM analysis.
SPOT_PRICE_INCREASE_PERCENTAGE = 0.02

# Number of parallel workers for fetching option data.
# Adjust based on your system's capabilities and API rate limits.
THREAD_WORKERS = 4