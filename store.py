from datetime import datetime
import os
from typing import Tuple
import pandas as pd

def save_current_week_data(symbols):
    current_date = datetime.now().date() 

    current_week_data = pd.DataFrame({
        'date': [current_date] * len(symbols), 
        'string': symbols 
    })
    current_week_data.to_csv('current_week_data.csv', index=False)

def rotate_week_data(symbols):
    if not os.path.exists('last_week_data.csv'):
        pd.DataFrame(columns=['symbol']).to_csv('last_week_data.csv', index=False)
    
    if not os.path.exists('current_week_data.csv'):
        save_current_week_data(symbols) 
        return  

    os.rename('current_week_data.csv', 'last_week_data.csv')

    save_current_week_data(symbols)