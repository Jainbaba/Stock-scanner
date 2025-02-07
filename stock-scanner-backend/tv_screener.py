import pandas as pd
from tradingview_screener import Query, Column
from typing import List

def fetch_tv_symbols() -> List[str]:
    """Fetch stock symbols from TradingView screener."""
    try:
        market = 'BSE'
        query = (Query().select('name', 'close', 'volume', 'market_cap_basic', 'change').set_markets('india')
                 .where(
                     Column('market_cap_basic') > 1e+09,
                     Column('close').between_pct('High.All', 0.8, 1),
                     Column('high') != Column('High.All'),
                     Column('exchange').like(market),
                 ).order_by('change').limit(6000))
        count, scanner_data = query.get_scanner_data()
        symbols = scanner_data['name'].tolist()
        return symbols
    except Exception as e:
        print(f"Error fetching TV symbols: {e}")
        return [] 

def fetch_nse_symbol() -> List[str]:
    """Fetch NSE stock symbols."""
    try:
        market = 'NSE'
        query = (Query().select('name').set_markets('india')
                 .where(
                     Column('exchange').like(market),
                 ).order_by('name', ascending=True).limit(6000))
        count, scanner_data = query.get_scanner_data()
        symbols = scanner_data['name'].tolist()
        return symbols
    except Exception as e:
        print(f"Error fetching NSE symbols: {e}")
        return [] 
