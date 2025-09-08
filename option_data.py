"""
option_data.py
--------------------
Purpose:
    Contains the core logic for fetching and structuring option chain data.

Functions:
    get_option_data_for_single_stock(smartApi, symbol_name, instrument_list, nearest_expiry_str)
        -> Fetches option data for a single stock.
    build_otm_dataframe(smartApi, stock_df, instrument_list, nearest_expiry_str)
        -> Orchestrates the parallel fetching and processing of data for multiple stocks.

Notes:
    - This file relies on utility functions like `safe_ltp` from `utils.py`
      to interact with the trading API.
"""
import time
import pandas as pd
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import safe_ltp, retry_sleep # Import the utility functions from the utils file

def get_option_data_for_single_stock(smartApi, symbol_name, instrument_list, nearest_expiry_str):
    """
    Fetches spot price and specific OTM call/put options data for a single stock.

    Args:
        smartApi: The SmartConnect API object.
        symbol_name (str): The symbol of the stock (e.g., "RELIANCE").
        instrument_list (list): The list of all instruments.
        nearest_expiry_str (str): The expiry date string (e.g., "30SEP2025").

    Returns:
        list of dicts or None: A list of dictionaries with option data, or None if data is not found.
    """
    try:
        # Find spot price from the equity segment
        spot_rec = next((inst for inst in instrument_list if inst.get("symbol") == f"{symbol_name}-EQ" and inst.get("exch_seg") == "NSE"), None)
        if not spot_rec:
            return None
        spot_price = safe_ltp(smartApi, "NSE", spot_rec["symbol"], spot_rec["token"])
        if not spot_price:
            return None

        # Calculate a hypothetical future price
        new_spot_price = round(spot_price * 1.02, 2)
        nearest_expiry = datetime.strptime(nearest_expiry_str, "%d%b%Y").date()
        if (nearest_expiry - date.today()).days < 0:
            return None

        # Find lot size from a relevant F&O instrument record
        opt_rows = [i for i in instrument_list if i.get("name") == symbol_name and i.get("expiry") == nearest_expiry_str and i.get("instrumenttype") == "OPTSTK"]
        if not opt_rows:
            return None
        
        # Take the lot size from the first valid option record found
        lot_size = int(opt_rows[0].get("lotsize", 1))

        strike_prices = sorted({float(i["strike"]) / 100.0 for i in opt_rows})
        selected_strikes = []
        otm_current = next((s for s in strike_prices if s > spot_price), None)
        if otm_current:
            selected_strikes.append(otm_current)
        otm_new = next((s for s in strike_prices if s > new_spot_price and s != otm_current), None)
        if otm_new:
            selected_strikes.append(otm_new)

        if not selected_strikes:
            return None

        data_for_strikes = []
        for strike_input in selected_strikes:
            for inst in opt_rows:
                if float(inst.get("strike", "0")) / 100.0 == strike_input:
                    option_type = "CE" if inst.get("symbol", "").endswith("CE") else "PE"
                    ltp = safe_ltp(smartApi, inst["exch_seg"], inst["symbol"], inst["token"])
                    if ltp > 0:
                        data_for_strikes.append({
                            "Symbol": symbol_name,
                            "Strike Price": float(f"{strike_input:.2f}"),
                            "Option Type": option_type,
                            "LTP": float(f"{ltp:.2f}"),
                            "Lot Size": lot_size
                        })
        return data_for_strikes or None
    except Exception as e:
        print(f"Error fetching data for {symbol_name}: {e}")
        return None

def build_otm_dataframe(smartApi, stock_df, instrument_list, nearest_expiry_str):
    """
    Builds a DataFrame of OTM option data for a list of stocks using parallel processing.

    Args:
        smartApi: The SmartConnect API object.
        stock_df (pd.DataFrame): DataFrame of stocks from the screener.
        instrument_list (list): The list of all instruments.
        nearest_expiry_str (str): The expiry date string.

    Returns:
        pd.DataFrame: A DataFrame with combined stock and option data.
    """
    symbols = stock_df["Symbol"].tolist()
    final_data = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_symbol = {
            executor.submit(get_option_data_for_single_stock, smartApi, symbol, instrument_list, nearest_expiry_str): symbol
            for symbol in symbols
        }
        for future in as_completed(future_to_symbol):
            option_data = future.result()
            if option_data:
                final_data.extend(option_data)
            retry_sleep(0.02) # Add a small delay between processing each stock

    if not final_data:
        return pd.DataFrame()

    df = pd.DataFrame(final_data)
    df = pd.merge(df, stock_df, on="Symbol", how="left")
    df = df[["Symbol", "Stock Name", "% Change", "Strike Price", "Option Type", "LTP", "Lot Size"]]

    pivot_df = df.pivot_table(index=["Symbol", "Stock Name", "% Change", "Strike Price", "Lot Size"],
                              columns="Option Type", values="LTP", aggfunc="first").reset_index()
    if "CE" not in pivot_df.columns: pivot_df["CE"] = None
    if "PE" not in pivot_df.columns: pivot_df["PE"] = None

    merged_rows = []
    for (sym, name, pct), group in pivot_df.groupby(["Symbol", "Stock Name", "% Change"]):
        group = group.sort_values("Strike Price").reset_index(drop=True)
        if len(group) >= 2:
            row = {
                "Symbol": sym,
                "Stock Name": name,
                "% Change": float(f"{pct:.2f}"),
                "Lot Size": int(group.loc[0, "Lot Size"]),
                "Nearest OTM Strike": float(f"{group.loc[0, 'Strike Price']:.2f}"),
                "Nearest OTM CE": float(f"{(group.loc[0, 'CE'] or 0):.2f}"),
                "Nearest OTM PE": float(f"{(group.loc[0, 'PE'] or 0):.2f}"),
                "New OTM Strike": float(f"{group.loc[1, 'Strike Price']:.2f}"),
                "New OTM CE": float(f"{(group.loc[1, 'CE'] or 0):.2f}"),
                "New OTM PE": float(f"{(group.loc[1, 'PE'] or 0):.2f}"),
            }
            row["CE P/L"] = float(f"{row['Lot Size'] * (row['Nearest OTM CE'] - row['New OTM CE']):.2f}")
            merged_rows.append(row)

    return pd.DataFrame(merged_rows)