import requests
import pyotp
import logging
import pandas as pd
from datetime import datetime, date
from SmartApi import SmartConnect
import math
from scipy.stats import norm

# Import all credentials from your credentials.py file
from credentials import API_KEY, CLIENT_CODE, PIN, TOTP_SECRET, SECRET_KEY

# --- Configuration & Utility Functions ---
RISK_FREE_RATE = 0.07

def calculate_implied_volatility(price, S, K, t, r, flag):
    if t == 0: return None
    MAX_ITERATIONS, PRECISION, sigma = 100, 1.0e-5, 0.5
    for _ in range(MAX_ITERATIONS):
        try:
            d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
            d2 = d1 - sigma * math.sqrt(t)
            price_implied = S * norm.cdf(d1) - K * math.exp(-r * t) * norm.cdf(d2) if flag == 'c' else K * math.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)
            vega = S * norm.pdf(d1) * math.sqrt(t)
            diff = price - price_implied
        except (ValueError, OverflowError): return None
        if abs(diff) < PRECISION or vega == 0: return sigma
        sigma += diff / vega
        if not (0.001 < sigma < 10.0): return None
    return sigma

def calculate_greeks(option_type, spot_price, strike_price, time_to_expiry, ltp):
    flag = 'c' if option_type == 'CE' else 'p'
    iv = calculate_implied_volatility(ltp, spot_price, strike_price, time_to_expiry, RISK_FREE_RATE, flag)
    if iv is None: return {'Delta': 0, 'Theta': 0, 'Vega': 0, 'Gamma': 0, 'IV': 0}
    try:
        d1 = (math.log(spot_price / strike_price) + (RISK_FREE_RATE + 0.5 * iv ** 2) * time_to_expiry) / (iv * math.sqrt(time_to_expiry))
        d2 = d1 - iv * math.sqrt(time_to_expiry)
    except (ValueError, ZeroDivisionError): return {'Delta': 0, 'Theta': 0, 'Vega': 0, 'Gamma': 0, 'IV': 0}
    
    if flag == 'c':
        delta = norm.cdf(d1)
        theta = -(spot_price * norm.pdf(d1) * iv) / (2 * math.sqrt(time_to_expiry)) - RISK_FREE_RATE * strike_price * math.exp(-RISK_FREE_RATE * time_to_expiry) * norm.cdf(d2)
    else:
        delta = norm.cdf(d1) - 1
        theta = -(spot_price * norm.pdf(d1) * iv) / (2 * math.sqrt(time_to_expiry)) + RISK_FREE_RATE * strike_price * math.exp(-RISK_FREE_RATE * time_to_expiry) * norm.cdf(-d2)
        
    gamma = norm.pdf(d1) / (spot_price * iv * math.sqrt(time_to_expiry))
    vega = spot_price * norm.pdf(d1) * math.sqrt(time_to_expiry)
    return {'Delta': round(delta, 3), 'Theta': round(theta / 365, 3), 'Vega': round(vega / 100, 3), 'Gamma': round(gamma, 3), 'IV': round(iv, 3)}

