# main.py
import os
import requests
import pyotp
import pandas as pd
from datetime import datetime
from rich.console import Console
from rich.table import Table
from SmartApi import SmartConnect

from credentials import API_KEY, CLIENT_CODE, PIN, TOTP_SECRET, SCRIP_MASTER_URL
from screener_conditions import GAINER_CONDITION, LOSER_CONDITION
from chartink_screener import get_chartink_screener_data
from option_data import build_otm_dataframe
from utils import fetch_json_with_retry
from table_theme import get_table_headers
from options_config import NEAREST_EXPIRY_STR
from export import save_to_excel
from sectors import sector_finder  # optimized bulk lookup

SAVE_PATH = r"C:\Users\91931\OneDrive\New folder\OneDrive\Desktop\angelone"

def display_rich_table(df, title):
    console = Console()

    def fmt(x):
        if pd.isna(x):
            return "-"
        try:
            return f"{float(x):.2f}"
        except:
            return str(x)

    headers_styles = get_table_headers()
    table = Table(title=title, show_lines=True)
    for col, style in headers_styles:
        table.add_column(col, style=style, justify="right")

    headers = [h[0] for h in headers_styles]
    for _, r in df.iterrows():
        row_vals = [fmt(r[c]) if c in df.columns else "-" for c in headers]
        table.add_row(*row_vals)

    console.print(table)

def get_dynamic_filename(base_name):
    now = datetime.now()
    hhmm = now.hour * 100 + now.minute
    if 915 <= hhmm <= 1017:
        suffix = "1015"
    elif 1018 <= hhmm <= 1217:
        suffix = "1217"
    else:
        suffix = "0330"
    return f"{base_name}{suffix}.xlsx"

def main():
    smartApi = SmartConnect(api_key=API_KEY)
    try:
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = smartApi.generateSession(CLIENT_CODE, PIN, totp)
        if not data.get("status"):
            print("❌ Login failed.")
            return
        print("✅ Login successful!")

        instrument_list = fetch_json_with_retry(SCRIP_MASTER_URL)
        if not instrument_list:
            print("❌ Failed to download Scrip Master.")
            return

        with requests.Session() as session:
            gainer_df = get_chartink_screener_data(session, GAINER_CONDITION)
            loser_df = get_chartink_screener_data(session, LOSER_CONDITION)

        # --- Gainers ---
        if not gainer_df.empty:
            gainers_otm = build_otm_dataframe(smartApi, gainer_df, instrument_list, NEAREST_EXPIRY_STR)
            if not gainers_otm.empty:
                # Bulk sector lookup (vectorized)
                gainers_otm["Sector"] = sector_finder.get_sector_bulk(gainers_otm["Symbol"])
                gainers_otm.sort_values("% Change", ascending=False, inplace=True)
                display_rich_table(gainers_otm, "Top Gainers Option Data")
                save_to_excel(gainers_otm, os.path.join(SAVE_PATH, get_dynamic_filename("gainers_scan")))
            else:
                print("❌ No option data found for gainers.")
        else:
            print("❌ No gainers found.")

        # --- Losers ---
        if not loser_df.empty:
            losers_otm = build_otm_dataframe(smartApi, loser_df, instrument_list, NEAREST_EXPIRY_STR)
            if not losers_otm.empty:
                losers_otm["Sector"] = sector_finder.get_sector_bulk(losers_otm["Symbol"])
                losers_otm.sort_values("% Change", ascending=True, inplace=True)
                display_rich_table(losers_otm, "Top Losers Option Data")
                save_to_excel(losers_otm, os.path.join(SAVE_PATH, get_dynamic_filename("losers_scan")))
            else:
                print("❌ No option data found for losers.")
        else:
            print("❌ No losers found.")

    finally:
        try:
            smartApi.terminateSession(CLIENT_CODE)
            print("🔒 Logout successful.")
        except:
            pass

if __name__ == "__main__":
    main()
