"""
main.py
------------
Purpose:
    The main script to run the options data analysis project. It orchestrates the
    login, data fetching, processing, and display of results.

Functions:
    - display_rich_table(df, title): Formats and prints a pandas DataFrame using the rich library.
    - main(): The main execution function that ties everything together.
"""
import time
import requests
import pyotp
import pandas as pd
from rich.console import Console
from rich.table import Table
from SmartApi import SmartConnect

# --- Credentials / Imports ---
from credentials import API_KEY, CLIENT_CODE, PIN, TOTP_SECRET, SCRIP_MASTER_URL
from screener_conditions import GAINER_CONDITION, LOSER_CONDITION
from chartink_screener import get_chartink_screener_data
from option_data import build_otm_dataframe
from utils import fetch_json_with_retry
from table_theme import get_table_headers

# --- Display with Rich ---
def display_rich_table(df, title):
    """
    Displays a pandas DataFrame as a formatted table using the rich library.
    
    Args:
        df (pd.DataFrame): The DataFrame to display.
        title (str): The title for the table.
    """
    console = Console()

    def fmt(x):
        if pd.isna(x): return "-"
        try: return f"{float(x):.2f}"
        except: return str(x)

    # Get headers and styles from the theme file
    headers_styles = get_table_headers()

    table = Table(title=title, show_lines=True)
    for col, style in headers_styles:
        table.add_column(col, style=style, justify="right")

    headers = [h[0] for h in headers_styles]

    for _, r in df.iterrows():
        row_vals = [fmt(r[c]) if c in df.columns else "-" for c in headers]
        table.add_row(*row_vals)

    console.print(table)


# --- Main ---
def main():
    """Main execution function to run the stock and options analysis."""
    smartApi = SmartConnect(api_key=API_KEY)
    try:
        # Step 1: Login to the API
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = smartApi.generateSession(CLIENT_CODE, PIN, totp)
        if not data.get("status"):
            print("❌ Login failed.")
            return
        print("✅ Login successful!")

        # Step 2: Download the list of all instruments
        instrument_list = fetch_json_with_retry(SCRIP_MASTER_URL)
        if not instrument_list:
            print("❌ Failed to download Scrip Master.")
            return

        # Step 3: Define nearest expiry and get screener data
        nearest_expiry_str = "30SEP2025"
        with requests.Session() as session:
            gainer_df = get_chartink_screener_data(session, GAINER_CONDITION)
            loser_df = get_chartink_screener_data(session, LOSER_CONDITION)

        # Step 4: Process gainers and display
        if not gainer_df.empty:
            gainers_otm = build_otm_dataframe(smartApi, gainer_df, instrument_list, nearest_expiry_str)
            if not gainers_otm.empty:
                gainers_otm = gainers_otm.sort_values("% Change", ascending=False)
                display_rich_table(gainers_otm, "Top Gainers Option Data")
            else:
                print("❌ No option data found for gainers.")
        else:
            print("❌ No gainers found.")

        # Step  5: Process losers and display
        if not loser_df.empty:
            losers_otm = build_otm_dataframe(smartApi, loser_df, instrument_list, nearest_expiry_str)
            if not losers_otm.empty:
                losers_otm = losers_otm.sort_values("% Change", ascending=True)
                display_rich_table(losers_otm, "Top Losers Option Data")
            else:
                print("❌ No option data found for losers.")
        else:
            print("❌ No losers found.")

    finally:
        # Step 6: Logout
        try:
            smartApi.terminateSession(CLIENT_CODE)
            print("🔒 Logout successful.")
        except:
            pass

if __name__ == "__main__":
    main()