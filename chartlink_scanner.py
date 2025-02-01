import os
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
import requests
import streamlit as st
from tv_screener import fetch_nse_symbol

class Chartlink_Scanner:
    def __init__(self) -> None:
        scan_settings = {'scan_clause': '( {cash} ( latest close > latest sma( latest close , 50 ) and( latest close - latest sma( latest close , 50 ) / latest sma( latest close , 50 ) ) < 0.1 and latest max( 3 , latest high ) / latest min( 3 , latest low ) <= 1.07 and market cap > 1 ) ) '}
        with requests.Session() as s:
            r = s.get('https://chartink.com/screener/50sma-484')
            soup = BeautifulSoup(r.content, 'lxml')
            s.headers['X-CSRF-TOKEN'] = soup.select_one('[name=csrf-token]')['content']
            self.data = s.post('https://chartink.com/screener/process', data=scan_settings).json()

    def getSymbol(self) -> list:
        symbols = [stock['nsecode'] for stock in self.data['data']]
        return symbols

def create_concatenated_string(stock_list: list) -> list:
   # Fetch data from the API
    #response = requests.get("http://localhost:8000/equities/equity-tickers")
    #api_data = response.json()  # Assuming the API returns a JSON array of stock symbols
    api_list = fetch_nse_symbol()
    # Convert the JSON response to a list
    #api_list = [item for item in api_data]
    

    # Compare the values from stock_list with the API response
    modified_list = []
    for stock in stock_list:
        if stock in api_list:
            modified_list.append(f"NSE:{stock}")
        else:
            modified_list.append(f"BSE:{stock}")

    # Break the modified list into chunks of 30
    concatenated_strings = []
    for i in range(0, len(modified_list), 30):
        chunk = modified_list[i:i+30]
        concatenated_string = ','.join(chunk)
        concatenated_strings.append(concatenated_string)

    return concatenated_strings