# --- Main Logic ---
def get_option_chain_with_greeks(smartApi, symbol_name):
    print(f"\nFetching data for {symbol_name}...")
    instrument_list = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json").json()
    
    spot_price = next((smartApi.ltpData('NSE', f"{inst['symbol']}", inst['token']).get('data', {}).get('ltp', 0) for inst in instrument_list if inst.get('symbol') == f"{symbol_name}-EQ" and inst.get('exch_seg') == 'NSE'), 0)
    if spot_price == 0:
        print(f"❌ Could not fetch spot price for {symbol_name}.")
        return
    print(f"✅ Current Spot Price for {symbol_name}: ₹{spot_price}")
    new_spot_price = round(spot_price * 1.02, 2)
    print(f"✅ New Spot Price (2% increase): ₹{new_spot_price}")

    # Simplified expiry logic
    nearest_expiry_str = '30SEP2025'
    try:
        nearest_expiry = datetime.strptime(nearest_expiry_str, '%d%b%Y').date()
        time_to_expiry = (nearest_expiry - date.today()).days / 365.0
        if time_to_expiry < 0:
            print(f"❌ The specified expiry date ({nearest_expiry_str}) is in the past.")
            return
        print(f"✅ Using Expiry: {nearest_expiry_str}")
    except ValueError:
        print("❌ Invalid hard-coded expiry date format.")
        return

    strike_prices = sorted({float(i['strike'])/100.0 for i in instrument_list if i.get('name') == symbol_name and i.get('expiry') == nearest_expiry_str and i.get('instrumenttype') == 'OPTSTK'})
    if not strike_prices:
        print(f"❌ No strike prices found for the selected expiry.")
        return

    # Find nearest OTM strikes and combine into a single list
    selected_strikes = []
    otm_current = next((s for s in strike_prices if s > spot_price), None)
    if otm_current: selected_strikes.append(otm_current)
    otm_new = next((s for s in strike_prices if s > new_spot_price), None)
    if otm_new and otm_new not in selected_strikes: selected_strikes.append(otm_new)

    if not selected_strikes:
        print("❌ No relevant OTM strikes found. Cannot proceed.")
        return

    # Combine data fetching and printing into one loop
    for strike_input in selected_strikes:
        print(f"\nBuilding option chain for strike {strike_input}...")
        option_chain_data = []
        for inst in instrument_list:
            if inst.get('name') == symbol_name and inst.get('expiry') == nearest_expiry_str and float(inst.get('strike', '0'))/100.0 == strike_input and inst.get('instrumenttype') == 'OPTSTK':
                option_type = 'CE' if inst.get('symbol', '').endswith('CE') else 'PE'
                ltp = smartApi.ltpData(inst['exch_seg'], inst['symbol'], inst['token']).get('data', {}).get('ltp', 0)
                if ltp > 0 and time_to_expiry > 0:
                    greeks_dict = calculate_greeks(option_type, spot_price, strike_input, time_to_expiry, ltp)
                    option_chain_data.append({'Type': option_type, 'Strike Price': strike_input, 'LTP': ltp, **greeks_dict})
        
        if option_chain_data:
            df = pd.DataFrame(option_chain_data)
            calls = df[df['Type'] == 'CE'].rename(columns={'LTP': 'Call LTP', 'IV': 'Call IV', 'Delta': 'Call Delta', 'Theta': 'Call Theta', 'Vega': 'Call Vega', 'Gamma': 'Call Gamma'})
            puts = df[df['Type'] == 'PE'].rename(columns={'LTP': 'Put LTP', 'IV': 'Put IV', 'Delta': 'Put Delta', 'Theta': 'Put Theta', 'Vega': 'Put Vega', 'Gamma': 'Put Gamma'})
            final_table = pd.merge(calls, puts, on='Strike Price', how='outer').fillna(0).set_index('Strike Price')
            print(f"\n--- Data for {symbol_name} (Expiry: {nearest_expiry_str}, Strike: {strike_input}) ---")
            print(final_table)
            print("--------------------------------------------------------------------------")
        else:
            print(f"❌ Could not find option chain data for strike price {strike_input} on {nearest_expiry_str}.")

# --- Main Script Execution ---
smartApi = SmartConnect(api_key=API_KEY)
try:
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = smartApi.generateSession(CLIENT_CODE, PIN, totp)
    if not data.get('status'):
        logging.error(f"Login Failed: {data}")
    else:
        print("✅ Login successful!")
        symbol_input = input("Enter the stock symbols (e.g., ADANIENT,TCS): ").upper()
        for symbol in [s.strip() for s in symbol_input.split(',')]:
            get_option_chain_with_greeks(smartApi, symbol)
finally:
    try:
        smartApi.terminateSession(CLIENT_CODE)
        print("🔒 Logout successful.")
    except Exception as e:
        print(f"❌ Logout failed: {e}")