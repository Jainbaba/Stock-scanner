from datetime import datetime
import pytz
from typing import List, Dict, Any
import pymongo
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

from chartlink_scanner import Chartlink_Scanner
from tv_screener import fetch_tv_symbols

# Load environment variables
load_dotenv()

def get_mongodb_collection(collection_name: str) -> Collection:
    """Connect to MongoDB Atlas and return the specified collection."""
    connection_string = os.getenv('MONGODB_URI')
    if not connection_string:
        raise ValueError("MongoDB connection string not found in environment variables")
    
    client = pymongo.MongoClient(connection_string)
    db = client["stock_scanner"]
    return db[collection_name]

def get_yearweek(current: bool = True) -> str:
    """Get year and week number in format YYYYWW."""
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    year = current_date.year
    week = current_date.isocalendar()[1]
    
    if not current:
        if week == 1:
            # If current week is first week, get last week of previous year
            return f"{year - 1}52"
        else:
            return f"{year}{week - 1:02d}"
    
    return f"{year}{week:02d}"

def save_current_week_data(symbols: List[str]) -> None:
    """Save current week's data to MongoDB."""
    collection = get_mongodb_collection("weekly_stocks")
    yearweek = get_yearweek()
    ist_now = datetime.now(pytz.timezone('Asia/Kolkata'))
    
    collection.update_one(
        {"yearweek": yearweek},
        {
            "$set": {
                "created_date": ist_now,
                "symbols": symbols,
                "count": len(symbols)
            }
        },
        upsert=True
    )

def get_weekly_data(yearweek: str) -> Dict[str, Any]:
    """Get data for a specific yearweek."""
    collection = get_mongodb_collection("weekly_stocks")
    return collection.find_one({"yearweek": yearweek}, {"_id": 0}) or {}

def log_fetch_operation(success: bool, message: str, symbols_count: int = 0) -> None:
    """Log fetch operations to MongoDB."""
    try:
        collection = get_mongodb_collection("fetch_logs")
        
        log_entry = {
            "timestamp": datetime.now(pytz.timezone('Asia/Kolkata')),
            "yearweek": get_yearweek(),
            "success": success,
            "message": message,
            "symbols_count": symbols_count,
            "source": "vercel_cron"
        }
        
        collection.insert_one(log_entry)
        
    except Exception as e:
        # If logging fails, we don't want to break the main operation
        print(f"Failed to log operation: {str(e)}")

def get_recent_logs(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent fetch operation logs."""
    collection = get_mongodb_collection("fetch_logs")
    
    logs = list(collection.find(
        {},
        {'_id': 0}
    ).sort('timestamp', -1).limit(limit))
    
    # Convert datetime objects to strings for JSON serialization
    for log in logs:
        log['timestamp'] = log['timestamp'].isoformat()
    
    return logs

def fetch_and_process_data():
    try:
        scanner = Chartlink_Scanner()
        symbols = scanner.getSymbol()
        
        tv_symbols = fetch_tv_symbols()
        all_symbols = sorted(list(set(symbols + tv_symbols)))
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
