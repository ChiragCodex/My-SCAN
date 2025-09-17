import os
import pandas as pd

# Absolute export folder
EXPORT_DIR = r"C:\Users\91931\OneDrive\New folder\OneDrive\Desktop\angelone"


def save_to_excel(df: pd.DataFrame, filename="scan_output.xlsx"):
    if df is None:
        print(f"⚠️ No data (None) for {filename}")
        return
    filepath = os.path.join(EXPORT_DIR, filename)
    df.to_excel(filepath, index=False)
    print(f"✅ Data saved to {filepath} (rows={len(df)})")

