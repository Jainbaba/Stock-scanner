# Stock Scanner Project

## Overview
This project consists of a stock scanner that fetches stock symbols from two different sources: TradingView and Chartlink. It merges and deduplicates the symbols, allowing users to view them in a convenient format.

## Files

### 1. `tv_screener.py`
This file contains functions to fetch stock symbols from TradingView. It includes:
- `fetch_tv_symbols()`: Retrieves stock symbols from the BSE (Bombay Stock Exchange) based on specific criteria such as market capitalization and price range.
- `fetch_nse_symbol()`: Retrieves stock symbols from the NSE (National Stock Exchange) with a focus on the exchange type.

### 2. `main.py`
This is the main application file that runs the Streamlit web app. It:
- Imports necessary modules and functions.
- Defines the `app()` function, which sets up the Streamlit interface.
- Fetches stock symbols from both Chartlink and TradingView.
- Merges and deduplicates the symbols.
- Displays the concatenated strings of stock symbols in the web app.

### 3. `chartlink_scanner.py`
This file contains the `Chartlink_Scanner` class, which is responsible for fetching stock symbols from Chartlink. It includes:
- `__init__()`: Initializes the scanner and fetches data from the Chartlink website.
- `getSymbol()`: Extracts and returns the stock symbols from the fetched data.
- `create_concatenated_string(stock_list)`: Takes a list of stock symbols and compares them with the NSE symbols, formatting them accordingly.

## How to Run the Project

1. **Install Dependencies**: Make sure you have Python installed. Then, install the required packages using pip:
   ```bash
   pip install pandas requests beautifulsoup4 streamlit
   ```

2. **Run the Streamlit App**: Navigate to the directory containing `main.py` and run the following command:
   ```bash
   streamlit run main.py
   ```

3. **Access the App**: After running the command, a new tab will open in your default web browser displaying the Stock Scanner app.

## Usage
- The app will display a list of stock symbols fetched from both TradingView and Chartlink.
- You can copy the concatenated strings of stock symbols for further use.

## Note
Ensure that you have a stable internet connection as the app fetches data from external sources.
