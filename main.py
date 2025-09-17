"""
main.py
------------
Purpose:
    Run options data analysis project with time-based Excel exports.
"""

import time
import os
import requests
import pyotp
import pandas as pd
from datetime import datetime
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
from options_config import NEAREST_EXPIRY_STR
from export import save_to_excel

# --- Absolute path for saving files ---
SAVE_PATH = r"C:\Users\91931\OneDrive\New folder\OneDrive\Desktop\angelone"

# --- Display with Rich ---
def display_rich_table(df, title):
    console = Console()

    def fmt(x):
        if pd.isna(x): return "-"
        try: return f"{float(x):.2f}"
        except: return str(x)

    headers_styles = get_table_headers()
    table = Table(title=title, show_lines=True)
    for col, style in headers_styles:
        table.add_column(col, style=style, justify="right")

    headers = [h[0] for h in headers_styles]
    for _, r in df.iterrows():
        row_vals = [fmt(r[c]) if c in df.columns else "-" for c in headers]
        table.add_row(*row_vals)

    console.print(table)

# --- Determine dynamic filename based on current time ---
def get_dynamic_filename(base_name):
    now = datetime.now()
    hhmm = now.hour*100 + now.minute  # e.g., 10:15 -> 1015

    if 915 <= hhmm <= 1017:
        suffix = "1015"
    elif 1018 <= hhmm <= 1217:
        suffix = "1217"
    else:  # 12:18 to 9:14 next day
        suffix = "0330"
    return f"{base_name}{suffix}.xlsx"

# --- Main ---
def main():
    smartApi = SmartConnect(api_key=API_KEY)
    try:
        # Step 1: Login
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = smartApi.generateSession(CLIENT_CODE, PIN, totp)
        if not data.get("status"):
            print("❌ Login failed.")
            return
        print("✅ Login successful!")

        # Step 2: Load instrument list
        instrument_list = fetch_json_with_retry(SCRIP_MASTER_URL)
        if not instrument_list:
            print("❌ Failed to download Scrip Master.")
            return

        # Step 3: Get screener data
        with requests.Session() as session:
            gainer_df = get_chartink_screener_data(session, GAINER_CONDITION)
            loser_df = get_chartink_screener_data(session, LOSER_CONDITION)

        # --- Process Gainers ---
        if not gainer_df.empty:
            gainers_otm = build_otm_dataframe(smartApi, gainer_df, instrument_list, NEAREST_EXPIRY_STR)
            if not gainers_otm.empty:
                gainers_otm = gainers_otm.sort_values("% Change", ascending=False)
                display_rich_table(gainers_otm, "Top Gainers Option Data")
                gainers_filename = os.path.join(SAVE_PATH, get_dynamic_filename("gainers_scan"))
                save_to_excel(gainers_otm, gainers_filename)
            else:
                print("❌ No option data found for gainers.")
        else:
            print("❌ No gainers found.")

        # --- Process Losers ---
        if not loser_df.empty:
            losers_otm = build_otm_dataframe(smartApi, loser_df, instrument_list, NEAREST_EXPIRY_STR)
            if not losers_otm.empty:
                losers_otm = losers_otm.sort_values("% Change", ascending=True)
                display_rich_table(losers_otm, "Top Losers Option Data")
                losers_filename = os.path.join(SAVE_PATH, get_dynamic_filename("losers_scan"))
                save_to_excel(losers_otm, losers_filename)
            else:
                print("❌ No option data found for losers.")
        else:
            print("❌ No losers found.")

    finally:
        # Step 4: Logout
        try:
            smartApi.terminateSession(CLIENT_CODE)
            print("🔒 Logout successful.")
        except:
            pass

if __name__ == "__main__":
    main()
