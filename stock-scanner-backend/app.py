from flask import Flask, jsonify
from flask_cors import CORS
import os
from store import (
    get_yearweek, 
    get_weekly_data, 
    save_current_week_data, 
    log_fetch_operation,
    get_recent_logs
)
from chartlink_scanner import Chartlink_Scanner
from tv_screener import fetch_tv_symbols

app = Flask(__name__)

# Get CORS origin from environment variable
CORS_ORIGIN = os.getenv('CORS_ORIGIN', 'http://localhost:3000')
CORS(app, origins=[CORS_ORIGIN])

@app.route('/api/trigger-fetch', methods=['POST'])
def trigger_fetch():
    """Endpoint for scheduled task to call."""
    try:
        scanner = Chartlink_Scanner()
        symbols = scanner.getSymbol()
        
        tv_symbols = fetch_tv_symbols()
        
        all_symbols = sorted(list(set(symbols + tv_symbols)))
        
        save_current_week_data(all_symbols)
        
        log_fetch_operation(
            success=True,
            message="Successfully fetched and saved symbols",
            symbols_count=len(all_symbols)
        )
        
        return jsonify({
            "success": True,
            "message": f"Successfully saved {len(all_symbols)} symbols"
        })
        
    except Exception as e:
        log_fetch_operation(
            success=False,
            message=f"Error: {str(e)}",
            symbols_count=0
        )
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stocks/current', methods=['GET'])
def get_current_stocks():
    """Get current week's stock data."""
    try:
        current_week = get_weekly_data(get_yearweek(current=True))
        
        if not current_week:
            return jsonify({
                "success": False,
                "error": "No data available for current week"
            }), 404
        
        return jsonify({
            "success": True,
            "data": current_week
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stocks/new', methods=['GET'])
def get_new_stocks():
    """Get newly added stocks compared to last week."""
    try:
        current_week = get_weekly_data(get_yearweek(current=True))
        last_week = get_weekly_data(get_yearweek(current=False))
        
        if not current_week:
            return jsonify({
                "success": False,
                "error": "No data available for current week"
            }), 404
        
        if not last_week:
            return jsonify({
                "success": False,
                "error": "No data available for last week"
            }), 404
        
        current_symbols = set(current_week.get("symbols", []))
        last_symbols = set(last_week.get("symbols", []))
        new_symbols = list(current_symbols - last_symbols)
        
        return jsonify({
            "success": True,
            "data": {
                "current_yearweek": current_week["yearweek"],
                "previous_yearweek": last_week["yearweek"],
                "new_symbols_count": len(new_symbols),
                "new_symbols": sorted(new_symbols)
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get fetch operation logs."""
    try:
        logs = get_recent_logs()
        return jsonify({
            "success": True,
            "data": logs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
