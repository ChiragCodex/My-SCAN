"""
utils.py
------------
Purpose:
    Contains general utility functions used across multiple files in the project.

Functions:
    - retry_sleep(backoff_sec): Sleeps for a given duration with a small random jitter.
    - fetch_json_with_retry(url, ...): Fetches JSON data from a URL with retry logic.
    - safe_ltp(smartApi, ...): Safely fetches the Last Traded Price (LTP) with retries.
"""
import time
import random
import logging
import requests

def retry_sleep(backoff_sec):
    """Sleeps for a given duration with a small random jitter."""
    time.sleep(backoff_sec + random.uniform(0, 0.15))

def fetch_json_with_retry(url, max_retries=4, base_backoff=0.8):
    """Fetches JSON data from a URL with exponential backoff and retries."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"[fetch_json_with_retry] Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                return None
            retry_sleep(base_backoff * attempt)

def safe_ltp(smartApi, exch_seg, symbol, token, max_retries=3, base_backoff=0.25):
    """
    Safely retrieves the Last Traded Price (LTP) for a given instrument with retries.
    
    Args:
        smartApi: The SmartConnect API object.
        exch_seg (str): Exchange segment (e.g., "NSE").
        symbol (str): Instrument symbol.
        token (str): Instrument token.
        max_retries (int): Maximum number of retries.
        base_backoff (float): Base backoff time in seconds.

    Returns:
        float: The LTP, or 0.0 if not found after retries.
    """
    for attempt in range(1, max_retries + 1):
        try:
            data = smartApi.ltpData(exch_seg, symbol, token)
            ltp = data.get("data", {}).get("ltp", 0)
            if ltp:
                return float(ltp)
        except Exception as e:
            logging.error(f"[safe_ltp] {symbol} attempt {attempt} failed: {e}")
        retry_sleep(base_backoff * attempt)
    return 0.0