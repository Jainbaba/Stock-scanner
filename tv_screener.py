import pandas as pd
from tradingview_screener import Query, Column

def fetch_tv_symbols() -> list:
    market = 'BSE'
    query = (Query().select('name', 'close', 'volume', 'market_cap_basic','Change %').set_markets('india')
             .where(
                 Column('Market Capitalization') > 1e+09,
                 Column('Price').between_pct('High.All', 0.8, 1),
                 Column('High') != Column('High.All'),
                 Column('exchange').like(market),
             ).order_by('Change %').limit(6000))
    count, scanner_data = query.get_scanner_data()
    symbols = scanner_data['name'].tolist()
    return symbols

def fetch_nse_symbol() -> list:
    market = 'NSE'
    query = (Query().select('name').set_markets('india')
             .where(
                 Column('exchange').like(market),
             ).order_by('name', ascending=True).limit(6000))
    count, scanner_data = query.get_scanner_data()
    symbols = scanner_data['name'].tolist()
    return symbols
