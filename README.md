# My-SCAN
# 📊 Options Data Screener

A Python-based tool to screen for top gaining and losing stocks and analyze their Out-of-the-Money (OTM) options data.

The tool logs into the Angel One SmartAPI, fetches a scrip master file, uses a Chartink screener to identify stocks with significant price movements, and then retrieves and displays detailed OTM options data for these stocks.

## 🚀 Features

- **Automated Login**: Secure login to Angel One SmartAPI using TOTP.
- **Stock Screening**: Integrates with Chartink to find top gainers and losers based on custom technical conditions.
- **Concurrent Data Fetching**: Uses a `ThreadPoolExecutor` to efficiently fetch options data for multiple stocks in parallel.
- **Options Data Analysis**: Fetches current and next OTM Call and Put prices for selected stocks.
- **Black-Scholes Model**: Includes a dedicated module to calculate option Greeks (Delta, Gamma, Vega, Theta).
- **Rich Output**: Presents data in a clean, readable, and color-coded table format using the `rich` library.

## 🗂️ Project Structure

The project is organized into a modular structure for better readability and maintenance.

project/
│── main.py
│── credentials.py
│── screener_conditions.py
│── chartink_screener.py
│── option_data.py
│── option_ltp_and_greeks_calculator.py
│── table_theme.py
│── utils.py
└── README.md


- `main.py`: The main script that runs the entire process.
- `credentials.py`: Stores all API keys and sensitive information. **Do not share this file.**
- `screener_conditions.py`: Defines the Chartink screener query strings.
- `chartink_screener.py`: Handles the logic for fetching data from the Chartink website.
- `option_data.py`: Contains functions for fetching and processing options data.
- `option_ltp_and_greeks_calculator.py`: Provides the Black-Scholes model for calculating option Greeks.
- `table_theme.py`: Centralized location for defining the styles of the `rich` tables.
- `utils.py`: A module for shared utility functions (e.g., retry logic, safe API calls).
- `README.md`: Project documentation.

## 🛠️ Setup and Installation

### 1. Prerequisites

- Python 3.7 or higher
- An active Angel One SmartAPI account.
- Required Python libraries:

```bash
pip install pandas requests SmartApi rich pyotp scipy tenacity beautifulsoup4
