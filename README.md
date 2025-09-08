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
