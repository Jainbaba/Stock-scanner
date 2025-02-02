from datetime import datetime
from typing import Tuple
import streamlit as st
import pandas as pd
from chartlink_scanner import Chartlink_Scanner, create_concatenated_string
from store import rotate_week_data
from tv_screener import fetch_tv_symbols
from pyperclip import copy


def load_data(current_file: str, last_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load current and last week data from CSV files."""
    try:
        current_week_data = pd.read_csv(current_file)
        last_week_data = pd.read_csv(last_file)
        return current_week_data, last_week_data
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure the CSV files exist.")
        return pd.DataFrame(), pd.DataFrame()  
    except pd.errors.EmptyDataError:
        st.error("Error: One of the CSV files is empty.")
        return pd.DataFrame(), pd.DataFrame() 
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return pd.DataFrame(), pd.DataFrame() 

def fetch_and_process_data():
    # Fetch data from both scanners
    st.write(f"Fetching data at {datetime.now()}...")
    try:
        scanner = Chartlink_Scanner()
        symbols = scanner.getSymbol()
        
        tv_symbols = fetch_tv_symbols()
        all_symbols = sorted(list(set(symbols + tv_symbols)))
        
        rotate_week_data(all_symbols)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")


params = st.query_params
if "run_task" in params:
    fetch_and_process_data()
    st.success("Scheduled task executed!")

def app() -> None:
    """Main function to run the Streamlit app."""
    st.title("Merged Stock Scanner")

    curr_week_data, prev_week_data = load_data('current_week_data.csv', 'last_week_data.csv')
    
    if curr_week_data.empty or prev_week_data.empty:
        st.warning("No data available to display.")
        return

    curr_string = create_concatenated_string(curr_week_data['string'])
    prev_string = create_concatenated_string(prev_week_data['string'])
    # Display current week's stock symbols
    st.subheader("Current Week's Stock Symbols")
    for string in curr_string:
        st.code(string, language="python", wrap_lines=True)

    # Find new stocks added this week
    new_stocks = set(curr_string) - set(prev_string)
    st.subheader(f"New Stocks Added This Week ({len(new_stocks)})")
    for stock in new_stocks:
        st.code(stock, language="python", wrap_lines=True)

if __name__ == '__main__':
    app()