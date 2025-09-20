# sectors.py
# Optimized for bulk lookups

import csv
import logging
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SectorFetcher:
    """
    Fetches sector/industry for stock symbols using a preloaded dict from CSV.
    Supports ultra-fast bulk lookups for pandas Series.
    """
    def __init__(self, csv_path: str):
        self.sector_cache = {}  # cache for repeated lookups
        self.symbol_to_sector = {}

        csv_file = Path(csv_path)
        if not csv_file.exists():
            logging.error(f"CSV file not found at {csv_file}")
            return

        # Load CSV into dict
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()
                industry = row.get("Industry", "Unknown").strip()
                if symbol:
                    self.symbol_to_sector[symbol] = industry

    def get_sector(self, symbol: str) -> str:
        """Single symbol lookup"""
        symbol_upper = symbol.upper()
        if symbol_upper in self.sector_cache:
            return self.sector_cache[symbol_upper]

        sector = self.symbol_to_sector.get(symbol_upper, "Unknown")
        self.sector_cache[symbol_upper] = sector
        return sector

    def get_sector_bulk(self, symbols):
        """
        Bulk lookup for a list or pandas Series of symbols.
        Returns a pandas Series of sectors, in the same order as input.
        """
        if isinstance(symbols, pd.Series):
            # Vectorized mapping
            sectors = symbols.str.upper().map(self.symbol_to_sector).fillna("Unknown")
        else:
            # Convert list/iterable to list
            sectors = [self.symbol_to_sector.get(s.upper(), "Unknown") for s in symbols]
        return sectors

# Initialize fetcher with CSV in the same folder
csv_file_path = Path(__file__).parent / "ind_nifty500list.csv"
sector_finder = SectorFetcher(str(csv_file_path))
