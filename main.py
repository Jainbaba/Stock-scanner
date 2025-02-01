import streamlit as st
from chartlink_scanner import Chartlink_Scanner, create_concatenated_string
from tv_screener import fetch_tv_symbols
from pyperclip import copy

def app():
    st.title("Merged Stock Scanner")

    # Fetch data from both scanners
    chartlink_scanner = Chartlink_Scanner()
    chartlink_symbols = chartlink_scanner.getSymbol()
    tv_symbols = fetch_tv_symbols()

    # Merge and deduplicate symbols
    all_symbols = sorted(list(set(chartlink_symbols + tv_symbols)))
    
    
    # Create concatenated strings
    concatenated_strings = create_concatenated_string(all_symbols)

    # Display concatenated strings with copy functionality
    st.subheader(f"Stock Symbols ({len(all_symbols)})")
    for string in concatenated_strings:
        st.code(string, language="python",wrap_lines=True)

if __name__ == '__main__':
    app()