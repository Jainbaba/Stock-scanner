from bs4 import BeautifulSoup
import requests
from tv_screener import fetch_nse_symbol
import time
from requests.exceptions import ConnectionError, Timeout, RequestException
from typing import List, Dict, Any

class Chartlink_Scanner:
    def __init__(self) -> None:
        self.scan_settings = {
            'scan_clause': '( {cash} ( latest close > latest sma( latest close , 50 ) and( latest close - latest sma( latest close , 50 ) / latest sma( latest close , 50 ) ) < 0.1 and latest max( 3 , latest high ) / latest min( 3 , latest low ) <= 1.07 and market cap > 1 ) ) '
        }
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.timeout = 30     # seconds
        self.data: Dict[str, Any] = self._fetch_data()

    def _fetch_data(self) -> Dict[str, Any]:
        """Fetch data from Chartlink."""
        for attempt in range(self.max_retries):
            try:
                with requests.Session() as s:
                    s.headers.update({
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    })
                    
                    r = s.get('https://chartink.com/screener/50sma-484', timeout=self.timeout)
                    r.raise_for_status()
                    
                    soup = BeautifulSoup(r.content, 'lxml') 
                    csrf_token = soup.select_one('[name=csrf-token]')
                    
                    if not csrf_token:
                        raise ValueError("CSRF token not found")
                        
                    s.headers['X-CSRF-TOKEN'] = csrf_token['content']
                    
                    response = s.post(
                        'https://chartink.com/screener/process',
                        data=self.scan_settings,
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    
                    return response.json()
                    
            except (ConnectionError, Timeout) as e:
                if attempt == self.max_retries - 1:  
                    raise Exception(f"Failed to connect after {self.max_retries} attempts: {str(e)}")
                time.sleep(self.retry_delay)
            except RequestException as e:
                raise Exception(f"Request failed: {str(e)}")
            except ValueError as e:
                raise Exception(f"Data processing error: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")

    def getSymbol(self) -> List[str]:
        """Get stock symbols from the fetched data."""
        try:
            return [stock['nsecode'] for stock in self.data['data']]
        except (KeyError, TypeError) as e:
            raise Exception(f"Error processing symbols: {str(e)}")
        

def create_concatenated_string(stock_list: List[str]) -> List[str]:
    """Create concatenated strings from stock list."""
    api_list = fetch_nse_symbol()
    modified_list = []
    for stock in stock_list:
        if stock in api_list:
            modified_list.append(f"NSE:{stock}")
        else:
            modified_list.append(f"BSE:{stock}")

    concatenated_strings = []
    for i in range(0, len(modified_list), 30):
        chunk = modified_list[i:i+30]
        concatenated_string = ','.join(chunk)
        concatenated_strings.append(concatenated_string)

    return concatenated_strings