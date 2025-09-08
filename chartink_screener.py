"""
chartink_screener.py
---------------------
Purpose:
    Provides a function to fetch stock data from Chartink based on custom conditions.

Functions:
    get_chartink_screener_data(session, scan_condition, timeout=20)
        -> Returns a pandas DataFrame with columns:
           ['Symbol', 'Stock Name', '% Change']

Notes:
    - Requires a requests.Session object for persistent connection.
    - Parses CSRF token before posting the screener request.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_chartink_screener_data(session, scan_condition, timeout=20):
    """
    Fetches stock symbols and their % change from Chartink.

    Args:
        session (requests.Session): Active HTTP session.
        scan_condition (str): Chartink screener query string.
        timeout (int): Request timeout (seconds).

    Returns:
        pd.DataFrame: Columns ['Symbol', 'Stock Name', '% Change']
    """
    try:
        # Get the CSRF token from the dashboard page
        response = session.get("https://chartink.com/screener/dashboard", timeout=timeout)
        response.raise_for_status()
        soup = bs(response.content, "html.parser")
        csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

        # Post the screener condition to the processing endpoint
        payload = {"scan_clause": scan_condition}
        post_response = session.post(
            "https://chartink.com/screener/process",
            data=payload,
            headers={"X-CSRF-TOKEN": csrf_token},
            timeout=timeout,
        )
        post_response.raise_for_status()

        # Extract data and create DataFrame
        data = post_response.json().get("data", [])
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df = df[["nsecode", "name", "per_chg"]]
        df.rename(columns={"nsecode": "Symbol", "name": "Stock Name", "per_chg": "% Change"}, inplace=True)
        df["% Change"] = pd.to_numeric(df["% Change"], errors="coerce").fillna(0.0)
        return df
    except Exception as e:
        print(f"An error occurred while fetching from Chartink: {e}")
        return pd.DataFrame()